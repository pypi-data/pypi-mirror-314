"""SingleWhineAnalysisResultsPropertyAccessor"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
    _5992,
)

_SINGLE_WHINE_ANALYSIS_RESULTS_PROPERTY_ACCESSOR = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults",
    "SingleWhineAnalysisResultsPropertyAccessor",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
        _5996,
        _6009,
    )

    Self = TypeVar("Self", bound="SingleWhineAnalysisResultsPropertyAccessor")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SingleWhineAnalysisResultsPropertyAccessor._Cast_SingleWhineAnalysisResultsPropertyAccessor",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SingleWhineAnalysisResultsPropertyAccessor",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SingleWhineAnalysisResultsPropertyAccessor:
    """Special nested class for casting SingleWhineAnalysisResultsPropertyAccessor to subclasses."""

    __parent__: "SingleWhineAnalysisResultsPropertyAccessor"

    @property
    def abstract_single_whine_analysis_results_property_accessor(
        self: "CastSelf",
    ) -> "_5992.AbstractSingleWhineAnalysisResultsPropertyAccessor":
        return self.__parent__._cast(
            _5992.AbstractSingleWhineAnalysisResultsPropertyAccessor
        )

    @property
    def fe_part_single_whine_analysis_results_property_accessor(
        self: "CastSelf",
    ) -> "_5996.FEPartSingleWhineAnalysisResultsPropertyAccessor":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
            _5996,
        )

        return self.__parent__._cast(
            _5996.FEPartSingleWhineAnalysisResultsPropertyAccessor
        )

    @property
    def single_whine_analysis_results_property_accessor(
        self: "CastSelf",
    ) -> "SingleWhineAnalysisResultsPropertyAccessor":
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
class SingleWhineAnalysisResultsPropertyAccessor(
    _5992.AbstractSingleWhineAnalysisResultsPropertyAccessor
):
    """SingleWhineAnalysisResultsPropertyAccessor

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SINGLE_WHINE_ANALYSIS_RESULTS_PROPERTY_ACCESSOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def orders(self: "Self") -> "List[_6009.ResultsForOrderIncludingNodes]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForOrderIncludingNodes]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Orders")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_SingleWhineAnalysisResultsPropertyAccessor":
        """Cast to another type.

        Returns:
            _Cast_SingleWhineAnalysisResultsPropertyAccessor
        """
        return _Cast_SingleWhineAnalysisResultsPropertyAccessor(self)
