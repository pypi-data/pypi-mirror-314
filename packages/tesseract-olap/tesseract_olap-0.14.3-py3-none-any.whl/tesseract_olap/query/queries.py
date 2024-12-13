"""Query-related data-handling models module.

This module contains data structs used to carry and compose objects used during
a Query. The elements are agnostic to the type of backend used, and its primary
purpose is organize and easily obtain the data needed for later steps.
"""

import hashlib
from collections import defaultdict
from copy import copy
from dataclasses import dataclass, field
from itertools import chain
from typing import Dict, List, Mapping, Optional, Tuple, Union

import immutables as immu
from typing_extensions import Literal

from tesseract_olap.common import stringify
from tesseract_olap.exceptions.query import (
    InvalidEntityName,
    InvalidParameter,
    MissingMeasures,
    NotAuthorized,
)
from tesseract_olap.schema import (
    CalculatedMeasure,
    CubeTraverser,
    DimensionTraverser,
    HierarchyTraverser,
    LevelTraverser,
    MemberType,
    SchemaTraverser,
)

from .enums import TimeScale
from .models import (
    CutIntent,
    GrowthIntent,
    HierarchyField,
    JoinIntent,
    JoinOnColumns,
    LevelField,
    MeasureField,
    PaginationIntent,
    SortingIntent,
    TopkIntent,
)
from .requests import DataRequest, MembersRequest

AnyQuery = Union["DataQuery", "MembersQuery"]


@dataclass(eq=False, order=False, repr=False)
class DataQuery:
    """Internal DataQuery class.

    Contains all the schema-hydrated elements corresponding to a
    :class:`DataRequest`, but also joining properties related to the same
    columnar entities.
    """

    cube: "CubeTraverser"
    locale: str
    fields_qualitative: Tuple["HierarchyField", ...] = field(default_factory=tuple)
    fields_quantitative: Tuple["MeasureField", ...] = field(default_factory=tuple)
    options: Mapping[str, bool] = field(default_factory=dict)
    pagination: "PaginationIntent" = field(default_factory=PaginationIntent)
    sorting: Optional["SortingIntent"] = None
    topk: Optional["TopkIntent"] = None
    growth: Optional["GrowthIntent"] = None

    def __copy__(self):
        return DataQuery(
            cube=self.cube,
            locale=self.locale,
            fields_qualitative=tuple(copy(item) for item in self.fields_qualitative),
            fields_quantitative=tuple(copy(item) for item in self.fields_quantitative),
            options=dict(self.options),
            pagination=self.pagination.model_copy(),
            sorting=None if self.sorting is None else self.sorting.model_copy(),
            topk=None if self.topk is None else self.topk.model_copy(),
            growth=None if self.growth is None else self.growth.model_copy(),
        )

    def __repr__(self):
        gen_levels = (
            repr(lvlfi)
            for hiefi in sorted(self.fields_qualitative, key=lambda x: x.dimension.name)
            for lvlfi in hiefi.levels
        )
        gen_measures = (
            repr(msrfi)
            for msrfi in sorted(self.fields_quantitative, key=lambda x: x.name)
        )
        params = (
            f"cube={repr(self.cube.name)}",
            f"locale={repr(self.locale)}",
            f"fields=({', '.join(chain(gen_levels, gen_measures))})",
            f"options={stringify(self.options)}",
            f"pagination={repr(self.pagination)}",
            f"sorting={repr(self.sorting)}",
            f"topk={repr(self.topk)}",
            f"growth={repr(self.growth)}",
        )
        return f"{type(self).__name__}({', '.join(params)})"

    @property
    def key(self) -> str:
        return hashlib.md5(repr(self).encode("utf-8")).hexdigest()

    @property
    def count_key(self) -> str:
        gen_levels = (
            repr(lvlfi)
            for hiefi in sorted(self.fields_qualitative, key=lambda x: x.dimension.name)
            for lvlfi in hiefi.levels
        )
        string = f"DataQuery(cube={self.cube.name!r}, fields=({', '.join(gen_levels)}))"
        return "d" + hashlib.md5(string.encode("utf-8")).hexdigest()

    @property
    def columns(self) -> Dict[str, MemberType]:
        locale = self.locale
        gen_measure = (
            (msrfi.name, msrfi.datatype) for msrfi in self.fields_quantitative
        )
        gen_ranking = (
            (f"{msrfi.name} Ranking", MemberType.UINT32)
            for msrfi in self.fields_quantitative
            if msrfi.with_ranking
        )
        gen_level = (
            (name, lvlfi.level.key_type)
            for hiefi in self.fields_qualitative
            for lvlfi in hiefi.drilldown_levels
            for _, name, _ in lvlfi.iter_columns(locale)
        )
        return dict(chain(gen_measure, gen_ranking, gen_level))

    @classmethod
    def from_request(cls, schema: "SchemaTraverser", request: "DataRequest"):
        """Generates a new :class:`Query` instance from the parameters defined
        in a :class:`DataRequest` object.

        If any of the parameters can't be found on the Schema, raises a derivate
        of the :class:`InvalidQuery` error.
        """
        if not schema.is_authorized(request):
            raise NotAuthorized(repr(request.cube), request.roles)

        cube = schema.get_cube(request.cube)

        # TODO: consider replacing the Intents with Directives for pagination,
        # sorting, topk, where field names are replaced with schema objects,
        # or errors are raised if they don't exist

        return cls(
            cube=cube,
            fields_qualitative=_get_data_hierarfields(cube, request),
            fields_quantitative=_get_data_measurefields(cube, request),
            locale=schema.default_locale if request.locale is None else request.locale,
            options=request.options,
            pagination=request.pagination,
            sorting=request.sorting,
            topk=request.topk,
            growth=request.growth,
        )


