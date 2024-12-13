"""HarmonicAnalysisOfSingleExcitation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7724

_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation",
    "HarmonicAnalysisOfSingleExcitation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2739
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7709
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5815,
    )

    Self = TypeVar("Self", bound="HarmonicAnalysisOfSingleExcitation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HarmonicAnalysisOfSingleExcitation._Cast_HarmonicAnalysisOfSingleExcitation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicAnalysisOfSingleExcitation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicAnalysisOfSingleExcitation:
    """Special nested class for casting HarmonicAnalysisOfSingleExcitation to subclasses."""

    __parent__: "HarmonicAnalysisOfSingleExcitation"

    @property
    def static_load_analysis_case(self: "CastSelf") -> "_7724.StaticLoadAnalysisCase":
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
    def harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "HarmonicAnalysisOfSingleExcitation":
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
class HarmonicAnalysisOfSingleExcitation(_7724.StaticLoadAnalysisCase):
    """HarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def excitation_detail(self: "Self") -> "_5815.AbstractPeriodicExcitationDetail":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.AbstractPeriodicExcitationDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExcitationDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_HarmonicAnalysisOfSingleExcitation":
        """Cast to another type.

        Returns:
            _Cast_HarmonicAnalysisOfSingleExcitation
        """
        return _Cast_HarmonicAnalysisOfSingleExcitation(self)
