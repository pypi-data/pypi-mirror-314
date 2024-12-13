"""MicroGeometryViewingOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
    constructor,
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
from mastapy._private.gears.ltca import _852
from mastapy._private.nodal_analysis import _90

_MICRO_GEOMETRY_VIEWING_OPTIONS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "MicroGeometryViewingOptions",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1146

    Self = TypeVar("Self", bound="MicroGeometryViewingOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MicroGeometryViewingOptions._Cast_MicroGeometryViewingOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MicroGeometryViewingOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MicroGeometryViewingOptions:
    """Special nested class for casting MicroGeometryViewingOptions to subclasses."""

    __parent__: "MicroGeometryViewingOptions"

    @property
    def micro_geometry_viewing_options(
        self: "CastSelf",
    ) -> "MicroGeometryViewingOptions":
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
class MicroGeometryViewingOptions(_0.APIBase):
    """MicroGeometryViewingOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MICRO_GEOMETRY_VIEWING_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def contact_results(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ContactResultType":
        """EnumWithSelectedValue[mastapy.gears.ltca.ContactResultType]"""
        temp = pythonnet_property_get(self.wrapped, "ContactResults")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ContactResultType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @contact_results.setter
    @enforce_parameter_types
    def contact_results(self: "Self", value: "_852.ContactResultType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ContactResultType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ContactResults", value)

    @property
    def gear_option(self: "Self") -> "_1146.DrawDefiningGearOrBoth":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.DrawDefiningGearOrBoth"""
        temp = pythonnet_property_get(self.wrapped, "GearOption")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry.DrawDefiningGearOrBoth",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1146",
            "DrawDefiningGearOrBoth",
        )(value)

    @gear_option.setter
    @enforce_parameter_types
    def gear_option(self: "Self", value: "_1146.DrawDefiningGearOrBoth") -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry.DrawDefiningGearOrBoth",
        )
        pythonnet_property_set(self.wrapped, "GearOption", value)

    @property
    def root_stress_results_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_StressResultsType":
        """EnumWithSelectedValue[mastapy.nodal_analysis.StressResultsType]"""
        temp = pythonnet_property_get(self.wrapped, "RootStressResultsType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_StressResultsType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @root_stress_results_type.setter
    @enforce_parameter_types
    def root_stress_results_type(self: "Self", value: "_90.StressResultsType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_StressResultsType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "RootStressResultsType", value)

    @property
    def show_contact_chart(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowContactChart")

        if temp is None:
            return False

        return temp

    @show_contact_chart.setter
    @enforce_parameter_types
    def show_contact_chart(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowContactChart",
            bool(value) if value is not None else False,
        )

    @property
    def show_contact_points(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowContactPoints")

        if temp is None:
            return False

        return temp

    @show_contact_points.setter
    @enforce_parameter_types
    def show_contact_points(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowContactPoints",
            bool(value) if value is not None else False,
        )

    @property
    def show_force_arrows(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowForceArrows")

        if temp is None:
            return False

        return temp

    @show_force_arrows.setter
    @enforce_parameter_types
    def show_force_arrows(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowForceArrows", bool(value) if value is not None else False
        )

    @property
    def show_root_stress_chart(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowRootStressChart")

        if temp is None:
            return False

        return temp

    @show_root_stress_chart.setter
    @enforce_parameter_types
    def show_root_stress_chart(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowRootStressChart",
            bool(value) if value is not None else False,
        )

    @property
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputDefaultReportTo", file_path if file_path else ""
        )

    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportTo", file_path if file_path else ""
        )

    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportAsTextTo", file_path if file_path else ""
        )

    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_MicroGeometryViewingOptions":
        """Cast to another type.

        Returns:
            _Cast_MicroGeometryViewingOptions
        """
        return _Cast_MicroGeometryViewingOptions(self)
