"""BevelDifferentialGearSteadyStateSynchronousResponse"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
    _3094,
)

_BEVEL_DIFFERENTIAL_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
    "BevelDifferentialGearSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740, _2742, _2746
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7719,
        _7722,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _6975
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3082,
        _3090,
        _3091,
        _3101,
        _3110,
        _3137,
        _3156,
        _3158,
    )
    from mastapy._private.system_model.part_model.gears import _2576

    Self = TypeVar("Self", bound="BevelDifferentialGearSteadyStateSynchronousResponse")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelDifferentialGearSteadyStateSynchronousResponse._Cast_BevelDifferentialGearSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelDifferentialGearSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelDifferentialGearSteadyStateSynchronousResponse:
    """Special nested class for casting BevelDifferentialGearSteadyStateSynchronousResponse to subclasses."""

    __parent__: "BevelDifferentialGearSteadyStateSynchronousResponse"

    @property
    def bevel_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3094.BevelGearSteadyStateSynchronousResponse":
        return self.__parent__._cast(_3094.BevelGearSteadyStateSynchronousResponse)

    @property
    def agma_gleason_conical_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3082.AGMAGleasonConicalGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3082,
        )

        return self.__parent__._cast(
            _3082.AGMAGleasonConicalGearSteadyStateSynchronousResponse
        )

    @property
    def conical_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3110.ConicalGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3110,
        )

        return self.__parent__._cast(_3110.ConicalGearSteadyStateSynchronousResponse)

    @property
    def gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3137.GearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3137,
        )

        return self.__parent__._cast(_3137.GearSteadyStateSynchronousResponse)

    @property
    def mountable_component_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3156.MountableComponentSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3156,
        )

        return self.__parent__._cast(
            _3156.MountableComponentSteadyStateSynchronousResponse
        )

    @property
    def component_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3101.ComponentSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3101,
        )

        return self.__parent__._cast(_3101.ComponentSteadyStateSynchronousResponse)

    @property
    def part_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3158.PartSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3158,
        )

        return self.__parent__._cast(_3158.PartSteadyStateSynchronousResponse)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7722.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7722,
        )

        return self.__parent__._cast(_7722.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7719.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7719,
        )

        return self.__parent__._cast(_7719.PartAnalysisCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2746.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2746

        return self.__parent__._cast(_2746.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2742.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2742

        return self.__parent__._cast(_2742.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2740.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2740

        return self.__parent__._cast(_2740.DesignEntityAnalysis)

    @property
    def bevel_differential_planet_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3090.BevelDifferentialPlanetGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3090,
        )

        return self.__parent__._cast(
            _3090.BevelDifferentialPlanetGearSteadyStateSynchronousResponse
        )

    @property
    def bevel_differential_sun_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3091.BevelDifferentialSunGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3091,
        )

        return self.__parent__._cast(
            _3091.BevelDifferentialSunGearSteadyStateSynchronousResponse
        )

    @property
    def bevel_differential_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "BevelDifferentialGearSteadyStateSynchronousResponse":
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
class BevelDifferentialGearSteadyStateSynchronousResponse(
    _3094.BevelGearSteadyStateSynchronousResponse
):
    """BevelDifferentialGearSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_DIFFERENTIAL_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2576.BevelDifferentialGear":
        """mastapy.system_model.part_model.gears.BevelDifferentialGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: "Self") -> "_6975.BevelDifferentialGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_BevelDifferentialGearSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_BevelDifferentialGearSteadyStateSynchronousResponse
        """
        return _Cast_BevelDifferentialGearSteadyStateSynchronousResponse(self)
