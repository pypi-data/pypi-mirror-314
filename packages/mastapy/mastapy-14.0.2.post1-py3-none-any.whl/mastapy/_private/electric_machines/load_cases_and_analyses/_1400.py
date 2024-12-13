"""EfficiencyMapAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.electric_machines.load_cases_and_analyses import _1402

_EFFICIENCY_MAP_ANALYSIS = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses", "EfficiencyMapAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines.load_cases_and_analyses import _1401
    from mastapy._private.electric_machines.results import _1372

    Self = TypeVar("Self", bound="EfficiencyMapAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="EfficiencyMapAnalysis._Cast_EfficiencyMapAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("EfficiencyMapAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_EfficiencyMapAnalysis:
    """Special nested class for casting EfficiencyMapAnalysis to subclasses."""

    __parent__: "EfficiencyMapAnalysis"

    @property
    def electric_machine_analysis(self: "CastSelf") -> "_1402.ElectricMachineAnalysis":
        return self.__parent__._cast(_1402.ElectricMachineAnalysis)

    @property
    def efficiency_map_analysis(self: "CastSelf") -> "EfficiencyMapAnalysis":
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
class EfficiencyMapAnalysis(_1402.ElectricMachineAnalysis):
    """EfficiencyMapAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _EFFICIENCY_MAP_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def field_winding_resistance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FieldWindingResistance")

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
    def efficiency_map_results(self: "Self") -> "_1372.EfficiencyResults":
        """mastapy.electric_machines.results.EfficiencyResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EfficiencyMapResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def load_case(self: "Self") -> "_1401.EfficiencyMapLoadCase":
        """mastapy.electric_machines.load_cases_and_analyses.EfficiencyMapLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_EfficiencyMapAnalysis":
        """Cast to another type.

        Returns:
            _Cast_EfficiencyMapAnalysis
        """
        return _Cast_EfficiencyMapAnalysis(self)
