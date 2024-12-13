from io import BytesIO
from typing import TYPE_CHECKING, Union

import polars as pl
import redis as valkey
from pydantic import BaseModel, model_validator

from tesseract_olap.common import URL, hide_dsn_password
from tesseract_olap.exceptions.backend import (
    UnexpectedResponseError,
    UpstreamInternalError,
    UpstreamNotPrepared,
)

from .cache import CacheConnection, CacheConnectionStatus, CacheProvider

if TYPE_CHECKING:
    from tesseract_olap.query import AnyQuery


class ValkeyConnectionParams(BaseModel):
    dsn: str
    default_ttl: int = 0

    @model_validator(mode="before")
    @classmethod
    def parse_dsn(cls, value):
        if isinstance(value, str):
            value = URL(value)

        if isinstance(value, URL):
            default_ttl = value.query_pop("default_ttl", "0")
            return {"dsn": str(value), "default_ttl": default_ttl}

        return value


class ValkeyProvider(CacheProvider):
    def __init__(self, dsn: Union[str, URL], **kwargs):
        params = ValkeyConnectionParams.model_validate(dsn)
        pool = valkey.ConnectionPool.from_url(params.dsn, **kwargs)

        self.connection_kwargs = {
            "default_ttl": params.default_ttl,
            "single_connection_client": True,
        }
        self.dsn = params.dsn
        self.pool = pool

    def __repr__(self):
        return f"{type(self).__name__}(dsn='{hide_dsn_password(self.dsn)}')"

    def connect(self):
        try:
            return ValkeyConnection(self.pool, **self.connection_kwargs)
        except valkey.ConnectionError as exc:
            message = "Attempt to use a not-open Redis connection."
            raise UpstreamNotPrepared(message, *exc.args) from exc
        except valkey.RedisError as exc:
            message = f"Redis{type(exc).__name__}:\n" + "\n".join(
                repr(arg) for arg in exc.args
            )
            raise UpstreamInternalError(message, *exc.args) from exc

    def clear(self):
        with valkey.Redis(connection_pool=self.pool) as conn:
            conn.flushdb(True)


class ValkeyConnection(CacheConnection):
    client: valkey.Redis
    default_ttl: int

    def __init__(self, pool: valkey.ConnectionPool, default_ttl: int = -1, **kwargs):
        self.client = valkey.Redis(connection_pool=pool, **kwargs)
        self.default_ttl = default_ttl

    @property
    def status(self) -> CacheConnectionStatus:
        return (
            CacheConnectionStatus.CONNECTED
            if self.client.connection is not None and self.client.ping()
            else CacheConnectionStatus.CLOSED
        )

    def close(self) -> None:
        return self.client.close()

    def exists(self, query: "AnyQuery") -> bool:
        return self.client.exists(query.key) == 1

    def store(self, query: "AnyQuery", data: "pl.DataFrame") -> None:
        dfio = data.write_ipc(file=None, compression="lz4")
        try:
            self.client.set(
                query.key,
                dfio.getvalue(),
                ex=self.default_ttl if self.default_ttl > 0 else None,
            )
        except valkey.ConnectionError as exc:
            raise UpstreamNotPrepared(*exc.args) from exc
        except valkey.RedisError as exc:
            raise UpstreamInternalError(*exc.args) from exc

    def retrieve(self, query: "AnyQuery") -> Union["pl.DataFrame", None]:
        try:
            res = self.client.get(query.key)
        except valkey.ConnectionError as exc:
            raise UpstreamNotPrepared(*exc.args) from exc
        except valkey.RedisError as exc:
            raise UpstreamInternalError(*exc.args) from exc

        if res is None:
            return None
        elif isinstance(res, bytes):
            return pl.read_ipc(BytesIO(res))
        else:
            raise UnexpectedResponseError(
                f"Unknown response from Valkey: Sent 'GET {query.key}', Recv {res!r}"
            )

    def ping(self) -> bool:
        res = self.client.ping()
        return res in ("PONG", b"PONG")
