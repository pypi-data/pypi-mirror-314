from enum import Enum
from typing import Any, Dict, Optional, Sequence, Type

import polars as pl


class AggregatorType(Enum):
    """Lists the possible aggregation operations to perform on the data to
    return a measure."""

    SUM = "sum"
    COUNT = "count"
    AVERAGE = "avg"
    MAX = "max"
    MIN = "min"
    MODE = "mode"
    BASICGROUPEDMEDIAN = "basic_grouped_median"
    WEIGHTEDSUM = "weighted_sum"
    WEIGHTEDAVERAGE = "weighted_avg"
    REPLICATEWEIGHTMOE = "replicate_weight_moe"
    CALCULATEDMOE = "moe"
    WEIGHTEDAVERAGEMOE = "weighted_average_moe"
    MEDIAN = "median"
    QUANTILE = "quantile"
    DISTINCTCOUNT = "distinct_count"

    @classmethod
    def from_str(cls, value: str):
        value = value.lower()
        try:
            return next((item for item in cls if item.value == value))
        except StopIteration:
            raise ValueError(f"Invalid AggregatorType value: {value}")


class DimensionType(Enum):
    """Lists the kinds of data a dimension is storing."""

    STANDARD = "standard"
    TIME = "time"
    GEO = "geo"

    def __repr__(self):
        return f"{type(self).__name__}.{self.name}"

    def __str__(self):
        return self.value

    @classmethod
    def from_str(cls, value: Optional[str]):
        if value is None:
            return cls.STANDARD
        value = value.lower()
        return next((item for item in cls if item.value == value), cls.STANDARD)


class MemberType(Enum):
    """Lists the types of the data the user can expect to find in the associated
    column."""

    BOOLEAN = "bool"
    DATE = "date"
    TIME = "time"
    DATETIME = "dttm"
    TIMESTAMP = "stmp"
    FLOAT32 = "f32"
    FLOAT64 = "f64"
    INT8 = "i8"
    INT16 = "i16"
    INT32 = "i32"
    INT64 = "i64"
    INT128 = "i128"
    UINT8 = "u8"
    UINT16 = "u16"
    UINT32 = "u32"
    UINT64 = "u64"
    UINT128 = "u128"
    STRING = "str"

    def __repr__(self):
        return f"{type(self).__name__}.{self.name}"

    def __str__(self):
        return self.value

    def get_caster(self):
        pldt = self.to_polars()
        if pldt.is_integer():
            return int
        elif pldt.is_float():
            return float
        elif self is MemberType.BOOLEAN:
            return bool
        return str

    def to_polars(self):
        return _POLARS_DATATYPES[self]

    @classmethod
    def from_str(cls, value: Optional[str]):
        if value is None:
            return cls.INT64
        value = value.lower()
        return next((item for item in cls if item.value == value), cls.INT64)

    @classmethod
    def from_polars(cls, value: Type[pl.DataType]):
        name = _MEMBERTYPE_REVERSE[value]
        return cls[name]

    @classmethod
    def from_values(cls, values: Sequence[Any]):
        types = frozenset(type(value) for value in values)

        if len(types) == 1 and bool in types:
            return MemberType.BOOLEAN

        if float in types:
            return MemberType.FLOAT64

        if int in types:
            return cls.from_int_values(values)

        return MemberType.STRING

    @classmethod
    def from_int_values(cls, values: Sequence[int]):
        mini = min(values)
        maxi = max(values)

        if mini < 0:
            if mini < -(2**63) or maxi > 2**63 - 1:
                return MemberType.INT128
            elif mini < -(2**31) or maxi > 2**31 - 1:
                return MemberType.INT64
            elif mini < -(2**15) or maxi > 2**15 - 1:
                return MemberType.INT32
            elif mini < -128 or maxi > 127:
                return MemberType.INT16
            else:
                return MemberType.INT8
        else:
            if maxi > 2**64 - 1:
                return MemberType.UINT128
            elif maxi > 2**32 - 1:
                return MemberType.UINT64
            elif maxi > 65535:
                return MemberType.UINT32
            elif maxi > 255:
                return MemberType.UINT16
            else:
                return MemberType.UINT8


_POLARS_DATATYPES: Dict[MemberType, Type[pl.DataType]] = {
    MemberType.BOOLEAN: pl.Boolean,
    MemberType.DATE: pl.Date,
    MemberType.TIME: pl.Time,
    MemberType.DATETIME: pl.Datetime,
    MemberType.TIMESTAMP: pl.UInt64,
    MemberType.FLOAT32: pl.Float32,
    MemberType.FLOAT64: pl.Float64,
    MemberType.INT8: pl.Int8,
    MemberType.INT16: pl.Int16,
    MemberType.INT32: pl.Int32,
    MemberType.INT64: pl.Int64,
    MemberType.INT128: pl.Int64,
    MemberType.UINT8: pl.UInt8,
    MemberType.UINT16: pl.UInt16,
    MemberType.UINT32: pl.UInt32,
    MemberType.UINT64: pl.UInt64,
    MemberType.UINT128: pl.UInt64,
    MemberType.STRING: pl.String,
}

_MEMBERTYPE_REVERSE = {value: key.name for key, value in _POLARS_DATATYPES.items()}
