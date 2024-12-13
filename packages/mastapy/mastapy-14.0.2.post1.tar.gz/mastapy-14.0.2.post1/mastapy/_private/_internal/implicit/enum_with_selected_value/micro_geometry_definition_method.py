"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving import _670

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_MicroGeometryDefinitionMethod")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_MicroGeometryDefinitionMethod",)


class EnumWithSelectedValue_MicroGeometryDefinitionMethod(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_MicroGeometryDefinitionMethod

    A specific implementation of 'EnumWithSelectedValue' for 'MicroGeometryDefinitionMethod' types.
    """

    __qualname__ = "MicroGeometryDefinitionMethod"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_MicroGeometryDefinitionMethod]",
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
        cls: "Type[EnumWithSelectedValue_MicroGeometryDefinitionMethod]",
    ) -> "_670.MicroGeometryDefinitionMethod":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _670.MicroGeometryDefinitionMethod
        """
        return _670.MicroGeometryDefinitionMethod

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_MicroGeometryDefinitionMethod]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _670.MicroGeometryDefinitionMethod.type_()

    @property
    def selected_value(self: "Self") -> "_670.MicroGeometryDefinitionMethod":
        """mastapy.gears.manufacturing.cylindrical.plunge_shaving.MicroGeometryDefinitionMethod

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_670.MicroGeometryDefinitionMethod]":
        """List[mastapy.gears.manufacturing.cylindrical.plunge_shaving.MicroGeometryDefinitionMethod]

        Note:
            This property is readonly.
        """
        return None
