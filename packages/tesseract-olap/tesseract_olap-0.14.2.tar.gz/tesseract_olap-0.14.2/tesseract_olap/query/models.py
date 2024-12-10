"""Query-related internal structs module.

This module contains data-storing structs, used mainly on the query and backend
modules.
"""

import dataclasses as dcls
from copy import copy
from typing import (
    Any,
    Dict,
    FrozenSet,
    Iterable,
    List,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
)

from pydantic import BaseModel, Field, model_validator
from typing_extensions import Annotated

from tesseract_olap.common import Array, Prim, shorthash
from tesseract_olap.schema import (
    AnyMeasure,
    CalculatedMeasure,
    DimensionTraverser,
    HierarchyTraverser,
    LevelTraverser,
    MemberType,
    PropertyTraverser,
)

from .enums import (
    AnyOrder,
    Comparison,
    JoinType,
    LogicOperator,
    Membership,
    NullityOperator,
    Order,
    RestrictionAge,
    TimeScale,
)

NumericConstraint = Tuple[Union[Comparison, str], float]
ConditionOperator = Union[LogicOperator, Literal["and", "or"]]
MembershipConstraint = Tuple[Membership, Array[str]]

SingleFilterCondition = Tuple[NumericConstraint]
DoubleFilterCondition = Tuple[NumericConstraint, ConditionOperator, NumericConstraint]

FilterCondition = Union[
    NullityOperator,
    # MembershipConstraint,
    SingleFilterCondition,
    DoubleFilterCondition,
]


def parse_filter_condition(value: str) -> FilterCondition:
    if value.lower() in ("isnull", "isnotnull"):
        return NullityOperator.from_str(value)

    if ".and." in value:
        cond1, cond2 = value.split(".and.")
        return (
            parse_numeric_constraint(cond1),
            "and",
            parse_numeric_constraint(cond2),
        )

    if ".or." in value:
        cond1, cond2 = value.split(".or.")
        return (
            parse_numeric_constraint(cond1),
            "or",
            parse_numeric_constraint(cond2),
        )

    return (parse_numeric_constraint(value),)


def parse_numeric_constraint(value: Union[str, Sequence]) -> NumericConstraint:
    if isinstance(value, str):
        comparison, scalar = value.split(".", 1)
    else:
        assert len(value) == 2, (
            "Invalid numeric constraint, tuple must contain only the comparison "
            + f"operator and the scalar value. Found {value!r}"
        )
        comparison, scalar = value
    return Comparison.from_str(comparison), float(scalar)


class CutIntent(BaseModel):
    """Filtering instructions for a qualitative value.

    Instances of this class are used to define cut parameters.
    Its values are directly inputted by the user, so should never be considered
    valid by itself.
    """

    level: str
    include_members: Set[Prim]
    exclude_members: Set[Prim]

    @model_validator(mode="before")
    @classmethod
    def parse(cls, value: Any):
        if isinstance(value, str):
            level, members = value.split(":", 1)
            value = {
                "level": level.lstrip("~"),
                "include_members": [] if level.startswith("~") else members.split(","),
                "exclude_members": members.split(",") if level.startswith("~") else [],
            }

        if isinstance(value, Sequence):
            level, incl, excl, *_ = [*value, [], []]
            value = {"level": level, "include_members": incl, "exclude_members": excl}

        if isinstance(value, dict):
            nullables = ("", ",")
            include = value.get("include") or value["include_members"]
            value["include_members"] = set(include).difference(nullables)
            exclude = value.get("exclude") or value["exclude_members"]
            value["exclude_members"] = set(exclude).difference(nullables)

        return value


class FilterIntent(BaseModel):
    """Filtering instructions for a quantitative value.

    Instances of this class are used to define filter parameters.
    Its values are directly inputted by the user, so should never be considered
    valid by itself.
    """

    field: str
    condition: FilterCondition

    @model_validator(mode="before")
    @classmethod
    def parse(cls, value: Any):
        if isinstance(value, str):
            field, condition = value.split(".", 1)
            return {"field": field, "condition": parse_filter_condition(condition)}

        if isinstance(value, Sequence):
            field, *condition = value
            assert isinstance(field, str), (
                "When parsing a tuple, the first element must be a string with "
                + f"the name of the measure to apply the filter. Found {field!r}"
            )

            if len(condition) == 1:
                if isinstance(condition[0], str):
                    condition = parse_filter_condition(condition[0])
                else:
                    condition = (parse_numeric_constraint(condition[0]),)

            elif len(condition) == 3:
                assert condition[1] in ("and", "or"), (
                    "Joint in double condition tuple is not valid. "
                    + f"Accepted values are 'and' 'or', found {condition[1]!r}"
                )
                condition = (
                    parse_numeric_constraint(condition[0]),
                    LogicOperator.from_str(condition[1]),
                    parse_numeric_constraint(condition[2]),
                )

            else:
                raise ValueError(
                    "This filter has no valid conditions. "
                    + "You must provide one of the following configurations:\n"
                    + "A single string: 'isnull' / 'gte.0' / 'gt.1000.and.lte.100000'\n"
                    + "A single condition tuple: ('gt', 3000)\n"
                    + "A double condition tuple: ('>', 0), 'and', ('<=', 100)\n"
                    + f"Found {condition!r}"
                )

            return {"field": field, "condition": condition}

        return value

    def as_tuple(self):
        return self.field, self.condition


