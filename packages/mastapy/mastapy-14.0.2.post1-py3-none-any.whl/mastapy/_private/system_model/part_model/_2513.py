"""GuideDxfModel"""

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
from mastapy._private.system_model.part_model import _2502
from mastapy._private.utility.units_and_measurements import _1662

_GUIDE_DXF_MODEL = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "GuideDxfModel"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2260
    from mastapy._private.system_model.part_model import _2528

    Self = TypeVar("Self", bound="GuideDxfModel")
    CastSelf = TypeVar("CastSelf", bound="GuideDxfModel._Cast_GuideDxfModel")


__docformat__ = "restructuredtext en"
__all__ = ("GuideDxfModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GuideDxfModel:
    """Special nested class for casting GuideDxfModel to subclasses."""

    __parent__: "GuideDxfModel"

    @property
    def component(self: "CastSelf") -> "_2502.Component":
        return self.__parent__._cast(_2502.Component)

    @property
    def part(self: "CastSelf") -> "_2528.Part":
        from mastapy._private.system_model.part_model import _2528

        return self.__parent__._cast(_2528.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2260.DesignEntity":
        from mastapy._private.system_model import _2260

        return self.__parent__._cast(_2260.DesignEntity)

    @property
    def guide_dxf_model(self: "CastSelf") -> "GuideDxfModel":
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
class GuideDxfModel(_2502.Component):
    """GuideDxfModel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GUIDE_DXF_MODEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def length_unit(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_Unit":
        """ListWithSelectedItem[mastapy.utility.units_and_measurements.Unit]"""
        temp = pythonnet_property_get(self.wrapped, "LengthUnit")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Unit",
        )(temp)

    @length_unit.setter
    @enforce_parameter_types
    def length_unit(self: "Self", value: "_1662.Unit") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.wrapper_type()
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "LengthUnit", value)

    @property
    def memory_usage(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MemoryUsage")

        if temp is None:
            return 0

        return temp

    @property
    def scale_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ScaleFactor")

        if temp is None:
            return 0.0

        return temp

    @scale_factor.setter
    @enforce_parameter_types
    def scale_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ScaleFactor", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GuideDxfModel":
        """Cast to another type.

        Returns:
            _Cast_GuideDxfModel
        """
        return _Cast_GuideDxfModel(self)
