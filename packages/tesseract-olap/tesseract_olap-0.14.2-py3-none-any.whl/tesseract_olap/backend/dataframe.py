import hashlib
from datetime import datetime
from typing import List, Literal, Optional, TypedDict, Union

import polars as pl
from dateutil.relativedelta import relativedelta

from tesseract_olap.exceptions.query import InvalidQuery
from tesseract_olap.query import (
    AnyQuery,
    DataQuery,
    JoinIntent,
    JoinOnColumns,
    PaginationIntent,
)
from tesseract_olap.schema import DimensionType, MemberType

from .models import Result


def generate_lag_column(series: pl.Series, delta: int):
    """Generates a pl.Expr that represents the same series used as reference,
    but with each value lagged by delta units."""
    value = str(series[0])

    # identify the type of date according to the number of digits
    if value.isdigit():
        # YYYY : Year
        if len(value) == 4:
            return pl.col(series.name) - delta
        # YYYYQ : Quarter
        if len(value) == 5:
            return pl.col(series.name).map_elements(
                lambda x: calc_quarter_delta(str(x), delta),
                return_dtype=series.dtype,
            )
        # YYYYMM : Month
        if len(value) == 6:
            return pl.col(series.name).map_elements(
                lambda x: calc_month_delta(str(x), delta),
                return_dtype=series.dtype,
            )
        # YYYYMMDD : Day
        if len(value) == 8:
            return pl.col(series.name).map_elements(
                lambda x: calc_day_delta(str(x), delta),
                return_dtype=series.dtype,
            )

    raise ValueError(f"Invalid time_id format: {value}")


def calc_quarter_delta(time_id: str, amount: int):
    # transform time column to datetime format
    current_date = datetime(int(time_id[0:4]), (int(time_id[4:6]) - 1) * 3 + 1, 1)
    prev_date = current_date - relativedelta(months=3 * amount)
    # get the quartile to which each month belongs
    prev_quarter = (prev_date.month - 1) // 3 + 1
    return int(f"{prev_date.year}{prev_quarter}")


def calc_month_delta(time_id: str, amount: int):
    # transform time column to datetime format
    current_date = datetime.strptime(f"{time_id[0:4]}-{time_id[4:6]}", "%Y-%m")
    prev_date = current_date - relativedelta(months=amount)
    return int(prev_date.strftime("%Y%m"))


def calc_day_delta(time_id: str, amount: int):
    # Parse the time_id into a datetime instance
    date = datetime.strptime(time_id, "%Y%m%d")
    # Subtract the delta_days
    new_date = date - relativedelta(days=amount)
    # Return the new date in 'YYYYMMDD' format
    return int(new_date.strftime("%Y%m%d"))


