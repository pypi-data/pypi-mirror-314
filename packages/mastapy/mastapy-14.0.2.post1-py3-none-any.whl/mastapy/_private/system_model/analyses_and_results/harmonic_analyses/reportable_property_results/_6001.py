"""HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
    _6000,
)

_HARMONIC_ANALYSIS_RESULTS_BROKEN_DOWN_BY_NODE_WITHIN_A_HARMONIC = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults",
    "HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
        _6012,
    )

    Self = TypeVar(
        "Self", bound="HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic._Cast_HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic:
    """Special nested class for casting HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic to subclasses."""

    __parent__: "HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic"

    @property
    def harmonic_analysis_results_broken_down_by_location_within_a_harmonic(
        self: "CastSelf",
    ) -> "_6000.HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic":
        return self.__parent__._cast(
            _6000.HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic
        )

    @property
    def harmonic_analysis_results_broken_down_by_node_within_a_harmonic(
        self: "CastSelf",
    ) -> "HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic":
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
class HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic(
    _6000.HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic
):
    """HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _HARMONIC_ANALYSIS_RESULTS_BROKEN_DOWN_BY_NODE_WITHIN_A_HARMONIC
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def node_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NodeName")

        if temp is None:
            return ""

        return temp

    @property
    def acceleration(self: "Self") -> "_6012.ResultsForResponseOfANodeOnAHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForResponseOfANodeOnAHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Acceleration")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def displacement(self: "Self") -> "_6012.ResultsForResponseOfANodeOnAHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForResponseOfANodeOnAHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Displacement")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def force(self: "Self") -> "_6012.ResultsForResponseOfANodeOnAHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForResponseOfANodeOnAHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Force")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def velocity(self: "Self") -> "_6012.ResultsForResponseOfANodeOnAHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForResponseOfANodeOnAHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Velocity")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic":
        """Cast to another type.

        Returns:
            _Cast_HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic
        """
        return _Cast_HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic(self)
