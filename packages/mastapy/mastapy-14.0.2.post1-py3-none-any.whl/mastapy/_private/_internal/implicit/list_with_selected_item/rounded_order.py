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
from mastapy._private.math_utility import _1579

_ARRAY = python_net_import("System", "Array")
_LIST_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Property", "ListWithSelectedItem"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="ListWithSelectedItem_RoundedOrder")


__docformat__ = "restructuredtext en"
__all__ = ("ListWithSelectedItem_RoundedOrder",)


class ListWithSelectedItem_RoundedOrder(
    _1579.RoundedOrder, mixins.ListWithSelectedItemMixin
):
    """ListWithSelectedItem_RoundedOrder

    A specific implementation of 'ListWithSelectedItem' for 'RoundedOrder' types.
    """

    __qualname__ = "RoundedOrder"

    def __init__(self: "Self", instance_to_wrap: "Any") -> None:
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls: "Type[ListWithSelectedItem_RoundedOrder]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls: "Type[ListWithSelectedItem_RoundedOrder]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1579.RoundedOrder.TYPE

    @property
    def selected_value(self: "Self") -> "_1579.RoundedOrder":
        """mastapy.math_utility.RoundedOrder

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.enclosing, "SelectedValue")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def available_values(self: "Self") -> "List[_1579.RoundedOrder]":
        """List[mastapy.math_utility.RoundedOrder]

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
