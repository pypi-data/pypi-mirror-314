"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.drawing.options import _2319

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_ExcitationAnalysisViewOption")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ExcitationAnalysisViewOption",)


class EnumWithSelectedValue_ExcitationAnalysisViewOption(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_ExcitationAnalysisViewOption

    A specific implementation of 'EnumWithSelectedValue' for 'ExcitationAnalysisViewOption' types.
    """

    __qualname__ = "ExcitationAnalysisViewOption"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_ExcitationAnalysisViewOption]",
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
        cls: "Type[EnumWithSelectedValue_ExcitationAnalysisViewOption]",
    ) -> "_2319.ExcitationAnalysisViewOption":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2319.ExcitationAnalysisViewOption
        """
        return _2319.ExcitationAnalysisViewOption

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_ExcitationAnalysisViewOption]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2319.ExcitationAnalysisViewOption.type_()

    @property
    def selected_value(self: "Self") -> "_2319.ExcitationAnalysisViewOption":
        """mastapy.system_model.drawing.options.ExcitationAnalysisViewOption

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_2319.ExcitationAnalysisViewOption]":
        """List[mastapy.system_model.drawing.options.ExcitationAnalysisViewOption]

        Note:
            This property is readonly.
        """
        return None
