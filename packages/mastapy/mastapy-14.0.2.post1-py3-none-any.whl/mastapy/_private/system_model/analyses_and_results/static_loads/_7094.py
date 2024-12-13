"""PowerLoadLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import (
    enum_with_selected_value,
    list_with_selected_item,
    overridable,
)
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model import _2274
from mastapy._private.system_model.analyses_and_results.static_loads import _7132, _7136
from mastapy._private.system_model.fe import _2431

_POWER_LOAD_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "PowerLoadLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.math_utility import _1585
    from mastapy._private.math_utility.control import _1627
    from mastapy._private.math_utility.measured_data import _1615
    from mastapy._private.nodal_analysis.varying_input_components import _100
    from mastapy._private.system_model import _2273, _2275
    from mastapy._private.system_model.analyses_and_results import _2740, _2742, _2746
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5649
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6990,
        _7024,
        _7079,
        _7083,
    )
    from mastapy._private.system_model.part_model import _2532

    Self = TypeVar("Self", bound="PowerLoadLoadCase")
    CastSelf = TypeVar("CastSelf", bound="PowerLoadLoadCase._Cast_PowerLoadLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("PowerLoadLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PowerLoadLoadCase:
    """Special nested class for casting PowerLoadLoadCase to subclasses."""

    __parent__: "PowerLoadLoadCase"

    @property
    def virtual_component_load_case(
        self: "CastSelf",
    ) -> "_7136.VirtualComponentLoadCase":
        return self.__parent__._cast(_7136.VirtualComponentLoadCase)

    @property
    def mountable_component_load_case(
        self: "CastSelf",
    ) -> "_7079.MountableComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7079,
        )

        return self.__parent__._cast(_7079.MountableComponentLoadCase)

    @property
    def component_load_case(self: "CastSelf") -> "_6990.ComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6990,
        )

        return self.__parent__._cast(_6990.ComponentLoadCase)

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
    def power_load_load_case(self: "CastSelf") -> "PowerLoadLoadCase":
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
class PowerLoadLoadCase(_7136.VirtualComponentLoadCase):
    """PowerLoadLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _POWER_LOAD_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def constant_resistance_coefficient(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ConstantResistanceCoefficient")

        if temp is None:
            return 0.0

        return temp

    @constant_resistance_coefficient.setter
    @enforce_parameter_types
    def constant_resistance_coefficient(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ConstantResistanceCoefficient",
            float(value) if value is not None else 0.0,
        )

    @property
    def constant_resistance_coefficient_time_profile(
        self: "Self",
    ) -> "_1585.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(
            self.wrapped, "ConstantResistanceCoefficientTimeProfile"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @constant_resistance_coefficient_time_profile.setter
    @enforce_parameter_types
    def constant_resistance_coefficient_time_profile(
        self: "Self", value: "_1585.Vector2DListAccessor"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "ConstantResistanceCoefficientTimeProfile", value.wrapped
        )

    @property
    def constant_torque(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ConstantTorque")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @constant_torque.setter
    @enforce_parameter_types
    def constant_torque(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ConstantTorque", value)

    @property
    def drag_torque_specification_method(
        self: "Self",
    ) -> "_2273.PowerLoadDragTorqueSpecificationMethod":
        """mastapy.system_model.PowerLoadDragTorqueSpecificationMethod"""
        temp = pythonnet_property_get(self.wrapped, "DragTorqueSpecificationMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.SystemModel.PowerLoadDragTorqueSpecificationMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model._2273",
            "PowerLoadDragTorqueSpecificationMethod",
        )(value)

    @drag_torque_specification_method.setter
    @enforce_parameter_types
    def drag_torque_specification_method(
        self: "Self", value: "_2273.PowerLoadDragTorqueSpecificationMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.SystemModel.PowerLoadDragTorqueSpecificationMethod"
        )
        pythonnet_property_set(self.wrapped, "DragTorqueSpecificationMethod", value)

    @property
    def drag_torque_vs_speed_and_time(self: "Self") -> "_1615.GriddedSurfaceAccessor":
        """mastapy.math_utility.measured_data.GriddedSurfaceAccessor"""
        temp = pythonnet_property_get(self.wrapped, "DragTorqueVsSpeedAndTime")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @drag_torque_vs_speed_and_time.setter
    @enforce_parameter_types
    def drag_torque_vs_speed_and_time(
        self: "Self", value: "_1615.GriddedSurfaceAccessor"
    ) -> None:
        pythonnet_property_set(self.wrapped, "DragTorqueVsSpeedAndTime", value.wrapped)

    @property
    def dynamic_torsional_stiffness(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "DynamicTorsionalStiffness")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @dynamic_torsional_stiffness.setter
    @enforce_parameter_types
    def dynamic_torsional_stiffness(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DynamicTorsionalStiffness", value)

    @property
    def electric_machine_data_set_selector(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_ElectricMachineDataSet":
        """ListWithSelectedItem[mastapy.system_model.fe.ElectricMachineDataSet]"""
        temp = pythonnet_property_get(self.wrapped, "ElectricMachineDataSetSelector")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_ElectricMachineDataSet",
        )(temp)

    @electric_machine_data_set_selector.setter
    @enforce_parameter_types
    def electric_machine_data_set_selector(
        self: "Self", value: "_2431.ElectricMachineDataSet"
    ) -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_ElectricMachineDataSet.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_ElectricMachineDataSet.implicit_type()
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "ElectricMachineDataSetSelector", value)

    @property
    def engine_throttle_position(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EngineThrottlePosition")

        if temp is None:
            return 0.0

        return temp

    @engine_throttle_position.setter
    @enforce_parameter_types
    def engine_throttle_position(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EngineThrottlePosition",
            float(value) if value is not None else 0.0,
        )

    @property
    def engine_throttle_time_profile(self: "Self") -> "_1585.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "EngineThrottleTimeProfile")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @engine_throttle_time_profile.setter
    @enforce_parameter_types
    def engine_throttle_time_profile(
        self: "Self", value: "_1585.Vector2DListAccessor"
    ) -> None:
        pythonnet_property_set(self.wrapped, "EngineThrottleTimeProfile", value.wrapped)

    @property
    def first_order_lag_cutoff_frequency(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FirstOrderLagCutoffFrequency")

        if temp is None:
            return 0.0

        return temp

    @first_order_lag_cutoff_frequency.setter
    @enforce_parameter_types
    def first_order_lag_cutoff_frequency(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FirstOrderLagCutoffFrequency",
            float(value) if value is not None else 0.0,
        )

    @property
    def first_order_lag_time_constant(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FirstOrderLagTimeConstant")

        if temp is None:
            return 0.0

        return temp

    @first_order_lag_time_constant.setter
    @enforce_parameter_types
    def first_order_lag_time_constant(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FirstOrderLagTimeConstant",
            float(value) if value is not None else 0.0,
        )

    @property
    def include_in_torsional_stiffness_calculation(
        self: "Self",
    ) -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(
            self.wrapped, "IncludeInTorsionalStiffnessCalculation"
        )

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @include_in_torsional_stiffness_calculation.setter
    @enforce_parameter_types
    def include_in_torsional_stiffness_calculation(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "IncludeInTorsionalStiffnessCalculation", value
        )

    @property
    def is_wheel_using_static_friction_initially(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "IsWheelUsingStaticFrictionInitially"
        )

        if temp is None:
            return False

        return temp

    @is_wheel_using_static_friction_initially.setter
    @enforce_parameter_types
    def is_wheel_using_static_friction_initially(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsWheelUsingStaticFrictionInitially",
            bool(value) if value is not None else False,
        )

    @property
    def linear_resistance_coefficient(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LinearResistanceCoefficient")

        if temp is None:
            return 0.0

        return temp

    @linear_resistance_coefficient.setter
    @enforce_parameter_types
    def linear_resistance_coefficient(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LinearResistanceCoefficient",
            float(value) if value is not None else 0.0,
        )

    @property
    def linear_resistance_coefficient_time_profile(
        self: "Self",
    ) -> "_1585.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(
            self.wrapped, "LinearResistanceCoefficientTimeProfile"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @linear_resistance_coefficient_time_profile.setter
    @enforce_parameter_types
    def linear_resistance_coefficient_time_profile(
        self: "Self", value: "_1585.Vector2DListAccessor"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "LinearResistanceCoefficientTimeProfile", value.wrapped
        )

    @property
    def maximum_throttle_in_drive_cycle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumThrottleInDriveCycle")

        if temp is None:
            return 0.0

        return temp

    @maximum_throttle_in_drive_cycle.setter
    @enforce_parameter_types
    def maximum_throttle_in_drive_cycle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumThrottleInDriveCycle",
            float(value) if value is not None else 0.0,
        )

    @property
    def power(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Power")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @power.setter
    @enforce_parameter_types
    def power(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Power", value)

    @property
    def power_load_for_pid_control(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "PowerLoadForPIDControl")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @power_load_for_pid_control.setter
    @enforce_parameter_types
    def power_load_for_pid_control(self: "Self", value: "str") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else ""
        )
        pythonnet_property_set(self.wrapped, "PowerLoadForPIDControl", value)

    @property
    def proportion_of_vehicle_weight_carried(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ProportionOfVehicleWeightCarried")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @proportion_of_vehicle_weight_carried.setter
    @enforce_parameter_types
    def proportion_of_vehicle_weight_carried(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ProportionOfVehicleWeightCarried", value)

    @property
    def quadratic_resistance_coefficient(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "QuadraticResistanceCoefficient")

        if temp is None:
            return 0.0

        return temp

    @quadratic_resistance_coefficient.setter
    @enforce_parameter_types
    def quadratic_resistance_coefficient(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "QuadraticResistanceCoefficient",
            float(value) if value is not None else 0.0,
        )

    @property
    def quadratic_resistance_coefficient_time_profile(
        self: "Self",
    ) -> "_1585.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(
            self.wrapped, "QuadraticResistanceCoefficientTimeProfile"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @quadratic_resistance_coefficient_time_profile.setter
    @enforce_parameter_types
    def quadratic_resistance_coefficient_time_profile(
        self: "Self", value: "_1585.Vector2DListAccessor"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "QuadraticResistanceCoefficientTimeProfile", value.wrapped
        )

    @property
    def specified_angle_for_input_torque(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedAngleForInputTorque")

        if temp is None:
            return 0.0

        return temp

    @specified_angle_for_input_torque.setter
    @enforce_parameter_types
    def specified_angle_for_input_torque(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifiedAngleForInputTorque",
            float(value) if value is not None else 0.0,
        )

    @property
    def specified_time_for_input_torque(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedTimeForInputTorque")

        if temp is None:
            return 0.0

        return temp

    @specified_time_for_input_torque.setter
    @enforce_parameter_types
    def specified_time_for_input_torque(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifiedTimeForInputTorque",
            float(value) if value is not None else 0.0,
        )

    @property
    def speed(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Speed")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @speed.setter
    @enforce_parameter_types
    def speed(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Speed", value)

    @property
    def speed_vs_time(self: "Self") -> "_1585.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "SpeedVsTime")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @speed_vs_time.setter
    @enforce_parameter_types
    def speed_vs_time(self: "Self", value: "_1585.Vector2DListAccessor") -> None:
        pythonnet_property_set(self.wrapped, "SpeedVsTime", value.wrapped)

    @property
    def system_deflection_torque_also_applies_to_advanced_system_deflection(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "SystemDeflectionTorqueAlsoAppliesToAdvancedSystemDeflection"
        )

        if temp is None:
            return False

        return temp

    @system_deflection_torque_also_applies_to_advanced_system_deflection.setter
    @enforce_parameter_types
    def system_deflection_torque_also_applies_to_advanced_system_deflection(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "SystemDeflectionTorqueAlsoAppliesToAdvancedSystemDeflection",
            bool(value) if value is not None else False,
        )

    @property
    def system_deflection_torque_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_TorqueSpecificationForSystemDeflection":
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.static_loads.TorqueSpecificationForSystemDeflection]"""
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionTorqueMethod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_TorqueSpecificationForSystemDeflection.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @system_deflection_torque_method.setter
    @enforce_parameter_types
    def system_deflection_torque_method(
        self: "Self", value: "_7132.TorqueSpecificationForSystemDeflection"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_TorqueSpecificationForSystemDeflection.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "SystemDeflectionTorqueMethod", value)

    @property
    def target_engine_idle_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TargetEngineIdleSpeed")

        if temp is None:
            return 0.0

        return temp

    @target_engine_idle_speed.setter
    @enforce_parameter_types
    def target_engine_idle_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TargetEngineIdleSpeed",
            float(value) if value is not None else 0.0,
        )

    @property
    def target_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TargetSpeed")

        if temp is None:
            return 0.0

        return temp

    @target_speed.setter
    @enforce_parameter_types
    def target_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TargetSpeed", float(value) if value is not None else 0.0
        )

    @property
    def target_speed_input_type(
        self: "Self",
    ) -> "_2275.PowerLoadPIDControlSpeedInputType":
        """mastapy.system_model.PowerLoadPIDControlSpeedInputType"""
        temp = pythonnet_property_get(self.wrapped, "TargetSpeedInputType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.SystemModel.PowerLoadPIDControlSpeedInputType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model._2275", "PowerLoadPIDControlSpeedInputType"
        )(value)

    @target_speed_input_type.setter
    @enforce_parameter_types
    def target_speed_input_type(
        self: "Self", value: "_2275.PowerLoadPIDControlSpeedInputType"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.SystemModel.PowerLoadPIDControlSpeedInputType"
        )
        pythonnet_property_set(self.wrapped, "TargetSpeedInputType", value)

    @property
    def target_speed_vs_time(self: "Self") -> "_1585.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "TargetSpeedVsTime")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @target_speed_vs_time.setter
    @enforce_parameter_types
    def target_speed_vs_time(self: "Self", value: "_1585.Vector2DListAccessor") -> None:
        pythonnet_property_set(self.wrapped, "TargetSpeedVsTime", value.wrapped)

    @property
    def torque(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Torque")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @torque.setter
    @enforce_parameter_types
    def torque(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Torque", value)

    @property
    def torque_input_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod":
        """EnumWithSelectedValue[mastapy.system_model.PowerLoadInputTorqueSpecificationMethod]"""
        temp = pythonnet_property_get(self.wrapped, "TorqueInputMethod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @torque_input_method.setter
    @enforce_parameter_types
    def torque_input_method(
        self: "Self", value: "_2274.PowerLoadInputTorqueSpecificationMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "TorqueInputMethod", value)

    @property
    def torque_time_profile_repeats(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "TorqueTimeProfileRepeats")

        if temp is None:
            return False

        return temp

    @torque_time_profile_repeats.setter
    @enforce_parameter_types
    def torque_time_profile_repeats(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TorqueTimeProfileRepeats",
            bool(value) if value is not None else False,
        )

    @property
    def torque_vs_angle(self: "Self") -> "_1585.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "TorqueVsAngle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @torque_vs_angle.setter
    @enforce_parameter_types
    def torque_vs_angle(self: "Self", value: "_1585.Vector2DListAccessor") -> None:
        pythonnet_property_set(self.wrapped, "TorqueVsAngle", value.wrapped)

    @property
    def torque_vs_angle_and_speed(self: "Self") -> "_1615.GriddedSurfaceAccessor":
        """mastapy.math_utility.measured_data.GriddedSurfaceAccessor"""
        temp = pythonnet_property_get(self.wrapped, "TorqueVsAngleAndSpeed")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @torque_vs_angle_and_speed.setter
    @enforce_parameter_types
    def torque_vs_angle_and_speed(
        self: "Self", value: "_1615.GriddedSurfaceAccessor"
    ) -> None:
        pythonnet_property_set(self.wrapped, "TorqueVsAngleAndSpeed", value.wrapped)

    @property
    def torque_vs_time(self: "Self") -> "_1585.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "TorqueVsTime")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @torque_vs_time.setter
    @enforce_parameter_types
    def torque_vs_time(self: "Self", value: "_1585.Vector2DListAccessor") -> None:
        pythonnet_property_set(self.wrapped, "TorqueVsTime", value.wrapped)

    @property
    def total_mean_rotor_x_force_over_all_nodes(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalMeanRotorXForceOverAllNodes")

        if temp is None:
            return 0.0

        return temp

    @property
    def total_mean_rotor_y_force_over_all_nodes(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalMeanRotorYForceOverAllNodes")

        if temp is None:
            return 0.0

        return temp

    @property
    def unbalanced_magnetic_pull_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "UnbalancedMagneticPullStiffness")

        if temp is None:
            return 0.0

        return temp

    @unbalanced_magnetic_pull_stiffness.setter
    @enforce_parameter_types
    def unbalanced_magnetic_pull_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UnbalancedMagneticPullStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    def use_engine_idle_speed_control(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseEngineIdleSpeedControl")

        if temp is None:
            return False

        return temp

    @use_engine_idle_speed_control.setter
    @enforce_parameter_types
    def use_engine_idle_speed_control(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseEngineIdleSpeedControl",
            bool(value) if value is not None else False,
        )

    @property
    def use_time_dependent_constant_resistance_coefficient(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseTimeDependentConstantResistanceCoefficient"
        )

        if temp is None:
            return False

        return temp

    @use_time_dependent_constant_resistance_coefficient.setter
    @enforce_parameter_types
    def use_time_dependent_constant_resistance_coefficient(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseTimeDependentConstantResistanceCoefficient",
            bool(value) if value is not None else False,
        )

    @property
    def use_time_dependent_linear_resistance_coefficient(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseTimeDependentLinearResistanceCoefficient"
        )

        if temp is None:
            return False

        return temp

    @use_time_dependent_linear_resistance_coefficient.setter
    @enforce_parameter_types
    def use_time_dependent_linear_resistance_coefficient(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseTimeDependentLinearResistanceCoefficient",
            bool(value) if value is not None else False,
        )

    @property
    def use_time_dependent_quadratic_resistance_coefficient(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseTimeDependentQuadraticResistanceCoefficient"
        )

        if temp is None:
            return False

        return temp

    @use_time_dependent_quadratic_resistance_coefficient.setter
    @enforce_parameter_types
    def use_time_dependent_quadratic_resistance_coefficient(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseTimeDependentQuadraticResistanceCoefficient",
            bool(value) if value is not None else False,
        )

    @property
    def use_time_dependent_throttle(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseTimeDependentThrottle")

        if temp is None:
            return False

        return temp

    @use_time_dependent_throttle.setter
    @enforce_parameter_types
    def use_time_dependent_throttle(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseTimeDependentThrottle",
            bool(value) if value is not None else False,
        )

    @property
    def vehicle_speed_to_start_idle_control(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "VehicleSpeedToStartIdleControl")

        if temp is None:
            return 0.0

        return temp

    @vehicle_speed_to_start_idle_control.setter
    @enforce_parameter_types
    def vehicle_speed_to_start_idle_control(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "VehicleSpeedToStartIdleControl",
            float(value) if value is not None else 0.0,
        )

    @property
    def vehicle_speed_to_stop_idle_control(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "VehicleSpeedToStopIdleControl")

        if temp is None:
            return 0.0

        return temp

    @vehicle_speed_to_stop_idle_control.setter
    @enforce_parameter_types
    def vehicle_speed_to_stop_idle_control(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "VehicleSpeedToStopIdleControl",
            float(value) if value is not None else 0.0,
        )

    @property
    def velocity_first_order_lag_cutoff_frequency(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "VelocityFirstOrderLagCutoffFrequency"
        )

        if temp is None:
            return 0.0

        return temp

    @velocity_first_order_lag_cutoff_frequency.setter
    @enforce_parameter_types
    def velocity_first_order_lag_cutoff_frequency(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "VelocityFirstOrderLagCutoffFrequency",
            float(value) if value is not None else 0.0,
        )

    @property
    def velocity_first_order_lag_time_constant(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "VelocityFirstOrderLagTimeConstant")

        if temp is None:
            return 0.0

        return temp

    @velocity_first_order_lag_time_constant.setter
    @enforce_parameter_types
    def velocity_first_order_lag_time_constant(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "VelocityFirstOrderLagTimeConstant",
            float(value) if value is not None else 0.0,
        )

    @property
    def wheel_slip_model(self: "Self") -> "_5649.WheelSlipType":
        """mastapy.system_model.analyses_and_results.mbd_analyses.WheelSlipType"""
        temp = pythonnet_property_get(self.wrapped, "WheelSlipModel")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.WheelSlipType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.mbd_analyses._5649",
            "WheelSlipType",
        )(value)

    @wheel_slip_model.setter
    @enforce_parameter_types
    def wheel_slip_model(self: "Self", value: "_5649.WheelSlipType") -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.WheelSlipType",
        )
        pythonnet_property_set(self.wrapped, "WheelSlipModel", value)

    @property
    def wheel_static_to_dynamic_friction_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WheelStaticToDynamicFrictionRatio")

        if temp is None:
            return 0.0

        return temp

    @wheel_static_to_dynamic_friction_ratio.setter
    @enforce_parameter_types
    def wheel_static_to_dynamic_friction_ratio(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WheelStaticToDynamicFrictionRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    def wheel_to_vehicle_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WheelToVehicleStiffness")

        if temp is None:
            return 0.0

        return temp

    @wheel_to_vehicle_stiffness.setter
    @enforce_parameter_types
    def wheel_to_vehicle_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WheelToVehicleStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    def coefficient_of_friction_with_ground(
        self: "Self",
    ) -> "_100.NonDimensionalInputComponent":
        """mastapy.nodal_analysis.varying_input_components.NonDimensionalInputComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CoefficientOfFrictionWithGround")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_design(self: "Self") -> "_2532.PowerLoad":
        """mastapy.system_model.part_model.PowerLoad

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def engine_idle_speed_control_pid_settings(
        self: "Self",
    ) -> "_1627.PIDControlSettings":
        """mastapy.math_utility.control.PIDControlSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EngineIdleSpeedControlPIDSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def pid_control_settings(self: "Self") -> "_1627.PIDControlSettings":
        """mastapy.math_utility.control.PIDControlSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PIDControlSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    def get_harmonic_load_data_for_import(
        self: "Self",
    ) -> "_7024.ElectricMachineHarmonicLoadData":
        """mastapy.system_model.analyses_and_results.static_loads.ElectricMachineHarmonicLoadData"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetHarmonicLoadDataForImport"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PowerLoadLoadCase":
        """Cast to another type.

        Returns:
            _Cast_PowerLoadLoadCase
        """
        return _Cast_PowerLoadLoadCase(self)
