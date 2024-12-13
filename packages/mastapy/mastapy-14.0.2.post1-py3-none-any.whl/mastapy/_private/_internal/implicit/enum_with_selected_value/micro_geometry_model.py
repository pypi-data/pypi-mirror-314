"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears import _349

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_MicroGeometryModel")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_MicroGeometryModel",)


class EnumWithSelectedValue_MicroGeometryModel(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_MicroGeometryModel

    A specific implementation of 'EnumWithSelectedValue' for 'MicroGeometryModel' types.
    """

    __qualname__ = "MicroGeometryModel"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_MicroGeometryModel]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_MicroGeometryModel]",
    ) -> "_349.MicroGeometryModel":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _349.MicroGeometryModel
        """
        return _349.MicroGeometryModel

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_MicroGeometryModel]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _349.MicroGeometryModel.type_()

    @property
    def selected_value(self: "Self") -> "_349.MicroGeometryModel":
        """mastapy.gears.MicroGeometryModel

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_349.MicroGeometryModel]":
        """List[mastapy.gears.MicroGeometryModel]

        Note:
            This property is readonly.
        """
        return None
