"""SpeedTorqueCurveAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.electric_machines.load_cases_and_analyses import _1402

_SPEED_TORQUE_CURVE_ANALYSIS = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses", "SpeedTorqueCurveAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.electric_machines.load_cases_and_analyses import _1425
    from mastapy._private.electric_machines.results import _1391

    Self = TypeVar("Self", bound="SpeedTorqueCurveAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="SpeedTorqueCurveAnalysis._Cast_SpeedTorqueCurveAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpeedTorqueCurveAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpeedTorqueCurveAnalysis:
    """Special nested class for casting SpeedTorqueCurveAnalysis to subclasses."""

    __parent__: "SpeedTorqueCurveAnalysis"

    @property
    def electric_machine_analysis(self: "CastSelf") -> "_1402.ElectricMachineAnalysis":
        return self.__parent__._cast(_1402.ElectricMachineAnalysis)

    @property
    def speed_torque_curve_analysis(self: "CastSelf") -> "SpeedTorqueCurveAnalysis":
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
class SpeedTorqueCurveAnalysis(_1402.ElectricMachineAnalysis):
    """SpeedTorqueCurveAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPEED_TORQUE_CURVE_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def base_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BaseSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_torque_at_rated_inverter_current(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumTorqueAtRatedInverterCurrent"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def permanent_magnet_flux_linkage_at_reference_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PermanentMagnetFluxLinkageAtReferenceTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def load_case(self: "Self") -> "_1425.SpeedTorqueCurveLoadCase":
        """mastapy.electric_machines.load_cases_and_analyses.SpeedTorqueCurveLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def results_points(self: "Self") -> "List[_1391.MaximumTorqueResultsPoints]":
        """List[mastapy.electric_machines.results.MaximumTorqueResultsPoints]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsPoints")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_SpeedTorqueCurveAnalysis":
        """Cast to another type.

        Returns:
            _Cast_SpeedTorqueCurveAnalysis
        """
        return _Cast_SpeedTorqueCurveAnalysis(self)
