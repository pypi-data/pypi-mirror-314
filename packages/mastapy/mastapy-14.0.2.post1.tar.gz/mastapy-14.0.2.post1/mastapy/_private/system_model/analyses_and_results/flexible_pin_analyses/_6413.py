"""FlexiblePinAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
    _6412,
)

_FLEXIBLE_PIN_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.FlexiblePinAnalyses",
    "FlexiblePinAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
        _6414,
        _6415,
        _6416,
        _6417,
        _6418,
        _6419,
    )

    Self = TypeVar("Self", bound="FlexiblePinAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="FlexiblePinAnalysis._Cast_FlexiblePinAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FlexiblePinAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FlexiblePinAnalysis:
    """Special nested class for casting FlexiblePinAnalysis to subclasses."""

    __parent__: "FlexiblePinAnalysis"

    @property
    def combination_analysis(self: "CastSelf") -> "_6412.CombinationAnalysis":
        return self.__parent__._cast(_6412.CombinationAnalysis)

    @property
    def flexible_pin_analysis_concept_level(
        self: "CastSelf",
    ) -> "_6414.FlexiblePinAnalysisConceptLevel":
        from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
            _6414,
        )

        return self.__parent__._cast(_6414.FlexiblePinAnalysisConceptLevel)

    @property
    def flexible_pin_analysis_detail_level_and_pin_fatigue_one_tooth_pass(
        self: "CastSelf",
    ) -> "_6415.FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass":
        from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
            _6415,
        )

        return self.__parent__._cast(
            _6415.FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass
        )

    @property
    def flexible_pin_analysis_gear_and_bearing_rating(
        self: "CastSelf",
    ) -> "_6416.FlexiblePinAnalysisGearAndBearingRating":
        from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
            _6416,
        )

        return self.__parent__._cast(_6416.FlexiblePinAnalysisGearAndBearingRating)

    @property
    def flexible_pin_analysis_manufacture_level(
        self: "CastSelf",
    ) -> "_6417.FlexiblePinAnalysisManufactureLevel":
        from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
            _6417,
        )

        return self.__parent__._cast(_6417.FlexiblePinAnalysisManufactureLevel)

    @property
    def flexible_pin_analysis_stop_start_analysis(
        self: "CastSelf",
    ) -> "_6419.FlexiblePinAnalysisStopStartAnalysis":
        from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
            _6419,
        )

        return self.__parent__._cast(_6419.FlexiblePinAnalysisStopStartAnalysis)

    @property
    def flexible_pin_analysis(self: "CastSelf") -> "FlexiblePinAnalysis":
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
class FlexiblePinAnalysis(_6412.CombinationAnalysis):
    """FlexiblePinAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FLEXIBLE_PIN_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def analysis_options(self: "Self") -> "_6418.FlexiblePinAnalysisOptions":
        """mastapy.system_model.analyses_and_results.flexible_pin_analyses.FlexiblePinAnalysisOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AnalysisOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_FlexiblePinAnalysis":
        """Cast to another type.

        Returns:
            _Cast_FlexiblePinAnalysis
        """
        return _Cast_FlexiblePinAnalysis(self)