def growth_calculation(query: AnyQuery, df: pl.DataFrame) -> pl.DataFrame:
    # Return df unchanged if Growth does not apply
    if not isinstance(query, DataQuery) or query.growth is None:
        return df

    # define parameters
    measure = query.growth.measure
    method = query.growth.method

    time_name = query.growth.time_level
    try:
        time = next(
            lvlfi
            for hiefi in query.fields_qualitative
            if hiefi.dimension.dim_type is DimensionType.TIME
            for lvlfi in hiefi.drilldown_levels
            if lvlfi.name == time_name
        )
    except StopIteration:
        msg = f"Time level '{time_name}' is required as a drilldown for its own growth calculation"
        raise InvalidQuery(msg) from None

    time_id = (
        time.name
        if time.level.get_name_column(query.locale) is None
        else f"{time.name} ID"
    )

    list_drilldowns = list(df.columns)
    list_drill_without_time_measure = [
        col for col in list_drilldowns if col not in {time_name, time_id, measure}
    ]

    if method[0] == "period":
        amount = method[1]

        df_current = df.with_columns(
            generate_lag_column(df[time_id], amount).alias("time_prev")
        )

        df = df_current.join(
            # filter the time_prev column string if it exists
            df.select(list_drill_without_time_measure + [time_id, measure]).rename(
                {time_id: "time_prev", measure: "previous_measure"}
            ),
            on=list_drill_without_time_measure + ["time_prev"],
            how="left",
        )

        # calculate the absolute change
        col_growth_value = pl.col(measure).cast(pl.Float64) - pl.col("previous_measure").cast(pl.Float64)
        # calculate the percentage change
        col_growth = (col_growth_value) / pl.col("previous_measure").cast(pl.Float64)

    else:
        type_caster = time.level.key_type.get_caster()
        member_key = type_caster(method[1])

        if len(list_drill_without_time_measure) == 0:
            # create a "dummy" column in case there are no columns for the join
            df = df.with_columns([pl.lit(1).alias("dummy")])

            list_drill_without_time_measure.append("dummy")

        # first, we get the values ​​at fixed time per group
        df_fixed = (
            df.filter(pl.col(time_id) == member_key)
            .select(list_drill_without_time_measure + [measure])
            .rename({measure: "previous_measure"})
        )

        # join the fixed values ​​to the original df
        df = df.join(df_fixed, on=list_drill_without_time_measure, how="left")

        # calculate the absolute change with a conditional
        col_growth_value = (
            pl.when(pl.col(time_id) < member_key)
            .then(pl.col("previous_measure").cast(pl.Float64) - pl.col(measure).cast(pl.Float64))
            .otherwise(pl.col(measure).cast(pl.Float64) - pl.col("previous_measure").cast(pl.Float64))
        )

        # calculate the percentage change with a conditional
        col_growth = (
            pl.when(pl.col(time_id) < member_key)
            .then(col_growth_value / pl.col(measure).cast(pl.Float64))
            .otherwise(col_growth_value / pl.col("previous_measure").cast(pl.Float64))
        )


    df = df.with_columns(
        col_growth_value.alias(f"{measure} Growth Value"),
        col_growth.alias(f"{measure} Growth"),
    )

    # remove temporary column 'previous measure' and 'dummy'
    columns_to_drop = ["previous_measure", "time_prev", "dummy"]
    existing_columns = [col for col in columns_to_drop if col in df.columns]
    df = df.drop(existing_columns)

    return df


class JoinParameters(TypedDict, total=False):
    on: Union[str, List[str]]
    coalesce: Optional[bool]
    join_nulls: bool
    left_on: Union[str, List[str]]
    right_on: Union[str, List[str]]
    suffix: str
    validate: Literal["m:m", "m:1", "1:m", "1:1"]


class JoinStep:
    data: pl.DataFrame
    keys: List[str]
    statuses: List[str]

    def __init__(
        self,
        data: pl.DataFrame,
        *,
        keys: List[str],
        statuses: List[str],
    ):
        self.data = data
        self.keys = keys
        self.statuses = statuses

    def join_with(self, result: Result[pl.DataFrame], join: JoinIntent):
        params: JoinParameters = {
            "suffix": join.suffix or "_",
            "validate": join.validate_relation,
            "join_nulls": join.join_nulls,
            "coalesce": join.coalesce,
        }

        if isinstance(join.on, (str, list)):
            params.update(on=join.on)
        elif isinstance(join.on, JoinOnColumns):
            params.update(left_on=join.on.left_on, right_on=join.on.right_on)

        return JoinStep(
            self.data.join(result.data, how=join.how, **params),
            keys=[*self.keys, result.cache["key"]],
            statuses=[*self.statuses, result.cache["status"]],
        )

    def get_result(self, pagi: PaginationIntent):
        df = self.data

        return Result(
            data=df.slice(pagi.offset, pagi.limit or None),
            columns={
                k: MemberType.from_str(str(v))
                for k, v in dict(zip(df.columns, df.dtypes)).items()
            },
            cache={
                "key": hashlib.md5("/".join(self.keys).encode("utf-8")).hexdigest(),
                "status": ",".join(self.statuses),
            },
            page={"limit": pagi.limit, "offset": pagi.offset, "total": df.height},
        )

    @classmethod
    def new(cls, result: Result[pl.DataFrame]):
        return cls(
            result.data,
            keys=[result.cache["key"]],
            statuses=[result.cache["status"]],
        )


def rename_columns(query: DataQuery, df: pl.DataFrame) -> pl.DataFrame:
    alias_label = {
        lvlfi.level.name: lvlfi.level_alias
        for hiefi in query.fields_qualitative
        for lvlfi in hiefi.drilldown_levels
        if lvlfi.level_alias is not None
    }
    alias_id = {
        f"{key} ID": f"{value} ID"
        for key, value in alias_label.items()
        if f"{key} ID" in df.columns
    }
    return df.rename({**alias_label, **alias_id})
