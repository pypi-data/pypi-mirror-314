"""ModalAnalysisForHarmonicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses import _4773

_MODAL_ANALYSIS_FOR_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation",
    "ModalAnalysisForHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2739
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7709,
        _7724,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5902,
    )

    Self = TypeVar("Self", bound="ModalAnalysisForHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ModalAnalysisForHarmonicAnalysis._Cast_ModalAnalysisForHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ModalAnalysisForHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ModalAnalysisForHarmonicAnalysis:
    """Special nested class for casting ModalAnalysisForHarmonicAnalysis to subclasses."""

    __parent__: "ModalAnalysisForHarmonicAnalysis"

    @property
    def modal_analysis(self: "CastSelf") -> "_4773.ModalAnalysis":
        return self.__parent__._cast(_4773.ModalAnalysis)

    @property
    def static_load_analysis_case(self: "CastSelf") -> "_7724.StaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7724,
        )

        return self.__parent__._cast(_7724.StaticLoadAnalysisCase)

    @property
    def analysis_case(self: "CastSelf") -> "_7709.AnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7709,
        )

        return self.__parent__._cast(_7709.AnalysisCase)

    @property
    def context(self: "CastSelf") -> "_2739.Context":
        from mastapy._private.system_model.analyses_and_results import _2739

        return self.__parent__._cast(_2739.Context)

    @property
    def modal_analysis_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "ModalAnalysisForHarmonicAnalysis":
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
class ModalAnalysisForHarmonicAnalysis(_4773.ModalAnalysis):
    """ModalAnalysisForHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MODAL_ANALYSIS_FOR_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def frequency_for_truncation_correction(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrequencyForTruncationCorrection")

        if temp is None:
            return 0.0

        return temp

    @property
    def harmonic_analysis_settings(self: "Self") -> "_5902.HarmonicAnalysisOptions":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.HarmonicAnalysisOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HarmonicAnalysisSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ModalAnalysisForHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ModalAnalysisForHarmonicAnalysis
        """
        return _Cast_ModalAnalysisForHarmonicAnalysis(self)
