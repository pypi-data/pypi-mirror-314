"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.materials import _278

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_LubricantViscosityClassISO")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_LubricantViscosityClassISO",)


class EnumWithSelectedValue_LubricantViscosityClassISO(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_LubricantViscosityClassISO

    A specific implementation of 'EnumWithSelectedValue' for 'LubricantViscosityClassISO' types.
    """

    __qualname__ = "LubricantViscosityClassISO"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_LubricantViscosityClassISO]",
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
        cls: "Type[EnumWithSelectedValue_LubricantViscosityClassISO]",
    ) -> "_278.LubricantViscosityClassISO":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _278.LubricantViscosityClassISO
        """
        return _278.LubricantViscosityClassISO

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_LubricantViscosityClassISO]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _278.LubricantViscosityClassISO.type_()

    @property
    def selected_value(self: "Self") -> "_278.LubricantViscosityClassISO":
        """mastapy.materials.LubricantViscosityClassISO

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_278.LubricantViscosityClassISO]":
        """List[mastapy.materials.LubricantViscosityClassISO]

        Note:
            This property is readonly.
        """
        return None