class JoinOnColumns(BaseModel):
    left_on: Union[str, List[str]]
    right_on: Union[str, List[str]]


class JoinIntent(BaseModel):
    """Specifies the intent of the user to perform a Join operation between 2 datasets."""

    on: Union[str, List[str], "JoinOnColumns", None] = None
    how: JoinType = JoinType.LEFT
    suffix: Optional[str] = None
    validate_relation: Literal["m:m", "m:1", "1:m", "1:1"] = "m:m"
    join_nulls: bool = False
    coalesce: Optional[bool] = None


class PaginationIntent(BaseModel):
    """Pagination instructions."""

    limit: Annotated[int, Field(ge=0)] = 0
    offset: Annotated[int, Field(ge=0)] = 0

    @model_validator(mode="before")
    @classmethod
    def parse(cls, value: Any):
        if isinstance(value, str):
            value = (0, 0) if value == "" else value.strip().split(",")

        if isinstance(value, Sequence):
            assert (
                0 < len(value) < 3
            ), f"Invalid pagination value, must provide 1 or 2 integers. Found {value!r}"
            return {"limit": value[0], "offset": value[1] if len(value) == 2 else 0}

        return value

    def as_tuple(self):
        return self.limit, self.offset


class SortingIntent(BaseModel):
    """Sorting instructions for internal use."""

    field: str
    order: AnyOrder

    @model_validator(mode="before")
    @classmethod
    def parse(cls, value: Any):
        if isinstance(value, str):
            field, order, *_ = f"{value}..".split(".")
            assert field, "Sorting field must be a valid column name"
            return {"field": field, "order": Order.from_str(order)}

        if isinstance(value, Sequence):
            field, order, *_ = [*value, ""]
            assert field, "Sorting field must be a valid column name"
            return {"field": field, "order": Order.from_str(order)}

        return value

    def as_tuple(self):
        return self.field, self.order


class TimeRestriction(BaseModel):
    """Time-axis filtering instructions for internal use.

    Instances of this class are used to define a time restriction over the
    resulting data. It must always contain both fields."""

    # TODO reformulate fields to use FilterCondition

    level: Union[str, TimeScale]
    age: RestrictionAge
    constraint: Optional[Union[int, str]] = None

    @model_validator(mode="before")
    @classmethod
    def parse(cls, value: Any):
        if isinstance(value, str):
            level, age, *constr = value.split(".", 2)

            assert level, (
                "Time restriction needs to specify a level from a time dimension, "
                "or a valid time scale available as level in this cube."
            )
            # Attempt to match a TimeScale, else use value as Level name
            gen_scale = (item for item in TimeScale if item.value == level)
            level = next(gen_scale, level)

            constraint = constr[0] if len(constr) == 1 else 1

            if age.lower() in ["latest", "last"]:
                age = RestrictionAge.LATEST
            elif age.lower() in ["oldest", "earliest"]:
                age = RestrictionAge.OLDEST
            elif age.lower() in {x.value for x in Comparison}:
                constraint = f"{age}.{constraint}"
                age = RestrictionAge.EXPR
            elif age.lower() in {x.value for x in NullityOperator}:
                constraint = age
                age = RestrictionAge.EXPR
            else:
                raise ValueError(f"Can't parse an age for the data: '{age}'")

            return {"level": level, "age": age, "constraint": constraint}

        return value


