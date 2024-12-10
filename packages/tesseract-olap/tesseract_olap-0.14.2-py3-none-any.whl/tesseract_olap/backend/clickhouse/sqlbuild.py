"""ClickHouse SQL generation module.

Comprises all the functions which generate SQL code, through the pypika library.
"""

import logging
from itertools import chain
from typing import Callable, Optional, Set, Tuple, Union

import immutables as immu
from pyparsing import ParseResults
from pypika import analytics as an
from pypika import functions as fn
from pypika.dialects import ClickHouseQuery, QueryBuilder
from pypika.enums import Arithmetic, Order
from pypika.queries import AliasedQuery, Join, Selectable, Table
from pypika.terms import (
    ArithmeticExpression,
    Case,
    Criterion,
    Field,
    Function,
    NullValue,
    PyformatParameter,
    Term,
    ValueWrapper,
)

from tesseract_olap.backend import ParamManager
from tesseract_olap.common import shorthash
from tesseract_olap.query import (
    Comparison,
    DataQuery,
    FilterCondition,
    LogicOperator,
    MeasureField,
    MembersQuery,
    NullityOperator,
    NumericConstraint,
    RestrictionAge,
    parse_filter_condition,
)
from tesseract_olap.schema import CubeTraverser, MemberType, models

from .dialect import (
    ArrayElement,
    AverageWeighted,
    ClickhouseJoinType,
    DistinctCount,
    Median,
    Power,
    Quantile,
    TopK,
)

logger = logging.getLogger("tesseract_olap.backend.clickhouse")


