"""ChartInfoBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from PIL.Image import Image

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

_CHART_INFO_BASE = python_net_import(
    "SMT.MastaAPI.Gears.GearSetParetoOptimiser", "ChartInfoBase"
)

if TYPE_CHECKING:
    from typing import Any, List, Type

    from mastapy._private.gears.analysis import _1257
    from mastapy._private.gears.gear_set_pareto_optimiser import (
        _927,
        _931,
        _939,
        _943,
        _958,
    )
    from mastapy._private.math_utility.optimisation import _1601
    from mastapy._private.utility.reporting_property_framework import _1842

    Self = TypeVar("Self", bound="ChartInfoBase")
    CastSelf = TypeVar("CastSelf", bound="ChartInfoBase._Cast_ChartInfoBase")

TAnalysis = TypeVar("TAnalysis", bound="_1257.AbstractGearSetAnalysis")
TCandidate = TypeVar("TCandidate")

__docformat__ = "restructuredtext en"
__all__ = ("ChartInfoBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ChartInfoBase:
    """Special nested class for casting ChartInfoBase to subclasses."""

    __parent__: "ChartInfoBase"

    @property
    def micro_geometry_design_space_search_chart_information(
        self: "CastSelf",
    ) -> "_943.MicroGeometryDesignSpaceSearchChartInformation":
        from mastapy._private.gears.gear_set_pareto_optimiser import _943

        return self.__parent__._cast(
            _943.MicroGeometryDesignSpaceSearchChartInformation
        )

    @property
    def pareto_optimiser_chart_information(
        self: "CastSelf",
    ) -> "_958.ParetoOptimiserChartInformation":
        from mastapy._private.gears.gear_set_pareto_optimiser import _958

        return self.__parent__._cast(_958.ParetoOptimiserChartInformation)

    @property
    def chart_info_base(self: "CastSelf") -> "ChartInfoBase":
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
class ChartInfoBase(_0.APIBase, Generic[TAnalysis, TCandidate]):
    """ChartInfoBase

    This is a mastapy class.

    Generic Types:
        TAnalysis
        TCandidate
    """

    TYPE: ClassVar["Type"] = _CHART_INFO_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def chart_name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "ChartName")

        if temp is None:
            return ""

        return temp

    @chart_name.setter
    @enforce_parameter_types
    def chart_name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "ChartName", str(value) if value is not None else ""
        )

    @property
    def chart_type(self: "Self") -> "_1842.CustomChartType":
        """mastapy.utility.reporting_property_framework.CustomChartType

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ChartType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.ReportingPropertyFramework.CustomChartType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility.reporting_property_framework._1842",
            "CustomChartType",
        )(value)

    @property
    def result_chart_bar_and_line(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultChartBarAndLine")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def result_chart_scatter(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultChartScatter")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def select_chart_type(
        self: "Self",
    ) -> "_1601.ParetoOptimisationStrategyChartInformation.ScatterOrBarChart":
        """mastapy.math_utility.optimisation.ParetoOptimisationStrategyChartInformation.ScatterOrBarChart"""
        temp = pythonnet_property_get(self.wrapped, "SelectChartType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.MathUtility.Optimisation.ParetoOptimisationStrategyChartInformation+ScatterOrBarChart",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility.optimisation.ParetoOptimisationStrategyChartInformation._1601",
            "ParetoOptimisationStrategyChartInformation",
        )(value)

    @select_chart_type.setter
    @enforce_parameter_types
    def select_chart_type(
        self: "Self",
        value: "_1601.ParetoOptimisationStrategyChartInformation.ScatterOrBarChart",
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.MathUtility.Optimisation.ParetoOptimisationStrategyChartInformation+ScatterOrBarChart",
        )
        pythonnet_property_set(self.wrapped, "SelectChartType", value)

    @property
    def selected_candidate_design(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SelectedCandidateDesign")

        if temp is None:
            return 0

        return temp

    @property
    def optimiser(self: "Self") -> "_931.DesignSpaceSearchBase[TAnalysis, TCandidate]":
        """mastapy.gears.gear_set_pareto_optimiser.DesignSpaceSearchBase[TAnalysis, TCandidate]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Optimiser")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[TAnalysis, TCandidate](temp)

    @property
    def bars(self: "Self") -> "List[_927.BarForPareto[TAnalysis, TCandidate]]":
        """List[mastapy.gears.gear_set_pareto_optimiser.BarForPareto[TAnalysis, TCandidate]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Bars")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def input_sliders(
        self: "Self",
    ) -> "List[_939.InputSliderForPareto[TAnalysis, TCandidate]]":
        """List[mastapy.gears.gear_set_pareto_optimiser.InputSliderForPareto[TAnalysis, TCandidate]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InputSliders")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

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

    def add_bar(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddBar")

    def add_selected_design(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddSelectedDesign")

    def add_selected_designs(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddSelectedDesigns")

    def remove_chart(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "RemoveChart")

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
    def cast_to(self: "Self") -> "_Cast_ChartInfoBase":
        """Cast to another type.

        Returns:
            _Cast_ChartInfoBase
        """
        return _Cast_ChartInfoBase(self)