class TopkIntent(BaseModel):
    """Limits the results to the K first/last elements in subsets determined by
    one or more levels and their associated value. Adds a column that indicates
    the position of each element in that ranking."""

    levels: Tuple[str, ...]
    measure: str
    order: AnyOrder = Order.DESC
    amount: int = 1

    @model_validator(mode="before")
    @classmethod
    def parse(cls, value: Any):
        if isinstance(value, str):
            amount, levels, measure, order, *_ = f"{value}....".split(".")
            assert levels, (
                "Topk 'levels' field must contain at least a valid level name "
                "from the drilldowns in your request."
            )
            assert measure, (
                "Topk 'measure' field must contain a valid measure name "
                "from the measures in your request."
            )
            return {
                "amount": amount,
                "levels": levels.split(","),
                "measure": measure,
                "order": Order.from_str(order),
            }

        return value


class GrowthIntent(BaseModel):
    """Calculation of growth with respect to a time parameter and a measure"""

    time_level: str
    measure: str
    method: Union[
        Tuple[Literal["period"], int],
        Tuple[Literal["fixed"], str],
    ] = ("period", 1)

    @model_validator(mode="before")
    @classmethod
    def parse(cls, value: Any):
        if isinstance(value, str):
            time_level, measure, *params = value.split(".")
            assert time_level, (
                "Growth calculation requires the name of a level from a "
                "time dimension included in your request."
            )
            assert measure, (
                "Growth calculation must contain a valid measure name "
                "from the measures in your request."
            )
            assert len(params) > 1, (
                "Growth calculation method requires 2 parameters: "
                "'fixed' and the member key to use as anchor value, or "
                "'period' and an integer for how many periods to take as difference."
            )
            if params[0] == "fixed":
                method = ("fixed", params[1])
            else:
                method = ("period", int(params[1]))
            return {"time_level": time_level, "measure": measure, "method": method}

        return value


class AliasesIntent(BaseModel):
    """Aliases for levels"""

    aliases: Mapping[str, str]

    @model_validator(mode="before")
    @classmethod
    def parse(cls, value: Any):
        if isinstance(value, str):
            string = value.strip()
            assert string, "Aliases parameter cannot be empty"

            # transform the string into a dictionary
            alias_pairs = cls._validate_str_pairs(
                pair.split(":", 1) for pair in string.split(";") if ":" in pair
            )
            value = dict(alias_pairs)

        if isinstance(value, Mapping):
            return {"aliases": value}

        return value

    @staticmethod
    def _validate_str_pairs(generator: Iterable[List[str]]):
        seen_keys = set()
        for name, alias in generator:
            clean_name, clean_alias = name.strip(), alias.strip()
            assert clean_name, f"Empty level name in alias pair: '{name}:{alias}'"
            assert clean_alias, f"Empty level alias in alias pair: '{name}:{alias}'"
            assert (
                clean_name not in seen_keys
            ), f"Request contains two aliases for the same level: '{clean_name}'"
            seen_keys.add(clean_name)
            yield clean_name, clean_alias


@dcls.dataclass(eq=True, frozen=True, order=False)
class HierarchyField:
    """Contains the parameters associated to a slicing operation on the data,
    based on a single Hierarchy from a Cube's Dimension.
    """

    dimension: "DimensionTraverser"
    hierarchy: "HierarchyTraverser"
    levels: Tuple["LevelField", ...]

    def __copy__(self):
        return HierarchyField(
            dimension=self.dimension,
            hierarchy=self.hierarchy,
            levels=tuple(self.levels),
        )

    @property
    def alias(self) -> str:
        """Returns a deterministic unique short ID for the entity."""
        return shorthash(self.dimension.name + self.hierarchy.primary_key)

    @property
    def cut_levels(self) -> Iterable["LevelField"]:
        return (item for item in self.levels if item.is_cut)

    @property
    def drilldown_levels(self) -> Iterable["LevelField"]:
        return (item for item in self.levels if item.is_drilldown)

    @property
    def deepest_level(self) -> "LevelField":
        """Returns the deepest LevelField requested in this Hierarchy, for this
        query operation."""
        # TODO: check if is needed to force this to use drilldowns only
        return self.levels[-1]

    @property
    def foreign_key(self) -> str:
        """Returns the column in the fact table of the Cube this Dimension
        belongs to, that matches the primary key of the items in the dim_table.
        """
        return self.dimension.foreign_key  # type: ignore

    @property
    def has_drilldowns(self) -> bool:
        """Verifies if any of the contained LevelFields is being used as a
        drilldown."""
        return any(self.drilldown_levels)

    @property
    def primary_key(self) -> str:
        """Returns the column in the dimension table for the parent Dimension,
        which is used as primary key for the whole set of levels in the chosen
        Hierarchy."""
        return self.hierarchy.primary_key

    @property
    def table(self):
        """Returns the table to use as source for the Dimension data. If not
        set, the data is stored directly in the fact table for the Cube."""
        return self.hierarchy.table


