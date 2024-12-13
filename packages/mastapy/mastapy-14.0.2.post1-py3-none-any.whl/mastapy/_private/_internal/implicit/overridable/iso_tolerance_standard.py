"""Implementations of 'Overridable' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears import _346

_OVERRIDABLE = python_net_import("SMT.MastaAPI.Utility.Property", "Overridable")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Overridable_ISOToleranceStandard")


__docformat__ = "restructuredtext en"
__all__ = ("Overridable_ISOToleranceStandard",)


class Overridable_ISOToleranceStandard(mixins.OverridableMixin, Enum):
    """Overridable_ISOToleranceStandard

    A specific implementation of 'Overridable' for 'ISOToleranceStandard' types.
    """

    __qualname__ = "ISOToleranceStandard"

    @classmethod
    def wrapper_type(cls: "Type[Overridable_ISOToleranceStandard]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _OVERRIDABLE

    @classmethod
    def wrapped_type(
        cls: "Type[Overridable_ISOToleranceStandard]",
    ) -> "_346.ISOToleranceStandard":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _346.ISOToleranceStandard
        """
        return _346.ISOToleranceStandard

    @classmethod
    def implicit_type(cls: "Type[Overridable_ISOToleranceStandard]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _346.ISOToleranceStandard.type_()

    @property
    def value(self: "Self") -> "_346.ISOToleranceStandard":
        """mastapy.gears.ISOToleranceStandard

        Note:
            This property is readonly.
        """
        return None

    @property
    def overridden(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        return None

    @property
    def override_value(self: "Self") -> "_346.ISOToleranceStandard":
        """mastapy.gears.ISOToleranceStandard

        Note:
            This property is readonly.
        """
        return None

    @property
    def calculated_value(self: "Self") -> "_346.ISOToleranceStandard":
        """mastapy.gears.ISOToleranceStandard

        Note:
            This property is readonly.
        """
        return None
