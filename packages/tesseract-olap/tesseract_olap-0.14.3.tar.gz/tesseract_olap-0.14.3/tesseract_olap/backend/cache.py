import abc
from enum import Enum
from typing import Union

import polars as pl
from lfudacache import LFUDACache

from tesseract_olap.query import AnyQuery

CacheConnectionStatus = Enum("CacheConnectionStatus", ["CLOSED", "CONNECTED"])


class CacheProvider(abc.ABC):
    """Base class for the implementation of a cache layer for the Backend."""

    def __repr__(self):
        return f"{type(self).__name__}"

    @abc.abstractmethod
    def connect(self) -> "CacheConnection":
        raise NotImplementedError

    @abc.abstractmethod
    def clear(self) -> None:
        raise NotImplementedError


class CacheConnection(abc.ABC):
    """Internal Base class for individual connections to the cache layer."""

    @property
    @abc.abstractmethod
    def status(self) -> "CacheConnectionStatus":
        raise NotImplementedError

    @abc.abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def store(self, query: "AnyQuery", data: "pl.DataFrame") -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def retrieve(self, query: "AnyQuery") -> Union["pl.DataFrame", None]:
        raise NotImplementedError

    @abc.abstractmethod
    def ping(self) -> bool:
        raise NotImplementedError


class DummyProvider(CacheProvider):
    """A CacheProvider used when the user doesn't set a valid one. Will always MISS."""

    def connect(self):
        return DummyConnection()

    def clear(self) -> None:
        pass


class DummyConnection(CacheConnection):
    """The CacheConnection associated to DummyProvider. Will always MISS."""

    @property
    def status(self):
        return CacheConnectionStatus.CONNECTED

    def close(self):
        pass

    def store(self, query: "AnyQuery", data: "pl.DataFrame"):
        pass

    def retrieve(self, query: "AnyQuery"):
        return None

    def ping(self):
        return True


class LfuProvider(CacheProvider):
    """Stores elements in a dictionary under the Least Frequently Used caching strategy."""

    def __init__(self, *, maxsize: int = 64, dfsize: int = 150) -> None:
        self.store = LFUDACache(maxsize)
        self.dfsize = dfsize

    def connect(self):
        return LfuConnection(self.store, self.dfsize)

    def clear(self):
        self.store.clear()  # type: ignore


class LfuConnection(CacheConnection):
    """The CacheConnection associated to LfuProvider."""

    def __init__(self, store: "LFUDACache", dfsize: int = 150) -> None:
        self.storage = store
        self.dfsize = dfsize

    @property
    def status(self):
        return CacheConnectionStatus.CONNECTED

    def close(self):
        pass

    def store(self, query: "AnyQuery", data: "pl.DataFrame"):
        if data.estimated_size("mb") < self.dfsize:
            self.storage[query.key] = data

    def retrieve(self, query: "AnyQuery") -> Union["pl.DataFrame", None]:
        return self.storage.get(query.key)

    def ping(self):
        return True
