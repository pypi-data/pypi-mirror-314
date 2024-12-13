from typing import Dict, List, Union
from urllib.parse import ParseResult, parse_qs, urlencode, urlparse, urlunparse


def hide_dsn_password(dsn: str) -> str:
    url = urlparse(dsn)
    if url.password is not None:
        url = url._replace(password="***")
    return url.geturl()


class URL:
    scheme: str
    netloc: str
    path: str
    params: str
    fragment: str
    query_params: Dict[str, List[str]]

    def __init__(self, url: str):
        parsed_url = urlparse(url)

        self.scheme = parsed_url.scheme
        self.netloc = parsed_url.netloc
        self.path = parsed_url.path
        self.params = parsed_url.params
        self.fragment = parsed_url.fragment
        self.query_params = parse_qs(parsed_url.query, strict_parsing=True)

    def __str__(self):
        parsed_url = ParseResult(
            self.scheme, self.netloc, self.path, self.params, self.query, self.fragment
        )
        return urlunparse(parsed_url)

    @property
    def query(self):
        return urlencode(self.query_params, doseq=True)

    @property
    def username(self):
        return self

    @property
    def password(self):
        return self

    @property
    def hostname(self):
        return self

    @property
    def port(self):
        return self

    def query_pop(self, key: str, default: str = ""):
        """
        Removes a key from the query string and returns its value.

        Args:
            key (str): The key to remove from the query string.
            default (any, optional): The default value to return if the key is not present or is empty. Defaults to None.

        Returns:
            any: The value of the key or the default value.
        """
        value = self.query_params.pop(key, [default])[0]
        return default if value == "" else value

    def query_add(self, key: str, value: Union[str, List[str]]):
        """
        Appends one or many values to a key in the query string.

        Args:
            key (str): The key to add from the query string.
            value (str | list[str]): The value or list of values to add to the key in the query string.

        Returns:
            None: Performs the action internally and returns nothing.
        """
        if isinstance(value, str):
            value = [value]
        self.query_params[key] = self.query_params.get(key, []) + value
