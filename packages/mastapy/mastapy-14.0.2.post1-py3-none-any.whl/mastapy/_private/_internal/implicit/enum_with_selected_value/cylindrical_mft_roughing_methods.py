"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.cylindrical import _649

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_CylindricalMftRoughingMethods")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_CylindricalMftRoughingMethods",)


class EnumWithSelectedValue_CylindricalMftRoughingMethods(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_CylindricalMftRoughingMethods

    A specific implementation of 'EnumWithSelectedValue' for 'CylindricalMftRoughingMethods' types.
    """

    __qualname__ = "CylindricalMftRoughingMethods"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_CylindricalMftRoughingMethods]",
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
        cls: "Type[EnumWithSelectedValue_CylindricalMftRoughingMethods]",
    ) -> "_649.CylindricalMftRoughingMethods":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _649.CylindricalMftRoughingMethods
        """
        return _649.CylindricalMftRoughingMethods

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_CylindricalMftRoughingMethods]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _649.CylindricalMftRoughingMethods.type_()

    @property
    def selected_value(self: "Self") -> "_649.CylindricalMftRoughingMethods":
        """mastapy.gears.manufacturing.cylindrical.CylindricalMftRoughingMethods

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_649.CylindricalMftRoughingMethods]":
        """List[mastapy.gears.manufacturing.cylindrical.CylindricalMftRoughingMethods]

        Note:
            This property is readonly.
        """
        return None
