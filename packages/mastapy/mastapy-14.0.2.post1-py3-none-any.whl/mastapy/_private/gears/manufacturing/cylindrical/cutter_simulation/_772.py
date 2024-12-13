"""VirtualSimulationCalculator"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import _756

_VIRTUAL_SIMULATION_CALCULATOR = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation",
    "VirtualSimulationCalculator",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="VirtualSimulationCalculator")
    CastSelf = TypeVar(
        "CastSelf",
        bound="VirtualSimulationCalculator._Cast_VirtualSimulationCalculator",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VirtualSimulationCalculator",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualSimulationCalculator:
    """Special nested class for casting VirtualSimulationCalculator to subclasses."""

    __parent__: "VirtualSimulationCalculator"

    @property
    def cutter_simulation_calc(self: "CastSelf") -> "_756.CutterSimulationCalc":
        return self.__parent__._cast(_756.CutterSimulationCalc)

    @property
    def virtual_simulation_calculator(
        self: "CastSelf",
    ) -> "VirtualSimulationCalculator":
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
class VirtualSimulationCalculator(_756.CutterSimulationCalc):
    """VirtualSimulationCalculator

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VIRTUAL_SIMULATION_CALCULATOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def bending_moment_arm_for_iso_rating_worst(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BendingMomentArmForISORatingWorst")

        if temp is None:
            return 0.0

        return temp

    @property
    def form_factor_for_iso_rating_worst(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FormFactorForISORatingWorst")

        if temp is None:
            return 0.0

        return temp

    @property
    def notch_depth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NotchDepth")

        if temp is None:
            return 0.0

        return temp

    @property
    def radius_of_critical_point_for_iso_rating_worst(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RadiusOfCriticalPointForISORatingWorst"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def root_fillet_radius_iso(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootFilletRadiusISO")

        if temp is None:
            return None

        value = conversion.to_list_any(temp)

        if value is None:
            return None

        return value

    @property
    def root_fillet_radius_for_agma_rating(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootFilletRadiusForAGMARating")

        if temp is None:
            return 0.0

        return temp

    @property
    def root_fillet_radius_for_iso_rating(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootFilletRadiusForISORating")

        if temp is None:
            return 0.0

        return temp

    @property
    def root_fillet_radius_for_iso_rating_worst(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootFilletRadiusForISORatingWorst")

        if temp is None:
            return 0.0

        return temp

    @property
    def stress_correction_form_factor_worst(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StressCorrectionFormFactorWorst")

        if temp is None:
            return 0.0

        return temp

    @property
    def stress_correction_factor_for_iso_rating_worst(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StressCorrectionFactorForISORatingWorst"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def tooth_root_chord_for_iso_rating(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothRootChordForISORating")

        if temp is None:
            return 0.0

        return temp

    @property
    def tooth_root_chord_for_iso_rating_worst(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothRootChordForISORatingWorst")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_VirtualSimulationCalculator":
        """Cast to another type.

        Returns:
            _Cast_VirtualSimulationCalculator
        """
        return _Cast_VirtualSimulationCalculator(self)
