"""Implementations of 'ListWithSelectedItem' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, mixins
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model.acoustics import _2687

_ARRAY = python_net_import("System", "Array")
_LIST_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Property", "ListWithSelectedItem"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="ListWithSelectedItem_AcousticAnalysisSetup")


__docformat__ = "restructuredtext en"
__all__ = ("ListWithSelectedItem_AcousticAnalysisSetup",)


class ListWithSelectedItem_AcousticAnalysisSetup(
    _2687.AcousticAnalysisSetup, mixins.ListWithSelectedItemMixin
):
    """ListWithSelectedItem_AcousticAnalysisSetup

    A specific implementation of 'ListWithSelectedItem' for 'AcousticAnalysisSetup' types.
    """

    __qualname__ = "AcousticAnalysisSetup"

    def __init__(self: "Self", instance_to_wrap: "Any") -> None:
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls: "Type[ListWithSelectedItem_AcousticAnalysisSetup]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls: "Type[ListWithSelectedItem_AcousticAnalysisSetup]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2687.AcousticAnalysisSetup.TYPE

    @property
    def selected_value(self: "Self") -> "_2687.AcousticAnalysisSetup":
        """mastapy.system_model.part_model.acoustics.AcousticAnalysisSetup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.enclosing, "SelectedValue")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def available_values(self: "Self") -> "List[_2687.AcousticAnalysisSetup]":
        """List[mastapy.system_model.part_model.acoustics.AcousticAnalysisSetup]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.enclosing, "AvailableValues")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value
