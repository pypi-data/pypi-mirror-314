"""ConicalGearMeshCompoundPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
    _4337,
)

_CONICAL_GEAR_MESH_COMPOUND_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound",
    "ConicalGearMeshCompoundPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7713,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4173
    from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
        _4283,
        _4290,
        _4295,
        _4313,
        _4341,
        _4343,
        _4345,
        _4348,
        _4351,
        _4380,
        _4386,
        _4389,
        _4407,
    )

    Self = TypeVar("Self", bound="ConicalGearMeshCompoundPowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearMeshCompoundPowerFlow._Cast_ConicalGearMeshCompoundPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearMeshCompoundPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearMeshCompoundPowerFlow:
    """Special nested class for casting ConicalGearMeshCompoundPowerFlow to subclasses."""

    __parent__: "ConicalGearMeshCompoundPowerFlow"

    @property
    def gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4337.GearMeshCompoundPowerFlow":
        return self.__parent__._cast(_4337.GearMeshCompoundPowerFlow)

    @property
    def inter_mountable_component_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4343.InterMountableComponentConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4343,
        )

        return self.__parent__._cast(
            _4343.InterMountableComponentConnectionCompoundPowerFlow
        )

    @property
    def connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4313.ConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4313,
        )

        return self.__parent__._cast(_4313.ConnectionCompoundPowerFlow)

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
    def agma_gleason_conical_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4283.AGMAGleasonConicalGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4283,
        )

        return self.__parent__._cast(_4283.AGMAGleasonConicalGearMeshCompoundPowerFlow)

    @property
    def bevel_differential_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4290.BevelDifferentialGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4290,
        )

        return self.__parent__._cast(_4290.BevelDifferentialGearMeshCompoundPowerFlow)

    @property
    def bevel_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4295.BevelGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4295,
        )

        return self.__parent__._cast(_4295.BevelGearMeshCompoundPowerFlow)

    @property
    def hypoid_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4341.HypoidGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4341,
        )

        return self.__parent__._cast(_4341.HypoidGearMeshCompoundPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4345.KlingelnbergCycloPalloidConicalGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4345,
        )

        return self.__parent__._cast(
            _4345.KlingelnbergCycloPalloidConicalGearMeshCompoundPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4348.KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4348,
        )

        return self.__parent__._cast(
            _4348.KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4351.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4351,
        )

        return self.__parent__._cast(
            _4351.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow
        )

    @property
    def spiral_bevel_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4380.SpiralBevelGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4380,
        )

        return self.__parent__._cast(_4380.SpiralBevelGearMeshCompoundPowerFlow)

    @property
    def straight_bevel_diff_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4386.StraightBevelDiffGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4386,
        )

        return self.__parent__._cast(_4386.StraightBevelDiffGearMeshCompoundPowerFlow)

    @property
    def straight_bevel_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4389.StraightBevelGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4389,
        )

        return self.__parent__._cast(_4389.StraightBevelGearMeshCompoundPowerFlow)

    @property
    def zerol_bevel_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4407.ZerolBevelGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4407,
        )

        return self.__parent__._cast(_4407.ZerolBevelGearMeshCompoundPowerFlow)

    @property
    def conical_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "ConicalGearMeshCompoundPowerFlow":
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
class ConicalGearMeshCompoundPowerFlow(_4337.GearMeshCompoundPowerFlow):
    """ConicalGearMeshCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_MESH_COMPOUND_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_4173.ConicalGearMeshPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.ConicalGearMeshPowerFlow]

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
    ) -> "List[_4173.ConicalGearMeshPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.ConicalGearMeshPowerFlow]

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
    def cast_to(self: "Self") -> "_Cast_ConicalGearMeshCompoundPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearMeshCompoundPowerFlow
        """
        return _Cast_ConicalGearMeshCompoundPowerFlow(self)
