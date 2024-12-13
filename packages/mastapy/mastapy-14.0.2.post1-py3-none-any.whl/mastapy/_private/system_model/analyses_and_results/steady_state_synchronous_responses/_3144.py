"""KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
    _3109,
)

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
        "KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse",
    )
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740, _2742, _2746
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7719,
        _7722,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3076,
        _3136,
        _3143,
        _3145,
        _3147,
        _3150,
        _3158,
        _3177,
    )
    from mastapy._private.system_model.part_model.gears import _2598

    Self = TypeVar(
        "Self",
        bound="KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse._Cast_KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse:
    """Special nested class for casting KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse to subclasses."""

    __parent__: "KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse"

    @property
    def conical_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3109.ConicalGearSetSteadyStateSynchronousResponse":
        return self.__parent__._cast(_3109.ConicalGearSetSteadyStateSynchronousResponse)

    @property
    def gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3136.GearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3136,
        )

        return self.__parent__._cast(_3136.GearSetSteadyStateSynchronousResponse)

    @property
    def specialised_assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3177.SpecialisedAssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3177,
        )

        return self.__parent__._cast(
            _3177.SpecialisedAssemblySteadyStateSynchronousResponse
        )

    @property
    def abstract_assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3076.AbstractAssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3076,
        )

        return self.__parent__._cast(
            _3076.AbstractAssemblySteadyStateSynchronousResponse
        )

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
    def klingelnberg_cyclo_palloid_hypoid_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3147.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3147,
        )

        return self.__parent__._cast(
            _3147.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> (
        "_3150.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponse"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3150,
        )

        return self.__parent__._cast(
            _3150.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse":
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
class KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse(
    _3109.ConicalGearSetSteadyStateSynchronousResponse
):
    """KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2598.KlingelnbergCycloPalloidConicalGearSet":
        """mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def conical_gears_steady_state_synchronous_response(
        self: "Self",
    ) -> (
        "List[_3145.KlingelnbergCycloPalloidConicalGearSteadyStateSynchronousResponse]"
    ):
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.KlingelnbergCycloPalloidConicalGearSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ConicalGearsSteadyStateSynchronousResponse"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_conical_gears_steady_state_synchronous_response(
        self: "Self",
    ) -> (
        "List[_3145.KlingelnbergCycloPalloidConicalGearSteadyStateSynchronousResponse]"
    ):
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.KlingelnbergCycloPalloidConicalGearSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "KlingelnbergCycloPalloidConicalGearsSteadyStateSynchronousResponse",
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def conical_meshes_steady_state_synchronous_response(
        self: "Self",
    ) -> "List[_3143.KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ConicalMeshesSteadyStateSynchronousResponse"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_conical_meshes_steady_state_synchronous_response(
        self: "Self",
    ) -> "List[_3143.KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "KlingelnbergCycloPalloidConicalMeshesSteadyStateSynchronousResponse",
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse
        """
        return (
            _Cast_KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse(
                self
            )
        )
