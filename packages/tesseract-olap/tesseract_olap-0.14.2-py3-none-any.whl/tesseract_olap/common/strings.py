from functools import lru_cache
from hashlib import md5
from typing import Any, Mapping, Optional, Union, overload
from urllib.parse import urlparse

from typing_extensions import Literal

NAN_VALUES = frozenset(
    (
        "-1.#IND",
        "1.#QNAN",
        "1.#IND",
        "-1.#QNAN",
        "#N/A N/A",
        "#N/A",
        "N/A",
        "n/a",
        "#NA",
        "NULL",
        "null",
        "NaN",
        "-NaN",
        "nan",
        "-nan",
    )
)

TRUTHY_STRINGS = frozenset(("1", "true", "on", "y", "yes"))
FALSEY_STRINGS = frozenset(("0", "false", "off", "n", "no", "none", ""))


@overload
def get_localization(
    dictionary: Mapping[str, str],
    locale: str,
) -> Optional[str]: ...
@overload
def get_localization(
    dictionary: Mapping[str, str],
    locale: str,
    *,
    force: Literal[True],
) -> str: ...
def get_localization(
    dictionary: Mapping[str, str],
    locale: str,
    *,
    force: bool = False,
) -> Optional[str]:
    """Attempts to return the value from a dictionary of terms, where the locale
    code is the key.

    If it doesn't find the specific locale, looks for the general locale code,
    and if it's not available either, returns the value for the default locale.
    """
    if locale not in dictionary:
        locale = locale[0:2]
    if locale not in dictionary:
        locale = "xx"
    return dictionary[locale] if force else dictionary.get(locale)


@lru_cache(128)
def shorthash(string: str) -> str:
    return str(md5(string.encode("utf-8")).hexdigest())[:8]


def numerify(string: Union[str, bytes]):
    string = string if isinstance(string, str) else str(string)
    if string in NAN_VALUES:
        return float("nan")
    _f = float(string)
    return int(string) if string.isnumeric() and int(string) == _f else _f


def is_numeric(string: Union[str, bytes]) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return string in NAN_VALUES


def hide_dsn_password(dsn: str) -> str:
    url = urlparse(dsn)
    if url.password is not None:
        url = url._replace(password="***")
    return url.geturl()


def stringify(obj: Any) -> str:
    if isinstance(obj, (list, set, tuple)):
        return repr(sorted(obj))

    if isinstance(obj, Mapping):
        return "{%s}" % ", ".join(
            f"{repr(key)}: {repr(value)}"
            for key, value in sorted(obj.items(), key=lambda x: x[0])
        )

    return repr(obj)
