"""Implementations of 'Overridable' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.math_utility.hertzian_contact import _1623

_OVERRIDABLE = python_net_import("SMT.MastaAPI.Utility.Property", "Overridable")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Overridable_ContactDampingModel")


__docformat__ = "restructuredtext en"
__all__ = ("Overridable_ContactDampingModel",)


class Overridable_ContactDampingModel(mixins.OverridableMixin, Enum):
    """Overridable_ContactDampingModel

    A specific implementation of 'Overridable' for 'ContactDampingModel' types.
    """

    __qualname__ = "ContactDampingModel"

    @classmethod
    def wrapper_type(cls: "Type[Overridable_ContactDampingModel]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _OVERRIDABLE

    @classmethod
    def wrapped_type(
        cls: "Type[Overridable_ContactDampingModel]",
    ) -> "_1623.ContactDampingModel":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1623.ContactDampingModel
        """
        return _1623.ContactDampingModel

    @classmethod
    def implicit_type(cls: "Type[Overridable_ContactDampingModel]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1623.ContactDampingModel.type_()

    @property
    def value(self: "Self") -> "_1623.ContactDampingModel":
        """mastapy.math_utility.hertzian_contact.ContactDampingModel

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
    def override_value(self: "Self") -> "_1623.ContactDampingModel":
        """mastapy.math_utility.hertzian_contact.ContactDampingModel

        Note:
            This property is readonly.
        """
        return None

    @property
    def calculated_value(self: "Self") -> "_1623.ContactDampingModel":
        """mastapy.math_utility.hertzian_contact.ContactDampingModel

        Note:
            This property is readonly.
        """
        return None