@dataclass(eq=False, order=False)
class DataMultiQuery:
    initial: "DataQuery"
    join_with: Tuple[Tuple["DataQuery", "JoinIntent"], ...]

    def get_annotations(self):
        queries = chain([self.initial], (item[0] for item in self.join_with))
        return {query.cube.name: dict(query.cube.annotations) for query in queries}

    @classmethod
    def from_requests(
        cls,
        schema: "SchemaTraverser",
        requests: List["DataRequest"],
        joins: List["JoinIntent"],
    ):
        """Validates the DataRequests into DataQueries and reorganizes the JoinIntent operations that are intended to be performed with each of them.

        By itself this class is not intended to be sent to the backend for execution (as the join operation is performed using DataFrames), but in the future and depending on the Backend implementation, it's subject to change.
        """

        queries = [DataQuery.from_request(schema, request) for request in requests]

        if len(queries) - 1 != len(joins):
            raise InvalidParameter(
                "joins",
                "Invalid number of 'joins' parameters; it must be one per query intended to be joined with the initial.",
            )

        join_with = tuple(
            cls._yield_step_pair(left, right, join)
            for left, right, join in zip(queries[:-1], queries[1:], joins)
        )

        return cls(initial=queries[0], join_with=join_with)

    @classmethod
    def _yield_step_pair(
        cls, query_left: DataQuery, query_right: DataQuery, join_intent: JoinIntent
    ) -> Tuple["DataQuery", "JoinIntent"]:
        columns_left = cls._get_columns(query_left)
        columns_right = cls._get_columns(query_right)

        left_fields = dict(columns_left)
        right_fields = dict(columns_right)

        join_on = join_intent.on
        if isinstance(join_on, str):
            join_on = [join_on]

        if isinstance(join_on, list):
            join_intent.on = [
                column
                for column in join_on
                if left_fields.get(column) == right_fields.get(column)
            ]
        elif isinstance(join_on, JoinOnColumns):
            if join_on.left_on not in left_fields:
                raise InvalidParameter(
                    "on.left_on",
                    f"Column '{join_on.left_on}' is not present in the left dataset at this stage of the merge.",
                )
            if join_on.right_on not in right_fields:
                raise InvalidParameter(
                    "on.right_on",
                    f"Column '{join_on.right_on}' is not present in the right dataset at this stage of the merge.",
                )
        else:
            common_aliases = set(left_fields.keys()) & set(right_fields.keys())
            common_fields = set(left_fields.values()) & set(right_fields.values())
            if len(common_aliases) > 0:
                join_intent.on = list(common_aliases)
            elif len(common_fields) > 0:
                fields = list(common_fields)
                join_intent.on = JoinOnColumns(
                    left_on=list(
                        next(
                            key for key, value in left_fields.items() if value == field
                        )
                        for field in fields
                    ),
                    right_on=list(
                        next(
                            key for key, value in right_fields.items() if value == field
                        )
                        for field in fields
                    ),
                )
            else:
                raise InvalidParameter(
                    "request", "Couldn't find common columns between requested queries"
                )

        return query_right, join_intent

    @classmethod
    def _get_columns(cls, query: "DataQuery"):
        locale = query.locale
        fact_table = query.cube.table
        return {
            (alias, f"{table.name}.{column}")
            for table, column, alias in (
                next(
                    (hiefi.table or fact_table, column, label)
                    for column, label, _ in lvlfi.iter_columns(locale)
                )
                for hiefi in query.fields_qualitative
                for lvlfi in hiefi.drilldown_levels
            )
        }


