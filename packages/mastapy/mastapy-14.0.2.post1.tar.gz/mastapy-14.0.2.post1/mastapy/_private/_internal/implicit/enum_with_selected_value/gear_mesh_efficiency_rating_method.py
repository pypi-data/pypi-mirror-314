"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating import _372

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_GearMeshEfficiencyRatingMethod")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_GearMeshEfficiencyRatingMethod",)


class EnumWithSelectedValue_GearMeshEfficiencyRatingMethod(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_GearMeshEfficiencyRatingMethod

    A specific implementation of 'EnumWithSelectedValue' for 'GearMeshEfficiencyRatingMethod' types.
    """

    __qualname__ = "GearMeshEfficiencyRatingMethod"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_GearMeshEfficiencyRatingMethod]",
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
        cls: "Type[EnumWithSelectedValue_GearMeshEfficiencyRatingMethod]",
    ) -> "_372.GearMeshEfficiencyRatingMethod":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _372.GearMeshEfficiencyRatingMethod
        """
        return _372.GearMeshEfficiencyRatingMethod

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_GearMeshEfficiencyRatingMethod]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _372.GearMeshEfficiencyRatingMethod.type_()

    @property
    def selected_value(self: "Self") -> "_372.GearMeshEfficiencyRatingMethod":
        """mastapy.gears.rating.GearMeshEfficiencyRatingMethod

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_372.GearMeshEfficiencyRatingMethod]":
        """List[mastapy.gears.rating.GearMeshEfficiencyRatingMethod]

        Note:
            This property is readonly.
        """
        return None