def count_dataquery_sql(query: DataQuery) -> Tuple[QueryBuilder, ParamManager]:
    """"""

    def _convert_table(
        table: Union[models.Table, models.InlineTable], alias: Optional[str]
    ):
        """Converts schema-defined tables into query tables for SQL generation."""
        if isinstance(table, models.Table):
            return Table(table.name, schema=table.schema, alias=alias)
        else:
            meta.set_table(table)
            return Table(table.name, alias=alias)

    def _get_table(
        table: Union[models.Table, models.InlineTable, None],
        *,
        alias: Optional[str] = None,
    ) -> Table:
        """Returns a specified table or the default fact table if not specified."""
        return table_fact if table is None else _convert_table(table, alias)

    meta = ParamManager()
    table_fact = _convert_table(query.cube.table, "tfact")  # Core fact table
    tfact_is_subset = query.cube.subset_table  # Checks if fact table is a subset

    qb = ClickHouseQuery.from_(table_fact)

    for hiefi in query.fields_qualitative:
        table_dim = _get_table(hiefi.table, alias=f"ft_{hiefi.alias}")

        # Foreign key in fact table
        field_fkey = table_fact.field(hiefi.foreign_key)

        drilldowns = tuple(hiefi.drilldown_levels)
        deepest_drilldown = drilldowns[-1] if drilldowns else None

        should_join = False

        for lvlfi in hiefi.levels:
            caster = lvlfi.level.type_caster
            members_include = sorted(caster(mem) for mem in lvlfi.members_include)
            members_exclude = sorted(caster(mem) for mem in lvlfi.members_exclude)

            # When the dimension table is the fact table, all columns are
            # already in the fact table, so no JOIN is needed
            if table_dim is table_fact:
                if lvlfi is deepest_drilldown:
                    field = table_fact.field(lvlfi.key_column)
                    qb = qb.select(field).groupby(field)

                if len(members_include) > 0:
                    qb = qb.where(
                        table_fact.field(lvlfi.key_column).isin(members_include)
                    )

                if len(members_exclude) > 0:
                    qb = qb.where(
                        table_fact.field(lvlfi.key_column).notin(members_exclude)
                    )

            # When the cut is being applied on the same column used as foreign key,
            # we can use the foreign key column instead of the primary key column
            elif lvlfi.key_column == hiefi.primary_key:
                if lvlfi is deepest_drilldown:
                    qb = qb.select(field_fkey).groupby(field_fkey)

                if len(members_include) > 0:
                    qb = qb.where(field_fkey.isin(members_include))

                if len(members_exclude) > 0:
                    qb = qb.where(field_fkey.notin(members_exclude))

            # Otherwise, apply cuts via subqueries on the dimension table
            else:
                if lvlfi is deepest_drilldown:
                    field = table_dim.field(lvlfi.key_column)
                    qb = qb.select(field).groupby(field)

                should_join = True
                subq = (
                    ClickHouseQuery.from_(table_dim)
                    .select(hiefi.primary_key)
                    .distinct()
                )

                if len(members_include) > 0:
                    subq = subq.where(
                        table_dim.field(lvlfi.key_column).isin(members_include)
                    )
                if len(members_exclude) > 0:
                    subq = subq.where(
                        table_dim.field(lvlfi.key_column).notin(members_exclude)
                    )
                if lvlfi.is_cut:
                    qb = qb.where(field_fkey.isin(subq))

        # Apply LEFT JOIN if a column from a different dimension table is needed
        # this includes PK columns for cuts on members not in the fact table
        if table_dim is not table_fact and (
            should_join or any(item for item in hiefi.levels if item.time_restriction)
        ):
            qb = qb.left_join(table_dim).on(
                table_dim.field(hiefi.primary_key) == field_fkey
            )

        # Apply subset filtering if the fact table contains records for multiple levels
        if table_dim is not table_fact and tfact_is_subset:
            qb = qb.where(
                field_fkey.isin(
                    ClickHouseQuery.from_(table_dim)
                    .select(hiefi.primary_key)
                    .distinct()
                )
            )

    # Apply time restrictions if defined in any hierarchy level
    # Restrictions are like cuts with relative indications; need to be handled afterwards
    time_restriction = False
    for hiefi in query.fields_qualitative:
        table_dim = _get_table(hiefi.table, alias=f"ft_{hiefi.alias}")

        field_fkey = table_fact.field(hiefi.foreign_key)

        for lvlfi in hiefi.levels:
            if lvlfi.time_restriction is not None:
                order = (
                    Order.asc
                    if lvlfi.time_restriction.age == RestrictionAge.OLDEST
                    else Order.desc
                )

                # we intend to create a subquery on the fact table for all
                # possible members of the relevant level/timescale, using
                # distinct unify, and get the first in the defined order
                # which translates into latest/oldest

                # TODO: use EXPLAIN to see if DISTINCT improves or worsens the query
                field_time = table_dim.field(lvlfi.key_column)

                if lvlfi.time_restriction.age == RestrictionAge.EXPR:
                    time_constraint = parse_filter_condition(
                        str(lvlfi.time_restriction.constraint)
                    )
                    criterion = _get_filter_criterion(field_time, time_constraint)
                    qb = qb.having(criterion)

                elif table_dim is table_fact:
                    # Hierarchy is defined in the fact table -> direct query
                    time_subqb = qb.select(field_time.as_("time_restr")).groupby(
                        field_time
                    )
                    time_qb = (
                        ClickHouseQuery.from_(time_subqb)
                        .select(time_subqb.field("time_restr"))
                        .distinct()
                        .orderby(time_subqb.field("time_restr"), order=order)
                        .limit(lvlfi.time_restriction.constraint)
                    )
                    qb = qb.where(field_time.isin(time_qb))

                elif lvlfi.key_column == hiefi.primary_key:
                    # The level column is used as foreign key for the fact table
                    time_subqb = qb.select(field_fkey.as_("time_restr")).groupby(
                        field_fkey
                    )
                    time_qb = (
                        ClickHouseQuery.from_(time_subqb)
                        .select(time_subqb.field("time_restr"))
                        .distinct()
                        .orderby(time_subqb.field("time_restr"), order=order)
                        .limit(lvlfi.time_restriction.constraint)
                    )
                    qb = qb.where(field_fkey.isin(time_qb))

                else:
                    time_subqb = qb.select(field_time.as_("time_restr")).groupby(
                        field_time
                    )
                    time_qb = (
                        ClickHouseQuery.from_(time_subqb)
                        .select(time_subqb.field("time_restr"))
                        .distinct()
                        .orderby(time_subqb.field("time_restr"), order=order)
                        .limit(lvlfi.time_restriction.constraint)
                    )
                    qb = qb.where(field_time.isin(time_qb))

                time_restriction = True
                break

        if time_restriction:
            break

    return ClickHouseQuery.from_(qb).select(fn.Count("*")), meta


def count_membersquery_sql(query: MembersQuery) -> Tuple[QueryBuilder, ParamManager]:
    qb, meta = membersquery_sql(query)
    return ClickHouseQuery.from_(qb).select(fn.Count("*")), meta