@dcls.dataclass(eq=True, frozen=True, order=False, repr=False)
class LevelField:
    """Contains the parameters associated to the slice operation, specifying the
    columns each resulting group should provide to the output data.
    """

    level: "LevelTraverser"
    level_alias: Optional[str] = None
    caption: Optional["PropertyTraverser"] = None
    is_drilldown: bool = False
    members_exclude: Set[str] = dcls.field(default_factory=set)
    members_include: Set[str] = dcls.field(default_factory=set)
    properties: FrozenSet["PropertyTraverser"] = dcls.field(default_factory=frozenset)
    time_restriction: Optional[TimeRestriction] = None

    def __copy__(self):
        return LevelField(
            level=self.level,
            level_alias=self.level_alias,
            caption=self.caption,
            is_drilldown=self.is_drilldown,
            members_exclude=set(self.members_exclude),
            members_include=set(self.members_include),
            properties=frozenset(self.properties),
            time_restriction=(
                self.time_restriction.model_copy() if self.time_restriction else None
            ),
        )

    def __repr__(self):
        params = (
            f"name={self.level.name!r}",
            f"is_drilldown={self.is_drilldown!r}",
            f"alias={self.level_alias!r}",
            f"caption={self.caption!r}",
            f"properties={sorted(self.properties, key=lambda x: x.name)!r}",
            f"cut_exclude={sorted(self.members_exclude)!r}",
            f"cut_include={sorted(self.members_include)!r}",
            f"time_restriction={self.time_restriction!r}",
        )
        return f"{type(self).__name__}({', '.join(params)})"

    @property
    def alias(self) -> str:
        """Returns a deterministic unique short ID for the entity."""
        return shorthash(self.level.name + self.level.key_column)

    @property
    def is_cut(self) -> bool:
        return len(self.members_exclude) + len(self.members_include) > 0

    @property
    def key_column(self) -> str:
        return self.level.key_column

    @property
    def name(self) -> str:
        return self.level.name

    def iter_columns(self, locale: str):
        """Generates triads of (column name, column alias, pair hash) for all fields related to
        a HierarchyField object.

        This comprises Drilldown Labels and IDs, and its requested Properties.
        """
        name = self.level.name
        key_column = self.level.key_column
        name_column = self.level.get_name_column(locale)
        if name_column is None:
            yield key_column, name, shorthash(name + key_column)
        else:
            yield key_column, f"{name} ID", shorthash(name + key_column)
            yield name_column, name, shorthash(name + name_column)
        for propty in self.properties:
            propty_column = propty.get_key_column(locale)
            yield propty_column, propty.name, shorthash(propty.name + propty_column)


@dcls.dataclass(eq=True, frozen=True, order=False, repr=False)
class MeasureField:
    """MeasureField dataclass.

    Contains the parameters needed to filter the data points returned by the
    query operation from the server.
    """

    measure: "AnyMeasure"
    is_measure: bool = False
    constraint: Optional[FilterCondition] = None
    with_ranking: Optional[Literal["asc", "desc"]] = None

    def __copy__(self):
        return MeasureField(
            measure=self.measure,
            is_measure=self.is_measure,
            constraint=(
                copy(self.constraint)
                if isinstance(self.constraint, tuple)
                else self.constraint
            ),
            with_ranking=self.with_ranking,
        )

    def __repr__(self):
        params = (
            f"name={repr(self.measure.name)}",
            f"is_measure={repr(self.is_measure)}",
            f"constraint={repr(self.constraint)}",
            f"with_ranking={repr(self.with_ranking)}",
        )
        return f"{type(self).__name__}({', '.join(params)})"

    @property
    def alias_name(self):
        """Returns a deterministic short hash of the name of the entity."""
        return shorthash(self.measure.name)

    @property
    def alias_key(self):
        """Returns a deterministic hash of the key column of the entity."""
        return shorthash(
            repr(self.measure.formula)
            if isinstance(self.measure, CalculatedMeasure)
            else self.measure.key_column
        )

    @property
    def name(self) -> str:
        """Quick method to return the measure name."""
        return self.measure.name

    @property
    def aggregator_params(self) -> Dict[str, str]:
        """Quick method to retrieve the measure aggregator params."""
        return self.measure.aggregator.get_params()

    @property
    def aggregator_type(self) -> str:
        """Quick method to retrieve the measure aggregator type."""
        return str(self.measure.aggregator)

    def get_source(self):
        # TODO add locale compatibility
        """Quick method to obtain the source information of the measure."""
        return self.measure.annotations.get("source")

    @property
    def datatype(self):
        return MemberType.FLOAT64
