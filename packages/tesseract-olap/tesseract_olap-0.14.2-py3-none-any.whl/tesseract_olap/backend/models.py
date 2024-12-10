"""Backend model definitions module.

This module contains abstract definitions for the interfaces of the Backend
class. Tesseract is compatible with any kind of data source as long as there's a
backend class that adapts the Query and the Results to the defined interface.
"""

import abc
from copy import copy
from dataclasses import dataclass, field
from types import TracebackType
from typing import TYPE_CHECKING, Dict, Generic, List, Optional, Type, TypedDict

import polars as pl

from tesseract_olap.common import T, shorthash
from tesseract_olap.query import PaginationIntent
from tesseract_olap.schema import MemberType

if TYPE_CHECKING:
    from tesseract_olap.common import AnyDict, AnyTuple
    from tesseract_olap.query import AnyQuery
    from tesseract_olap.schema import InlineTable, SchemaTraverser


class CacheMeta(TypedDict):
    key: str
    status: str


class PaginationMeta(TypedDict):
    total: int
    limit: int
    offset: int


@dataclass(eq=False, order=False)
class Result(Generic[T]):
    data: T
    columns: Dict[str, MemberType]
    cache: CacheMeta = field(
        default_factory=lambda: {"key": "0" * 32, "status": "MISS"}
    )
    page: PaginationMeta = field(
        default_factory=lambda: {"limit": 0, "offset": 0, "total": 0}
    )


class Backend(abc.ABC):
    """Base class for database backends compatible with Tesseract."""

    @abc.abstractmethod
    def new_session(self, **kwargs) -> "Session":
        """Establishes the connection to the backend server.

        This operation must be done before running any other data method, and
        must be separate from the creation of a :class:`Backend` instance.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def ping(self) -> bool:
        """Performs a ping call to the backend server.
        If the call is successful, this function should return :bool:`True`.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def validate_schema(self, schema: "SchemaTraverser") -> None:
        """Ensures all columns defined in the schema are present in the backend.
        Should raise an Error if it finds any problem, otherwise should return `None`.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def generate_sql(self, query: "AnyQuery", **kwargs) -> str:
        raise NotImplementedError()


class Session(abc.ABC):
    """Base class for connections made to a backend compatible with Tesseract."""

    def __enter__(self):
        self.connect()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        self.close()

    @abc.abstractmethod
    def connect(self) -> None:
        """Establishes the connection to the backend server.

        This operation is called automatically when the Session instance is
        used within a context manager.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def close(self) -> None:
        """Closes the connection to the backend server.

        This operation is called automatically at the end of the context manager
        this instance was called into."""
        raise NotImplementedError()

    @abc.abstractmethod
    def fetch(self, query: "AnyQuery", **kwargs) -> Result[List["AnyTuple"]]:
        raise NotImplementedError()

    @abc.abstractmethod
    def fetch_dataframe(self, query: "AnyQuery", **kwargs) -> Result[pl.DataFrame]:
        raise NotImplementedError()

    @abc.abstractmethod
    def fetch_records(self, query: "AnyQuery", **kwargs) -> Result[List["AnyDict"]]:
        raise NotImplementedError()


@dataclass
class ParamManager:
    """Keeps track of the SQL named parameters and their values, to combine them
    through all the functions where they're defined, and output them at the
    final generation step.
    """

    params: Dict[str, str] = field(default_factory=dict)
    tables: List["InlineTable"] = field(default_factory=list)

    def set_param(self, value: str, key: Optional[str] = None) -> str:
        """Stores a new named parameter value, and returns the parameter name."""
        key = f"p_{shorthash(value)}" if key is None else key
        self.params[key] = value
        return key

    def set_table(self, table: "InlineTable"):
        """Stores an inline table."""
        self.tables.append(table)


def chunk_queries(query: "AnyQuery", *, limit: int = 500000):
    if limit == 0:
        yield query
        return

    pagi = query.pagination
    index = pagi.offset // limit
    while True:
        chunk_query = copy(query)
        chunk_query.pagination = PaginationIntent(limit=limit, offset=index * limit)
        yield chunk_query

        index += 1
        if pagi.limit > 0 and index * limit > pagi.limit:
            break
