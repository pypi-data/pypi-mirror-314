"""ConicalGearMeshCompoundHarmonicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
    _6076,
)

_CONICAL_GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "ConicalGearMeshCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7713,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5849,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6022,
        _6029,
        _6034,
        _6052,
        _6080,
        _6082,
        _6084,
        _6087,
        _6090,
        _6119,
        _6125,
        _6128,
        _6146,
    )

    Self = TypeVar("Self", bound="ConicalGearMeshCompoundHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearMeshCompoundHarmonicAnalysis._Cast_ConicalGearMeshCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearMeshCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearMeshCompoundHarmonicAnalysis:
    """Special nested class for casting ConicalGearMeshCompoundHarmonicAnalysis to subclasses."""

    __parent__: "ConicalGearMeshCompoundHarmonicAnalysis"

    @property
    def gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6076.GearMeshCompoundHarmonicAnalysis":
        return self.__parent__._cast(_6076.GearMeshCompoundHarmonicAnalysis)

    @property
    def inter_mountable_component_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6082.InterMountableComponentConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6082,
        )

        return self.__parent__._cast(
            _6082.InterMountableComponentConnectionCompoundHarmonicAnalysis
        )

    @property
    def connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6052.ConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6052,
        )

        return self.__parent__._cast(_6052.ConnectionCompoundHarmonicAnalysis)

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
    def agma_gleason_conical_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6022.AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6022,
        )

        return self.__parent__._cast(
            _6022.AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis
        )

    @property
    def bevel_differential_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6029.BevelDifferentialGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6029,
        )

        return self.__parent__._cast(
            _6029.BevelDifferentialGearMeshCompoundHarmonicAnalysis
        )

    @property
    def bevel_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6034.BevelGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6034,
        )

        return self.__parent__._cast(_6034.BevelGearMeshCompoundHarmonicAnalysis)

    @property
    def hypoid_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6080.HypoidGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6080,
        )

        return self.__parent__._cast(_6080.HypoidGearMeshCompoundHarmonicAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6084.KlingelnbergCycloPalloidConicalGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6084,
        )

        return self.__parent__._cast(
            _6084.KlingelnbergCycloPalloidConicalGearMeshCompoundHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6087.KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6087,
        )

        return self.__parent__._cast(
            _6087.KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6090.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6090,
        )

        return self.__parent__._cast(
            _6090.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6119.SpiralBevelGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6119,
        )

        return self.__parent__._cast(_6119.SpiralBevelGearMeshCompoundHarmonicAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6125.StraightBevelDiffGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6125,
        )

        return self.__parent__._cast(
            _6125.StraightBevelDiffGearMeshCompoundHarmonicAnalysis
        )

    @property
    def straight_bevel_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6128.StraightBevelGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6128,
        )

        return self.__parent__._cast(
            _6128.StraightBevelGearMeshCompoundHarmonicAnalysis
        )

    @property
    def zerol_bevel_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6146.ZerolBevelGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6146,
        )

        return self.__parent__._cast(_6146.ZerolBevelGearMeshCompoundHarmonicAnalysis)

    @property
    def conical_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "ConicalGearMeshCompoundHarmonicAnalysis":
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
class ConicalGearMeshCompoundHarmonicAnalysis(_6076.GearMeshCompoundHarmonicAnalysis):
    """ConicalGearMeshCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def planetaries(self: "Self") -> "List[ConicalGearMeshCompoundHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.ConicalGearMeshCompoundHarmonicAnalysis]

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
    ) -> "List[_5849.ConicalGearMeshHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.ConicalGearMeshHarmonicAnalysis]

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
    ) -> "List[_5849.ConicalGearMeshHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.ConicalGearMeshHarmonicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_ConicalGearMeshCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearMeshCompoundHarmonicAnalysis
        """
        return _Cast_ConicalGearMeshCompoundHarmonicAnalysis(self)
