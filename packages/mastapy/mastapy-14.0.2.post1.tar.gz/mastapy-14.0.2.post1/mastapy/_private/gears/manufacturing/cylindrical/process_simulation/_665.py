"""FormWheelGrindingProcessSimulation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.manufacturing.cylindrical.process_simulation import _664

_FORM_WHEEL_GRINDING_PROCESS_SIMULATION = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.ProcessSimulation",
    "FormWheelGrindingProcessSimulation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FormWheelGrindingProcessSimulation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FormWheelGrindingProcessSimulation._Cast_FormWheelGrindingProcessSimulation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FormWheelGrindingProcessSimulation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FormWheelGrindingProcessSimulation:
    """Special nested class for casting FormWheelGrindingProcessSimulation to subclasses."""

    __parent__: "FormWheelGrindingProcessSimulation"

    @property
    def cutter_process_simulation(self: "CastSelf") -> "_664.CutterProcessSimulation":
        return self.__parent__._cast(_664.CutterProcessSimulation)

    @property
    def form_wheel_grinding_process_simulation(
        self: "CastSelf",
    ) -> "FormWheelGrindingProcessSimulation":
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
class FormWheelGrindingProcessSimulation(_664.CutterProcessSimulation):
    """FormWheelGrindingProcessSimulation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FORM_WHEEL_GRINDING_PROCESS_SIMULATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def gear_relative_tilt_x(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "GearRelativeTiltX")

        if temp is None:
            return 0.0

        return temp

    @gear_relative_tilt_x.setter
    @enforce_parameter_types
    def gear_relative_tilt_x(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "GearRelativeTiltX",
            float(value) if value is not None else 0.0,
        )

    @property
    def gear_relative_tilt_y(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "GearRelativeTiltY")

        if temp is None:
            return 0.0

        return temp

    @gear_relative_tilt_y.setter
    @enforce_parameter_types
    def gear_relative_tilt_y(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "GearRelativeTiltY",
            float(value) if value is not None else 0.0,
        )

    @property
    def grind_wheel_axial_offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "GrindWheelAxialOffset")

        if temp is None:
            return 0.0

        return temp

    @grind_wheel_axial_offset.setter
    @enforce_parameter_types
    def grind_wheel_axial_offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "GrindWheelAxialOffset",
            float(value) if value is not None else 0.0,
        )

    @property
    def grind_wheel_axial_runout_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "GrindWheelAxialRunoutRadius")

        if temp is None:
            return 0.0

        return temp

    @grind_wheel_axial_runout_radius.setter
    @enforce_parameter_types
    def grind_wheel_axial_runout_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "GrindWheelAxialRunoutRadius",
            float(value) if value is not None else 0.0,
        )

    @property
    def grind_wheel_axial_runout_reading(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "GrindWheelAxialRunoutReading")

        if temp is None:
            return 0.0

        return temp

    @grind_wheel_axial_runout_reading.setter
    @enforce_parameter_types
    def grind_wheel_axial_runout_reading(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "GrindWheelAxialRunoutReading",
            float(value) if value is not None else 0.0,
        )

    @property
    def grind_wheel_diameter_deviation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "GrindWheelDiameterDeviation")

        if temp is None:
            return 0.0

        return temp

    @grind_wheel_diameter_deviation.setter
    @enforce_parameter_types
    def grind_wheel_diameter_deviation(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "GrindWheelDiameterDeviation",
            float(value) if value is not None else 0.0,
        )

    @property
    def grind_wheel_tilt_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "GrindWheelTiltAngle")

        if temp is None:
            return 0.0

        return temp

    @grind_wheel_tilt_angle.setter
    @enforce_parameter_types
    def grind_wheel_tilt_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "GrindWheelTiltAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    def grind_wheel_tilt_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "GrindWheelTiltRadius")

        if temp is None:
            return 0.0

        return temp

    @grind_wheel_tilt_radius.setter
    @enforce_parameter_types
    def grind_wheel_tilt_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "GrindWheelTiltRadius",
            float(value) if value is not None else 0.0,
        )

    @property
    def left_amplitude(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LeftAmplitude")

        if temp is None:
            return 0.0

        return temp

    @left_amplitude.setter
    @enforce_parameter_types
    def left_amplitude(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "LeftAmplitude", float(value) if value is not None else 0.0
        )

    @property
    def left_number_of_cycles(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LeftNumberOfCycles")

        if temp is None:
            return 0.0

        return temp

    @left_number_of_cycles.setter
    @enforce_parameter_types
    def left_number_of_cycles(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LeftNumberOfCycles",
            float(value) if value is not None else 0.0,
        )

    @property
    def left_starting_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LeftStartingAngle")

        if temp is None:
            return 0.0

        return temp

    @left_starting_angle.setter
    @enforce_parameter_types
    def left_starting_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LeftStartingAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    def right_amplitude(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RightAmplitude")

        if temp is None:
            return 0.0

        return temp

    @right_amplitude.setter
    @enforce_parameter_types
    def right_amplitude(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RightAmplitude", float(value) if value is not None else 0.0
        )

    @property
    def right_number_of_cycles(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RightNumberOfCycles")

        if temp is None:
            return 0.0

        return temp

    @right_number_of_cycles.setter
    @enforce_parameter_types
    def right_number_of_cycles(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RightNumberOfCycles",
            float(value) if value is not None else 0.0,
        )

    @property
    def right_starting_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RightStartingAngle")

        if temp is None:
            return 0.0

        return temp

    @right_starting_angle.setter
    @enforce_parameter_types
    def right_starting_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RightStartingAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_FormWheelGrindingProcessSimulation":
        """Cast to another type.

        Returns:
            _Cast_FormWheelGrindingProcessSimulation
        """
        return _Cast_FormWheelGrindingProcessSimulation(self)
