from typing import Union

from lxml import etree

from . import SchemaError


class XMLParseError(SchemaError):
    """An error happened while trying to parse a XML Schema."""


class MalformedXML(XMLParseError):
    """An unexpected node was found."""

    def __init__(self, expected: str, actual: Union[str, etree._Element]) -> None:
        message = ("A node '{1}' was found while attempting to parse a '{0}'").format(
            expected, actual
        )
        super().__init__(message)


class InvalidXMLAttributeName(XMLParseError):
    """An invalid attribute was found in a node."""

    def __init__(self, node: str, node_name: str, attr: str) -> None:
        message = (
            "An attribute '{2}' was found while attempting to parse {0} '{1}'"
        ).format(node, node_name, attr)
        super().__init__(message)


class InvalidXMLAttributeValue(XMLParseError):
    """An invalid value was found in the attribute of a node."""

    def __init__(self, node: str, node_name: str, attr: str, value: str) -> None:
        message = (
            "An invalid value '{3}' for the '{2}' attribute was found while "
            "trying to parse {0} '{1}'"
        ).format(node, node_name, attr, value)
        super().__init__(message)


class MissingXMLNode(XMLParseError):
    """A required child node is missing."""

    def __init__(self, node: str, node_name: str, child_node: str) -> None:
        message = ("A '{2}' child node is missing in {0} '{1}'").format(
            node, node_name, child_node
        )
        super().__init__(message)


class MissingXMLAttribute(XMLParseError):
    """A required attribute is not present."""

    def __init__(self, node: str, attr: str) -> None:
        message = ("A required attribute '{1}' is missing in a '{0}' node").format(
            node, attr
        )
        super().__init__(message)


class JSONParseError(SchemaError):
    """An error happened while trying to parse a JSON Schema."""


class MalformedJSON(JSONParseError):
    """An unexpected object was found."""

    def __init__(self, expected: str) -> None:
        message = ""
        super().__init__(message)


class MissingPropertyError(SchemaError):
    """A mandatory property couldn't be retrieved from a Shared/Usage entity
    combination."""

    def __init__(self, entity: str, name: str, attr: str):
        message = ("There's a missing '{2}' attribute in {0} '{1}'.").format(
            entity, name, attr
        )
        super().__init__(message)


class InvalidNameError(SchemaError):
    """The name of an Entity contains invalid characters."""

    def __init__(self, cube: str, entity: str, name: str) -> None:
        message = (
            "There's a {1} with an invalid name '{2}' in the cube '{0}'. "
            "Entity names can't contain the following characters: , ; :"
        ).format(cube, entity, name)
        super().__init__(message)


class DuplicateKeyError(SchemaError):
    """The key of some property in the schema is shared in two nodes."""

    def __init__(self, key: str) -> None:
        message = f"Key '{key}' is duplicated"
        super().__init__(message)


class DuplicatedNameError(SchemaError):
    """The name of an Entity is duplicated across its parent cube."""

    def __init__(self, cube: str, entity_prev: str, entity: str, name: str):
        message = (
            "In the cube '{0}' a {1} and a {2} share the same name '{3}'. "
            "Names of Measures, Levels and Properties must be unique across its cube."
        ).format(cube, entity_prev, entity, name)
        super().__init__(message)


class EntityUsageError(SchemaError):
    """There's a declared Usage reference pointing to a non-existent shared
    Entity."""

    def __init__(self, entity: str, source: str) -> None:
        message = ("An usage reference for '{}' {} cannot be found.").format(
            source, entity
        )
        super().__init__(message)