def dataquery_sql(query: DataQuery) -> Tuple[QueryBuilder, ParamManager]:
    """Build the query which will retrieve an aggregated dataset from the
    database.

    The construction of this query has two main parts:
    - The Core Query,
        which retrieves all the columns needed for later steps, and applies the
        filter on the qualitative fields (cuts)
    - The Grouping Query,
        which applies the calculations/aggregations over the data, filters on
        quantitative fields (filters), applies pagination, sorting and the
        aliases over the columns

    The returned query is composed by the Grouping query on the Core query as
    subquery.
    """
    # Manages parameters for safe SQL execution
    meta = ParamManager()

    # Converts schema-defined tables into query tables for SQL generation
    def _convert_table(
        table: Union[models.Table, models.InlineTable], alias: Optional[str]
    ):
        if isinstance(table, models.Table):
            return Table(table.name, schema=table.schema, alias=alias)
        else:
            meta.set_table(table)
            return Table(table.name, alias=alias)

    # Returns a specified table or the default fact table if not specified
    def _get_table(
        table: Union[models.Table, models.InlineTable, None],
        *,
        alias: Optional[str] = None,
    ) -> Table:
        return table_fact if table is None else _convert_table(table, alias)

    locale = query.locale  # Locale information for translations
    table_fact = _convert_table(query.cube.table, "tfact")  # Core fact table
    tfact_is_subset = query.cube.subset_table  # Checks if fact table is a subset

    # Constructs the Core Query to retrieve necessary fields and apply qualitative cuts
    def dataquery_tcore_sql() -> QueryBuilder:
        """
        Build the query which will create the `core_table`, an intermediate query
        which contains all data from the Dimension Tables and the Fact Table the
        cube is associated to.

        This query also retrieves the row for all associated dimensions used in
        drilldowns and cuts, through a LEFT JOIN using the foreign key.
        """
        # Base query from the fact table
        qb = ClickHouseQuery.from_(table_fact)

        key_columns = (
            # from the fact table, get the fields which contain the values
            # to aggregate and filter; ensure to not duplicate key_column
            Field(
                item.measure.key_column,
                alias=f"ms_{item.alias_key}",
                table=table_fact,
            )
            # ensure key_columns are being selected just once
            for item in dict(
                (obj.alias_key, obj) for obj in query.fields_quantitative
            ).values()
            if isinstance(item.measure, models.Measure)
        )
        param_columns = set(
            Field(column, alias=f"msp_{msrfi.alias_key}_{alias}", table=table_fact)
            for msrfi in query.fields_quantitative
            for alias, column in msrfi.measure.aggregator.get_columns()
        )

        qb = qb.select(*key_columns, *param_columns)

        # Processes each qualitative field, applying necessary joins and filters
        for hiefi in query.fields_qualitative:
            table_dim = _get_table(hiefi.table, alias=f"ft_{hiefi.alias}")

            # Foreign key in fact table
            field_fkey = table_fact.field(hiefi.foreign_key)

            # Store dimension fields to be selected
            columns: Set[Field] = set()

            # Process each level, applying cuts and building columns for selection
            for lvlfi in hiefi.levels:
                caster = lvlfi.level.type_caster
                members_include = sorted(caster(mem) for mem in lvlfi.members_include)
                members_exclude = sorted(caster(mem) for mem in lvlfi.members_exclude)

                # Collect columns for this level, using locale-specific aliases
                lvl_columns = [
                    Field(column, table=table_dim, alias=f"lv_{alias}")
                    for column, _, alias in lvlfi.iter_columns(locale)
                ]

                # When the dimension table is the fact table, all columns are
                # already in the fact table, so no JOIN is needed
                if table_dim is table_fact:
                    if len(members_include) > 0:
                        qb = qb.where(
                            table_fact.field(lvlfi.key_column).isin(members_include)
                        )

                    if len(members_exclude) > 0:
                        qb = qb.where(
                            table_fact.field(lvlfi.key_column).notin(members_exclude)
                        )

                # When the cut is being applied on the same column used as foreign key,
                # we can use the foreign key column instead of the primary key column
                elif lvlfi.key_column == hiefi.primary_key:
                    # for _yield_lvlfi_columns, index 0 is the ID column
                    lvl_columns[0] = Field(
                        hiefi.foreign_key, table=table_fact, alias=lvl_columns[0].alias
                    )

                    if len(members_include) > 0:
                        qb = qb.where(field_fkey.isin(members_include))

                    if len(members_exclude) > 0:
                        qb = qb.where(field_fkey.notin(members_exclude))

                # Otherwise, apply cuts via subqueries on the dimension table
                elif lvlfi.is_cut:
                    subq = ClickHouseQuery.from_(table_dim).select(hiefi.primary_key)

                    if len(members_include) > 0:
                        subq = subq.where(
                            table_dim.field(lvlfi.key_column).isin(members_include)
                        )

                    if len(members_exclude) > 0:
                        subq = subq.where(
                            table_dim.field(lvlfi.key_column).notin(members_exclude)
                        )

                    qb = qb.where(field_fkey.isin(subq))

                # Include drilldown columns in the selection
                if lvlfi.is_drilldown:
                    columns.update(lvl_columns)

            # Select all relevant columns after sorting by name
            qb = qb.select(*sorted(columns, key=lambda x: x.name))

            # Apply LEFT JOIN if a column from a different dimension table is needed
            # this includes PK columns for cuts on members not in the fact table
            if table_dim is not table_fact and (
                any(field.table is not table_fact for field in columns)
                or any(
                    item
                    for item in hiefi.levels
                    if item.is_cut or item.time_restriction
                )
            ):
                qb = qb.left_join(table_dim).on(
                    table_dim.field(hiefi.primary_key) == field_fkey
                )

            # Apply subset filtering if the fact table contains records for multiple levels
            if table_dim is not table_fact and tfact_is_subset:
                qb = qb.where(
                    field_fkey.isin(
                        ClickHouseQuery.from_(table_dim)
                        .select(hiefi.primary_key)
                        .distinct()
                    )
                )

        # Apply time restrictions if defined in any hierarchy level
        # Restrictions are like cuts with relative indications; need to be handled afterwards
        time_restriction = False
        for hiefi in query.fields_qualitative:
            table_dim = _get_table(hiefi.table, alias=f"ft_{hiefi.alias}")

            field_fkey = table_fact.field(hiefi.foreign_key)

            for lvlfi in hiefi.levels:
                if lvlfi.time_restriction is not None:
                    order = (
                        Order.asc
                        if lvlfi.time_restriction.age == RestrictionAge.OLDEST
                        else Order.desc
                    )

                    # we intend to create a subquery on the fact table for all
                    # possible members of the relevant level/timescale, using
                    # distinct unify, and get the first in the defined order
                    # which translates into latest/oldest

                    # TODO: use EXPLAIN to see if DISTINCT improves or worsens the query
                    field_time = table_dim.field(lvlfi.key_column)

                    if lvlfi.time_restriction.age == RestrictionAge.EXPR:
                        time_constraint = parse_filter_condition(
                            str(lvlfi.time_restriction.constraint)
                        )
                        criterion = _get_filter_criterion(field_time, time_constraint)
                        qb = qb.having(criterion)

                    elif table_dim is table_fact:
                        # Hierarchy is defined in the fact table -> direct query
                        qb = qb.where(
                            field_time.isin(
                                ClickHouseQuery.from_(
                                    qb.select(field_time.as_("time_restr"))
                                )
                                .select(Field("time_restr"))
                                .distinct()
                                .orderby(Field("time_restr"), order=order)
                                .limit(lvlfi.time_restriction.constraint)
                            )
                        )

                    elif lvlfi.key_column == hiefi.primary_key:
                        # The level column is used as foreign key for the fact table
                        qb = qb.where(
                            field_fkey.isin(
                                ClickHouseQuery.from_(
                                    qb.select(field_fkey.as_("time_restr"))
                                )
                                .select(Field("time_restr"))
                                .distinct()
                                .orderby(Field("time_restr"), order=order)
                                .limit(lvlfi.time_restriction.constraint)
                            )
                        )

                    else:
                        qb = qb.where(
                            field_time.isin(
                                ClickHouseQuery.from_(
                                    qb.select(field_time.as_("time_restr"))
                                )
                                .select(Field("time_restr"))
                                .distinct()
                                .orderby(Field("time_restr"), order=order)
                                .limit(lvlfi.time_restriction.constraint)
                            )
                        )

                    time_restriction = True
                    break

            if time_restriction:
                break

        return qb.as_("tcore")

    def dataquery_tgroup_sql(tcore: QueryBuilder) -> QueryBuilder:
        """
        Builds the query which will perform the grouping by drilldown members,
        and then the aggregation over the resulting groups.
        """
        qb: QueryBuilder = ClickHouseQuery.from_(tcore)

        level_columns = immu.Map(
            (column_name, f"lv_{column_alias}")
            for hiefi in query.fields_qualitative
            for lvlfi in hiefi.levels
            for _, column_name, column_alias in lvlfi.iter_columns(query.locale)
        )

        def _yield_measures(msrfi: MeasureField):
            """Yields the expressions for aggregated/calculated columns of a MeasureField."""
            if isinstance(msrfi.measure, models.Measure):
                yield _get_aggregate(tcore, msrfi)

            if isinstance(msrfi.measure, models.CalculatedMeasure):
                formula = msrfi.measure.formula
                yield _transf_formula(formula, _translate_col).as_(msrfi.name)

            # Creates Ranking columns using window functions
            if msrfi.with_ranking is not None:
                yield an.Rank(alias=f"{msrfi.name} Ranking").orderby(
                    Field(msrfi.name),
                    order=Order.asc if msrfi.with_ranking == "asc" else Order.desc,
                )

        # Translates column names to fields in the grouping query
        def _translate_col(column: str):
            return Field(
                level_columns.get(column, column),
                table=tcore if column in level_columns else None,
            )

        measure_fields = (
            term
            for msrfi in query.fields_quantitative
            for term in _yield_measures(msrfi)
        )

        level_fields = (
            Field(f"lv_{alias}", alias=name, table=tcore)
            for hiefi in query.fields_qualitative
            for lvlfi in hiefi.drilldown_levels
            for _, name, alias in lvlfi.iter_columns(locale)
        )

        groupby_fields = (
            tcore.field(f"lv_{alias}")
            for hiefi in query.fields_qualitative
            for lvlfi in hiefi.drilldown_levels
            for _, _, alias in lvlfi.iter_columns(locale)
        )
        qb = qb.groupby(*groupby_fields)

        # Default sorting directions
        # The results are sorted by the ID column of each drilldown
        # If there's a topK directive, only the levels used to build the partitions
        # will be considered for sorting, as it meddles with the Top Measure column.
        order = Order.asc
        orderby = (
            tcore.field(f"lv_{hiefi.deepest_level.alias}")
            for hiefi in query.fields_qualitative
            if (
                hiefi.has_drilldowns
                and (not query.topk or hiefi.deepest_level.name in query.topk.levels)
            )
        )

        # Flag to know an user-defined sorting field hasn't been set
        sort_field = None  # Track if a specific sorting field was set

        # Apply user-defined filters on aggregated data
        for msrfi in query.fields_quantitative:
            if not msrfi.constraint:
                continue

            criterion = _get_filter_criterion(Field(msrfi.name), msrfi.constraint)
            qb = qb.having(criterion)

        for hiefi in query.fields_qualitative:
            # skip field if is not a drilldown
            if not hiefi.has_drilldowns:
                continue

            # User-defined sorting directions for Properties
            if sort_field is None and query.sorting:
                sort_field, sort_order = query.sorting.as_tuple()
                # TODO: this method could still use a drilldown for sorting, check
                field_finder = (
                    tcore.field(f"lv_{alias}")
                    for lvlfi in hiefi.drilldown_levels
                    for _, name, alias in lvlfi.iter_columns(locale)
                    if name == sort_field
                )
                sort_field = next(field_finder, None)
                if sort_field is not None:
                    order = Order.asc if sort_order == "asc" else Order.desc
                    orderby = chain((sort_field,), orderby)

        # User-defined sorting directions for Measures
        if sort_field is None and query.sorting:
            sort_field, sort_order = query.sorting.as_tuple()
            field_finder = (
                Field(msrfi.name)
                for msrfi in query.fields_quantitative
                if msrfi.name == sort_field
            )
            sort_field = next(field_finder, None)
            if sort_field is not None:
                order = Order.asc if sort_order == "asc" else Order.desc
                orderby = chain((sort_field,), orderby)

        qb = qb.orderby(*orderby, order=order)

        if query.topk:
            topk_fields = [Field(x) for x in query.topk.levels]
            topk_colname = f"Top {query.topk.measure}"
            topk_order = Order.asc if query.topk.order == "asc" else Order.desc

            subquery = (
                qb.select(*measure_fields, *level_fields)
                .select(
                    an.RowNumber()
                    .over(*topk_fields)
                    .orderby(Field(query.topk.measure), order=topk_order)
                    .as_(topk_colname),
                )
                .orderby(Field(topk_colname), order=Order.asc)
            )

            qb = (
                ClickHouseQuery.from_(subquery)
                .select(subquery.star)
                .where(subquery.field(topk_colname) <= query.topk.amount)
            )

        else:
            qb = qb.select(*measure_fields, *level_fields)

        # apply pagination parameters if values are higher than zero
        limit, offset = query.pagination.as_tuple()
        if limit > 0:
            qb = qb.limit(limit)
        if offset > 0:
            qb = qb.offset(offset)

        return qb.as_("tgroup")

    # Constructs the Base Record Query, containing the filtered rows to be aggregated
    table_core = dataquery_tcore_sql()

    # Constructs the Grouping Query, applying drilldowns, aggregations, and filters
    table_group = dataquery_tgroup_sql(table_core)

    # Wrap the query to get rid of the measures not in the request
    if any(not msrfi.is_measure for msrfi in query.fields_quantitative):
        drilldowns = (
            column_name
            for hiefi in query.fields_qualitative
            for lvlfi in hiefi.drilldown_levels
            for _, column_name, _ in lvlfi.iter_columns(locale)
        )
        measures = (
            measure.name
            for msrfi in query.fields_quantitative
            if msrfi.is_measure
            for measure in msrfi.measure.and_submeasures()
        )
        table_with = (
            ClickHouseQuery.with_(table_group, "mq")
            .from_(AliasedQuery("mq"))
            .select(*drilldowns, *measures)
        )
        return table_with, meta

    return table_group, meta


