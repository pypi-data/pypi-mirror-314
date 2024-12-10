"""Requests module.

Contains structs to build a :class:`DataRequest` instance: an object to describe
the parameters needed for the query using only entity names and relationships.
"""

import hashlib
from dataclasses import dataclass, field
from itertools import chain
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple, Union

from pydantic import BaseModel, Field, model_validator
from typing_extensions import Literal, Protocol, TypedDict

from tesseract_olap.common import Array, stringify
from tesseract_olap.query import AnyOrder

from .models import (
    AliasesIntent,
    CutIntent,
    FilterCondition,
    FilterIntent,
    GrowthIntent,
    JoinIntent,
    PaginationIntent,
    SortingIntent,
    TimeRestriction,
    TopkIntent,
)

AnyRequest = Union["DataRequest", "MembersRequest"]


class RequestWithRoles(Protocol):
    """Defines an interface of commons between DataRequest and MembersRequest."""

    cube: str
    roles: Set[str]


class DataRequestOptionalParams(TypedDict, total=False):
    """Defines the optional parameters in the DataRequestParams interface.

    Is a separate class is due to the implementation of the
    [Totality](https://www.python.org/dev/peps/pep-0589/#totality) in the
    :class:`TypedDict` class.

    This will give a better hint to the type checker when the user makes use of
    this interface.
    """

    aliases: Union[str, Mapping[str, str]]
    captions: Array[str]
    cuts_exclude: Mapping[str, Array[str]]
    cuts_include: Mapping[str, Array[str]]
    filters: Mapping[str, FilterCondition]
    locale: str
    pagination: Union[str, Tuple[int, int]]
    parents: Union[bool, str, Array[str]]
    properties: Array[str]
    ranking: Union[bool, Mapping[str, AnyOrder]]
    roles: Array[str]
    sorting: Union[str, Tuple[str, AnyOrder]]
    time: str
    top: str
    growth: str


class DataRequestParams(DataRequestOptionalParams, total=True):
    """DataRequestParams interface.

    Determines the expected params in a :class:`dict`, to use when creating a
    new :class:`DataRequest` object via the :func:`DataRequest.new` class method.
    """

    drilldowns: Array[str]
    measures: Array[str]


@dataclass(eq=False, order=False, repr=False)
class DataRequest:
    """Represents the intent for a Data Query made by the user.

    All its properties are defined by strings of the names of the components
    from the schema.
    None of these parameters are verified during construction, so it's possible
    for the query to be invalid; a subclass of :class:`backend.exceptions.BackendError`
    will be raised in that case.
    The only purpose of this structure is containing and passing over the query
    intent to the internals.

    During a request, a :class:`Query` instance is constructed with objects from
    a schema, using parameters from this instance.
    """

    cube: str
    drilldowns: Set[str]
    measures: Set[str]
    aliases: Mapping[str, str] = field(default_factory=dict)
    captions: Set[str] = field(default_factory=set)
    cuts: Mapping[str, "CutIntent"] = field(default_factory=dict)
    filters: Mapping[str, "FilterIntent"] = field(default_factory=dict)
    locale: Optional[str] = None
    options: Mapping[str, bool] = field(default_factory=dict)
    pagination: "PaginationIntent" = field(default_factory=PaginationIntent)
    parents: Union[bool, Set[str]] = False
    properties: Set[str] = field(default_factory=set)
    ranking: Union[bool, Mapping[str, Literal["asc", "desc"]]] = False
    roles: Set[str] = field(default_factory=set)
    sorting: Optional["SortingIntent"] = None
    time_restriction: Optional["TimeRestriction"] = None
    topk: Optional["TopkIntent"] = None
    growth: Optional["GrowthIntent"] = None

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, DataRequest) and hash(self) == hash(__value)

    def __hash__(self):
        return hash((repr(self), *sorted(self.roles)))

    def __repr__(self):
        params = (
            f"cube={repr(self.cube)}",
            f"locale={repr(self.locale)}",
            f"drilldowns={stringify(self.drilldowns)}",
            f"aliases={repr(self.aliases)}",
            f"captions={stringify(self.captions)}",
            f"properties={stringify(self.properties)}",
            f"cuts={stringify(list(self.cuts.values()))}",
            f"time={repr(self.time_restriction)}",
            f"topk={repr(self.topk)}",
            f"measures={stringify(self.measures)}",
            f"filters={stringify(list(self.filters.values()))}",
            f"ranking={stringify(self.ranking)}",
            f"options={stringify(self.options)}",
            f"pagination={repr(self.pagination)}",
            f"parents={stringify(self.parents)}",
            f"sorting={repr(self.sorting)}",
            f"growth={repr(self.growth)}",
        )
        return f"{type(self).__name__}({', '.join(params)})"

    @classmethod
    def new(cls, cube: str, request: DataRequestParams):
        """Creates a new :class:`DataRequest` instance from a set of parameters
        defined in a dict.

        This should be the preferred method by final users, as it doesn't
        require the use of internal dataclasses and the setup of internal
        structures and unique conditions.
        """

        cuts_include = request.get("cuts_include", {})
        cuts_exclude = request.get("cuts_exclude", {})
        filters = request.get("filters", {})
        roles = request.get("roles", [])

        kwargs: Dict[str, Any] = {
            "locale": request.get("locale"),
            "cuts": {
                item: CutIntent.model_validate(
                    (item, cuts_include.get(item, []), cuts_exclude.get(item, [])),
                )
                for item in set(chain(cuts_include.keys(), cuts_exclude.keys()))
            },
            "filters": {
                item: FilterIntent(field=item, condition=condition)
                for item, condition in filters.items()
            },
            "captions": set(request.get("captions", [])),
            "properties": set(request.get("properties", [])),
            "options": {},
            "pagination": PaginationIntent.model_validate(
                request.get("pagination", "0")
            ),
            "ranking": request.get("ranking", False),
            "roles": set(roles) if isinstance(roles, (list, tuple)) else roles,
        }

        item = request.get("aliases")
        if item:
            parsed = AliasesIntent.model_validate(item)
            kwargs["aliases"] = parsed.aliases

        item = request.get("parents", False)
        if isinstance(item, (set, bool)):
            kwargs["parents"] = item
        elif isinstance(item, (list, tuple)):
            kwargs["parents"] = set(item)
        elif isinstance(item, str):
            kwargs["parents"] = set(item.split(","))

        item = request.get("sorting")
        if item:
            kwargs["sorting"] = SortingIntent.model_validate(item)

        item = request.get("time")
        if item:
            kwargs["time_restriction"] = TimeRestriction.model_validate(item)

        item = request.get("top")
        if item:
            kwargs["topk"] = TopkIntent.model_validate(item)

        item = request.get("growth")
        if item:
            kwargs["growth"] = GrowthIntent.model_validate(item)

        return cls(
            cube=cube,
            drilldowns=set(request["drilldowns"]),
            measures=set(request["measures"]),
            **kwargs,
        )

    def key(self):
        """Generates a hash to differentiate the parameters that influence the resulting data.

        This hash can be used to compare requests, and as cache key for the resulting data.
        It doesn't consider roles on purpose, as the roles define the access to the dataset
        instead of its contents. This also means a comparison operation between requests must
        compare roles separately.
        """
        return hashlib.md5(repr(self).encode("utf-8")).hexdigest()


