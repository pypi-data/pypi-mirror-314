"""StabilityAnalysisOptions"""

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
from mastapy._private.system_model.part_model import _2532

_STABILITY_ANALYSIS_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "StabilityAnalysisOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="StabilityAnalysisOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="StabilityAnalysisOptions._Cast_StabilityAnalysisOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("StabilityAnalysisOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StabilityAnalysisOptions:
    """Special nested class for casting StabilityAnalysisOptions to subclasses."""

    __parent__: "StabilityAnalysisOptions"

    @property
    def stability_analysis_options(self: "CastSelf") -> "StabilityAnalysisOptions":
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
class StabilityAnalysisOptions(_0.APIBase):
    """StabilityAnalysisOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STABILITY_ANALYSIS_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def end_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EndSpeed")

        if temp is None:
            return 0.0

        return temp

    @end_speed.setter
    @enforce_parameter_types
    def end_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "EndSpeed", float(value) if value is not None else 0.0
        )

    @property
    def include_damping_effects(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeDampingEffects")

        if temp is None:
            return False

        return temp

    @include_damping_effects.setter
    @enforce_parameter_types
    def include_damping_effects(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeDampingEffects",
            bool(value) if value is not None else False,
        )

    @property
    def include_gyroscopic_effects(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeGyroscopicEffects")

        if temp is None:
            return False

        return temp

    @include_gyroscopic_effects.setter
    @enforce_parameter_types
    def include_gyroscopic_effects(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeGyroscopicEffects",
            bool(value) if value is not None else False,
        )

    @property
    def number_of_modes(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfModes")

        if temp is None:
            return 0

        return temp

    @number_of_modes.setter
    @enforce_parameter_types
    def number_of_modes(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfModes", int(value) if value is not None else 0
        )

    @property
    def number_of_speeds(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfSpeeds")

        if temp is None:
            return 0

        return temp

    @number_of_speeds.setter
    @enforce_parameter_types
    def number_of_speeds(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfSpeeds", int(value) if value is not None else 0
        )

    @property
    def reference_power_load(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_PowerLoad":
        """ListWithSelectedItem[mastapy.system_model.part_model.PowerLoad]"""
        temp = pythonnet_property_get(self.wrapped, "ReferencePowerLoad")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_PowerLoad",
        )(temp)

    @reference_power_load.setter
    @enforce_parameter_types
    def reference_power_load(self: "Self", value: "_2532.PowerLoad") -> None:
        wrapper_type = (
            list_with_selected_item.ListWithSelectedItem_PowerLoad.wrapper_type()
        )
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_PowerLoad.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "ReferencePowerLoad", value)

    @property
    def sort_modes(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SortModes")

        if temp is None:
            return False

        return temp

    @sort_modes.setter
    @enforce_parameter_types
    def sort_modes(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "SortModes", bool(value) if value is not None else False
        )

    @property
    def start_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartSpeed")

        if temp is None:
            return 0.0

        return temp

    @start_speed.setter
    @enforce_parameter_types
    def start_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "StartSpeed", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_StabilityAnalysisOptions":
        """Cast to another type.

        Returns:
            _Cast_StabilityAnalysisOptions
        """
        return _Cast_StabilityAnalysisOptions(self)