def membersquery_sql(query: MembersQuery) -> Tuple[QueryBuilder, ParamManager]:
    """Build the query which will list all the members of a Level in a dimension
    table.

    Depending on the filtering parameters set by the user, this list can also
    be limited by pagination, search terms, or members observed in a fact table.
    """
    meta = ParamManager()

    def _convert_table(
        table: Union[models.Table, models.InlineTable], alias: Optional[str]
    ):
        if isinstance(table, models.Table):
            return Table(table.name, schema=table.schema, alias=alias)
        else:
            meta.set_table(table)
            return Table(table.name, alias=alias)

    locale = query.locale
    hiefi = query.hiefield

    table_fact = _convert_table(query.cube.table, "tfact")

    table_dim = (
        _convert_table(query.cube.table, "tdim")
        if hiefi.table is None
        else _convert_table(hiefi.table, "tdim")
    )

    ancestor_columns = tuple(
        (alias, column_name)
        for depth, lvlfi in enumerate(hiefi.levels[:-1])
        for alias, column_name in (
            (f"ancestor.{depth}.key", lvlfi.level.key_column),
            (f"ancestor.{depth}.caption", lvlfi.level.get_name_column(locale)),
        )
        if column_name is not None
    )
    level_columns = ancestor_columns + tuple(
        (alias, column_name)
        for alias, column_name in (
            ("key", hiefi.deepest_level.level.key_column),
            ("caption", hiefi.deepest_level.level.get_name_column(locale)),
        )
        if column_name is not None
    )

    level_fields = tuple(
        Field(column_name, alias=alias, table=table_dim)
        for alias, column_name in level_columns
    )

    subquery = (
        ClickHouseQuery.from_(table_fact)
        .select(table_fact.field(hiefi.foreign_key))
        .distinct()
        .as_("tfact_distinct")
    )

    qb: QueryBuilder = (
        ClickHouseQuery.from_(table_dim)
        .right_join(subquery)
        .on(subquery.field(hiefi.foreign_key) == table_dim.field(hiefi.primary_key))
        .select(*level_fields)
        .distinct()
        .orderby(*level_fields, order=Order.asc)
    )

    limit, offset = query.pagination.as_tuple()
    if limit > 0:
        qb = qb.limit(limit)
    if offset > 0:
        qb = qb.offset(offset)

    if query.search is not None:
        pname = meta.set_param(f"%{query.search}%")
        param = PyformatParameter(pname)
        search_criterion = Criterion.any(
            Field(field).ilike(param)  # type: ignore
            for lvlfield in query.hiefield.levels
            for field in (
                lvlfield.level.key_column
                if lvlfield.level.key_type == MemberType.STRING
                else None,
                lvlfield.level.get_name_column(locale),
            )
            if field is not None
        )
        qb = qb.where(search_criterion)

    return qb, meta


