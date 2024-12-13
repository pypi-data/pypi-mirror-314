"""AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
    _6857,
)

_AGMA_GLEASON_CONICAL_GEAR_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound",
    "AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6695,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
        _6836,
        _6839,
        _6840,
        _6841,
        _6850,
        _6883,
        _6887,
        _6904,
        _6906,
        _6926,
        _6932,
        _6935,
        _6938,
        _6939,
        _6953,
    )

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis._Cast_AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis:
    """Special nested class for casting AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis to subclasses."""

    __parent__: "AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis"

    @property
    def conical_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6857.ConicalGearCompoundCriticalSpeedAnalysis":
        return self.__parent__._cast(_6857.ConicalGearCompoundCriticalSpeedAnalysis)

    @property
    def gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6883.GearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6883,
        )

        return self.__parent__._cast(_6883.GearCompoundCriticalSpeedAnalysis)

    @property
    def mountable_component_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6904.MountableComponentCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6904,
        )

        return self.__parent__._cast(
            _6904.MountableComponentCompoundCriticalSpeedAnalysis
        )

    @property
    def component_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6850.ComponentCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6850,
        )

        return self.__parent__._cast(_6850.ComponentCompoundCriticalSpeedAnalysis)

    @property
    def part_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6906.PartCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6906,
        )

        return self.__parent__._cast(_6906.PartCompoundCriticalSpeedAnalysis)

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
    def bevel_differential_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6836.BevelDifferentialGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6836,
        )

        return self.__parent__._cast(
            _6836.BevelDifferentialGearCompoundCriticalSpeedAnalysis
        )

    @property
    def bevel_differential_planet_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6839.BevelDifferentialPlanetGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6839,
        )

        return self.__parent__._cast(
            _6839.BevelDifferentialPlanetGearCompoundCriticalSpeedAnalysis
        )

    @property
    def bevel_differential_sun_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6840.BevelDifferentialSunGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6840,
        )

        return self.__parent__._cast(
            _6840.BevelDifferentialSunGearCompoundCriticalSpeedAnalysis
        )

    @property
    def bevel_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6841.BevelGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6841,
        )

        return self.__parent__._cast(_6841.BevelGearCompoundCriticalSpeedAnalysis)

    @property
    def hypoid_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6887.HypoidGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6887,
        )

        return self.__parent__._cast(_6887.HypoidGearCompoundCriticalSpeedAnalysis)

    @property
    def spiral_bevel_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6926.SpiralBevelGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6926,
        )

        return self.__parent__._cast(_6926.SpiralBevelGearCompoundCriticalSpeedAnalysis)

    @property
    def straight_bevel_diff_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6932.StraightBevelDiffGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6932,
        )

        return self.__parent__._cast(
            _6932.StraightBevelDiffGearCompoundCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6935.StraightBevelGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6935,
        )

        return self.__parent__._cast(
            _6935.StraightBevelGearCompoundCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_planet_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6938.StraightBevelPlanetGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6938,
        )

        return self.__parent__._cast(
            _6938.StraightBevelPlanetGearCompoundCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_sun_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6939.StraightBevelSunGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6939,
        )

        return self.__parent__._cast(
            _6939.StraightBevelSunGearCompoundCriticalSpeedAnalysis
        )

    @property
    def zerol_bevel_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6953.ZerolBevelGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6953,
        )

        return self.__parent__._cast(_6953.ZerolBevelGearCompoundCriticalSpeedAnalysis)

    @property
    def agma_gleason_conical_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis":
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
class AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis(
    _6857.ConicalGearCompoundCriticalSpeedAnalysis
):
    """AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR_COMPOUND_CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_6695.AGMAGleasonConicalGearCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.AGMAGleasonConicalGearCriticalSpeedAnalysis]

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
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6695.AGMAGleasonConicalGearCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.AGMAGleasonConicalGearCriticalSpeedAnalysis]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis
        """
        return _Cast_AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis(self)
