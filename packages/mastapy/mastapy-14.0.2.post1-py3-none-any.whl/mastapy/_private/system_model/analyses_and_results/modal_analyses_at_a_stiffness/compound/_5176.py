"""InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
    _5146,
)

_INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound",
    "InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7713,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5044,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
        _5116,
        _5120,
        _5123,
        _5128,
        _5133,
        _5138,
        _5141,
        _5144,
        _5149,
        _5151,
        _5159,
        _5165,
        _5170,
        _5174,
        _5178,
        _5181,
        _5184,
        _5194,
        _5203,
        _5206,
        _5213,
        _5216,
        _5219,
        _5222,
        _5231,
        _5237,
        _5240,
    )

    Self = TypeVar(
        "Self",
        bound="InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness._Cast_InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness:
    """Special nested class for casting InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness to subclasses."""

    __parent__: "InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness"

    @property
    def connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5146.ConnectionCompoundModalAnalysisAtAStiffness":
        return self.__parent__._cast(_5146.ConnectionCompoundModalAnalysisAtAStiffness)

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7713.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7713,
        )

        return self.__parent__._cast(_7713.ConnectionCompoundAnalysis)

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
    def agma_gleason_conical_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5116.AGMAGleasonConicalGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5116,
        )

        return self.__parent__._cast(
            _5116.AGMAGleasonConicalGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def belt_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5120.BeltConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5120,
        )

        return self.__parent__._cast(
            _5120.BeltConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def bevel_differential_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5123.BevelDifferentialGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5123,
        )

        return self.__parent__._cast(
            _5123.BevelDifferentialGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def bevel_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5128.BevelGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5128,
        )

        return self.__parent__._cast(
            _5128.BevelGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def clutch_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5133.ClutchConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5133,
        )

        return self.__parent__._cast(
            _5133.ClutchConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def concept_coupling_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5138.ConceptCouplingConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5138,
        )

        return self.__parent__._cast(
            _5138.ConceptCouplingConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def concept_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5141.ConceptGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5141,
        )

        return self.__parent__._cast(
            _5141.ConceptGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def conical_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5144.ConicalGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5144,
        )

        return self.__parent__._cast(
            _5144.ConicalGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def coupling_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5149.CouplingConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5149,
        )

        return self.__parent__._cast(
            _5149.CouplingConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def cvt_belt_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5151.CVTBeltConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5151,
        )

        return self.__parent__._cast(
            _5151.CVTBeltConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def cylindrical_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5159.CylindricalGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5159,
        )

        return self.__parent__._cast(
            _5159.CylindricalGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def face_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5165.FaceGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5165,
        )

        return self.__parent__._cast(
            _5165.FaceGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5170.GearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5170,
        )

        return self.__parent__._cast(_5170.GearMeshCompoundModalAnalysisAtAStiffness)

    @property
    def hypoid_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5174.HypoidGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5174,
        )

        return self.__parent__._cast(
            _5174.HypoidGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> (
        "_5178.KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysisAtAStiffness"
    ):
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5178,
        )

        return self.__parent__._cast(
            _5178.KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> (
        "_5181.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysisAtAStiffness"
    ):
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5181,
        )

        return self.__parent__._cast(
            _5181.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5184.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5184,
        )

        return self.__parent__._cast(
            _5184.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def part_to_part_shear_coupling_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5194.PartToPartShearCouplingConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5194,
        )

        return self.__parent__._cast(
            _5194.PartToPartShearCouplingConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def ring_pins_to_disc_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5203.RingPinsToDiscConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5203,
        )

        return self.__parent__._cast(
            _5203.RingPinsToDiscConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def rolling_ring_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5206.RollingRingConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5206,
        )

        return self.__parent__._cast(
            _5206.RollingRingConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def spiral_bevel_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5213.SpiralBevelGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5213,
        )

        return self.__parent__._cast(
            _5213.SpiralBevelGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def spring_damper_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5216.SpringDamperConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5216,
        )

        return self.__parent__._cast(
            _5216.SpringDamperConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5219.StraightBevelDiffGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5219,
        )

        return self.__parent__._cast(
            _5219.StraightBevelDiffGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5222.StraightBevelGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5222,
        )

        return self.__parent__._cast(
            _5222.StraightBevelGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def torque_converter_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5231.TorqueConverterConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5231,
        )

        return self.__parent__._cast(
            _5231.TorqueConverterConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def worm_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5237.WormGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5237,
        )

        return self.__parent__._cast(
            _5237.WormGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def zerol_bevel_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5240.ZerolBevelGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5240,
        )

        return self.__parent__._cast(
            _5240.ZerolBevelGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def inter_mountable_component_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness":
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
class InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness(
    _5146.ConnectionCompoundModalAnalysisAtAStiffness
):
    """InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_5044.InterMountableComponentConnectionModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.InterMountableComponentConnectionModalAnalysisAtAStiffness]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5044.InterMountableComponentConnectionModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.InterMountableComponentConnectionModalAnalysisAtAStiffness]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness":
        """Cast to another type.

        Returns:
            _Cast_InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness
        """
        return _Cast_InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness(
            self
        )
