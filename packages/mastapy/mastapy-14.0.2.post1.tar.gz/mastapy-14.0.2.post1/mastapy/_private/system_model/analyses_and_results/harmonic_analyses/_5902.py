"""HarmonicAnalysisOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import list_with_selected_item, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model.acoustics import _2687

_HARMONIC_ANALYSIS_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "HarmonicAnalysisOptions",
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7227,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5888,
        _5937,
        _5949,
        _5956,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results import (
        _5985,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4776

    Self = TypeVar("Self", bound="HarmonicAnalysisOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="HarmonicAnalysisOptions._Cast_HarmonicAnalysisOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicAnalysisOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicAnalysisOptions:
    """Special nested class for casting HarmonicAnalysisOptions to subclasses."""

    __parent__: "HarmonicAnalysisOptions"

    @property
    def harmonic_analysis_options_for_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7227.HarmonicAnalysisOptionsForAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7227,
        )

        return self.__parent__._cast(
            _7227.HarmonicAnalysisOptionsForAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def harmonic_analysis_options(self: "CastSelf") -> "HarmonicAnalysisOptions":
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
class HarmonicAnalysisOptions(_0.APIBase):
    """HarmonicAnalysisOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HARMONIC_ANALYSIS_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def acoustic_analysis_setup(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_AcousticAnalysisSetup":
        """ListWithSelectedItem[mastapy.system_model.part_model.acoustics.AcousticAnalysisSetup]"""
        temp = pythonnet_property_get(self.wrapped, "AcousticAnalysisSetup")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_AcousticAnalysisSetup",
        )(temp)

    @acoustic_analysis_setup.setter
    @enforce_parameter_types
    def acoustic_analysis_setup(
        self: "Self", value: "_2687.AcousticAnalysisSetup"
    ) -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_AcousticAnalysisSetup.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_AcousticAnalysisSetup.implicit_type()
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "AcousticAnalysisSetup", value)

    @property
    def amplitude_cut_off_for_linear_te(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AmplitudeCutOffForLinearTE")

        if temp is None:
            return 0.0

        return temp

    @amplitude_cut_off_for_linear_te.setter
    @enforce_parameter_types
    def amplitude_cut_off_for_linear_te(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AmplitudeCutOffForLinearTE",
            float(value) if value is not None else 0.0,
        )

    @property
    def amplitude_cut_off_for_misalignment_excitation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "AmplitudeCutOffForMisalignmentExcitation"
        )

        if temp is None:
            return 0.0

        return temp

    @amplitude_cut_off_for_misalignment_excitation.setter
    @enforce_parameter_types
    def amplitude_cut_off_for_misalignment_excitation(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "AmplitudeCutOffForMisalignmentExcitation",
            float(value) if value is not None else 0.0,
        )

    @property
    def calculate_uncoupled_modes_during_analysis(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "CalculateUncoupledModesDuringAnalysis"
        )

        if temp is None:
            return False

        return temp

    @calculate_uncoupled_modes_during_analysis.setter
    @enforce_parameter_types
    def calculate_uncoupled_modes_during_analysis(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CalculateUncoupledModesDuringAnalysis",
            bool(value) if value is not None else False,
        )

    @property
    def crop_to_speed_range_for_export_and_reports(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "CropToSpeedRangeForExportAndReports"
        )

        if temp is None:
            return False

        return temp

    @crop_to_speed_range_for_export_and_reports.setter
    @enforce_parameter_types
    def crop_to_speed_range_for_export_and_reports(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CropToSpeedRangeForExportAndReports",
            bool(value) if value is not None else False,
        )

    @property
    def include_truncation_correction(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeTruncationCorrection")

        if temp is None:
            return False

        return temp

    @include_truncation_correction.setter
    @enforce_parameter_types
    def include_truncation_correction(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeTruncationCorrection",
            bool(value) if value is not None else False,
        )

    @property
    def modal_damping_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ModalDampingFactor")

        if temp is None:
            return 0.0

        return temp

    @modal_damping_factor.setter
    @enforce_parameter_types
    def modal_damping_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ModalDampingFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def number_of_harmonics(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfHarmonics")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_harmonics.setter
    @enforce_parameter_types
    def number_of_harmonics(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NumberOfHarmonics", value)

    @property
    def penalty_mass_for_enforced_te(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PenaltyMassForEnforcedTE")

        if temp is None:
            return 0.0

        return temp

    @penalty_mass_for_enforced_te.setter
    @enforce_parameter_types
    def penalty_mass_for_enforced_te(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PenaltyMassForEnforcedTE",
            float(value) if value is not None else 0.0,
        )

    @property
    def penalty_stiffness_for_enforced_te(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PenaltyStiffnessForEnforcedTE")

        if temp is None:
            return 0.0

        return temp

    @penalty_stiffness_for_enforced_te.setter
    @enforce_parameter_types
    def penalty_stiffness_for_enforced_te(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PenaltyStiffnessForEnforcedTE",
            float(value) if value is not None else 0.0,
        )

    @property
    def rayleigh_damping_alpha(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RayleighDampingAlpha")

        if temp is None:
            return 0.0

        return temp

    @rayleigh_damping_alpha.setter
    @enforce_parameter_types
    def rayleigh_damping_alpha(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RayleighDampingAlpha",
            float(value) if value is not None else 0.0,
        )

    @property
    def rayleigh_damping_beta(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RayleighDampingBeta")

        if temp is None:
            return 0.0

        return temp

    @rayleigh_damping_beta.setter
    @enforce_parameter_types
    def rayleigh_damping_beta(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RayleighDampingBeta",
            float(value) if value is not None else 0.0,
        )

    @property
    def response_cache_level(self: "Self") -> "_5937.ResponseCacheLevel":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.ResponseCacheLevel"""
        temp = pythonnet_property_get(self.wrapped, "ResponseCacheLevel")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ResponseCacheLevel",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.harmonic_analyses._5937",
            "ResponseCacheLevel",
        )(value)

    @response_cache_level.setter
    @enforce_parameter_types
    def response_cache_level(self: "Self", value: "_5937.ResponseCacheLevel") -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ResponseCacheLevel",
        )
        pythonnet_property_set(self.wrapped, "ResponseCacheLevel", value)

    @property
    def specify_per_mode_damping_factors(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SpecifyPerModeDampingFactors")

        if temp is None:
            return False

        return temp

    @specify_per_mode_damping_factors.setter
    @enforce_parameter_types
    def specify_per_mode_damping_factors(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifyPerModeDampingFactors",
            bool(value) if value is not None else False,
        )

    @property
    def update_dynamic_response_chart_on_change_of_settings(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UpdateDynamicResponseChartOnChangeOfSettings"
        )

        if temp is None:
            return False

        return temp

    @update_dynamic_response_chart_on_change_of_settings.setter
    @enforce_parameter_types
    def update_dynamic_response_chart_on_change_of_settings(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UpdateDynamicResponseChartOnChangeOfSettings",
            bool(value) if value is not None else False,
        )

    @property
    def excitation_selection(self: "Self") -> "_5985.ExcitationSourceSelectionGroup":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.results.ExcitationSourceSelectionGroup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExcitationSelection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def frequency_options(
        self: "Self",
    ) -> "_5888.FrequencyOptionsForHarmonicAnalysisResults":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.FrequencyOptionsForHarmonicAnalysisResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrequencyOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def modal_analysis_options(self: "Self") -> "_4776.ModalAnalysisOptions":
        """mastapy.system_model.analyses_and_results.modal_analyses.ModalAnalysisOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModalAnalysisOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def reference_speed_options(
        self: "Self",
    ) -> "_5949.SpeedOptionsForHarmonicAnalysisResults":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.SpeedOptionsForHarmonicAnalysisResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceSpeedOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def stiffness_options(self: "Self") -> "_5956.StiffnessOptionsForHarmonicAnalysis":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.StiffnessOptionsForHarmonicAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def per_mode_damping_factors(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PerModeDampingFactors")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

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
    def set_per_mode_damping_factor(
        self: "Self", mode: "int", damping: "float"
    ) -> None:
        """Method does not return.

        Args:
            mode (int)
            damping (float)
        """
        mode = int(mode)
        damping = float(damping)
        pythonnet_method_call(
            self.wrapped,
            "SetPerModeDampingFactor",
            mode if mode else 0,
            damping if damping else 0.0,
        )

    @enforce_parameter_types
    def set_per_mode_damping_factors(
        self: "Self", damping_values: "List[float]"
    ) -> None:
        """Method does not return.

        Args:
            damping_values (List[float])
        """
        damping_values = conversion.mp_to_pn_list_float(damping_values)
        pythonnet_method_call(self.wrapped, "SetPerModeDampingFactors", damping_values)

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
    def cast_to(self: "Self") -> "_Cast_HarmonicAnalysisOptions":
        """Cast to another type.

        Returns:
            _Cast_HarmonicAnalysisOptions
        """
        return _Cast_HarmonicAnalysisOptions(self)
