from enum import Enum
from typing import List, Tuple, Union

from clickhouse_driver.dbapi.extras import Cursor
from pypika.terms import AggregateFunction, Function, Term

from tesseract_olap.schema import InlineTable, MemberType


class TypedCursor(Cursor):
    _columns: List[str]
    _columns_with_types: List[Tuple[str, str]]

    def fetchall(self):
        result = super().fetchall()
        assert result is None or isinstance(result, list)
        return [] if result is None else result

    def fetchmany(self, size=None):
        result = super().fetchmany(size)
        assert result is None or isinstance(result, list)
        return [] if result is None else result

    def fetchone(self):
        result = super().fetchone()
        assert result is None or isinstance(result, tuple)
        return result

    def reset_cursor(self):
        self._reset_state()

    def set_inline_table(self, table: InlineTable):
        tblmeta_gen = (ClickhouseDataType[item.name].value for item in table.types)
        structure = zip(table.headers, tblmeta_gen)
        self.set_external_table(table.name, list(structure), table.rows)


class TypedDictCursor(TypedCursor):
    """
    A cursor that generates results as :class:`dict`.

    ``fetch*()`` methods will return dicts instead of tuples.
    """

    def fetchall(self):
        rv = super(TypedDictCursor, self).fetchall()
        return [dict(zip(self._columns, x)) for x in rv]

    def fetchmany(self, size=None):
        rv = super(TypedDictCursor, self).fetchmany(size=size)
        return [] if rv is None else [dict(zip(self._columns, x)) for x in rv]

    def fetchone(self):
        rv = super(TypedDictCursor, self).fetchone()
        return None if rv is None else dict(zip(self._columns, rv))


class ClickhouseDataType(Enum):
    """Lists the types of the data the user can expect to find in the associated
    column."""

    BOOLEAN = "Bool"
    DATE = "Date32"
    DATETIME = "DateTime64"
    TIMESTAMP = "UInt32"
    FLOAT32 = "Float32"
    FLOAT64 = "Float64"
    INT8 = "Int8"
    INT16 = "Int16"
    INT32 = "Int32"
    INT64 = "Int64"
    INT128 = "Int128"
    UINT8 = "UInt8"
    UINT16 = "UInt16"
    UINT32 = "UInt32"
    UINT64 = "UInt64"
    UINT128 = "UInt128"
    STRING = "String"

    def __repr__(self):
        return f"ClickhouseDataType.{self.name}"

    def __str__(self):
        return self.value

    @classmethod
    def from_membertype(cls, mt: MemberType):
        """Transforms a MemberType enum value into a ClickhouseDataType."""
        return cls[mt.name]

    def to_membertype(self):
        """Transforms a ClickhouseDataType enum value into a MemberType."""
        return MemberType[self.name]


class ClickhouseJoinType(Enum):
    inner = ""
    left = "LEFT"
    right = "RIGHT"
    outer = "FULL OUTER"
    left_outer = "LEFT OUTER"
    right_outer = "RIGHT OUTER"
    full_outer = "FULL OUTER"
    cross = "CROSS"
    asof = "ASOF"
    paste = "PASTE"


class ArrayElement(Function):
    def __init__(
        self,
        array: Union[str, Term],
        n: Union[int, Term],
        alias: Union[str, None] = None,
    ) -> None:
        super(ArrayElement, self).__init__("arrayElement", array, n, alias=alias)


class Power(Function):
    def __init__(
        self,
        base: Union[int, Term],
        exp: Union[int, Term],
        alias: Union[str, None] = None,
    ):
        super(Power, self).__init__("pow", base, exp, alias=alias)


class AverageWeighted(AggregateFunction):
    def __init__(
        self,
        value_field: Union[str, Term],
        weight_field: Union[str, Term],
        alias: Union[str, None] = None,
    ):
        super(AverageWeighted, self).__init__(
            "avgWeighted", value_field, weight_field, alias=alias
        )


class TopK(AggregateFunction):
    def __init__(
        self,
        amount: int,
        field: Union[str, Term],
        alias: Union[str, None] = None,
    ):
        super(TopK, self).__init__("topK(%d)" % amount, field, alias=alias)


class Median(AggregateFunction):
    def __init__(
        self,
        field: Union[str, Term],
        alias: Union[str, None] = None,
    ):
        super(Median, self).__init__("median", field, alias=alias)


class Quantile(AggregateFunction):
    def __init__(
        self,
        quantile_level: float,
        field: Union[str, Term],
        alias: Union[str, None] = None,
    ):
        if quantile_level <= 0 or quantile_level >= 1:
            raise ValueError("The quantile_level parameter is not in the range ]0, 1[")

        super(Quantile, self).__init__(
            "quantileExact(%f)" % quantile_level, field, alias=alias
        )


class DistinctCount(AggregateFunction):
    def __init__(
        self,
        field: Union[str, Term],
        alias: Union[str, None] = None,
    ):
        super(DistinctCount, self).__init__("uniqExact", field, alias=alias)
