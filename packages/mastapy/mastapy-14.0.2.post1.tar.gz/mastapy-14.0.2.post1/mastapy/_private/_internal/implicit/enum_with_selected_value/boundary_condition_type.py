"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.fe_export_utility import _173

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_BoundaryConditionType")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_BoundaryConditionType",)


class EnumWithSelectedValue_BoundaryConditionType(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_BoundaryConditionType

    A specific implementation of 'EnumWithSelectedValue' for 'BoundaryConditionType' types.
    """

    __qualname__ = "BoundaryConditionType"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_BoundaryConditionType]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_BoundaryConditionType]",
    ) -> "_173.BoundaryConditionType":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _173.BoundaryConditionType
        """
        return _173.BoundaryConditionType

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_BoundaryConditionType]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _173.BoundaryConditionType.type_()

    @property
    def selected_value(self: "Self") -> "_173.BoundaryConditionType":
        """mastapy.nodal_analysis.fe_export_utility.BoundaryConditionType

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_173.BoundaryConditionType]":
        """List[mastapy.nodal_analysis.fe_export_utility.BoundaryConditionType]

        Note:
            This property is readonly.
        """
        return None
