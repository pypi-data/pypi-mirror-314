"""FlexiblePinAnalysisConceptLevel"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
    _6413,
)

_FLEXIBLE_PIN_ANALYSIS_CONCEPT_LEVEL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.FlexiblePinAnalyses",
    "FlexiblePinAnalysisConceptLevel",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
        _6412,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2787,
        _2847,
    )

    Self = TypeVar("Self", bound="FlexiblePinAnalysisConceptLevel")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FlexiblePinAnalysisConceptLevel._Cast_FlexiblePinAnalysisConceptLevel",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FlexiblePinAnalysisConceptLevel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FlexiblePinAnalysisConceptLevel:
    """Special nested class for casting FlexiblePinAnalysisConceptLevel to subclasses."""

    __parent__: "FlexiblePinAnalysisConceptLevel"

    @property
    def flexible_pin_analysis(self: "CastSelf") -> "_6413.FlexiblePinAnalysis":
        return self.__parent__._cast(_6413.FlexiblePinAnalysis)

    @property
    def combination_analysis(self: "CastSelf") -> "_6412.CombinationAnalysis":
        from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
            _6412,
        )

        return self.__parent__._cast(_6412.CombinationAnalysis)

    @property
    def flexible_pin_analysis_concept_level(
        self: "CastSelf",
    ) -> "FlexiblePinAnalysisConceptLevel":
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
class FlexiblePinAnalysisConceptLevel(_6413.FlexiblePinAnalysis):
    """FlexiblePinAnalysisConceptLevel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FLEXIBLE_PIN_ANALYSIS_CONCEPT_LEVEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def flexible_pin_extreme_load_case(
        self: "Self",
    ) -> "_2847.FlexiblePinAssemblySystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.FlexiblePinAssemblySystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FlexiblePinExtremeLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def flexible_pin_nominal_load_case(
        self: "Self",
    ) -> "_2847.FlexiblePinAssemblySystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.FlexiblePinAssemblySystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FlexiblePinNominalLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def planet_bearings_in_nominal_load(
        self: "Self",
    ) -> "List[_2787.BearingSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.BearingSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlanetBearingsInNominalLoad")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_FlexiblePinAnalysisConceptLevel":
        """Cast to another type.

        Returns:
            _Cast_FlexiblePinAnalysisConceptLevel
        """
        return _Cast_FlexiblePinAnalysisConceptLevel(self)
