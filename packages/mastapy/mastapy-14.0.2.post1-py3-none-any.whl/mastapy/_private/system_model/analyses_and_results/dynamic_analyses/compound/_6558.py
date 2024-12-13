"""AGMAGleasonConicalGearCompoundDynamicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
    _6586,
)

_AGMA_GLEASON_CONICAL_GEAR_COMPOUND_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound",
    "AGMAGleasonConicalGearCompoundDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6425,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6565,
        _6568,
        _6569,
        _6570,
        _6579,
        _6612,
        _6616,
        _6633,
        _6635,
        _6655,
        _6661,
        _6664,
        _6667,
        _6668,
        _6682,
    )

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearCompoundDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearCompoundDynamicAnalysis._Cast_AGMAGleasonConicalGearCompoundDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearCompoundDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearCompoundDynamicAnalysis:
    """Special nested class for casting AGMAGleasonConicalGearCompoundDynamicAnalysis to subclasses."""

    __parent__: "AGMAGleasonConicalGearCompoundDynamicAnalysis"

    @property
    def conical_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6586.ConicalGearCompoundDynamicAnalysis":
        return self.__parent__._cast(_6586.ConicalGearCompoundDynamicAnalysis)

    @property
    def gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6612.GearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6612,
        )

        return self.__parent__._cast(_6612.GearCompoundDynamicAnalysis)

    @property
    def mountable_component_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6633.MountableComponentCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6633,
        )

        return self.__parent__._cast(_6633.MountableComponentCompoundDynamicAnalysis)

    @property
    def component_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6579.ComponentCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6579,
        )

        return self.__parent__._cast(_6579.ComponentCompoundDynamicAnalysis)

    @property
    def part_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6635.PartCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6635,
        )

        return self.__parent__._cast(_6635.PartCompoundDynamicAnalysis)

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
    def bevel_differential_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6565.BevelDifferentialGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6565,
        )

        return self.__parent__._cast(_6565.BevelDifferentialGearCompoundDynamicAnalysis)

    @property
    def bevel_differential_planet_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6568.BevelDifferentialPlanetGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6568,
        )

        return self.__parent__._cast(
            _6568.BevelDifferentialPlanetGearCompoundDynamicAnalysis
        )

    @property
    def bevel_differential_sun_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6569.BevelDifferentialSunGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6569,
        )

        return self.__parent__._cast(
            _6569.BevelDifferentialSunGearCompoundDynamicAnalysis
        )

    @property
    def bevel_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6570.BevelGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6570,
        )

        return self.__parent__._cast(_6570.BevelGearCompoundDynamicAnalysis)

    @property
    def hypoid_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6616.HypoidGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6616,
        )

        return self.__parent__._cast(_6616.HypoidGearCompoundDynamicAnalysis)

    @property
    def spiral_bevel_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6655.SpiralBevelGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6655,
        )

        return self.__parent__._cast(_6655.SpiralBevelGearCompoundDynamicAnalysis)

    @property
    def straight_bevel_diff_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6661.StraightBevelDiffGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6661,
        )

        return self.__parent__._cast(_6661.StraightBevelDiffGearCompoundDynamicAnalysis)

    @property
    def straight_bevel_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6664.StraightBevelGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6664,
        )

        return self.__parent__._cast(_6664.StraightBevelGearCompoundDynamicAnalysis)

    @property
    def straight_bevel_planet_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6667.StraightBevelPlanetGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6667,
        )

        return self.__parent__._cast(
            _6667.StraightBevelPlanetGearCompoundDynamicAnalysis
        )

    @property
    def straight_bevel_sun_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6668.StraightBevelSunGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6668,
        )

        return self.__parent__._cast(_6668.StraightBevelSunGearCompoundDynamicAnalysis)

    @property
    def zerol_bevel_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6682.ZerolBevelGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6682,
        )

        return self.__parent__._cast(_6682.ZerolBevelGearCompoundDynamicAnalysis)

    @property
    def agma_gleason_conical_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearCompoundDynamicAnalysis":
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
class AGMAGleasonConicalGearCompoundDynamicAnalysis(
    _6586.ConicalGearCompoundDynamicAnalysis
):
    """AGMAGleasonConicalGearCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR_COMPOUND_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_6425.AGMAGleasonConicalGearDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.AGMAGleasonConicalGearDynamicAnalysis]

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
    ) -> "List[_6425.AGMAGleasonConicalGearDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.AGMAGleasonConicalGearDynamicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalGearCompoundDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearCompoundDynamicAnalysis
        """
        return _Cast_AGMAGleasonConicalGearCompoundDynamicAnalysis(self)
