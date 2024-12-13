"""EfficiencyMapLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines.load_cases_and_analyses import _1417

_EFFICIENCY_MAP_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses", "EfficiencyMapLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines import _1310
    from mastapy._private.electric_machines.load_cases_and_analyses import (
        _1400,
        _1405,
        _1409,
    )

    Self = TypeVar("Self", bound="EfficiencyMapLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="EfficiencyMapLoadCase._Cast_EfficiencyMapLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("EfficiencyMapLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_EfficiencyMapLoadCase:
    """Special nested class for casting EfficiencyMapLoadCase to subclasses."""

    __parent__: "EfficiencyMapLoadCase"

    @property
    def non_linear_dq_model_multiple_operating_points_load_case(
        self: "CastSelf",
    ) -> "_1417.NonLinearDQModelMultipleOperatingPointsLoadCase":
        return self.__parent__._cast(
            _1417.NonLinearDQModelMultipleOperatingPointsLoadCase
        )

    @property
    def electric_machine_load_case_base(
        self: "CastSelf",
    ) -> "_1409.ElectricMachineLoadCaseBase":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1409

        return self.__parent__._cast(_1409.ElectricMachineLoadCaseBase)

    @property
    def efficiency_map_load_case(self: "CastSelf") -> "EfficiencyMapLoadCase":
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
class EfficiencyMapLoadCase(_1417.NonLinearDQModelMultipleOperatingPointsLoadCase):
    """EfficiencyMapLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _EFFICIENCY_MAP_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def efficiency_map_settings(
        self: "Self",
    ) -> "_1405.ElectricMachineEfficiencyMapSettings":
        """mastapy.electric_machines.load_cases_and_analyses.ElectricMachineEfficiencyMapSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EfficiencyMapSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @enforce_parameter_types
    def analysis_for(
        self: "Self", setup: "_1310.ElectricMachineSetup"
    ) -> "_1400.EfficiencyMapAnalysis":
        """mastapy.electric_machines.load_cases_and_analyses.EfficiencyMapAnalysis

        Args:
            setup (mastapy.electric_machines.ElectricMachineSetup)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "AnalysisFor", setup.wrapped if setup else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_EfficiencyMapLoadCase":
        """Cast to another type.

        Returns:
            _Cast_EfficiencyMapLoadCase
        """
        return _Cast_EfficiencyMapLoadCase(self)
