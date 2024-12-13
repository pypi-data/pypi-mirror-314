"""BevelDifferentialSunGearCompoundHarmonicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
    _6028,
)

_BEVEL_DIFFERENTIAL_SUN_GEAR_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "BevelDifferentialSunGearCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5830,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6021,
        _6033,
        _6042,
        _6049,
        _6075,
        _6096,
        _6098,
    )

    Self = TypeVar("Self", bound="BevelDifferentialSunGearCompoundHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelDifferentialSunGearCompoundHarmonicAnalysis._Cast_BevelDifferentialSunGearCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelDifferentialSunGearCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelDifferentialSunGearCompoundHarmonicAnalysis:
    """Special nested class for casting BevelDifferentialSunGearCompoundHarmonicAnalysis to subclasses."""

    __parent__: "BevelDifferentialSunGearCompoundHarmonicAnalysis"

    @property
    def bevel_differential_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6028.BevelDifferentialGearCompoundHarmonicAnalysis":
        return self.__parent__._cast(
            _6028.BevelDifferentialGearCompoundHarmonicAnalysis
        )

    @property
    def bevel_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6033.BevelGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6033,
        )

        return self.__parent__._cast(_6033.BevelGearCompoundHarmonicAnalysis)

    @property
    def agma_gleason_conical_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6021.AGMAGleasonConicalGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6021,
        )

        return self.__parent__._cast(
            _6021.AGMAGleasonConicalGearCompoundHarmonicAnalysis
        )

    @property
    def conical_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6049.ConicalGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6049,
        )

        return self.__parent__._cast(_6049.ConicalGearCompoundHarmonicAnalysis)

    @property
    def gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6075.GearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6075,
        )

        return self.__parent__._cast(_6075.GearCompoundHarmonicAnalysis)

    @property
    def mountable_component_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6096.MountableComponentCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6096,
        )

        return self.__parent__._cast(_6096.MountableComponentCompoundHarmonicAnalysis)

    @property
    def component_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6042.ComponentCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6042,
        )

        return self.__parent__._cast(_6042.ComponentCompoundHarmonicAnalysis)

    @property
    def part_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6098.PartCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6098,
        )

        return self.__parent__._cast(_6098.PartCompoundHarmonicAnalysis)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7720.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7720,
        )

        return self.__parent__._cast(_7720.PartCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7717.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7717,
        )

        return self.__parent__._cast(_7717.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2740.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2740

        return self.__parent__._cast(_2740.DesignEntityAnalysis)

    @property
    def bevel_differential_sun_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "BevelDifferentialSunGearCompoundHarmonicAnalysis":
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
class BevelDifferentialSunGearCompoundHarmonicAnalysis(
    _6028.BevelDifferentialGearCompoundHarmonicAnalysis
):
    """BevelDifferentialSunGearCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_DIFFERENTIAL_SUN_GEAR_COMPOUND_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5830.BevelDifferentialSunGearHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.BevelDifferentialSunGearHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_5830.BevelDifferentialSunGearHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.BevelDifferentialSunGearHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_BevelDifferentialSunGearCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_BevelDifferentialSunGearCompoundHarmonicAnalysis
        """
        return _Cast_BevelDifferentialSunGearCompoundHarmonicAnalysis(self)
