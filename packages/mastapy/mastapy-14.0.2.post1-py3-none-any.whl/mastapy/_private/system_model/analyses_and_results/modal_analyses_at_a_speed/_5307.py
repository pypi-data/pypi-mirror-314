"""InterMountableComponentConnectionModalAnalysisAtASpeed"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
    _5277,
)

_INTER_MOUNTABLE_COMPONENT_CONNECTION_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed",
    "InterMountableComponentConnectionModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2742
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5246,
        _5251,
        _5253,
        _5258,
        _5263,
        _5268,
        _5271,
        _5274,
        _5279,
        _5282,
        _5289,
        _5295,
        _5300,
        _5304,
        _5308,
        _5311,
        _5314,
        _5325,
        _5335,
        _5337,
        _5344,
        _5347,
        _5350,
        _5353,
        _5362,
        _5368,
        _5371,
    )
    from mastapy._private.system_model.connections_and_sockets import _2338

    Self = TypeVar(
        "Self", bound="InterMountableComponentConnectionModalAnalysisAtASpeed"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterMountableComponentConnectionModalAnalysisAtASpeed._Cast_InterMountableComponentConnectionModalAnalysisAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnectionModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterMountableComponentConnectionModalAnalysisAtASpeed:
    """Special nested class for casting InterMountableComponentConnectionModalAnalysisAtASpeed to subclasses."""

    __parent__: "InterMountableComponentConnectionModalAnalysisAtASpeed"

    @property
    def connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5277.ConnectionModalAnalysisAtASpeed":
        return self.__parent__._cast(_5277.ConnectionModalAnalysisAtASpeed)

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
    def agma_gleason_conical_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5246.AGMAGleasonConicalGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5246,
        )

        return self.__parent__._cast(
            _5246.AGMAGleasonConicalGearMeshModalAnalysisAtASpeed
        )

    @property
    def belt_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5251.BeltConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5251,
        )

        return self.__parent__._cast(_5251.BeltConnectionModalAnalysisAtASpeed)

    @property
    def bevel_differential_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5253.BevelDifferentialGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5253,
        )

        return self.__parent__._cast(
            _5253.BevelDifferentialGearMeshModalAnalysisAtASpeed
        )

    @property
    def bevel_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5258.BevelGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5258,
        )

        return self.__parent__._cast(_5258.BevelGearMeshModalAnalysisAtASpeed)

    @property
    def clutch_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5263.ClutchConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5263,
        )

        return self.__parent__._cast(_5263.ClutchConnectionModalAnalysisAtASpeed)

    @property
    def concept_coupling_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5268.ConceptCouplingConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5268,
        )

        return self.__parent__._cast(
            _5268.ConceptCouplingConnectionModalAnalysisAtASpeed
        )

    @property
    def concept_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5271.ConceptGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5271,
        )

        return self.__parent__._cast(_5271.ConceptGearMeshModalAnalysisAtASpeed)

    @property
    def conical_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5274.ConicalGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5274,
        )

        return self.__parent__._cast(_5274.ConicalGearMeshModalAnalysisAtASpeed)

    @property
    def coupling_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5279.CouplingConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5279,
        )

        return self.__parent__._cast(_5279.CouplingConnectionModalAnalysisAtASpeed)

    @property
    def cvt_belt_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5282.CVTBeltConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5282,
        )

        return self.__parent__._cast(_5282.CVTBeltConnectionModalAnalysisAtASpeed)

    @property
    def cylindrical_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5289.CylindricalGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5289,
        )

        return self.__parent__._cast(_5289.CylindricalGearMeshModalAnalysisAtASpeed)

    @property
    def face_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5295.FaceGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5295,
        )

        return self.__parent__._cast(_5295.FaceGearMeshModalAnalysisAtASpeed)

    @property
    def gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5300.GearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5300,
        )

        return self.__parent__._cast(_5300.GearMeshModalAnalysisAtASpeed)

    @property
    def hypoid_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5304.HypoidGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5304,
        )

        return self.__parent__._cast(_5304.HypoidGearMeshModalAnalysisAtASpeed)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5308.KlingelnbergCycloPalloidConicalGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5308,
        )

        return self.__parent__._cast(
            _5308.KlingelnbergCycloPalloidConicalGearMeshModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5311.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5311,
        )

        return self.__parent__._cast(
            _5311.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5314.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5314,
        )

        return self.__parent__._cast(
            _5314.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysisAtASpeed
        )

    @property
    def part_to_part_shear_coupling_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5325.PartToPartShearCouplingConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5325,
        )

        return self.__parent__._cast(
            _5325.PartToPartShearCouplingConnectionModalAnalysisAtASpeed
        )

    @property
    def ring_pins_to_disc_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5335.RingPinsToDiscConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5335,
        )

        return self.__parent__._cast(
            _5335.RingPinsToDiscConnectionModalAnalysisAtASpeed
        )

    @property
    def rolling_ring_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5337.RollingRingConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5337,
        )

        return self.__parent__._cast(_5337.RollingRingConnectionModalAnalysisAtASpeed)

    @property
    def spiral_bevel_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5344.SpiralBevelGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5344,
        )

        return self.__parent__._cast(_5344.SpiralBevelGearMeshModalAnalysisAtASpeed)

    @property
    def spring_damper_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5347.SpringDamperConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5347,
        )

        return self.__parent__._cast(_5347.SpringDamperConnectionModalAnalysisAtASpeed)

    @property
    def straight_bevel_diff_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5350.StraightBevelDiffGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5350,
        )

        return self.__parent__._cast(
            _5350.StraightBevelDiffGearMeshModalAnalysisAtASpeed
        )

    @property
    def straight_bevel_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5353.StraightBevelGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5353,
        )

        return self.__parent__._cast(_5353.StraightBevelGearMeshModalAnalysisAtASpeed)

    @property
    def torque_converter_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5362.TorqueConverterConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5362,
        )

        return self.__parent__._cast(
            _5362.TorqueConverterConnectionModalAnalysisAtASpeed
        )

    @property
    def worm_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5368.WormGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5368,
        )

        return self.__parent__._cast(_5368.WormGearMeshModalAnalysisAtASpeed)

    @property
    def zerol_bevel_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5371.ZerolBevelGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5371,
        )

        return self.__parent__._cast(_5371.ZerolBevelGearMeshModalAnalysisAtASpeed)

    @property
    def inter_mountable_component_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "InterMountableComponentConnectionModalAnalysisAtASpeed":
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
class InterMountableComponentConnectionModalAnalysisAtASpeed(
    _5277.ConnectionModalAnalysisAtASpeed
):
    """InterMountableComponentConnectionModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _INTER_MOUNTABLE_COMPONENT_CONNECTION_MODAL_ANALYSIS_AT_A_SPEED
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2338.InterMountableComponentConnection":
        """mastapy.system_model.connections_and_sockets.InterMountableComponentConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_InterMountableComponentConnectionModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_InterMountableComponentConnectionModalAnalysisAtASpeed
        """
        return _Cast_InterMountableComponentConnectionModalAnalysisAtASpeed(self)
