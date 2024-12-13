"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.shafts import _34

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_ShaftRatingMethod")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ShaftRatingMethod",)


class EnumWithSelectedValue_ShaftRatingMethod(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ShaftRatingMethod

    A specific implementation of 'EnumWithSelectedValue' for 'ShaftRatingMethod' types.
    """

    __qualname__ = "ShaftRatingMethod"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_ShaftRatingMethod]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_ShaftRatingMethod]",
    ) -> "_34.ShaftRatingMethod":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _34.ShaftRatingMethod
        """
        return _34.ShaftRatingMethod

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_ShaftRatingMethod]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _34.ShaftRatingMethod.type_()

    @property
    def selected_value(self: "Self") -> "_34.ShaftRatingMethod":
        """mastapy.shafts.ShaftRatingMethod

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_34.ShaftRatingMethod]":
        """List[mastapy.shafts.ShaftRatingMethod]

        Note:
            This property is readonly.
        """
        return None
