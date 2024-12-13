"""Implementations of 'Overridable' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears import _331

_OVERRIDABLE = python_net_import("SMT.MastaAPI.Utility.Property", "Overridable")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Overridable_CoefficientOfFrictionCalculationMethod")


__docformat__ = "restructuredtext en"
__all__ = ("Overridable_CoefficientOfFrictionCalculationMethod",)


class Overridable_CoefficientOfFrictionCalculationMethod(mixins.OverridableMixin, Enum):
    """Overridable_CoefficientOfFrictionCalculationMethod

    A specific implementation of 'Overridable' for 'CoefficientOfFrictionCalculationMethod' types.
    """

    __qualname__ = "CoefficientOfFrictionCalculationMethod"

    @classmethod
    def wrapper_type(
        cls: "Type[Overridable_CoefficientOfFrictionCalculationMethod]",
    ) -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _OVERRIDABLE

    @classmethod
    def wrapped_type(
        cls: "Type[Overridable_CoefficientOfFrictionCalculationMethod]",
    ) -> "_331.CoefficientOfFrictionCalculationMethod":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _331.CoefficientOfFrictionCalculationMethod
        """
        return _331.CoefficientOfFrictionCalculationMethod

    @classmethod
    def implicit_type(
        cls: "Type[Overridable_CoefficientOfFrictionCalculationMethod]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _331.CoefficientOfFrictionCalculationMethod.type_()

    @property
    def value(self: "Self") -> "_331.CoefficientOfFrictionCalculationMethod":
        """mastapy.gears.CoefficientOfFrictionCalculationMethod

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
    def override_value(self: "Self") -> "_331.CoefficientOfFrictionCalculationMethod":
        """mastapy.gears.CoefficientOfFrictionCalculationMethod

        Note:
            This property is readonly.
        """
        return None

    @property
    def calculated_value(self: "Self") -> "_331.CoefficientOfFrictionCalculationMethod":
        """mastapy.gears.CoefficientOfFrictionCalculationMethod

        Note:
            This property is readonly.
        """
        return None
