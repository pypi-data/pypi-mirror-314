"""ModalContributionViewOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_MODAL_CONTRIBUTION_VIEW_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.Drawing.Options", "ModalContributionViewOptions"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility import _1539
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results import (
        _5987,
        _5988,
    )
    from mastapy._private.utility import _1639

    Self = TypeVar("Self", bound="ModalContributionViewOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ModalContributionViewOptions._Cast_ModalContributionViewOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ModalContributionViewOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ModalContributionViewOptions:
    """Special nested class for casting ModalContributionViewOptions to subclasses."""

    __parent__: "ModalContributionViewOptions"

    @property
    def modal_contribution_view_options(
        self: "CastSelf",
    ) -> "ModalContributionViewOptions":
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
class ModalContributionViewOptions(_0.APIBase):
    """ModalContributionViewOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MODAL_CONTRIBUTION_VIEW_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def filtering_frequency(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FilteringFrequency")

        if temp is None:
            return 0.0

        return temp

    @filtering_frequency.setter
    @enforce_parameter_types
    def filtering_frequency(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FilteringFrequency",
            float(value) if value is not None else 0.0,
        )

    @property
    def filtering_frequency_range(self: "Self") -> "_1539.Range":
        """mastapy.math_utility.Range"""
        temp = pythonnet_property_get(self.wrapped, "FilteringFrequencyRange")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @filtering_frequency_range.setter
    @enforce_parameter_types
    def filtering_frequency_range(self: "Self", value: "_1539.Range") -> None:
        pythonnet_property_set(self.wrapped, "FilteringFrequencyRange", value.wrapped)

    @property
    def filtering_method(self: "Self") -> "_5988.ModalContributionFilteringMethod":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.results.ModalContributionFilteringMethod"""
        temp = pythonnet_property_get(self.wrapped, "FilteringMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Results.ModalContributionFilteringMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.harmonic_analyses.results._5988",
            "ModalContributionFilteringMethod",
        )(value)

    @filtering_method.setter
    @enforce_parameter_types
    def filtering_method(
        self: "Self", value: "_5988.ModalContributionFilteringMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Results.ModalContributionFilteringMethod",
        )
        pythonnet_property_set(self.wrapped, "FilteringMethod", value)

    @property
    def frequency_range(self: "Self") -> "_1539.Range":
        """mastapy.math_utility.Range"""
        temp = pythonnet_property_get(self.wrapped, "FrequencyRange")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @frequency_range.setter
    @enforce_parameter_types
    def frequency_range(self: "Self", value: "_1539.Range") -> None:
        pythonnet_property_set(self.wrapped, "FrequencyRange", value.wrapped)

    @property
    def index(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "Index")

        if temp is None:
            return 0

        return temp

    @index.setter
    @enforce_parameter_types
    def index(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "Index", int(value) if value is not None else 0
        )

    @property
    def index_range(self: "Self") -> "_1639.IntegerRange":
        """mastapy.utility.IntegerRange"""
        temp = pythonnet_property_get(self.wrapped, "IndexRange")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @index_range.setter
    @enforce_parameter_types
    def index_range(self: "Self", value: "_1639.IntegerRange") -> None:
        pythonnet_property_set(self.wrapped, "IndexRange", value.wrapped)

    @property
    def modes_to_display(self: "Self") -> "_5987.ModalContributionDisplayMethod":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.results.ModalContributionDisplayMethod"""
        temp = pythonnet_property_get(self.wrapped, "ModesToDisplay")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Results.ModalContributionDisplayMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.harmonic_analyses.results._5987",
            "ModalContributionDisplayMethod",
        )(value)

    @modes_to_display.setter
    @enforce_parameter_types
    def modes_to_display(
        self: "Self", value: "_5987.ModalContributionDisplayMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Results.ModalContributionDisplayMethod",
        )
        pythonnet_property_set(self.wrapped, "ModesToDisplay", value)

    @property
    def percentage_of_total_response(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PercentageOfTotalResponse")

        if temp is None:
            return 0.0

        return temp

    @percentage_of_total_response.setter
    @enforce_parameter_types
    def percentage_of_total_response(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PercentageOfTotalResponse",
            float(value) if value is not None else 0.0,
        )

    @property
    def show_modal_contribution(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowModalContribution")

        if temp is None:
            return False

        return temp

    @show_modal_contribution.setter
    @enforce_parameter_types
    def show_modal_contribution(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowModalContribution",
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
    def cast_to(self: "Self") -> "_Cast_ModalContributionViewOptions":
        """Cast to another type.

        Returns:
            _Cast_ModalContributionViewOptions
        """
        return _Cast_ModalContributionViewOptions(self)
