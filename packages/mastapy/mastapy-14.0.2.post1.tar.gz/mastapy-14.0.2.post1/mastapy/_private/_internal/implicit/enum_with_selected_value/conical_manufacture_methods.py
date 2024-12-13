"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.gear_designs.conical import _1198

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_ConicalManufactureMethods")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ConicalManufactureMethods",)


class EnumWithSelectedValue_ConicalManufactureMethods(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_ConicalManufactureMethods

    A specific implementation of 'EnumWithSelectedValue' for 'ConicalManufactureMethods' types.
    """

    __qualname__ = "ConicalManufactureMethods"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_ConicalManufactureMethods]",
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
        cls: "Type[EnumWithSelectedValue_ConicalManufactureMethods]",
    ) -> "_1198.ConicalManufactureMethods":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1198.ConicalManufactureMethods
        """
        return _1198.ConicalManufactureMethods

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_ConicalManufactureMethods]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1198.ConicalManufactureMethods.type_()

    @property
    def selected_value(self: "Self") -> "_1198.ConicalManufactureMethods":
        """mastapy.gears.gear_designs.conical.ConicalManufactureMethods

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_1198.ConicalManufactureMethods]":
        """List[mastapy.gears.gear_designs.conical.ConicalManufactureMethods]

        Note:
            This property is readonly.
        """
        return None
