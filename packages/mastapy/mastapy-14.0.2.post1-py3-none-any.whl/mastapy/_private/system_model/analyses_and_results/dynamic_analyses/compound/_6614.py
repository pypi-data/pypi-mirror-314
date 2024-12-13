"""GearSetCompoundDynamicAnalysis"""

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
    _6654,
)

_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound",
    "GearSetCompoundDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6483,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6554,
        _6560,
        _6567,
        _6572,
        _6585,
        _6588,
        _6603,
        _6609,
        _6618,
        _6622,
        _6625,
        _6628,
        _6635,
        _6640,
        _6657,
        _6663,
        _6666,
        _6681,
        _6684,
    )

    Self = TypeVar("Self", bound="GearSetCompoundDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearSetCompoundDynamicAnalysis._Cast_GearSetCompoundDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetCompoundDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetCompoundDynamicAnalysis:
    """Special nested class for casting GearSetCompoundDynamicAnalysis to subclasses."""

    __parent__: "GearSetCompoundDynamicAnalysis"

    @property
    def specialised_assembly_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6654.SpecialisedAssemblyCompoundDynamicAnalysis":
        return self.__parent__._cast(_6654.SpecialisedAssemblyCompoundDynamicAnalysis)

    @property
    def abstract_assembly_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6554.AbstractAssemblyCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6554,
        )

        return self.__parent__._cast(_6554.AbstractAssemblyCompoundDynamicAnalysis)

    @property
    def part_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6635.PartCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6635,
        )

        return self.__parent__._cast(_6635.PartCompoundDynamicAnalysis)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7720.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7720,
        )

        return self.__parent__._cast(_7720.PartCompoundAnalysis)

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
    def agma_gleason_conical_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6560.AGMAGleasonConicalGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6560,
        )

        return self.__parent__._cast(
            _6560.AGMAGleasonConicalGearSetCompoundDynamicAnalysis
        )

    @property
    def bevel_differential_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6567.BevelDifferentialGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6567,
        )

        return self.__parent__._cast(
            _6567.BevelDifferentialGearSetCompoundDynamicAnalysis
        )

    @property
    def bevel_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6572.BevelGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6572,
        )

        return self.__parent__._cast(_6572.BevelGearSetCompoundDynamicAnalysis)

    @property
    def concept_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6585.ConceptGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6585,
        )

        return self.__parent__._cast(_6585.ConceptGearSetCompoundDynamicAnalysis)

    @property
    def conical_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6588.ConicalGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6588,
        )

        return self.__parent__._cast(_6588.ConicalGearSetCompoundDynamicAnalysis)

    @property
    def cylindrical_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6603.CylindricalGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6603,
        )

        return self.__parent__._cast(_6603.CylindricalGearSetCompoundDynamicAnalysis)

    @property
    def face_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6609.FaceGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6609,
        )

        return self.__parent__._cast(_6609.FaceGearSetCompoundDynamicAnalysis)

    @property
    def hypoid_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6618.HypoidGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6618,
        )

        return self.__parent__._cast(_6618.HypoidGearSetCompoundDynamicAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6622.KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6622,
        )

        return self.__parent__._cast(
            _6622.KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6625.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6625,
        )

        return self.__parent__._cast(
            _6625.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6628.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6628,
        )

        return self.__parent__._cast(
            _6628.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis
        )

    @property
    def planetary_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6640.PlanetaryGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6640,
        )

        return self.__parent__._cast(_6640.PlanetaryGearSetCompoundDynamicAnalysis)

    @property
    def spiral_bevel_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6657.SpiralBevelGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6657,
        )

        return self.__parent__._cast(_6657.SpiralBevelGearSetCompoundDynamicAnalysis)

    @property
    def straight_bevel_diff_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6663.StraightBevelDiffGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6663,
        )

        return self.__parent__._cast(
            _6663.StraightBevelDiffGearSetCompoundDynamicAnalysis
        )

    @property
    def straight_bevel_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6666.StraightBevelGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6666,
        )

        return self.__parent__._cast(_6666.StraightBevelGearSetCompoundDynamicAnalysis)

    @property
    def worm_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6681.WormGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6681,
        )

        return self.__parent__._cast(_6681.WormGearSetCompoundDynamicAnalysis)

    @property
    def zerol_bevel_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6684.ZerolBevelGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6684,
        )

        return self.__parent__._cast(_6684.ZerolBevelGearSetCompoundDynamicAnalysis)

    @property
    def gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "GearSetCompoundDynamicAnalysis":
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
class GearSetCompoundDynamicAnalysis(_6654.SpecialisedAssemblyCompoundDynamicAnalysis):
    """GearSetCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_analysis_cases(self: "Self") -> "List[_6483.GearSetDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.GearSetDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6483.GearSetDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.GearSetDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetCompoundDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearSetCompoundDynamicAnalysis
        """
        return _Cast_GearSetCompoundDynamicAnalysis(self)