def membercountquery_sql(cube: "CubeTraverser"):
    fact_table = Table(cube.table.name, alias="tfact")
    query = ClickHouseQuery._builder()
    meta = ParamManager()
    flag_join = False

    for dimension in cube.dimensions:
        for hierarchy in dimension.hierarchies:
            table = hierarchy.table
            table_alias = shorthash(f"{dimension.name}.{hierarchy.name}")
            levels = [(level, shorthash(level.name)) for level in hierarchy.levels]

            if table is None:
                gen_columns = (
                    fn.Count(fact_table.field(level.key_column), alias).distinct()
                    for level, alias in levels
                )
                tquery = (
                    ClickHouseQuery.from_(fact_table)
                    .select(*gen_columns)
                    .as_(f"sq_{table_alias}")
                )

            else:
                if isinstance(table, models.InlineTable):
                    meta.set_table(table)

                dim_table = Table(table.name, alias="tdim")

                gen_columns = (
                    fn.Count(dim_table.field(level.key_column), alias).distinct()
                    for level, alias in levels
                )
                tquery = (
                    ClickHouseQuery.from_(dim_table)
                    .select(*gen_columns)
                    .where(
                        dim_table.field(hierarchy.primary_key).isin(
                            ClickHouseQuery.from_(fact_table)
                            .select(fact_table.field(dimension.foreign_key))
                            .distinct()
                        )
                    )
                    .as_(f"sq_{table_alias}")
                )

            if flag_join:
                query.do_join(Join(tquery, how=ClickhouseJoinType.paste))
            else:
                query = query.from_(tquery)
                flag_join = True

            gen_fields = (
                tquery.field(alias).as_(level.name) for level, alias in levels
            )
            query = query.select(*gen_fields)

    return query, meta


