"""ConicalGearMeshCompoundStabilityAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
    _4063,
)

_CONICAL_GEAR_MESH_COMPOUND_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
    "ConicalGearMeshCompoundStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7713,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3900,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
        _4009,
        _4016,
        _4021,
        _4039,
        _4067,
        _4069,
        _4071,
        _4074,
        _4077,
        _4106,
        _4112,
        _4115,
        _4133,
    )

    Self = TypeVar("Self", bound="ConicalGearMeshCompoundStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearMeshCompoundStabilityAnalysis._Cast_ConicalGearMeshCompoundStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearMeshCompoundStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearMeshCompoundStabilityAnalysis:
    """Special nested class for casting ConicalGearMeshCompoundStabilityAnalysis to subclasses."""

    __parent__: "ConicalGearMeshCompoundStabilityAnalysis"

    @property
    def gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4063.GearMeshCompoundStabilityAnalysis":
        return self.__parent__._cast(_4063.GearMeshCompoundStabilityAnalysis)

    @property
    def inter_mountable_component_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4069.InterMountableComponentConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4069,
        )

        return self.__parent__._cast(
            _4069.InterMountableComponentConnectionCompoundStabilityAnalysis
        )

    @property
    def connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4039.ConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4039,
        )

        return self.__parent__._cast(_4039.ConnectionCompoundStabilityAnalysis)

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
    def agma_gleason_conical_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4009.AGMAGleasonConicalGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4009,
        )

        return self.__parent__._cast(
            _4009.AGMAGleasonConicalGearMeshCompoundStabilityAnalysis
        )

    @property
    def bevel_differential_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4016.BevelDifferentialGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4016,
        )

        return self.__parent__._cast(
            _4016.BevelDifferentialGearMeshCompoundStabilityAnalysis
        )

    @property
    def bevel_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4021.BevelGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4021,
        )

        return self.__parent__._cast(_4021.BevelGearMeshCompoundStabilityAnalysis)

    @property
    def hypoid_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4067.HypoidGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4067,
        )

        return self.__parent__._cast(_4067.HypoidGearMeshCompoundStabilityAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4071.KlingelnbergCycloPalloidConicalGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4071,
        )

        return self.__parent__._cast(
            _4071.KlingelnbergCycloPalloidConicalGearMeshCompoundStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4074.KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4074,
        )

        return self.__parent__._cast(
            _4074.KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4077.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4077,
        )

        return self.__parent__._cast(
            _4077.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundStabilityAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4106.SpiralBevelGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4106,
        )

        return self.__parent__._cast(_4106.SpiralBevelGearMeshCompoundStabilityAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4112.StraightBevelDiffGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4112,
        )

        return self.__parent__._cast(
            _4112.StraightBevelDiffGearMeshCompoundStabilityAnalysis
        )

    @property
    def straight_bevel_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4115.StraightBevelGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4115,
        )

        return self.__parent__._cast(
            _4115.StraightBevelGearMeshCompoundStabilityAnalysis
        )

    @property
    def zerol_bevel_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4133.ZerolBevelGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4133,
        )

        return self.__parent__._cast(_4133.ZerolBevelGearMeshCompoundStabilityAnalysis)

    @property
    def conical_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "ConicalGearMeshCompoundStabilityAnalysis":
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
class ConicalGearMeshCompoundStabilityAnalysis(_4063.GearMeshCompoundStabilityAnalysis):
    """ConicalGearMeshCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_MESH_COMPOUND_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def planetaries(self: "Self") -> "List[ConicalGearMeshCompoundStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.compound.ConicalGearMeshCompoundStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planetaries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_3900.ConicalGearMeshStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.ConicalGearMeshStabilityAnalysis]

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
    ) -> "List[_3900.ConicalGearMeshStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.ConicalGearMeshStabilityAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_ConicalGearMeshCompoundStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearMeshCompoundStabilityAnalysis
        """
        return _Cast_ConicalGearMeshCompoundStabilityAnalysis(self)
