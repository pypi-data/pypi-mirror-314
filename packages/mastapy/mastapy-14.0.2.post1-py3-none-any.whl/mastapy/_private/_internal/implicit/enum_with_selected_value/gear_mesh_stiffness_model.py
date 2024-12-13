"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5568

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_GearMeshStiffnessModel")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_GearMeshStiffnessModel",)


class EnumWithSelectedValue_GearMeshStiffnessModel(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_GearMeshStiffnessModel

    A specific implementation of 'EnumWithSelectedValue' for 'GearMeshStiffnessModel' types.
    """

    __qualname__ = "GearMeshStiffnessModel"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_GearMeshStiffnessModel]",
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
        cls: "Type[EnumWithSelectedValue_GearMeshStiffnessModel]",
    ) -> "_5568.GearMeshStiffnessModel":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _5568.GearMeshStiffnessModel
        """
        return _5568.GearMeshStiffnessModel

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_GearMeshStiffnessModel]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _5568.GearMeshStiffnessModel.type_()

    @property
    def selected_value(self: "Self") -> "_5568.GearMeshStiffnessModel":
        """mastapy.system_model.analyses_and_results.mbd_analyses.GearMeshStiffnessModel

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_5568.GearMeshStiffnessModel]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.GearMeshStiffnessModel]

        Note:
            This property is readonly.
        """
        return None