def _get_aggregate(
    table: Selectable, msrfi: MeasureField
) -> Union[Function, ArithmeticExpression]:
    """Generates an AggregateFunction instance from a measure, including all its
    parameters, to be used in the SQL query.
    """
    field = table.field(f"ms_{msrfi.alias_key}")
    # alias = f"ag_{msrfi.alias_name}"
    alias = msrfi.name

    if msrfi.aggregator_type == "Sum":
        return fn.Sum(field, alias=alias)

    elif msrfi.aggregator_type == "Count":
        return fn.Count(field, alias=alias)

    elif msrfi.aggregator_type == "Average":
        return fn.Avg(field, alias=alias)

    elif msrfi.aggregator_type == "Max":
        return fn.Max(field, alias=alias)

    elif msrfi.aggregator_type == "Min":
        return fn.Min(field, alias=alias)

    elif msrfi.aggregator_type == "Mode":
        return ArrayElement(TopK(1, field), 1, alias=alias)

    # elif msrfi.aggregator_type == "BasicGroupedMedian":
    #     return fn.Abs()

    elif msrfi.aggregator_type == "WeightedSum":
        params = msrfi.aggregator_params
        weight_field = table.field(f"msp_{msrfi.alias_key}_weight")
        return fn.Sum(field * weight_field, alias=alias)

    elif msrfi.aggregator_type == "WeightedAverage":
        params = msrfi.aggregator_params
        weight_field = table.field(f"msp_{msrfi.alias_key}_weight")
        return AverageWeighted(field, weight_field, alias=alias)

    # elif msrfi.aggregator_type == "ReplicateWeightMoe":
    #     return fn.Abs()

    elif msrfi.aggregator_type == "CalculatedMoe":
        params = msrfi.aggregator_params
        critical_value = ValueWrapper(params["critical_value"])
        term = fn.Sqrt(fn.Sum(Power(field / critical_value, 2)))
        return ArithmeticExpression(Arithmetic.mul, term, critical_value, alias=alias)

    elif msrfi.aggregator_type == "Median":
        return Median(field, alias=alias)

    elif msrfi.aggregator_type == "Quantile":
        params = msrfi.aggregator_params
        quantile_level = float(params["quantile_level"])
        return Quantile(quantile_level, field, alias=alias)

    elif msrfi.aggregator_type == "DistinctCount":
        return DistinctCount(field, alias=alias)

    # elif msrfi.aggregator_type == "WeightedAverageMoe":
    #     return fn.Abs()

    raise NameError(
        f"Clickhouse module not prepared to handle aggregation type: {msrfi.aggregator_type}"
    )


