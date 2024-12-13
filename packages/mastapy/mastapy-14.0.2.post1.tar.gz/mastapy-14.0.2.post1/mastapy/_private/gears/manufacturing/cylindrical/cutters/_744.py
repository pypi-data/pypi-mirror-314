"""MutableCommon"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.manufacturing.cylindrical import _634
from mastapy._private.gears.manufacturing.cylindrical.cutters import _728

_MUTABLE_COMMON = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters", "MutableCommon"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.cutters import _745, _746

    Self = TypeVar("Self", bound="MutableCommon")
    CastSelf = TypeVar("CastSelf", bound="MutableCommon._Cast_MutableCommon")


__docformat__ = "restructuredtext en"
__all__ = ("MutableCommon",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MutableCommon:
    """Special nested class for casting MutableCommon to subclasses."""

    __parent__: "MutableCommon"

    @property
    def curve_in_linked_list(self: "CastSelf") -> "_728.CurveInLinkedList":
        return self.__parent__._cast(_728.CurveInLinkedList)

    @property
    def mutable_curve(self: "CastSelf") -> "_745.MutableCurve":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _745

        return self.__parent__._cast(_745.MutableCurve)

    @property
    def mutable_fillet(self: "CastSelf") -> "_746.MutableFillet":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _746

        return self.__parent__._cast(_746.MutableFillet)

    @property
    def mutable_common(self: "CastSelf") -> "MutableCommon":
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
class MutableCommon(_728.CurveInLinkedList):
    """MutableCommon

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MUTABLE_COMMON

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Height")

        if temp is None:
            return 0.0

        return temp

    @height.setter
    @enforce_parameter_types
    def height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Height", float(value) if value is not None else 0.0
        )

    @property
    def height_for_tabulation(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "HeightForTabulation")

        if temp is None:
            return ""

        return temp

    @height_for_tabulation.setter
    @enforce_parameter_types
    def height_for_tabulation(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "HeightForTabulation", str(value) if value is not None else ""
        )

    @property
    def offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Offset")

        if temp is None:
            return 0.0

        return temp

    @offset.setter
    @enforce_parameter_types
    def offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Offset", float(value) if value is not None else 0.0
        )

    @property
    def offset_for_tabulation(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OffsetForTabulation")

        if temp is None:
            return ""

        return temp

    @property
    def protuberance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Protuberance")

        if temp is None:
            return 0.0

        return temp

    @protuberance.setter
    @enforce_parameter_types
    def protuberance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Protuberance", float(value) if value is not None else 0.0
        )

    @property
    def radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Radius")

        if temp is None:
            return 0.0

        return temp

    @radius.setter
    @enforce_parameter_types
    def radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Radius", float(value) if value is not None else 0.0
        )

    @property
    def section(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_CutterFlankSections":
        """EnumWithSelectedValue[mastapy.gears.manufacturing.cylindrical.CutterFlankSections]"""
        temp = pythonnet_property_get(self.wrapped, "Section")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_CutterFlankSections.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @section.setter
    @enforce_parameter_types
    def section(self: "Self", value: "_634.CutterFlankSections") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_CutterFlankSections.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "Section", value)

    def remove(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Remove")

    def split(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Split")

    @property
    def cast_to(self: "Self") -> "_Cast_MutableCommon":
        """Cast to another type.

        Returns:
            _Cast_MutableCommon
        """
        return _Cast_MutableCommon(self)