@dataclass(eq=False, order=False, repr=False)
class MembersQuery:
    """Internal MembersQuery class."""

    cube: "CubeTraverser"
    hiefield: "HierarchyField"
    locale: str
    pagination: "PaginationIntent" = field(default_factory=PaginationIntent)
    search: Optional[str] = None

    def __repr__(self):
        fields = (
            repr(item) for item in sorted(self.hiefield.levels, key=lambda x: x.name)
        )
        params = (
            f'cube="{self.cube.name}"',
            f'locale="{self.locale}"',
            f'fields=({", ".join(fields)})',
            f"pagination={repr(self.pagination)}",
            f"search={repr(self.search)}",
        )
        return f"{type(self).__name__}({', '.join(params)})"

    @property
    def key(self) -> str:
        return hashlib.md5(repr(self).encode("utf-8")).hexdigest()

    @property
    def count_key(self) -> str:
        return "m" + self.key

    @property
    def columns(self) -> Dict[str, MemberType]:
        locale = self.locale
        return {
            name: lvlfi.level.key_type
            for lvlfi in self.hiefield.levels
            for _, name, _ in lvlfi.iter_columns(locale)
        }

    @classmethod
    def from_request(cls, schema: "SchemaTraverser", request: "MembersRequest"):
        """Generates a new :class:`MembersQuery` instance from a user-provided
        :class:`MembersRequest` instance.
        """
        if not schema.is_authorized(request):
            raise NotAuthorized(f"Cube({request.cube})", request.roles)

        cube = schema.get_cube(request.cube)

        return cls(
            cube=cube,
            hiefield=_get_members_hierarfield(cube, request),
            locale=schema.default_locale if request.locale is None else request.locale,
            pagination=request.pagination,
            search=request.search,
        )


def _get_data_hierarfields(cube: "CubeTraverser", req: "DataRequest"):
    """Regroups query parameters related to a Level, to simplify later usage."""
    # we need a map with all possible levels, including the cube's shared dimensions
    level_map = immu.Map(
        (level.name, (dimension, hierarchy, level))
        for dimension in cube.dimensions
        for hierarchy in dimension.hierarchies
        for level in hierarchy.levels
    )

    drilldown_set = req.drilldowns
    property_set = req.properties
    caption_set = req.captions
    alias_map = {**req.aliases}
    cut_map = {**req.cuts}

    with_parents = req.parents
    if isinstance(with_parents, bool):
        with_parents = drilldown_set if with_parents else set("")

    involved_levels = req.drilldowns.copy()
    involved_levels.update(item.level for item in req.cuts.values())

    time_level = None
    time_restr = req.time_restriction
    if time_restr is not None:
        granularity = time_restr.level
        time_level = (
            cube.get_time_level(granularity.value)
            if isinstance(granularity, TimeScale)
            else cube.get_time_level(granularity)
        )
        involved_levels.add(time_level.name)

    # Ensure all levels involved in the request don't break
    # the 'single dimension, same hierarchy' rule
    dim_store: Mapping[DimensionTraverser, HierarchyTraverser] = {}
    hie_store: Mapping[HierarchyTraverser, List[LevelTraverser]] = defaultdict(list)

    for name in involved_levels:
        try:
            dimension, hierarchy, level = level_map[name]
        except KeyError:
            raise InvalidParameter(
                "drilldowns",
                f"Could not find a Level named '{name}' in the '{cube.name}' cube.",
            ) from None
        if dim_store.get(dimension, hierarchy) != hierarchy:
            raise InvalidParameter(
                "drilldowns",
                "Multiple Hierarchies from the same Dimension are being requested. "
                "Only a single Hierarchy can be used at a time for a query.",
            )
        dim_store[dimension] = hierarchy
        hie_store[hierarchy].append(level)

    # Apply default members
    for dimension in cube.dimensions:
        # Get the relevant Hierarchy for each Dimension in the Cube
        hierarchy = dim_store.get(dimension, dimension.default_hierarchy)

        # The default_member logic will be applied only if the
        # (dimension, hierarchy) is not present in the user request
        levels = hie_store[hierarchy]
        if len(levels) > 0:
            continue

        # Store the default hierarchy for the SQL subset filter
        dim_store[dimension] = hierarchy

        default_member = hierarchy.default_member
        if default_member is None:
            continue

        level, member = default_member
        levels.append(level)
        cut_map[level.name] = CutIntent.model_validate((level.name, [member], []))

    def _compose_field(level: "LevelTraverser", is_drilldown: bool) -> "LevelField":
        """Capsules the logic to fill a LevelField instance with data from both
        a Drilldown and a Cut.
        """
        kwargs = {
            "level_alias": alias_map.get(level.name) if is_drilldown else None,
            "is_drilldown": is_drilldown,
            "properties": frozenset(
                prop for prop in level.properties if prop.name in property_set
            ),
            "caption": next(
                (capt for capt in level.properties if capt.name in caption_set), None
            ),
            "time_restriction": time_restr if time_level == level else None,
        }

        cut = cut_map.get(level.name)
        if cut is not None:
            kwargs["members_exclude"] = set(cut.exclude_members)
            kwargs["members_include"] = set(cut.include_members)

        return LevelField(level=level, **kwargs)

    def _resolve_fields(hierarchy: "HierarchyTraverser"):
        """Calculates the levels involved in the request, depending on the
        with_parent parameter.
        """
        involved_levels = hie_store[hierarchy]
        fields: List[LevelField] = []

        parent_flag = False
        # iterations will be done in reverse to use a flag for parents
        for level in reversed(tuple(hierarchy.levels)):
            # if includes_parents, and a deeper level is drilldown,
            # or if it's explicitly a drilldown
            is_drilldown = parent_flag or level.name in drilldown_set
            # is_field means the level needs to be SELECTed
            # to be used as a foreign key for a drilldown or a cut
            is_field = is_drilldown or level in involved_levels
            if is_field:
                fields.append(_compose_field(level, is_drilldown))
            # if level is marked in parents, raise flag
            # TODO: can be improved
            parent_flag = parent_flag or (is_drilldown and level.name in with_parents)

        fields.reverse()
        return tuple(fields)

    return tuple(
        HierarchyField(dimension, hierarchy, levels)
        for dimension, hierarchy, levels in (
            (dimension, hierarchy, _resolve_fields(hierarchy))
            for dimension, hierarchy in (
                sorted(dim_store.items(), key=lambda item: item[0].name)
            )
        )
        if len(levels) > 0
    )


