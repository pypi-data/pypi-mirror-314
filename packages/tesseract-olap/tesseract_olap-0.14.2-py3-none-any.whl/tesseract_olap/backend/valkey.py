from io import BytesIO
from typing import TYPE_CHECKING, Optional, Union

import polars as pl
import redis as valkey

from tesseract_olap.common import hide_dsn_password
from tesseract_olap.exceptions.backend import UpstreamInternalError, UpstreamNotPrepared

from .cache import CacheConnection, CacheConnectionStatus, CacheProvider

if TYPE_CHECKING:
    from tesseract_olap.query import AnyQuery


class ValkeyProvider(CacheProvider):
    def __init__(self, dsn: str, **kwargs):
        self.dsn = dsn
        self.pool = valkey.ConnectionPool.from_url(dsn, **kwargs)

    def __repr__(self):
        return f"{type(self).__name__}(dsn='{hide_dsn_password(self.dsn)}')"

    def connect(self):
        try:
            return ValkeyConnection(self.pool, single_connection_client=True)
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
    def __init__(self, pool: valkey.ConnectionPool, **kwargs):
        self.valkey = valkey.Redis(connection_pool=pool, **kwargs)

    @property
    def status(self) -> CacheConnectionStatus:
        return (
            CacheConnectionStatus.CONNECTED
            if self.valkey.connection is not None and self.valkey.ping()
            else CacheConnectionStatus.CLOSED
        )

    def close(self) -> None:
        return self.valkey.close()

    def exists(self, query: "AnyQuery") -> bool:
        return self.valkey.exists(query.key) == 1

    def store(self, query: "AnyQuery", data: "pl.DataFrame") -> None:
        dfio = data.write_ipc(file=None, compression="lz4")
        try:
            self.valkey.set(query.key, dfio.getvalue())
        except valkey.ConnectionError as exc:
            raise UpstreamNotPrepared(*exc.args) from exc
        except valkey.RedisError as exc:
            raise UpstreamInternalError(*exc.args) from exc

    def retrieve(self, query: "AnyQuery") -> Union["pl.DataFrame", None]:
        try:
            res: Optional[bytes] = self.valkey.get(query.key)  # type:ignore
        except valkey.ConnectionError as exc:
            raise UpstreamNotPrepared(*exc.args) from exc
        except valkey.RedisError as exc:
            raise UpstreamInternalError(*exc.args) from exc

        return None if res is None else pl.read_ipc(BytesIO(res))

    def ping(self) -> bool:
        return self.valkey.ping()  # type: ignore
