"""ConnectionModalAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7715

_CONNECTION_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "ConnectionModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2742
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7712
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4692,
        _4693,
        _4698,
        _4700,
        _4705,
        _4710,
        _4713,
        _4715,
        _4718,
        _4721,
        _4727,
        _4730,
        _4734,
        _4736,
        _4737,
        _4746,
        _4752,
        _4756,
        _4759,
        _4760,
        _4763,
        _4766,
        _4773,
        _4782,
        _4785,
        _4792,
        _4794,
        _4800,
        _4802,
        _4805,
        _4808,
        _4811,
        _4820,
        _4829,
        _4832,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
        _4845,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2816,
    )
    from mastapy._private.system_model.connections_and_sockets import _2329

    Self = TypeVar("Self", bound="ConnectionModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="ConnectionModalAnalysis._Cast_ConnectionModalAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionModalAnalysis:
    """Special nested class for casting ConnectionModalAnalysis to subclasses."""

    __parent__: "ConnectionModalAnalysis"

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
    def abstract_shaft_to_mountable_component_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4692.AbstractShaftToMountableComponentConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4692,
        )

        return self.__parent__._cast(
            _4692.AbstractShaftToMountableComponentConnectionModalAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4693.AGMAGleasonConicalGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4693,
        )

        return self.__parent__._cast(_4693.AGMAGleasonConicalGearMeshModalAnalysis)

    @property
    def belt_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4698.BeltConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4698,
        )

        return self.__parent__._cast(_4698.BeltConnectionModalAnalysis)

    @property
    def bevel_differential_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4700.BevelDifferentialGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4700,
        )

        return self.__parent__._cast(_4700.BevelDifferentialGearMeshModalAnalysis)

    @property
    def bevel_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4705.BevelGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4705,
        )

        return self.__parent__._cast(_4705.BevelGearMeshModalAnalysis)

    @property
    def clutch_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4710.ClutchConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4710,
        )

        return self.__parent__._cast(_4710.ClutchConnectionModalAnalysis)

    @property
    def coaxial_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4713.CoaxialConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4713,
        )

        return self.__parent__._cast(_4713.CoaxialConnectionModalAnalysis)

    @property
    def concept_coupling_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4715.ConceptCouplingConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4715,
        )

        return self.__parent__._cast(_4715.ConceptCouplingConnectionModalAnalysis)

    @property
    def concept_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4718.ConceptGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4718,
        )

        return self.__parent__._cast(_4718.ConceptGearMeshModalAnalysis)

    @property
    def conical_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4721.ConicalGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4721,
        )

        return self.__parent__._cast(_4721.ConicalGearMeshModalAnalysis)

    @property
    def coupling_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4727.CouplingConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4727,
        )

        return self.__parent__._cast(_4727.CouplingConnectionModalAnalysis)

    @property
    def cvt_belt_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4730.CVTBeltConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4730,
        )

        return self.__parent__._cast(_4730.CVTBeltConnectionModalAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4734.CycloidalDiscCentralBearingConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4734,
        )

        return self.__parent__._cast(
            _4734.CycloidalDiscCentralBearingConnectionModalAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4736.CycloidalDiscPlanetaryBearingConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4736,
        )

        return self.__parent__._cast(
            _4736.CycloidalDiscPlanetaryBearingConnectionModalAnalysis
        )

    @property
    def cylindrical_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4737.CylindricalGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4737,
        )

        return self.__parent__._cast(_4737.CylindricalGearMeshModalAnalysis)

    @property
    def face_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4746.FaceGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4746,
        )

        return self.__parent__._cast(_4746.FaceGearMeshModalAnalysis)

    @property
    def gear_mesh_modal_analysis(self: "CastSelf") -> "_4752.GearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4752,
        )

        return self.__parent__._cast(_4752.GearMeshModalAnalysis)

    @property
    def hypoid_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4756.HypoidGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4756,
        )

        return self.__parent__._cast(_4756.HypoidGearMeshModalAnalysis)

    @property
    def inter_mountable_component_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4759.InterMountableComponentConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4759,
        )

        return self.__parent__._cast(
            _4759.InterMountableComponentConnectionModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4760.KlingelnbergCycloPalloidConicalGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4760,
        )

        return self.__parent__._cast(
            _4760.KlingelnbergCycloPalloidConicalGearMeshModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4763.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4763,
        )

        return self.__parent__._cast(
            _4763.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4766.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4766,
        )

        return self.__parent__._cast(
            _4766.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4782.PartToPartShearCouplingConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4782,
        )

        return self.__parent__._cast(
            _4782.PartToPartShearCouplingConnectionModalAnalysis
        )

    @property
    def planetary_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4785.PlanetaryConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4785,
        )

        return self.__parent__._cast(_4785.PlanetaryConnectionModalAnalysis)

    @property
    def ring_pins_to_disc_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4792.RingPinsToDiscConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4792,
        )

        return self.__parent__._cast(_4792.RingPinsToDiscConnectionModalAnalysis)

    @property
    def rolling_ring_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4794.RollingRingConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4794,
        )

        return self.__parent__._cast(_4794.RollingRingConnectionModalAnalysis)

    @property
    def shaft_to_mountable_component_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4800.ShaftToMountableComponentConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4800,
        )

        return self.__parent__._cast(
            _4800.ShaftToMountableComponentConnectionModalAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4802.SpiralBevelGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4802,
        )

        return self.__parent__._cast(_4802.SpiralBevelGearMeshModalAnalysis)

    @property
    def spring_damper_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4805.SpringDamperConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4805,
        )

        return self.__parent__._cast(_4805.SpringDamperConnectionModalAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4808.StraightBevelDiffGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4808,
        )

        return self.__parent__._cast(_4808.StraightBevelDiffGearMeshModalAnalysis)

    @property
    def straight_bevel_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4811.StraightBevelGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4811,
        )

        return self.__parent__._cast(_4811.StraightBevelGearMeshModalAnalysis)

    @property
    def torque_converter_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4820.TorqueConverterConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4820,
        )

        return self.__parent__._cast(_4820.TorqueConverterConnectionModalAnalysis)

    @property
    def worm_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4829.WormGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4829,
        )

        return self.__parent__._cast(_4829.WormGearMeshModalAnalysis)

    @property
    def zerol_bevel_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4832.ZerolBevelGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4832,
        )

        return self.__parent__._cast(_4832.ZerolBevelGearMeshModalAnalysis)

    @property
    def connection_modal_analysis(self: "CastSelf") -> "ConnectionModalAnalysis":
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
class ConnectionModalAnalysis(_7715.ConnectionStaticLoadAnalysisCase):
    """ConnectionModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION_MODAL_ANALYSIS

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
    def modal_analysis(self: "Self") -> "_4773.ModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ModalAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModalAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def excited_modes_summary(
        self: "Self",
    ) -> "List[_4845.SingleExcitationResultsModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.reporting.SingleExcitationResultsModalAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExcitedModesSummary")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def system_deflection_results(self: "Self") -> "_2816.ConnectionSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.ConnectionSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConnectionModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConnectionModalAnalysis
        """
        return _Cast_ConnectionModalAnalysis(self)
