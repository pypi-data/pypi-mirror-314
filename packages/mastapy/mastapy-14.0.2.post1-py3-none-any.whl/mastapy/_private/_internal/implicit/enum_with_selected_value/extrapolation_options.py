"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.math_utility import _1560

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_ExtrapolationOptions")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ExtrapolationOptions",)


class EnumWithSelectedValue_ExtrapolationOptions(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_ExtrapolationOptions

    A specific implementation of 'EnumWithSelectedValue' for 'ExtrapolationOptions' types.
    """

    __qualname__ = "ExtrapolationOptions"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_ExtrapolationOptions]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_ExtrapolationOptions]",
    ) -> "_1560.ExtrapolationOptions":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1560.ExtrapolationOptions
        """
        return _1560.ExtrapolationOptions

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_ExtrapolationOptions]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1560.ExtrapolationOptions.type_()

    @property
    def selected_value(self: "Self") -> "_1560.ExtrapolationOptions":
        """mastapy.math_utility.ExtrapolationOptions

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_1560.ExtrapolationOptions]":
        """List[mastapy.math_utility.ExtrapolationOptions]

        Note:
            This property is readonly.
        """
        return None