class DataMultiRequest(BaseModel):
    requests: List["DataRequest"]
    joins: List["JoinIntent"] = Field(default_factory=list)
    pagination: "PaginationIntent" = Field(default_factory=PaginationIntent)

    @model_validator(mode="before")
    @classmethod
    def parse_request(cls, value: Any):
        if isinstance(value, dict):
            requests = value.get("queries") or value.get("requests", [])
            assert isinstance(
                requests, Sequence
            ), "Invalid 'requests' parameter: it must be a list of dictionaries containing the request parameters of the queries to be merged."
            request_count = len(requests)
            assert (
                request_count > 1
            ), "At least 2 DataRequest objects are required to perform a join operation."

            joins = value.get("joins", [])
            assert isinstance(
                joins, Sequence
            ), "Invalid 'joins' parameter. It must be a list of dictionaries with the parameters to use."
            if not joins:
                joins = [{}] * (request_count - 1)
            elif len(joins) == 1:
                joins = list(joins) * (request_count - 1)
            elif len(joins) == request_count - 1:
                joins = joins
            else:
                raise ValueError(
                    f"Invalid 'joins' parameter. It must be a list of objects with the parameters to use; this list must contain 1 object (if you intend to apply the same parameters to all queries), {request_count - 1} objects (one per each step of this join operation), or left empty/unset to let the server attempt to guess the parameters."
                )

            return {
                "requests": requests,
                "joins": joins,
                "pagination": value.get("pagination", "0,0"),
            }
        return value


class MembersRequestOptionalParams(TypedDict, total=False):
    """Defines the optional parameters in the MembersRequestParams interface.

    Is a separate class is due to the implementation of the
    [Totality](https://www.python.org/dev/peps/pep-0589/#totality) in the
    :class:`TypedDict` class.

    This will give a better hint to the type checker when the user makes use of
    this interface.
    """

    children: bool
    locale: str
    pagination: Union[str, Tuple[int, int]]
    parents: bool
    roles: Array[str]
    search: str


class MembersRequestParams(MembersRequestOptionalParams, total=True):
    """MembersRequestParams interface.

    Determines the expected params in a :class:`dict`, to use when creating a
    new :class:`MembersRequest` object via the :func:`MembersRequest.new` class
    method.
    """

    level: str


@dataclass(eq=False, order=False)
class MembersRequest:
    """Represents the intent for a Level Metadata Query made by the user.

    Parameters are constructed with primitives that describe the entities being
    requested.

    It is suggested to use the :func:`MembersRequest.new` method to create a new
    instance of this class, instead of calling a new instance directly.
    """

    cube: str
    level: str
    locale: Optional[str] = None
    options: Mapping[str, bool] = field(default_factory=dict)
    pagination: "PaginationIntent" = field(default_factory=PaginationIntent)
    roles: Set[str] = field(default_factory=set)
    search: Optional[str] = None

    @classmethod
    def new(cls, cube: str, request: MembersRequestParams):
        """Creates a new :class:`MembersRequest` instance from a set of parameters
        defined in a dict.

        This should be the preferred method by final users, as it doesn't
        require the use of internal dataclasses and the setup of internal
        structures and unique conditions.
        """

        item = request.get("roles", [])
        roles = set(item) if isinstance(item, (list, tuple)) else item

        return cls(
            cube=cube,
            level=request["level"],
            locale=request.get("locale"),
            options={
                "parents": request.get("parents", False),
                "children": request.get("children", False),
            },
            pagination=PaginationIntent.model_validate(request.get("pagination", "0")),
            roles=roles,
            search=request.get("search"),
        )
