"""MBDRunUpAnalysisOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
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
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7710
from mastapy._private.system_model.analyses_and_results.static_loads import _6958

_MBD_RUN_UP_ANALYSIS_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses", "MBDRunUpAnalysisOptions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5578,
        _5615,
        _5620,
    )
    from mastapy._private.utility_gui.charts import _1922

    Self = TypeVar("Self", bound="MBDRunUpAnalysisOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="MBDRunUpAnalysisOptions._Cast_MBDRunUpAnalysisOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MBDRunUpAnalysisOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MBDRunUpAnalysisOptions:
    """Special nested class for casting MBDRunUpAnalysisOptions to subclasses."""

    __parent__: "MBDRunUpAnalysisOptions"

    @property
    def abstract_analysis_options(self: "CastSelf") -> "_7710.AbstractAnalysisOptions":
        return self.__parent__._cast(_7710.AbstractAnalysisOptions)

    @property
    def mbd_run_up_analysis_options(self: "CastSelf") -> "MBDRunUpAnalysisOptions":
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
class MBDRunUpAnalysisOptions(_7710.AbstractAnalysisOptions[_6958.TimeSeriesLoadCase]):
    """MBDRunUpAnalysisOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MBD_RUN_UP_ANALYSIS_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def initial_speed_for_run_up(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InitialSpeedForRunUp")

        if temp is None:
            return 0.0

        return temp

    @initial_speed_for_run_up.setter
    @enforce_parameter_types
    def initial_speed_for_run_up(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InitialSpeedForRunUp",
            float(value) if value is not None else 0.0,
        )

    @property
    def input_velocity_processing_type(
        self: "Self",
    ) -> "_5578.InputVelocityForRunUpProcessingType":
        """mastapy.system_model.analyses_and_results.mbd_analyses.InputVelocityForRunUpProcessingType"""
        temp = pythonnet_property_get(self.wrapped, "InputVelocityProcessingType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.InputVelocityForRunUpProcessingType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.mbd_analyses._5578",
            "InputVelocityForRunUpProcessingType",
        )(value)

    @input_velocity_processing_type.setter
    @enforce_parameter_types
    def input_velocity_processing_type(
        self: "Self", value: "_5578.InputVelocityForRunUpProcessingType"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.InputVelocityForRunUpProcessingType",
        )
        pythonnet_property_set(self.wrapped, "InputVelocityProcessingType", value)

    @property
    def polynomial_order(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "PolynomialOrder")

        if temp is None:
            return 0

        return temp

    @polynomial_order.setter
    @enforce_parameter_types
    def polynomial_order(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "PolynomialOrder", int(value) if value is not None else 0
        )

    @property
    def power_load_for_run_up_torque(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "PowerLoadForRunUpTorque")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @power_load_for_run_up_torque.setter
    @enforce_parameter_types
    def power_load_for_run_up_torque(self: "Self", value: "str") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else ""
        )
        pythonnet_property_set(self.wrapped, "PowerLoadForRunUpTorque", value)

    @property
    def reference_power_load_for_run_up_speed(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "ReferencePowerLoadForRunUpSpeed")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @reference_power_load_for_run_up_speed.setter
    @enforce_parameter_types
    def reference_power_load_for_run_up_speed(self: "Self", value: "str") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else ""
        )
        pythonnet_property_set(self.wrapped, "ReferencePowerLoadForRunUpSpeed", value)

    @property
    def run_down_after(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "RunDownAfter")

        if temp is None:
            return False

        return temp

    @run_down_after.setter
    @enforce_parameter_types
    def run_down_after(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "RunDownAfter", bool(value) if value is not None else False
        )

    @property
    def run_up_driving_mode(self: "Self") -> "_5615.RunUpDrivingMode":
        """mastapy.system_model.analyses_and_results.mbd_analyses.RunUpDrivingMode"""
        temp = pythonnet_property_get(self.wrapped, "RunUpDrivingMode")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.RunUpDrivingMode",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.mbd_analyses._5615",
            "RunUpDrivingMode",
        )(value)

    @run_up_driving_mode.setter
    @enforce_parameter_types
    def run_up_driving_mode(self: "Self", value: "_5615.RunUpDrivingMode") -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.RunUpDrivingMode",
        )
        pythonnet_property_set(self.wrapped, "RunUpDrivingMode", value)

    @property
    def run_up_end_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RunUpEndSpeed")

        if temp is None:
            return 0.0

        return temp

    @run_up_end_speed.setter
    @enforce_parameter_types
    def run_up_end_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RunUpEndSpeed", float(value) if value is not None else 0.0
        )

    @property
    def run_up_speed_profile(self: "Self") -> "_1922.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RunUpSpeedProfile")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def run_up_start_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RunUpStartSpeed")

        if temp is None:
            return 0.0

        return temp

    @run_up_start_speed.setter
    @enforce_parameter_types
    def run_up_start_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RunUpStartSpeed", float(value) if value is not None else 0.0
        )

    @property
    def shape_of_initial_acceleration_period(
        self: "Self",
    ) -> "_5620.ShapeOfInitialAccelerationPeriodForRunUp":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ShapeOfInitialAccelerationPeriodForRunUp"""
        temp = pythonnet_property_get(self.wrapped, "ShapeOfInitialAccelerationPeriod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.ShapeOfInitialAccelerationPeriodForRunUp",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.mbd_analyses._5620",
            "ShapeOfInitialAccelerationPeriodForRunUp",
        )(value)

    @shape_of_initial_acceleration_period.setter
    @enforce_parameter_types
    def shape_of_initial_acceleration_period(
        self: "Self", value: "_5620.ShapeOfInitialAccelerationPeriodForRunUp"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.ShapeOfInitialAccelerationPeriodForRunUp",
        )
        pythonnet_property_set(self.wrapped, "ShapeOfInitialAccelerationPeriod", value)

    @property
    def time_to_change_direction(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TimeToChangeDirection")

        if temp is None:
            return 0.0

        return temp

    @time_to_change_direction.setter
    @enforce_parameter_types
    def time_to_change_direction(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TimeToChangeDirection",
            float(value) if value is not None else 0.0,
        )

    @property
    def time_to_keep_linear_speed_before_reaching_minimum_speed(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "TimeToKeepLinearSpeedBeforeReachingMinimumSpeed"
        )

        if temp is None:
            return 0.0

        return temp

    @time_to_keep_linear_speed_before_reaching_minimum_speed.setter
    @enforce_parameter_types
    def time_to_keep_linear_speed_before_reaching_minimum_speed(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "TimeToKeepLinearSpeedBeforeReachingMinimumSpeed",
            float(value) if value is not None else 0.0,
        )

    @property
    def time_to_reach_minimum_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TimeToReachMinimumSpeed")

        if temp is None:
            return 0.0

        return temp

    @time_to_reach_minimum_speed.setter
    @enforce_parameter_types
    def time_to_reach_minimum_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TimeToReachMinimumSpeed",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_MBDRunUpAnalysisOptions":
        """Cast to another type.

        Returns:
            _Cast_MBDRunUpAnalysisOptions
        """
        return _Cast_MBDRunUpAnalysisOptions(self)
