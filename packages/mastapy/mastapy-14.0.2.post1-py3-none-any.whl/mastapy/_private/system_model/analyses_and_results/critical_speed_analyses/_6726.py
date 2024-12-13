"""ConnectionCriticalSpeedAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7715

_CONNECTION_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses",
    "ConnectionCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2742
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7712
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6694,
        _6696,
        _6700,
        _6703,
        _6708,
        _6712,
        _6715,
        _6717,
        _6721,
        _6724,
        _6728,
        _6731,
        _6734,
        _6738,
        _6740,
        _6742,
        _6748,
        _6753,
        _6757,
        _6759,
        _6761,
        _6764,
        _6767,
        _6776,
        _6779,
        _6786,
        _6788,
        _6793,
        _6796,
        _6798,
        _6802,
        _6805,
        _6813,
        _6820,
        _6823,
    )
    from mastapy._private.system_model.connections_and_sockets import _2329

    Self = TypeVar("Self", bound="ConnectionCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConnectionCriticalSpeedAnalysis._Cast_ConnectionCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionCriticalSpeedAnalysis:
    """Special nested class for casting ConnectionCriticalSpeedAnalysis to subclasses."""

    __parent__: "ConnectionCriticalSpeedAnalysis"

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7715.ConnectionStaticLoadAnalysisCase":
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
    def abstract_shaft_to_mountable_component_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6694.AbstractShaftToMountableComponentConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6694,
        )

        return self.__parent__._cast(
            _6694.AbstractShaftToMountableComponentConnectionCriticalSpeedAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6696.AGMAGleasonConicalGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6696,
        )

        return self.__parent__._cast(
            _6696.AGMAGleasonConicalGearMeshCriticalSpeedAnalysis
        )

    @property
    def belt_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6700.BeltConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6700,
        )

        return self.__parent__._cast(_6700.BeltConnectionCriticalSpeedAnalysis)

    @property
    def bevel_differential_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6703.BevelDifferentialGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6703,
        )

        return self.__parent__._cast(
            _6703.BevelDifferentialGearMeshCriticalSpeedAnalysis
        )

    @property
    def bevel_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6708.BevelGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6708,
        )

        return self.__parent__._cast(_6708.BevelGearMeshCriticalSpeedAnalysis)

    @property
    def clutch_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6712.ClutchConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6712,
        )

        return self.__parent__._cast(_6712.ClutchConnectionCriticalSpeedAnalysis)

    @property
    def coaxial_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6715.CoaxialConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6715,
        )

        return self.__parent__._cast(_6715.CoaxialConnectionCriticalSpeedAnalysis)

    @property
    def concept_coupling_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6717.ConceptCouplingConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6717,
        )

        return self.__parent__._cast(
            _6717.ConceptCouplingConnectionCriticalSpeedAnalysis
        )

    @property
    def concept_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6721.ConceptGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6721,
        )

        return self.__parent__._cast(_6721.ConceptGearMeshCriticalSpeedAnalysis)

    @property
    def conical_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6724.ConicalGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6724,
        )

        return self.__parent__._cast(_6724.ConicalGearMeshCriticalSpeedAnalysis)

    @property
    def coupling_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6728.CouplingConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6728,
        )

        return self.__parent__._cast(_6728.CouplingConnectionCriticalSpeedAnalysis)

    @property
    def cvt_belt_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6734.CVTBeltConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6734,
        )

        return self.__parent__._cast(_6734.CVTBeltConnectionCriticalSpeedAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6738.CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6738,
        )

        return self.__parent__._cast(
            _6738.CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6740.CycloidalDiscPlanetaryBearingConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6740,
        )

        return self.__parent__._cast(
            _6740.CycloidalDiscPlanetaryBearingConnectionCriticalSpeedAnalysis
        )

    @property
    def cylindrical_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6742.CylindricalGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6742,
        )

        return self.__parent__._cast(_6742.CylindricalGearMeshCriticalSpeedAnalysis)

    @property
    def face_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6748.FaceGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6748,
        )

        return self.__parent__._cast(_6748.FaceGearMeshCriticalSpeedAnalysis)

    @property
    def gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6753.GearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6753,
        )

        return self.__parent__._cast(_6753.GearMeshCriticalSpeedAnalysis)

    @property
    def hypoid_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6757.HypoidGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6757,
        )

        return self.__parent__._cast(_6757.HypoidGearMeshCriticalSpeedAnalysis)

    @property
    def inter_mountable_component_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6759.InterMountableComponentConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6759,
        )

        return self.__parent__._cast(
            _6759.InterMountableComponentConnectionCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6761.KlingelnbergCycloPalloidConicalGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6761,
        )

        return self.__parent__._cast(
            _6761.KlingelnbergCycloPalloidConicalGearMeshCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6764.KlingelnbergCycloPalloidHypoidGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6764,
        )

        return self.__parent__._cast(
            _6764.KlingelnbergCycloPalloidHypoidGearMeshCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6767.KlingelnbergCycloPalloidSpiralBevelGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6767,
        )

        return self.__parent__._cast(
            _6767.KlingelnbergCycloPalloidSpiralBevelGearMeshCriticalSpeedAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6776.PartToPartShearCouplingConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6776,
        )

        return self.__parent__._cast(
            _6776.PartToPartShearCouplingConnectionCriticalSpeedAnalysis
        )

    @property
    def planetary_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6779.PlanetaryConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6779,
        )

        return self.__parent__._cast(_6779.PlanetaryConnectionCriticalSpeedAnalysis)

    @property
    def ring_pins_to_disc_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6786.RingPinsToDiscConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6786,
        )

        return self.__parent__._cast(
            _6786.RingPinsToDiscConnectionCriticalSpeedAnalysis
        )

    @property
    def rolling_ring_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6788.RollingRingConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6788,
        )

        return self.__parent__._cast(_6788.RollingRingConnectionCriticalSpeedAnalysis)

    @property
    def shaft_to_mountable_component_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6793.ShaftToMountableComponentConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6793,
        )

        return self.__parent__._cast(
            _6793.ShaftToMountableComponentConnectionCriticalSpeedAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6796.SpiralBevelGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6796,
        )

        return self.__parent__._cast(_6796.SpiralBevelGearMeshCriticalSpeedAnalysis)

    @property
    def spring_damper_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6798.SpringDamperConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6798,
        )

        return self.__parent__._cast(_6798.SpringDamperConnectionCriticalSpeedAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6802.StraightBevelDiffGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6802,
        )

        return self.__parent__._cast(
            _6802.StraightBevelDiffGearMeshCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6805.StraightBevelGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6805,
        )

        return self.__parent__._cast(_6805.StraightBevelGearMeshCriticalSpeedAnalysis)

    @property
    def torque_converter_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6813.TorqueConverterConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6813,
        )

        return self.__parent__._cast(
            _6813.TorqueConverterConnectionCriticalSpeedAnalysis
        )

    @property
    def worm_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6820.WormGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6820,
        )

        return self.__parent__._cast(_6820.WormGearMeshCriticalSpeedAnalysis)

    @property
    def zerol_bevel_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6823.ZerolBevelGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6823,
        )

        return self.__parent__._cast(_6823.ZerolBevelGearMeshCriticalSpeedAnalysis)

    @property
    def connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "ConnectionCriticalSpeedAnalysis":
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
class ConnectionCriticalSpeedAnalysis(_7715.ConnectionStaticLoadAnalysisCase):
    """ConnectionCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION_CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2329.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_design(self: "Self") -> "_2329.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def critical_speed_analysis(self: "Self") -> "_6731.CriticalSpeedAnalysis":
        """mastapy.system_model.analyses_and_results.critical_speed_analyses.CriticalSpeedAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CriticalSpeedAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConnectionCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConnectionCriticalSpeedAnalysis
        """
        return _Cast_ConnectionCriticalSpeedAnalysis(self)
