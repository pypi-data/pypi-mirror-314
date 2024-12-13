"""CylindricalComponentConnection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.connections_and_sockets import _2327

_CYLINDRICAL_COMPONENT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "CylindricalComponentConnection"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import _2328

    Self = TypeVar("Self", bound="CylindricalComponentConnection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalComponentConnection._Cast_CylindricalComponentConnection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalComponentConnection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalComponentConnection:
    """Special nested class for casting CylindricalComponentConnection to subclasses."""

    __parent__: "CylindricalComponentConnection"

    @property
    def component_connection(self: "CastSelf") -> "_2327.ComponentConnection":
        return self.__parent__._cast(_2327.ComponentConnection)

    @property
    def component_measurer(self: "CastSelf") -> "_2328.ComponentMeasurer":
        from mastapy._private.system_model.connections_and_sockets import _2328

        return self.__parent__._cast(_2328.ComponentMeasurer)

    @property
    def cylindrical_component_connection(
        self: "CastSelf",
    ) -> "CylindricalComponentConnection":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class CylindricalComponentConnection(_2327.ComponentConnection):
    """CylindricalComponentConnection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_COMPONENT_CONNECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def measuring_position_for_component(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "MeasuringPositionForComponent")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @measuring_position_for_component.setter
    @enforce_parameter_types
    def measuring_position_for_component(self: "Self", value: "str") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else ""
        )
        pythonnet_property_set(self.wrapped, "MeasuringPositionForComponent", value)

    @property
    def measuring_position_for_connected_component(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(
            self.wrapped, "MeasuringPositionForConnectedComponent"
        )

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @measuring_position_for_connected_component.setter
    @enforce_parameter_types
    def measuring_position_for_connected_component(self: "Self", value: "str") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else ""
        )
        pythonnet_property_set(
            self.wrapped, "MeasuringPositionForConnectedComponent", value
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalComponentConnection":
        """Cast to another type.

        Returns:
            _Cast_CylindricalComponentConnection
        """
        return _Cast_CylindricalComponentConnection(self)
