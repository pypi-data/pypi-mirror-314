"""DatumMeasurement"""

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
from mastapy._private.system_model.connections_and_sockets import _2328

_DATUM_MEASUREMENT = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "DatumMeasurement"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DatumMeasurement")
    CastSelf = TypeVar("CastSelf", bound="DatumMeasurement._Cast_DatumMeasurement")


__docformat__ = "restructuredtext en"
__all__ = ("DatumMeasurement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DatumMeasurement:
    """Special nested class for casting DatumMeasurement to subclasses."""

    __parent__: "DatumMeasurement"

    @property
    def component_measurer(self: "CastSelf") -> "_2328.ComponentMeasurer":
        return self.__parent__._cast(_2328.ComponentMeasurer)

    @property
    def datum_measurement(self: "CastSelf") -> "DatumMeasurement":
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
class DatumMeasurement(_2328.ComponentMeasurer):
    """DatumMeasurement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DATUM_MEASUREMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def measuring_position(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "MeasuringPosition")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @measuring_position.setter
    @enforce_parameter_types
    def measuring_position(self: "Self", value: "str") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else ""
        )
        pythonnet_property_set(self.wrapped, "MeasuringPosition", value)

    @property
    def cast_to(self: "Self") -> "_Cast_DatumMeasurement":
        """Cast to another type.

        Returns:
            _Cast_DatumMeasurement
        """
        return _Cast_DatumMeasurement(self)
