"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.report import _1798

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_CadPageOrientation")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_CadPageOrientation",)


class EnumWithSelectedValue_CadPageOrientation(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_CadPageOrientation

    A specific implementation of 'EnumWithSelectedValue' for 'CadPageOrientation' types.
    """

    __qualname__ = "CadPageOrientation"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_CadPageOrientation]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_CadPageOrientation]",
    ) -> "_1798.CadPageOrientation":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1798.CadPageOrientation
        """
        return _1798.CadPageOrientation

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_CadPageOrientation]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1798.CadPageOrientation.type_()

    @property
    def selected_value(self: "Self") -> "_1798.CadPageOrientation":
        """mastapy.utility.report.CadPageOrientation

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_1798.CadPageOrientation]":
        """List[mastapy.utility.report.CadPageOrientation]

        Note:
            This property is readonly.
        """
        return None
