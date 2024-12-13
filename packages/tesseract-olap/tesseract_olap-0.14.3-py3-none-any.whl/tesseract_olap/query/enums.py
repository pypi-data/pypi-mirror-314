from typing import Literal, Optional, Union

from strenum import StrEnum

AnyOrder = Union[Literal["asc", "desc"], "Order"]


class Comparison(StrEnum):
    """Comparison Enum.

    Defines the available value comparison operations.
    """

    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    EQ = "eq"
    NEQ = "neq"

    @classmethod
    def from_str(cls, string: str):
        key = string.strip().upper()
        value = SYMBOL_MAP.get(key)
        if not isinstance(value, cls):
            raise ValueError(f"Invalid Comparison value: {string}")
        return value


class JoinType(StrEnum):
    """Defines the different types of join operations available to the user."""

    INNER = "inner"
    LEFT = "left"
    RIGHT = "right"
    FULL = "full"
    SEMI = "semi"
    ANTI = "anti"
    CROSS = "cross"


class LogicOperator(StrEnum):
    """Logical connector Enum.

    Defines logical operations between conditional predicates.
    """

    AND = "and"
    OR = "or"
    XOR = "xor"

    def __repr__(self):
        return f"{type(self).__name__}.{self.name}"

    def __str__(self):
        return self.value

    @classmethod
    def from_str(cls, string: str):
        key = string.strip().upper()
        value = SYMBOL_MAP.get(key)
        if not isinstance(value, cls):
            raise ValueError(f"Invalid LogicOperator value: {string}")
        return value


class Membership(StrEnum):
    """Membership Enum.

    Defines the membership of a value to a set."""

    IN = "in"
    NIN = "nin"

    @classmethod
    def from_str(cls, string: str):
        key = string.strip().upper()
        value = SYMBOL_MAP.get(key)
        if not isinstance(value, cls):
            raise ValueError(f"Invalid Membership value: {string}")
        return value


class NullityOperator(StrEnum):
    """Nullity correspondence Enum.

    Evaluates if a value is or not is NULL.
    """

    ISNULL = "isnull"
    ISNOTNULL = "isnotnull"

    @classmethod
    def from_str(cls, string: str):
        key = string.replace(" ", "").strip().upper()
        value = SYMBOL_MAP.get(key)
        if not isinstance(value, cls):
            raise ValueError(f"Invalid NullityOperator value: {string}")
        return value


class Order(StrEnum):
    """Order direction Enum.

    Defines a direction to use in a sorting operation.
    """

    ASC = "asc"
    DESC = "desc"

    def __repr__(self):
        return f"{type(self).__name__}.{self.name}"

    def __str__(self):
        return self.value

    @classmethod
    def from_str(cls, string: Optional[str]):
        key = str(string).strip().upper()
        enum = SYMBOL_MAP.get(key, cls.ASC)
        return enum


class TimeScale(StrEnum):
    YEAR = "year"
    QUARTER = "quarter"
    MONTH = "month"
    WEEK = "week"
    DAY = "day"

    def __repr__(self):
        return f"{type(self).__name__}.{self.name}"

    def __str__(self):
        return self.value

    @classmethod
    def from_str(cls, string: str):
        assert string, "Invalid TimeScale: no value provided"
        key = string.strip().upper()
        value = SYMBOL_MAP.get(key)
        if not isinstance(value, cls):
            raise ValueError(f"Invalid TimeScale value: {string}")
        return value


class RestrictionAge(StrEnum):
    LATEST = "latest"
    OLDEST = "oldest"
    EXPR = "expr"

    def __repr__(self):
        return f"{type(self).__name__}.{self.name}"

    def __str__(self):
        return self.value

    @classmethod
    def from_str(cls, string: str):
        assert string, "Invalid RestrictionAge: no value provided"
        key = string.strip().upper()
        value = SYMBOL_MAP.get(key)
        if not isinstance(value, cls):
            raise ValueError(f"Invalid RestrictionAge value: {string}")
        return value


SYMBOL_MAP = {
    ">": Comparison.GT,
    ">=": Comparison.GTE,
    "<": Comparison.LT,
    "<=": Comparison.LTE,
    "=": Comparison.EQ,
    "==": Comparison.EQ,
    "!=": Comparison.NEQ,
    "GT": Comparison.GT,
    "GTE": Comparison.GTE,
    "LT": Comparison.LT,
    "LTE": Comparison.LTE,
    "EQ": Comparison.EQ,
    "NEQ": Comparison.NEQ,
    "AND": LogicOperator.AND,
    "OR": LogicOperator.OR,
    "XOR": LogicOperator.XOR,
    "IN": Membership.IN,
    "NIN": Membership.NIN,
    "ISNULL": NullityOperator.ISNULL,
    "ISNOTNULL": NullityOperator.ISNOTNULL,
    "ASC": Order.ASC,
    "DESC": Order.DESC,
    "LATEST": RestrictionAge.LATEST,
    "OLDEST": RestrictionAge.OLDEST,
    "YEAR": TimeScale.YEAR,
    "QUARTER": TimeScale.QUARTER,
    "MONTH": TimeScale.MONTH,
    "WEEK": TimeScale.WEEK,
    "DAY": TimeScale.DAY,
}
