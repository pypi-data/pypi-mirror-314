"""GearCompoundSteadyStateSynchronousResponseOnAShaft"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
    _3553,
)

_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound",
    "GearCompoundSteadyStateSynchronousResponseOnAShaft",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
        _3402,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
        _3478,
        _3485,
        _3488,
        _3489,
        _3490,
        _3499,
        _3503,
        _3506,
        _3521,
        _3524,
        _3527,
        _3536,
        _3540,
        _3543,
        _3546,
        _3555,
        _3575,
        _3581,
        _3584,
        _3587,
        _3588,
        _3599,
        _3602,
    )

    Self = TypeVar("Self", bound="GearCompoundSteadyStateSynchronousResponseOnAShaft")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearCompoundSteadyStateSynchronousResponseOnAShaft._Cast_GearCompoundSteadyStateSynchronousResponseOnAShaft",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearCompoundSteadyStateSynchronousResponseOnAShaft",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearCompoundSteadyStateSynchronousResponseOnAShaft:
    """Special nested class for casting GearCompoundSteadyStateSynchronousResponseOnAShaft to subclasses."""

    __parent__: "GearCompoundSteadyStateSynchronousResponseOnAShaft"

    @property
    def mountable_component_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3553.MountableComponentCompoundSteadyStateSynchronousResponseOnAShaft":
        return self.__parent__._cast(
            _3553.MountableComponentCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def component_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3499.ComponentCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3499,
        )

        return self.__parent__._cast(
            _3499.ComponentCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def part_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3555.PartCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3555,
        )

        return self.__parent__._cast(
            _3555.PartCompoundSteadyStateSynchronousResponseOnAShaft
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
    def agma_gleason_conical_gear_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3478.AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3478,
        )

        return self.__parent__._cast(
            _3478.AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_differential_gear_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3485.BevelDifferentialGearCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3485,
        )

        return self.__parent__._cast(
            _3485.BevelDifferentialGearCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_differential_planet_gear_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3488.BevelDifferentialPlanetGearCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3488,
        )

        return self.__parent__._cast(
            _3488.BevelDifferentialPlanetGearCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_differential_sun_gear_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3489.BevelDifferentialSunGearCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3489,
        )

        return self.__parent__._cast(
            _3489.BevelDifferentialSunGearCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_gear_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3490.BevelGearCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3490,
        )

        return self.__parent__._cast(
            _3490.BevelGearCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def concept_gear_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3503.ConceptGearCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3503,
        )

        return self.__parent__._cast(
            _3503.ConceptGearCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def conical_gear_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3506.ConicalGearCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3506,
        )

        return self.__parent__._cast(
            _3506.ConicalGearCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cylindrical_gear_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3521.CylindricalGearCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3521,
        )

        return self.__parent__._cast(
            _3521.CylindricalGearCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cylindrical_planet_gear_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3524.CylindricalPlanetGearCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3524,
        )

        return self.__parent__._cast(
            _3524.CylindricalPlanetGearCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def face_gear_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3527.FaceGearCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3527,
        )

        return self.__parent__._cast(
            _3527.FaceGearCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def hypoid_gear_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3536.HypoidGearCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3536,
        )

        return self.__parent__._cast(
            _3536.HypoidGearCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3540.KlingelnbergCycloPalloidConicalGearCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3540,
        )

        return self.__parent__._cast(
            _3540.KlingelnbergCycloPalloidConicalGearCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3543.KlingelnbergCycloPalloidHypoidGearCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3543,
        )

        return self.__parent__._cast(
            _3543.KlingelnbergCycloPalloidHypoidGearCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3546.KlingelnbergCycloPalloidSpiralBevelGearCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3546,
        )

        return self.__parent__._cast(
            _3546.KlingelnbergCycloPalloidSpiralBevelGearCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def spiral_bevel_gear_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3575.SpiralBevelGearCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3575,
        )

        return self.__parent__._cast(
            _3575.SpiralBevelGearCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_diff_gear_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3581.StraightBevelDiffGearCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3581,
        )

        return self.__parent__._cast(
            _3581.StraightBevelDiffGearCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_gear_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3584.StraightBevelGearCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3584,
        )

        return self.__parent__._cast(
            _3584.StraightBevelGearCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_planet_gear_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3587.StraightBevelPlanetGearCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3587,
        )

        return self.__parent__._cast(
            _3587.StraightBevelPlanetGearCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_sun_gear_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3588.StraightBevelSunGearCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3588,
        )

        return self.__parent__._cast(
            _3588.StraightBevelSunGearCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def worm_gear_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3599.WormGearCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3599,
        )

        return self.__parent__._cast(
            _3599.WormGearCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def zerol_bevel_gear_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3602.ZerolBevelGearCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3602,
        )

        return self.__parent__._cast(
            _3602.ZerolBevelGearCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def gear_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "GearCompoundSteadyStateSynchronousResponseOnAShaft":
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
class GearCompoundSteadyStateSynchronousResponseOnAShaft(
    _3553.MountableComponentCompoundSteadyStateSynchronousResponseOnAShaft
):
    """GearCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_3402.GearSteadyStateSynchronousResponseOnAShaft]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.GearSteadyStateSynchronousResponseOnAShaft]

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
    ) -> "List[_3402.GearSteadyStateSynchronousResponseOnAShaft]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.GearSteadyStateSynchronousResponseOnAShaft]

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
    ) -> "_Cast_GearCompoundSteadyStateSynchronousResponseOnAShaft":
        """Cast to another type.

        Returns:
            _Cast_GearCompoundSteadyStateSynchronousResponseOnAShaft
        """
        return _Cast_GearCompoundSteadyStateSynchronousResponseOnAShaft(self)
