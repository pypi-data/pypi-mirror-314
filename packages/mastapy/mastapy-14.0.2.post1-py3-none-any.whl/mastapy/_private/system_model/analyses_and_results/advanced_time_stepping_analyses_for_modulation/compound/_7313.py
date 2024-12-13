"""BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
    _7301,
)

_BEVEL_GEAR_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound",
    "BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7181,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
        _7308,
        _7311,
        _7312,
        _7322,
        _7329,
        _7355,
        _7376,
        _7378,
        _7398,
        _7404,
        _7407,
        _7410,
        _7411,
        _7425,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )

    Self = TypeVar(
        "Self", bound="BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation:
    """Special nested class for casting BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation to subclasses."""

    __parent__: "BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation"

    @property
    def agma_gleason_conical_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> (
        "_7301.AGMAGleasonConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation"
    ):
        return self.__parent__._cast(
            _7301.AGMAGleasonConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def conical_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7329.ConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7329,
        )

        return self.__parent__._cast(
            _7329.ConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7355.GearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7355,
        )

        return self.__parent__._cast(
            _7355.GearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def mountable_component_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7376.MountableComponentCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7376,
        )

        return self.__parent__._cast(
            _7376.MountableComponentCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def component_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7322.ComponentCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7322,
        )

        return self.__parent__._cast(
            _7322.ComponentCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7378.PartCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7378,
        )

        return self.__parent__._cast(
            _7378.PartCompoundAdvancedTimeSteppingAnalysisForModulation
        )

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
    def bevel_differential_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7308.BevelDifferentialGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7308,
        )

        return self.__parent__._cast(
            _7308.BevelDifferentialGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_differential_planet_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7311.BevelDifferentialPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7311,
        )

        return self.__parent__._cast(
            _7311.BevelDifferentialPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_differential_sun_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7312.BevelDifferentialSunGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7312,
        )

        return self.__parent__._cast(
            _7312.BevelDifferentialSunGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spiral_bevel_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7398.SpiralBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7398,
        )

        return self.__parent__._cast(
            _7398.SpiralBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_diff_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7404.StraightBevelDiffGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7404,
        )

        return self.__parent__._cast(
            _7404.StraightBevelDiffGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7407.StraightBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7407,
        )

        return self.__parent__._cast(
            _7407.StraightBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_planet_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> (
        "_7410.StraightBevelPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation"
    ):
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7410,
        )

        return self.__parent__._cast(
            _7410.StraightBevelPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_sun_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7411.StraightBevelSunGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7411,
        )

        return self.__parent__._cast(
            _7411.StraightBevelSunGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def zerol_bevel_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7425.ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7425,
        )

        return self.__parent__._cast(
            _7425.ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation":
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
class BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation(
    _7301.AGMAGleasonConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation
):
    """BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _BEVEL_GEAR_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_7181.BevelGearAdvancedTimeSteppingAnalysisForModulation]":
        """List[mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.BevelGearAdvancedTimeSteppingAnalysisForModulation]

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
    ) -> "List[_7181.BevelGearAdvancedTimeSteppingAnalysisForModulation]":
        """List[mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.BevelGearAdvancedTimeSteppingAnalysisForModulation]

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
    ) -> "_Cast_BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        """Cast to another type.

        Returns:
            _Cast_BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation
        """
        return _Cast_BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation(self)
