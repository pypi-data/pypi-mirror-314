"""AdvancedTimeSteppingAnalysisForModulationModeViewOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model.gears import _2593

_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION_MODE_VIEW_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.Drawing.Options",
    "AdvancedTimeSteppingAnalysisForModulationModeViewOptions",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7165,
        _7166,
    )

    Self = TypeVar(
        "Self", bound="AdvancedTimeSteppingAnalysisForModulationModeViewOptions"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="AdvancedTimeSteppingAnalysisForModulationModeViewOptions._Cast_AdvancedTimeSteppingAnalysisForModulationModeViewOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AdvancedTimeSteppingAnalysisForModulationModeViewOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AdvancedTimeSteppingAnalysisForModulationModeViewOptions:
    """Special nested class for casting AdvancedTimeSteppingAnalysisForModulationModeViewOptions to subclasses."""

    __parent__: "AdvancedTimeSteppingAnalysisForModulationModeViewOptions"

    @property
    def advanced_time_stepping_analysis_for_modulation_mode_view_options(
        self: "CastSelf",
    ) -> "AdvancedTimeSteppingAnalysisForModulationModeViewOptions":
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
class AdvancedTimeSteppingAnalysisForModulationModeViewOptions(_0.APIBase):
    """AdvancedTimeSteppingAnalysisForModulationModeViewOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION_MODE_VIEW_OPTIONS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def excitations_type(self: "Self") -> "_7165.AtsamExcitationsOrOthers":
        """mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.AtsamExcitationsOrOthers"""
        temp = pythonnet_property_get(self.wrapped, "ExcitationsType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.AtsamExcitationsOrOthers",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation._7165",
            "AtsamExcitationsOrOthers",
        )(value)

    @excitations_type.setter
    @enforce_parameter_types
    def excitations_type(self: "Self", value: "_7165.AtsamExcitationsOrOthers") -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.AtsamExcitationsOrOthers",
        )
        pythonnet_property_set(self.wrapped, "ExcitationsType", value)

    @property
    def gear_set(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_GearSet":
        """ListWithSelectedItem[mastapy.system_model.part_model.gears.GearSet]"""
        temp = pythonnet_property_get(self.wrapped, "GearSet")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_GearSet",
        )(temp)

    @gear_set.setter
    @enforce_parameter_types
    def gear_set(self: "Self", value: "_2593.GearSet") -> None:
        wrapper_type = (
            list_with_selected_item.ListWithSelectedItem_GearSet.wrapper_type()
        )
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_GearSet.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "GearSet", value)

    @property
    def large_time_step(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "LargeTimeStep")

        if temp is None:
            return 0

        return temp

    @large_time_step.setter
    @enforce_parameter_types
    def large_time_step(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "LargeTimeStep", int(value) if value is not None else 0
        )

    @property
    def mode_view_options(self: "Self") -> "_7166.AtsamNaturalFrequencyViewOption":
        """mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.AtsamNaturalFrequencyViewOption"""
        temp = pythonnet_property_get(self.wrapped, "ModeViewOptions")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.AtsamNaturalFrequencyViewOption",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation._7166",
            "AtsamNaturalFrequencyViewOption",
        )(value)

    @mode_view_options.setter
    @enforce_parameter_types
    def mode_view_options(
        self: "Self", value: "_7166.AtsamNaturalFrequencyViewOption"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.AtsamNaturalFrequencyViewOption",
        )
        pythonnet_property_set(self.wrapped, "ModeViewOptions", value)

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_AdvancedTimeSteppingAnalysisForModulationModeViewOptions":
        """Cast to another type.

        Returns:
            _Cast_AdvancedTimeSteppingAnalysisForModulationModeViewOptions
        """
        return _Cast_AdvancedTimeSteppingAnalysisForModulationModeViewOptions(self)