def _get_filter_criterion(column: Field, constraint: FilterCondition) -> Criterion:
    """Apply comparison filters to query"""
    # create criterion for first constraint
    if constraint == NullityOperator.ISNULL:
        criterion = column.isnull()
    elif constraint == NullityOperator.ISNOTNULL:
        criterion = column.isnotnull()
    else:
        criterion = _get_filter_comparison(column, constraint[0])
        # add second constraint to criterion if defined
        if len(constraint) == 3:
            criterion2 = _get_filter_comparison(column, constraint[2])
            if constraint[1] == LogicOperator.AND:
                criterion &= criterion2
            elif constraint[1] == LogicOperator.OR:
                criterion |= criterion2
    return criterion


def _get_filter_comparison(field: Field, constr: NumericConstraint) -> Criterion:
    """Retrieves the comparison operator for the provided field."""
    comparison, scalar = constr

    # Note we must use == to also compare Enums values to strings
    if comparison == Comparison.GT:
        return field.gt(scalar)
    elif comparison == Comparison.GTE:
        return field.gte(scalar)
    elif comparison == Comparison.LT:
        return field.lt(scalar)
    elif comparison == Comparison.LTE:
        return field.lte(scalar)
    elif comparison == Comparison.EQ:
        return field.eq(scalar)
    elif comparison == Comparison.NEQ:
        return field.ne(scalar)

    raise NameError(f"Invalid criterion type: {comparison}")


