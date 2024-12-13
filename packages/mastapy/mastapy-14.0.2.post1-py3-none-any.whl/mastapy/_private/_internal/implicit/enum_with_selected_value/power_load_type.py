"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model import _2276

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_PowerLoadType")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_PowerLoadType",)


class EnumWithSelectedValue_PowerLoadType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_PowerLoadType

    A specific implementation of 'EnumWithSelectedValue' for 'PowerLoadType' types.
    """

    __qualname__ = "PowerLoadType"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_PowerLoadType]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_PowerLoadType]",
    ) -> "_2276.PowerLoadType":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2276.PowerLoadType
        """
        return _2276.PowerLoadType

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_PowerLoadType]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2276.PowerLoadType.type_()

    @property
    def selected_value(self: "Self") -> "_2276.PowerLoadType":
        """mastapy.system_model.PowerLoadType

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_2276.PowerLoadType]":
        """List[mastapy.system_model.PowerLoadType]

        Note:
            This property is readonly.
        """
        return None
