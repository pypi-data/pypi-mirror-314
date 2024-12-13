"""FlexiblePinAnalysisOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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
from mastapy._private.system_model.analyses_and_results.load_case_groups import _5800
from mastapy._private.system_model.analyses_and_results.static_loads import _6957

_FLEXIBLE_PIN_ANALYSIS_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.FlexiblePinAnalyses",
    "FlexiblePinAnalysisOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FlexiblePinAnalysisOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="FlexiblePinAnalysisOptions._Cast_FlexiblePinAnalysisOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FlexiblePinAnalysisOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FlexiblePinAnalysisOptions:
    """Special nested class for casting FlexiblePinAnalysisOptions to subclasses."""

    __parent__: "FlexiblePinAnalysisOptions"

    @property
    def flexible_pin_analysis_options(self: "CastSelf") -> "FlexiblePinAnalysisOptions":
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
class FlexiblePinAnalysisOptions(_0.APIBase):
    """FlexiblePinAnalysisOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FLEXIBLE_PIN_ANALYSIS_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def extreme_load_case(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_StaticLoadCase":
        """ListWithSelectedItem[mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase]"""
        temp = pythonnet_property_get(self.wrapped, "ExtremeLoadCase")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_StaticLoadCase",
        )(temp)

    @extreme_load_case.setter
    @enforce_parameter_types
    def extreme_load_case(self: "Self", value: "_6957.StaticLoadCase") -> None:
        wrapper_type = (
            list_with_selected_item.ListWithSelectedItem_StaticLoadCase.wrapper_type()
        )
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "ExtremeLoadCase", value)

    @property
    def extreme_load_case_for_stop_start(self: "Self") -> "_6957.StaticLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase"""
        temp = pythonnet_property_get(self.wrapped, "ExtremeLoadCaseForStopStart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @extreme_load_case_for_stop_start.setter
    @enforce_parameter_types
    def extreme_load_case_for_stop_start(
        self: "Self", value: "_6957.StaticLoadCase"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "ExtremeLoadCaseForStopStart", value.wrapped
        )

    @property
    def include_flexible_bearing_races(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeFlexibleBearingRaces")

        if temp is None:
            return False

        return temp

    @include_flexible_bearing_races.setter
    @enforce_parameter_types
    def include_flexible_bearing_races(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeFlexibleBearingRaces",
            bool(value) if value is not None else False,
        )

    @property
    def ldd(self: "Self") -> "list_with_selected_item.ListWithSelectedItem_DutyCycle":
        """ListWithSelectedItem[mastapy.system_model.analyses_and_results.load_case_groups.DutyCycle]"""
        temp = pythonnet_property_get(self.wrapped, "LDD")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_DutyCycle",
        )(temp)

    @ldd.setter
    @enforce_parameter_types
    def ldd(self: "Self", value: "_5800.DutyCycle") -> None:
        wrapper_type = (
            list_with_selected_item.ListWithSelectedItem_DutyCycle.wrapper_type()
        )
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_DutyCycle.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "LDD", value)

    @property
    def nominal_load_case(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_StaticLoadCase":
        """ListWithSelectedItem[mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase]"""
        temp = pythonnet_property_get(self.wrapped, "NominalLoadCase")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_StaticLoadCase",
        )(temp)

    @nominal_load_case.setter
    @enforce_parameter_types
    def nominal_load_case(self: "Self", value: "_6957.StaticLoadCase") -> None:
        wrapper_type = (
            list_with_selected_item.ListWithSelectedItem_StaticLoadCase.wrapper_type()
        )
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "NominalLoadCase", value)

    @property
    def nominal_load_case_for_stop_start(self: "Self") -> "_6957.StaticLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase"""
        temp = pythonnet_property_get(self.wrapped, "NominalLoadCaseForStopStart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @nominal_load_case_for_stop_start.setter
    @enforce_parameter_types
    def nominal_load_case_for_stop_start(
        self: "Self", value: "_6957.StaticLoadCase"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "NominalLoadCaseForStopStart", value.wrapped
        )

    @property
    def cast_to(self: "Self") -> "_Cast_FlexiblePinAnalysisOptions":
        """Cast to another type.

        Returns:
            _Cast_FlexiblePinAnalysisOptions
        """
        return _Cast_FlexiblePinAnalysisOptions(self)
