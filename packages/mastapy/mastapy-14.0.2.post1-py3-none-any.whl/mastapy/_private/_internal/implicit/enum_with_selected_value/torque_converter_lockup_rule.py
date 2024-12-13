"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5642

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_TorqueConverterLockupRule")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_TorqueConverterLockupRule",)


class EnumWithSelectedValue_TorqueConverterLockupRule(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_TorqueConverterLockupRule

    A specific implementation of 'EnumWithSelectedValue' for 'TorqueConverterLockupRule' types.
    """

    __qualname__ = "TorqueConverterLockupRule"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_TorqueConverterLockupRule]",
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
        cls: "Type[EnumWithSelectedValue_TorqueConverterLockupRule]",
    ) -> "_5642.TorqueConverterLockupRule":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _5642.TorqueConverterLockupRule
        """
        return _5642.TorqueConverterLockupRule

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_TorqueConverterLockupRule]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _5642.TorqueConverterLockupRule.type_()

    @property
    def selected_value(self: "Self") -> "_5642.TorqueConverterLockupRule":
        """mastapy.system_model.analyses_and_results.mbd_analyses.TorqueConverterLockupRule

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_5642.TorqueConverterLockupRule]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.TorqueConverterLockupRule]

        Note:
            This property is readonly.
        """
        return None
