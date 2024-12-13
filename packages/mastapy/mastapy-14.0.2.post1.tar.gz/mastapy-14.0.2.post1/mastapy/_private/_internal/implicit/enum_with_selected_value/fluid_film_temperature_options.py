"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings import _1939

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_FluidFilmTemperatureOptions")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_FluidFilmTemperatureOptions",)


class EnumWithSelectedValue_FluidFilmTemperatureOptions(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_FluidFilmTemperatureOptions

    A specific implementation of 'EnumWithSelectedValue' for 'FluidFilmTemperatureOptions' types.
    """

    __qualname__ = "FluidFilmTemperatureOptions"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_FluidFilmTemperatureOptions]",
    ) -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_FluidFilmTemperatureOptions]",
    ) -> "_1939.FluidFilmTemperatureOptions":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1939.FluidFilmTemperatureOptions
        """
        return _1939.FluidFilmTemperatureOptions

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_FluidFilmTemperatureOptions]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1939.FluidFilmTemperatureOptions.type_()

    @property
    def selected_value(self: "Self") -> "_1939.FluidFilmTemperatureOptions":
        """mastapy.bearings.FluidFilmTemperatureOptions

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_1939.FluidFilmTemperatureOptions]":
        """List[mastapy.bearings.FluidFilmTemperatureOptions]

        Note:
            This property is readonly.
        """
        return None
