import logging
from pathlib import Path
from typing import Union
from urllib.parse import parse_qs

from typing_extensions import deprecated

from tesseract_olap.backend import Backend, CacheProvider, DummyProvider, LfuProvider
from tesseract_olap.exceptions.query import InvalidQuery
from tesseract_olap.exceptions.server import UnknownBackendError
from tesseract_olap.query import (
    AnyQuery,
    AnyRequest,
    DataQuery,
    DataRequest,
    MembersQuery,
    MembersRequest,
)
from tesseract_olap.schema import Schema, SchemaTraverser

from .schema import setup_schema

logger = logging.getLogger("tesseract_olap.server")


class OlapServer:
    """Main server class.

    This object manages the connection with the backend database and the schema
    instance containing the database references, to enable make queries against
    them.
    """

    schema: "SchemaTraverser"
    backend: "Backend"
    cache: "CacheProvider"

    def __init__(
        self,
        *,
        backend: Union[str, "Backend"],
        schema: Union[str, "Path", "Schema"],
        cache: Union[str, "CacheProvider"] = "",
    ):
        self.backend = (
            backend if isinstance(backend, Backend) else _setup_backend(backend)
        )

        self.cache = cache if isinstance(cache, CacheProvider) else _setup_cache(cache)

        self.schema = SchemaTraverser(
            schema if isinstance(schema, Schema) else setup_schema(schema)
        )

    @property
    def raw_schema(self):
        """Retrieves the raw Schema instance used by this server."""
        return self.schema.schema

    def build_query(self, request: AnyRequest):
        """Uses the internal schema to validate a Request and generate its
        matching Query instance."""
        if isinstance(request, DataRequest):
            return DataQuery.from_request(self.schema, request)
        if isinstance(request, MembersRequest):
            return MembersQuery.from_request(self.schema, request)

        raise InvalidQuery(
            "Attempt to build a Query using an invalid Request instance."
        )

    def clear_cache(self) -> None:
        """Clears all stored items in the cache."""
        self.cache.clear()

    def generate_sql(self, query: AnyQuery) -> str:
        """Builds the SQL query for a Query instance, using the backend currently
        configured in this server."""
        return self.backend.generate_sql(query)

    @deprecated(
        "The session() method allows to reuse a connection for multiple queries."
    )
    def execute(self, request: AnyRequest):
        query = self.build_query(request)
        with self.session() as session:
            result = session.fetch(query)
        return result

    def ping(self) -> bool:
        """Performs a ping call to the backend server.
        A succesful call should make this function return :bool:`True`.
        """
        try:
            return self.backend.ping()
        except Exception:
            return False

    def session(self, **kwargs):
        return self.backend.new_session(cache=self.cache, **kwargs)

    def validate(self):
        """Verifies the information declared in the Schema matches the data
        structures in the Backend."""
        self.schema.validate()
        self.backend.validate_schema(self.schema)


def _setup_backend(dsn: str):
    """Generates a new instance of a backend bundled in this package, or raises
    an error if no one is compatible, with a provided connection string.
    """
    if dsn.startswith("clickhouse:") or dsn.startswith("clickhouses:"):
        from tesseract_olap.backend.clickhouse import ClickhouseBackend

        return ClickhouseBackend(dsn)

    raise UnknownBackendError(dsn)


def _setup_cache(dsn: str) -> CacheProvider:
    """Generates a new instance of a CacheProvider bundled in this package."""
    if dsn.startswith(":memory:"):
        try:
            params = parse_qs(dsn.replace(":memory:", ""), strict_parsing=True)
            maxsize = params.get("maxsize", ["64"])
            dfsize = params.get("dfsize", ["150"])
            return LfuProvider(maxsize=int(maxsize[0]), dfsize=int(dfsize[0]))
        except ValueError:
            return LfuProvider()

    if (
        dsn.startswith("valkey:")
        or dsn.startswith("valkeys:")
        or dsn.startswith("redis:")
        or dsn.startswith("rediss:")
    ):
        from tesseract_olap.backend.valkey import ValkeyProvider

        return ValkeyProvider(dsn)

    return DummyProvider()
