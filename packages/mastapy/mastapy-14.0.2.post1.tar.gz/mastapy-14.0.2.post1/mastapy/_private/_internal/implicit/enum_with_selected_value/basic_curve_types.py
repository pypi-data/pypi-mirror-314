"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.geometry.two_d.curves import _325

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_BasicCurveTypes")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_BasicCurveTypes",)


class EnumWithSelectedValue_BasicCurveTypes(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_BasicCurveTypes

    A specific implementation of 'EnumWithSelectedValue' for 'BasicCurveTypes' types.
    """

    __qualname__ = "BasicCurveTypes"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_BasicCurveTypes]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_BasicCurveTypes]",
    ) -> "_325.BasicCurveTypes":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _325.BasicCurveTypes
        """
        return _325.BasicCurveTypes

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_BasicCurveTypes]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _325.BasicCurveTypes.type_()

    @property
    def selected_value(self: "Self") -> "_325.BasicCurveTypes":
        """mastapy.geometry.two_d.curves.BasicCurveTypes

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_325.BasicCurveTypes]":
        """List[mastapy.geometry.two_d.curves.BasicCurveTypes]

        Note:
            This property is readonly.
        """
        return None
