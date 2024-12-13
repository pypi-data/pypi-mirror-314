"""InterMountableComponentConnectionCompoundDynamicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
    _6589,
)

_INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound",
    "InterMountableComponentConnectionCompoundDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7713,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6488,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6559,
        _6563,
        _6566,
        _6571,
        _6576,
        _6581,
        _6584,
        _6587,
        _6592,
        _6594,
        _6602,
        _6608,
        _6613,
        _6617,
        _6621,
        _6624,
        _6627,
        _6637,
        _6646,
        _6649,
        _6656,
        _6659,
        _6662,
        _6665,
        _6674,
        _6680,
        _6683,
    )

    Self = TypeVar(
        "Self", bound="InterMountableComponentConnectionCompoundDynamicAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterMountableComponentConnectionCompoundDynamicAnalysis._Cast_InterMountableComponentConnectionCompoundDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnectionCompoundDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterMountableComponentConnectionCompoundDynamicAnalysis:
    """Special nested class for casting InterMountableComponentConnectionCompoundDynamicAnalysis to subclasses."""

    __parent__: "InterMountableComponentConnectionCompoundDynamicAnalysis"

    @property
    def connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6589.ConnectionCompoundDynamicAnalysis":
        return self.__parent__._cast(_6589.ConnectionCompoundDynamicAnalysis)

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
    def agma_gleason_conical_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6559.AGMAGleasonConicalGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6559,
        )

        return self.__parent__._cast(
            _6559.AGMAGleasonConicalGearMeshCompoundDynamicAnalysis
        )

    @property
    def belt_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6563.BeltConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6563,
        )

        return self.__parent__._cast(_6563.BeltConnectionCompoundDynamicAnalysis)

    @property
    def bevel_differential_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6566.BevelDifferentialGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6566,
        )

        return self.__parent__._cast(
            _6566.BevelDifferentialGearMeshCompoundDynamicAnalysis
        )

    @property
    def bevel_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6571.BevelGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6571,
        )

        return self.__parent__._cast(_6571.BevelGearMeshCompoundDynamicAnalysis)

    @property
    def clutch_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6576.ClutchConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6576,
        )

        return self.__parent__._cast(_6576.ClutchConnectionCompoundDynamicAnalysis)

    @property
    def concept_coupling_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6581.ConceptCouplingConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6581,
        )

        return self.__parent__._cast(
            _6581.ConceptCouplingConnectionCompoundDynamicAnalysis
        )

    @property
    def concept_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6584.ConceptGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6584,
        )

        return self.__parent__._cast(_6584.ConceptGearMeshCompoundDynamicAnalysis)

    @property
    def conical_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6587.ConicalGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6587,
        )

        return self.__parent__._cast(_6587.ConicalGearMeshCompoundDynamicAnalysis)

    @property
    def coupling_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6592.CouplingConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6592,
        )

        return self.__parent__._cast(_6592.CouplingConnectionCompoundDynamicAnalysis)

    @property
    def cvt_belt_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6594.CVTBeltConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6594,
        )

        return self.__parent__._cast(_6594.CVTBeltConnectionCompoundDynamicAnalysis)

    @property
    def cylindrical_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6602.CylindricalGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6602,
        )

        return self.__parent__._cast(_6602.CylindricalGearMeshCompoundDynamicAnalysis)

    @property
    def face_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6608.FaceGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6608,
        )

        return self.__parent__._cast(_6608.FaceGearMeshCompoundDynamicAnalysis)

    @property
    def gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6613.GearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6613,
        )

        return self.__parent__._cast(_6613.GearMeshCompoundDynamicAnalysis)

    @property
    def hypoid_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6617.HypoidGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6617,
        )

        return self.__parent__._cast(_6617.HypoidGearMeshCompoundDynamicAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6621.KlingelnbergCycloPalloidConicalGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6621,
        )

        return self.__parent__._cast(
            _6621.KlingelnbergCycloPalloidConicalGearMeshCompoundDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6624.KlingelnbergCycloPalloidHypoidGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6624,
        )

        return self.__parent__._cast(
            _6624.KlingelnbergCycloPalloidHypoidGearMeshCompoundDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6627.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6627,
        )

        return self.__parent__._cast(
            _6627.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundDynamicAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6637.PartToPartShearCouplingConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6637,
        )

        return self.__parent__._cast(
            _6637.PartToPartShearCouplingConnectionCompoundDynamicAnalysis
        )

    @property
    def ring_pins_to_disc_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6646.RingPinsToDiscConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6646,
        )

        return self.__parent__._cast(
            _6646.RingPinsToDiscConnectionCompoundDynamicAnalysis
        )

    @property
    def rolling_ring_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6649.RollingRingConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6649,
        )

        return self.__parent__._cast(_6649.RollingRingConnectionCompoundDynamicAnalysis)

    @property
    def spiral_bevel_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6656.SpiralBevelGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6656,
        )

        return self.__parent__._cast(_6656.SpiralBevelGearMeshCompoundDynamicAnalysis)

    @property
    def spring_damper_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6659.SpringDamperConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6659,
        )

        return self.__parent__._cast(
            _6659.SpringDamperConnectionCompoundDynamicAnalysis
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6662.StraightBevelDiffGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6662,
        )

        return self.__parent__._cast(
            _6662.StraightBevelDiffGearMeshCompoundDynamicAnalysis
        )

    @property
    def straight_bevel_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6665.StraightBevelGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6665,
        )

        return self.__parent__._cast(_6665.StraightBevelGearMeshCompoundDynamicAnalysis)

    @property
    def torque_converter_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6674.TorqueConverterConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6674,
        )

        return self.__parent__._cast(
            _6674.TorqueConverterConnectionCompoundDynamicAnalysis
        )

    @property
    def worm_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6680.WormGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6680,
        )

        return self.__parent__._cast(_6680.WormGearMeshCompoundDynamicAnalysis)

    @property
    def zerol_bevel_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6683.ZerolBevelGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6683,
        )

        return self.__parent__._cast(_6683.ZerolBevelGearMeshCompoundDynamicAnalysis)

    @property
    def inter_mountable_component_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "InterMountableComponentConnectionCompoundDynamicAnalysis":
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
class InterMountableComponentConnectionCompoundDynamicAnalysis(
    _6589.ConnectionCompoundDynamicAnalysis
):
    """InterMountableComponentConnectionCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_DYNAMIC_ANALYSIS
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
    ) -> "List[_6488.InterMountableComponentConnectionDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.InterMountableComponentConnectionDynamicAnalysis]

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
    ) -> "List[_6488.InterMountableComponentConnectionDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.InterMountableComponentConnectionDynamicAnalysis]

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
    ) -> "_Cast_InterMountableComponentConnectionCompoundDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_InterMountableComponentConnectionCompoundDynamicAnalysis
        """
        return _Cast_InterMountableComponentConnectionCompoundDynamicAnalysis(self)
