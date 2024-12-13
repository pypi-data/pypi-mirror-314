"""Implementations of 'Overridable' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.dev_tools_analyses import _215

_OVERRIDABLE = python_net_import("SMT.MastaAPI.Utility.Property", "Overridable")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Overridable_RigidCouplingType")


__docformat__ = "restructuredtext en"
__all__ = ("Overridable_RigidCouplingType",)


class Overridable_RigidCouplingType(mixins.OverridableMixin, Enum):
    """Overridable_RigidCouplingType

    A specific implementation of 'Overridable' for 'RigidCouplingType' types.
    """

    __qualname__ = "RigidCouplingType"

    @classmethod
    def wrapper_type(cls: "Type[Overridable_RigidCouplingType]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _OVERRIDABLE

    @classmethod
    def wrapped_type(
        cls: "Type[Overridable_RigidCouplingType]",
    ) -> "_215.RigidCouplingType":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _215.RigidCouplingType
        """
        return _215.RigidCouplingType

    @classmethod
    def implicit_type(cls: "Type[Overridable_RigidCouplingType]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _215.RigidCouplingType.type_()

    @property
    def value(self: "Self") -> "_215.RigidCouplingType":
        """mastapy.nodal_analysis.dev_tools_analyses.RigidCouplingType

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
    def override_value(self: "Self") -> "_215.RigidCouplingType":
        """mastapy.nodal_analysis.dev_tools_analyses.RigidCouplingType

        Note:
            This property is readonly.
        """
        return None

    @property
    def calculated_value(self: "Self") -> "_215.RigidCouplingType":
        """mastapy.nodal_analysis.dev_tools_analyses.RigidCouplingType

        Note:
            This property is readonly.
        """
        return None
