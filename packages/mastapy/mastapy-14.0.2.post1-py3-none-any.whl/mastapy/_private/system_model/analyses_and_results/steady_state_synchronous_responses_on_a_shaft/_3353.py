"""BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
    _3358,
)

_BEVEL_DIFFERENTIAL_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft",
    "BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2742
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _6976
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
        _3346,
        _3374,
        _3377,
        _3400,
        _3407,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2358

    Self = TypeVar(
        "Self", bound="BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft._Cast_BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft:
    """Special nested class for casting BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft to subclasses."""

    __parent__: "BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft"

    @property
    def bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3358.BevelGearMeshSteadyStateSynchronousResponseOnAShaft":
        return self.__parent__._cast(
            _3358.BevelGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def agma_gleason_conical_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3346.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3346,
        )

        return self.__parent__._cast(
            _3346.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def conical_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3374.ConicalGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3374,
        )

        return self.__parent__._cast(
            _3374.ConicalGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3400.GearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3400,
        )

        return self.__parent__._cast(
            _3400.GearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def inter_mountable_component_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> (
        "_3407.InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3407,
        )

        return self.__parent__._cast(
            _3407.InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3377.ConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3377,
        )

        return self.__parent__._cast(
            _3377.ConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7715.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7715,
        )

        return self.__parent__._cast(_7715.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7712.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7712,
        )

        return self.__parent__._cast(_7712.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2738.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2738

        return self.__parent__._cast(_2738.ConnectionAnalysis)

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
    def bevel_differential_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft":
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
class BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft(
    _3358.BevelGearMeshSteadyStateSynchronousResponseOnAShaft
):
    """BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _BEVEL_DIFFERENTIAL_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2358.BevelDifferentialGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_load_case(self: "Self") -> "_6976.BevelDifferentialGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft":
        """Cast to another type.

        Returns:
            _Cast_BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft
        """
        return _Cast_BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft(
            self
        )
