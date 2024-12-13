"""This module holds utility classes and methods to be used internally by mastapy.

These should not be accessed by package users.
"""

from __future__ import annotations

import contextlib
import re
from functools import lru_cache
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from re import Pattern
    from typing import Any, TypeVar

    Self_StrEnum = TypeVar("Self_StrEnum", "StrEnum")

try:
    from enum import StrEnum
except ImportError:
    from enum import Enum

    class StrEnum(str, Enum):
        """Polyfill for Python 3.11+ StrEnum."""

        def __str__(self: "Self_StrEnum") -> str:
            """Override of the str magic method.

            Returns:
                str
            """
            return str(self.value)


class Setter:
    """Decorator class for setter-only properties.

    By using this instead of @property and @func.setter for setter-only properties,
    we remove some minor overheads.

    Args:
        func: the function to be decorated.
        doc (str, optional): documentation for the setter.


    Attributes:
        func: the decorated function.
    """

    def __init__(self, func, doc=None):
        self.func = func
        self.__doc__ = doc if doc is not None else func.__doc__

    def __set__(self, obj, value):
        """Override of the set magic method."""
        return self.func(obj, value)


def qualname(input: "Any") -> str:
    """Safely get the qualified name of an object.

    Args:
        input (Any): Object.

    Returns:
        str
    """

    with contextlib.suppress(AttributeError):
        return input.__qualname__

    with contextlib.suppress(AttributeError):
        return input.__name__

    return str(input)


@lru_cache(maxsize=None)
def _get_snake_case_regex() -> "Pattern[str]":
    return re.compile(r"((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))")


def snake(input: str) -> str:
    """Convert a string to snake case.

    Args:
        input (str): Input string to convert.

    Returns:
        str
    """
    reg = _get_snake_case_regex()
    return reg.sub(r"_\1", input).lower()


def camel_spaced(input: str) -> str:
    """Convert a string to spaced camel case.

    Args:
        input (str): Input string to convert.

    Returns:
        str
    """
    return " ".join(x.capitalize() for x in input.replace(" ", "_").split("_"))


def camel(input: str) -> str:
    """Convert a string to camel case.

    Args:
        input (str): Input string to convert.

    Returns:
        str
    """
    return "".join(x.capitalize() for x in input.replace(" ", "_").split("_"))


def camel_lower(input: str) -> str:
    """Convert a string to lower camel case.

    Args:
        input (str): Input string to convert.

    Returns:
        str
    """
    result = camel(input)
    return result[0].lower() + result[1:]


@lru_cache(maxsize=None)
def _get_punctuation_table():
    import string

    return str.maketrans(dict.fromkeys(string.punctuation))


def strip_punctuation(input: str) -> str:
    """Strip punctuation from a string.

    Args:
        input (str): Input string to strip of punctuation.

    Returns:
        str
    """
    return input.translate(_get_punctuation_table())
