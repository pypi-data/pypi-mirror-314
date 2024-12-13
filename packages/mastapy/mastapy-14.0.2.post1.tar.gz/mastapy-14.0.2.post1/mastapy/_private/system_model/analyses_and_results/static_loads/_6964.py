"""AdvancedTimeSteppingAnalysisForModulationStaticLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.static_loads import _6957

_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION_STATIC_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AdvancedTimeSteppingAnalysisForModulationStaticLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2739
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5902,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _6956

    Self = TypeVar(
        "Self", bound="AdvancedTimeSteppingAnalysisForModulationStaticLoadCase"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="AdvancedTimeSteppingAnalysisForModulationStaticLoadCase._Cast_AdvancedTimeSteppingAnalysisForModulationStaticLoadCase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AdvancedTimeSteppingAnalysisForModulationStaticLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AdvancedTimeSteppingAnalysisForModulationStaticLoadCase:
    """Special nested class for casting AdvancedTimeSteppingAnalysisForModulationStaticLoadCase to subclasses."""

    __parent__: "AdvancedTimeSteppingAnalysisForModulationStaticLoadCase"

    @property
    def static_load_case(self: "CastSelf") -> "_6957.StaticLoadCase":
        return self.__parent__._cast(_6957.StaticLoadCase)

    @property
    def load_case(self: "CastSelf") -> "_6956.LoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6956,
        )

        return self.__parent__._cast(_6956.LoadCase)

    @property
    def context(self: "CastSelf") -> "_2739.Context":
        from mastapy._private.system_model.analyses_and_results import _2739

        return self.__parent__._cast(_2739.Context)

    @property
    def advanced_time_stepping_analysis_for_modulation_static_load_case(
        self: "CastSelf",
    ) -> "AdvancedTimeSteppingAnalysisForModulationStaticLoadCase":
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
class AdvancedTimeSteppingAnalysisForModulationStaticLoadCase(_6957.StaticLoadCase):
    """AdvancedTimeSteppingAnalysisForModulationStaticLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION_STATIC_LOAD_CASE
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def harmonic_analysis_options(self: "Self") -> "_5902.HarmonicAnalysisOptions":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.HarmonicAnalysisOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HarmonicAnalysisOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_AdvancedTimeSteppingAnalysisForModulationStaticLoadCase":
        """Cast to another type.

        Returns:
            _Cast_AdvancedTimeSteppingAnalysisForModulationStaticLoadCase
        """
        return _Cast_AdvancedTimeSteppingAnalysisForModulationStaticLoadCase(self)
