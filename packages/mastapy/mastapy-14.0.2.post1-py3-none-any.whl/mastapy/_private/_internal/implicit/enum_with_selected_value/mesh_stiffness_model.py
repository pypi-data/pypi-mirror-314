"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model import _2271

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_MeshStiffnessModel")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_MeshStiffnessModel",)


class EnumWithSelectedValue_MeshStiffnessModel(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_MeshStiffnessModel

    A specific implementation of 'EnumWithSelectedValue' for 'MeshStiffnessModel' types.
    """

    __qualname__ = "MeshStiffnessModel"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_MeshStiffnessModel]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_MeshStiffnessModel]",
    ) -> "_2271.MeshStiffnessModel":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2271.MeshStiffnessModel
        """
        return _2271.MeshStiffnessModel

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_MeshStiffnessModel]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2271.MeshStiffnessModel.type_()

    @property
    def selected_value(self: "Self") -> "_2271.MeshStiffnessModel":
        """mastapy.system_model.MeshStiffnessModel

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_2271.MeshStiffnessModel]":
        """List[mastapy.system_model.MeshStiffnessModel]

        Note:
            This property is readonly.
        """
        return None
