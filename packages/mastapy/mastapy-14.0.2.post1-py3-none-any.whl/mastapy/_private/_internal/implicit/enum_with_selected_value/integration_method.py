"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis import _71

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_IntegrationMethod")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_IntegrationMethod",)


class EnumWithSelectedValue_IntegrationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_IntegrationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'IntegrationMethod' types.
    """

    __qualname__ = "IntegrationMethod"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_IntegrationMethod]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_IntegrationMethod]",
    ) -> "_71.IntegrationMethod":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _71.IntegrationMethod
        """
        return _71.IntegrationMethod

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_IntegrationMethod]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _71.IntegrationMethod.type_()

    @property
    def selected_value(self: "Self") -> "_71.IntegrationMethod":
        """mastapy.nodal_analysis.IntegrationMethod

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_71.IntegrationMethod]":
        """List[mastapy.nodal_analysis.IntegrationMethod]

        Note:
            This property is readonly.
        """
        return None
