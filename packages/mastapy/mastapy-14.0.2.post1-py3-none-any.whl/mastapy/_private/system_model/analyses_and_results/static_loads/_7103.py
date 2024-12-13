"""RootAssemblyLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.static_loads import _6971

_ROOT_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "RootAssemblyLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.math_utility.control import _1627
    from mastapy._private.nodal_analysis.varying_input_components import _97, _98, _102
    from mastapy._private.system_model.analyses_and_results import _2740, _2742, _2746
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6957,
        _6959,
        _7018,
        _7083,
    )
    from mastapy._private.system_model.part_model import _2535

    Self = TypeVar("Self", bound="RootAssemblyLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="RootAssemblyLoadCase._Cast_RootAssemblyLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RootAssemblyLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RootAssemblyLoadCase:
    """Special nested class for casting RootAssemblyLoadCase to subclasses."""

    __parent__: "RootAssemblyLoadCase"

    @property
    def assembly_load_case(self: "CastSelf") -> "_6971.AssemblyLoadCase":
        return self.__parent__._cast(_6971.AssemblyLoadCase)

    @property
    def abstract_assembly_load_case(
        self: "CastSelf",
    ) -> "_6959.AbstractAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6959,
        )

        return self.__parent__._cast(_6959.AbstractAssemblyLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7083.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7083,
        )

        return self.__parent__._cast(_7083.PartLoadCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2746.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2746

        return self.__parent__._cast(_2746.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2742.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2742

        return self.__parent__._cast(_2742.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2740.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2740

        return self.__parent__._cast(_2740.DesignEntityAnalysis)

    @property
    def root_assembly_load_case(self: "CastSelf") -> "RootAssemblyLoadCase":
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
class RootAssemblyLoadCase(_6971.AssemblyLoadCase):
    """RootAssemblyLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROOT_ASSEMBLY_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def brake_force_gain(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BrakeForceGain")

        if temp is None:
            return 0.0

        return temp

    @brake_force_gain.setter
    @enforce_parameter_types
    def brake_force_gain(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "BrakeForceGain", float(value) if value is not None else 0.0
        )

    @property
    def max_brake_force(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaxBrakeForce")

        if temp is None:
            return 0.0

        return temp

    @max_brake_force.setter
    @enforce_parameter_types
    def max_brake_force(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MaxBrakeForce", float(value) if value is not None else 0.0
        )

    @property
    def oil_initial_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OilInitialTemperature")

        if temp is None:
            return 0.0

        return temp

    @oil_initial_temperature.setter
    @enforce_parameter_types
    def oil_initial_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OilInitialTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    def rayleigh_damping_alpha(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RayleighDampingAlpha")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @rayleigh_damping_alpha.setter
    @enforce_parameter_types
    def rayleigh_damping_alpha(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RayleighDampingAlpha", value)

    @property
    def assembly_design(self: "Self") -> "_2535.RootAssembly":
        """mastapy.system_model.part_model.RootAssembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def brake_force_input_values(self: "Self") -> "_98.ForceInputComponent":
        """mastapy.nodal_analysis.varying_input_components.ForceInputComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BrakeForceInputValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def drive_cycle_pid_control_settings(self: "Self") -> "_1627.PIDControlSettings":
        """mastapy.math_utility.control.PIDControlSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DriveCyclePIDControlSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def load_case(self: "Self") -> "_6957.StaticLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def road_incline_input_values(self: "Self") -> "_97.AngleInputComponent":
        """mastapy.nodal_analysis.varying_input_components.AngleInputComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RoadInclineInputValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def target_vehicle_speed(self: "Self") -> "_102.VelocityInputComponent":
        """mastapy.nodal_analysis.varying_input_components.VelocityInputComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TargetVehicleSpeed")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def supercharger_rotor_sets(
        self: "Self",
    ) -> "List[_7018.CylindricalGearSetLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SuperchargerRotorSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_RootAssemblyLoadCase":
        """Cast to another type.

        Returns:
            _Cast_RootAssemblyLoadCase
        """
        return _Cast_RootAssemblyLoadCase(self)