def _transf_formula(tokens, field_builder: Callable[[str], Field]) -> Term:
    if isinstance(tokens, ParseResults):
        if len(tokens) == 1:
            return _transf_formula(tokens[0], field_builder)

        if tokens[0] == "CASE":
            case = Case()

            for item in tokens[1:]:
                if item[0] == "WHEN":
                    clauses = _transf_formula(item[1], field_builder)
                    expr = _transf_formula(item[3], field_builder)
                    case = case.when(clauses, expr)
                elif item[0] == "ELSE":
                    expr = _transf_formula(item[1], field_builder)
                    case = case.else_(expr)
                    break

            return case

        column = tokens[1]
        assert isinstance(column, str), f"Malformed formula: {tokens}"

        if tokens[0] == "ISNULL":
            return field_builder(column).isnull()

        if tokens[0] == "ISNOTNULL":
            return field_builder(column).isnotnull()

        if tokens[0] == "TOTAL":
            return an.Sum(field_builder(column)).over()

        if tokens[0] == "SQRT":
            return fn.Sqrt(field_builder(column))

        if tokens[0] == "POW":
            return field_builder(column) ** tokens[2]

        operator = column

        if operator in ">= <= == != <>":
            branch_left = _transf_formula(tokens[0], field_builder)
            branch_right = _transf_formula(tokens[2], field_builder)

            if operator == ">":
                return branch_left > branch_right
            elif operator == "<":
                return branch_left < branch_right
            elif operator == ">=":
                return branch_left >= branch_right
            elif operator == "<=":
                return branch_left <= branch_right
            elif operator == "==":
                return branch_left == branch_right
            elif operator in ("!=", "<>"):
                return branch_left != branch_right

            raise ValueError(f"Operator '{operator}' is not supported")

        if operator in "+-*/%":
            branch_left = _transf_formula(tokens[0], field_builder)
            branch_right = _transf_formula(tokens[2], field_builder)

            if operator == "+":
                return branch_left + branch_right
            elif operator == "-":
                return branch_left - branch_right
            elif operator == "*":
                return branch_left * branch_right
            elif operator == "/":
                return branch_left / branch_right
            elif operator == "%":
                return branch_left % branch_right

            raise ValueError(f"Operator '{operator}' is not supported")

    elif isinstance(tokens, (int, float)):
        return ValueWrapper(tokens)

    elif isinstance(tokens, str):
        if tokens.startswith("'") and tokens.endswith("'"):
            return ValueWrapper(tokens[1:-1])
        elif tokens.startswith('"') and tokens.endswith('"'):
            return ValueWrapper(tokens[1:-1])
        elif tokens == "NULL":
            return NullValue()
        else:
            return field_builder(tokens)

    logger.debug("Formula couldn't be parsed: %s, %r", type(tokens), tokens)
    raise ValueError(f"Expression '{tokens!r}' can't be parsed")