def _get_data_measurefields(cube: "CubeTraverser", req: "DataRequest"):
    """Regroups query parameters related to a Measure, to simplify contextual use."""
    if isinstance(req.ranking, bool):
        ranking_flags: Mapping[str, Literal["asc", "desc"]] = (
            {item: "desc" for item in req.measures} if req.ranking else {}
        )

    else:
        ranking_flags = req.ranking
        # All measures in the requested ranking must be in the requested measures
        rank_diff = set(ranking_flags.keys()).difference(req.measures)
        if len(rank_diff) > 0:
            raise MissingMeasures("ranking", rank_diff)

    filter_constr = {item.field: item.condition for item in req.filters.values()}

    calcmeasure_deps = (
        column
        for measure in (cube.get_measure(name) for name in req.measures)
        if isinstance(measure, CalculatedMeasure)
        for column in measure.dependencies
        if column in cube.measure_map
    )

    return tuple(
        MeasureField(
            measure=item,
            is_measure=item.name in req.measures,
            with_ranking=ranking_flags.get(item.name),
            constraint=filter_constr.get(item.name),
        )
        for measure in (
            cube.get_measure(name)
            for name in sorted(
                req.measures.union(filter_constr.keys(), calcmeasure_deps)
            )
        )
        for item in measure.and_submeasures()
    )


def _get_members_hierarfield(cube: "CubeTraverser", req: "MembersRequest"):
    """Regroups query parameters related to a Level, to simplify later usage."""
    level_name = req.level
    with_parents = req.options.get("parents", False)

    try:
        dimension, hierarchy, level = next(
            (dimension, hierarchy, level)
            for dimension in cube.dimensions
            for hierarchy in dimension.hierarchies
            for level in hierarchy.levels
            if level.name == level_name
        )
    except StopIteration:
        raise InvalidEntityName("Level", level_name) from None

    if with_parents:
        levels = tuple(hierarchy.levels)
        last_index = levels.index(level) + 1
        fields = tuple(LevelField(level) for level in levels[0:last_index])
    else:
        fields = (LevelField(level),)

    return HierarchyField(dimension, hierarchy, levels=fields)
