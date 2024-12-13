"""OnLoadElectricMachineResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.electric_machines.results import _1376

_ON_LOAD_ELECTRIC_MACHINE_RESULTS = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Results", "OnLoadElectricMachineResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines import _1365
    from mastapy._private.electric_machines.load_cases_and_analyses import _1413, _1416

    Self = TypeVar("Self", bound="OnLoadElectricMachineResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="OnLoadElectricMachineResults._Cast_OnLoadElectricMachineResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("OnLoadElectricMachineResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OnLoadElectricMachineResults:
    """Special nested class for casting OnLoadElectricMachineResults to subclasses."""

    __parent__: "OnLoadElectricMachineResults"

    @property
    def electric_machine_results(self: "CastSelf") -> "_1376.ElectricMachineResults":
        return self.__parent__._cast(_1376.ElectricMachineResults)

    @property
    def on_load_electric_machine_results(
        self: "CastSelf",
    ) -> "OnLoadElectricMachineResults":
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
class OnLoadElectricMachineResults(_1376.ElectricMachineResults):
    """OnLoadElectricMachineResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ON_LOAD_ELECTRIC_MACHINE_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def average_power_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AveragePowerFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def average_power_factor_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AveragePowerFactorAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def average_power_factor_with_harmonic_distortion_adjustment(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AveragePowerFactorWithHarmonicDistortionAdjustment"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def average_torque_dq(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageTorqueDQ")

        if temp is None:
            return 0.0

        return temp

    @property
    def dc_winding_losses(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DCWindingLosses")

        if temp is None:
            return 0.0

        return temp

    @property
    def efficiency(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Efficiency")

        if temp is None:
            return 0.0

        return temp

    @property
    def electrical_loading(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElectricalLoading")

        if temp is None:
            return 0.0

        return temp

    @property
    def input_power(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InputPower")

        if temp is None:
            return 0.0

        return temp

    @property
    def line_resistance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LineResistance")

        if temp is None:
            return 0.0

        return temp

    @property
    def line_to_line_terminal_voltage_peak(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LineToLineTerminalVoltagePeak")

        if temp is None:
            return 0.0

        return temp

    @property
    def line_to_line_terminal_voltage_rms(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LineToLineTerminalVoltageRMS")

        if temp is None:
            return 0.0

        return temp

    @property
    def line_to_line_terminal_voltage_total_harmonic_distortion(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LineToLineTerminalVoltageTotalHarmonicDistortion"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def motor_constant(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MotorConstant")

        if temp is None:
            return 0.0

        return temp

    @property
    def motoring_or_generating(self: "Self") -> "_1416.MotoringOrGenerating":
        """mastapy.electric_machines.load_cases_and_analyses.MotoringOrGenerating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MotoringOrGenerating")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses.MotoringOrGenerating",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines.load_cases_and_analyses._1416",
            "MotoringOrGenerating",
        )(value)

    @property
    def output_power(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OutputPower")

        if temp is None:
            return 0.0

        return temp

    @property
    def phase_resistance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PhaseResistance")

        if temp is None:
            return 0.0

        return temp

    @property
    def phase_resistive_voltage_peak(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PhaseResistiveVoltagePeak")

        if temp is None:
            return 0.0

        return temp

    @property
    def phase_resistive_voltage_rms(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PhaseResistiveVoltageRMS")

        if temp is None:
            return 0.0

        return temp

    @property
    def phase_resistive_voltage_drms(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PhaseResistiveVoltageDRMS")

        if temp is None:
            return 0.0

        return temp

    @property
    def phase_resistive_voltage_qrms(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PhaseResistiveVoltageQRMS")

        if temp is None:
            return 0.0

        return temp

    @property
    def phase_terminal_voltage_peak(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PhaseTerminalVoltagePeak")

        if temp is None:
            return 0.0

        return temp

    @property
    def phase_terminal_voltage_rms(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PhaseTerminalVoltageRMS")

        if temp is None:
            return 0.0

        return temp

    @property
    def phase_terminal_voltage_total_harmonic_distortion(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PhaseTerminalVoltageTotalHarmonicDistortion"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def power_factor_direction(self: "Self") -> "_1413.LeadingOrLagging":
        """mastapy.electric_machines.load_cases_and_analyses.LeadingOrLagging

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFactorDirection")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses.LeadingOrLagging"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines.load_cases_and_analyses._1413",
            "LeadingOrLagging",
        )(value)

    @property
    def power_from_electromagnetic_analysis(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFromElectromagneticAnalysis")

        if temp is None:
            return 0.0

        return temp

    @property
    def stall_current(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StallCurrent")

        if temp is None:
            return 0.0

        return temp

    @property
    def stall_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StallTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    def torque_constant(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueConstant")

        if temp is None:
            return 0.0

        return temp

    @property
    def torque_ripple_percentage_mst(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueRipplePercentageMST")

        if temp is None:
            return 0.0

        return temp

    @property
    def total_power_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalPowerLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    def winding_material_resistivity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WindingMaterialResistivity")

        if temp is None:
            return 0.0

        return temp

    @property
    def winding_skin_depth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WindingSkinDepth")

        if temp is None:
            return 0.0

        return temp

    @property
    def windings(self: "Self") -> "_1365.Windings":
        """mastapy.electric_machines.Windings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Windings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_OnLoadElectricMachineResults":
        """Cast to another type.

        Returns:
            _Cast_OnLoadElectricMachineResults
        """
        return _Cast_OnLoadElectricMachineResults(self)
