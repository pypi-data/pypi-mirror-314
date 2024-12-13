"""GearCompoundAdvancedSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
    _7645,
)

_GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound",
    "GearCompoundAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating import _370
    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7491,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
        _7570,
        _7577,
        _7580,
        _7581,
        _7582,
        _7591,
        _7595,
        _7598,
        _7613,
        _7616,
        _7619,
        _7628,
        _7632,
        _7635,
        _7638,
        _7647,
        _7667,
        _7673,
        _7676,
        _7679,
        _7680,
        _7691,
        _7694,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )

    Self = TypeVar("Self", bound="GearCompoundAdvancedSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearCompoundAdvancedSystemDeflection._Cast_GearCompoundAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearCompoundAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearCompoundAdvancedSystemDeflection:
    """Special nested class for casting GearCompoundAdvancedSystemDeflection to subclasses."""

    __parent__: "GearCompoundAdvancedSystemDeflection"

    @property
    def mountable_component_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7645.MountableComponentCompoundAdvancedSystemDeflection":
        return self.__parent__._cast(
            _7645.MountableComponentCompoundAdvancedSystemDeflection
        )

    @property
    def component_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7591.ComponentCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7591,
        )

        return self.__parent__._cast(_7591.ComponentCompoundAdvancedSystemDeflection)

    @property
    def part_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7647.PartCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7647,
        )

        return self.__parent__._cast(_7647.PartCompoundAdvancedSystemDeflection)

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
    def agma_gleason_conical_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7570.AGMAGleasonConicalGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7570,
        )

        return self.__parent__._cast(
            _7570.AGMAGleasonConicalGearCompoundAdvancedSystemDeflection
        )

    @property
    def bevel_differential_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7577.BevelDifferentialGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7577,
        )

        return self.__parent__._cast(
            _7577.BevelDifferentialGearCompoundAdvancedSystemDeflection
        )

    @property
    def bevel_differential_planet_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7580.BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7580,
        )

        return self.__parent__._cast(
            _7580.BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection
        )

    @property
    def bevel_differential_sun_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7581.BevelDifferentialSunGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7581,
        )

        return self.__parent__._cast(
            _7581.BevelDifferentialSunGearCompoundAdvancedSystemDeflection
        )

    @property
    def bevel_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7582.BevelGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7582,
        )

        return self.__parent__._cast(_7582.BevelGearCompoundAdvancedSystemDeflection)

    @property
    def concept_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7595.ConceptGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7595,
        )

        return self.__parent__._cast(_7595.ConceptGearCompoundAdvancedSystemDeflection)

    @property
    def conical_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7598.ConicalGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7598,
        )

        return self.__parent__._cast(_7598.ConicalGearCompoundAdvancedSystemDeflection)

    @property
    def cylindrical_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7613.CylindricalGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7613,
        )

        return self.__parent__._cast(
            _7613.CylindricalGearCompoundAdvancedSystemDeflection
        )

    @property
    def cylindrical_planet_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7616.CylindricalPlanetGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7616,
        )

        return self.__parent__._cast(
            _7616.CylindricalPlanetGearCompoundAdvancedSystemDeflection
        )

    @property
    def face_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7619.FaceGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7619,
        )

        return self.__parent__._cast(_7619.FaceGearCompoundAdvancedSystemDeflection)

    @property
    def hypoid_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7628.HypoidGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7628,
        )

        return self.__parent__._cast(_7628.HypoidGearCompoundAdvancedSystemDeflection)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7632.KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7632,
        )

        return self.__parent__._cast(
            _7632.KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7635.KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7635,
        )

        return self.__parent__._cast(
            _7635.KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> (
        "_7638.KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedSystemDeflection"
    ):
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7638,
        )

        return self.__parent__._cast(
            _7638.KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedSystemDeflection
        )

    @property
    def spiral_bevel_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7667.SpiralBevelGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7667,
        )

        return self.__parent__._cast(
            _7667.SpiralBevelGearCompoundAdvancedSystemDeflection
        )

    @property
    def straight_bevel_diff_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7673.StraightBevelDiffGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7673,
        )

        return self.__parent__._cast(
            _7673.StraightBevelDiffGearCompoundAdvancedSystemDeflection
        )

    @property
    def straight_bevel_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7676.StraightBevelGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7676,
        )

        return self.__parent__._cast(
            _7676.StraightBevelGearCompoundAdvancedSystemDeflection
        )

    @property
    def straight_bevel_planet_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7679.StraightBevelPlanetGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7679,
        )

        return self.__parent__._cast(
            _7679.StraightBevelPlanetGearCompoundAdvancedSystemDeflection
        )

    @property
    def straight_bevel_sun_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7680.StraightBevelSunGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7680,
        )

        return self.__parent__._cast(
            _7680.StraightBevelSunGearCompoundAdvancedSystemDeflection
        )

    @property
    def worm_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7691.WormGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7691,
        )

        return self.__parent__._cast(_7691.WormGearCompoundAdvancedSystemDeflection)

    @property
    def zerol_bevel_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7694.ZerolBevelGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7694,
        )

        return self.__parent__._cast(
            _7694.ZerolBevelGearCompoundAdvancedSystemDeflection
        )

    @property
    def gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "GearCompoundAdvancedSystemDeflection":
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
class GearCompoundAdvancedSystemDeflection(
    _7645.MountableComponentCompoundAdvancedSystemDeflection
):
    """GearCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def gear_duty_cycle_rating(self: "Self") -> "_370.GearDutyCycleRating":
        """mastapy.gears.rating.GearDutyCycleRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearDutyCycleRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_7491.GearAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.GearAdvancedSystemDeflection]

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
    ) -> "List[_7491.GearAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.GearAdvancedSystemDeflection]

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
    def cast_to(self: "Self") -> "_Cast_GearCompoundAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_GearCompoundAdvancedSystemDeflection
        """
        return _Cast_GearCompoundAdvancedSystemDeflection(self)
