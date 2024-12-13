"""SpecialisedAssemblyCompoundHarmonicAnalysis"""

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
    _6017,
)

_SPECIALISED_ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "SpecialisedAssemblyCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5948,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6023,
        _6027,
        _6030,
        _6035,
        _6037,
        _6038,
        _6043,
        _6048,
        _6051,
        _6054,
        _6058,
        _6060,
        _6066,
        _6072,
        _6074,
        _6077,
        _6081,
        _6085,
        _6088,
        _6091,
        _6094,
        _6098,
        _6099,
        _6103,
        _6110,
        _6120,
        _6121,
        _6126,
        _6129,
        _6132,
        _6136,
        _6144,
        _6147,
    )

    Self = TypeVar("Self", bound="SpecialisedAssemblyCompoundHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssemblyCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpecialisedAssemblyCompoundHarmonicAnalysis:
    """Special nested class for casting SpecialisedAssemblyCompoundHarmonicAnalysis to subclasses."""

    __parent__: "SpecialisedAssemblyCompoundHarmonicAnalysis"

    @property
    def abstract_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6017.AbstractAssemblyCompoundHarmonicAnalysis":
        return self.__parent__._cast(_6017.AbstractAssemblyCompoundHarmonicAnalysis)

    @property
    def part_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6098.PartCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6098,
        )

        return self.__parent__._cast(_6098.PartCompoundHarmonicAnalysis)

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
    def agma_gleason_conical_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6023.AGMAGleasonConicalGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6023,
        )

        return self.__parent__._cast(
            _6023.AGMAGleasonConicalGearSetCompoundHarmonicAnalysis
        )

    @property
    def belt_drive_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6027.BeltDriveCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6027,
        )

        return self.__parent__._cast(_6027.BeltDriveCompoundHarmonicAnalysis)

    @property
    def bevel_differential_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6030.BevelDifferentialGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6030,
        )

        return self.__parent__._cast(
            _6030.BevelDifferentialGearSetCompoundHarmonicAnalysis
        )

    @property
    def bevel_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6035.BevelGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6035,
        )

        return self.__parent__._cast(_6035.BevelGearSetCompoundHarmonicAnalysis)

    @property
    def bolted_joint_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6037.BoltedJointCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6037,
        )

        return self.__parent__._cast(_6037.BoltedJointCompoundHarmonicAnalysis)

    @property
    def clutch_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6038.ClutchCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6038,
        )

        return self.__parent__._cast(_6038.ClutchCompoundHarmonicAnalysis)

    @property
    def concept_coupling_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6043.ConceptCouplingCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6043,
        )

        return self.__parent__._cast(_6043.ConceptCouplingCompoundHarmonicAnalysis)

    @property
    def concept_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6048.ConceptGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6048,
        )

        return self.__parent__._cast(_6048.ConceptGearSetCompoundHarmonicAnalysis)

    @property
    def conical_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6051.ConicalGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6051,
        )

        return self.__parent__._cast(_6051.ConicalGearSetCompoundHarmonicAnalysis)

    @property
    def coupling_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6054.CouplingCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6054,
        )

        return self.__parent__._cast(_6054.CouplingCompoundHarmonicAnalysis)

    @property
    def cvt_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6058.CVTCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6058,
        )

        return self.__parent__._cast(_6058.CVTCompoundHarmonicAnalysis)

    @property
    def cycloidal_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6060.CycloidalAssemblyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6060,
        )

        return self.__parent__._cast(_6060.CycloidalAssemblyCompoundHarmonicAnalysis)

    @property
    def cylindrical_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6066.CylindricalGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6066,
        )

        return self.__parent__._cast(_6066.CylindricalGearSetCompoundHarmonicAnalysis)

    @property
    def face_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6072.FaceGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6072,
        )

        return self.__parent__._cast(_6072.FaceGearSetCompoundHarmonicAnalysis)

    @property
    def flexible_pin_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6074.FlexiblePinAssemblyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6074,
        )

        return self.__parent__._cast(_6074.FlexiblePinAssemblyCompoundHarmonicAnalysis)

    @property
    def gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6077.GearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6077,
        )

        return self.__parent__._cast(_6077.GearSetCompoundHarmonicAnalysis)

    @property
    def hypoid_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6081.HypoidGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6081,
        )

        return self.__parent__._cast(_6081.HypoidGearSetCompoundHarmonicAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6085.KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6085,
        )

        return self.__parent__._cast(
            _6085.KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6088.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6088,
        )

        return self.__parent__._cast(
            _6088.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6091.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6091,
        )

        return self.__parent__._cast(
            _6091.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis
        )

    @property
    def microphone_array_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6094.MicrophoneArrayCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6094,
        )

        return self.__parent__._cast(_6094.MicrophoneArrayCompoundHarmonicAnalysis)

    @property
    def part_to_part_shear_coupling_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6099.PartToPartShearCouplingCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6099,
        )

        return self.__parent__._cast(
            _6099.PartToPartShearCouplingCompoundHarmonicAnalysis
        )

    @property
    def planetary_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6103.PlanetaryGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6103,
        )

        return self.__parent__._cast(_6103.PlanetaryGearSetCompoundHarmonicAnalysis)

    @property
    def rolling_ring_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6110.RollingRingAssemblyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6110,
        )

        return self.__parent__._cast(_6110.RollingRingAssemblyCompoundHarmonicAnalysis)

    @property
    def spiral_bevel_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6120.SpiralBevelGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6120,
        )

        return self.__parent__._cast(_6120.SpiralBevelGearSetCompoundHarmonicAnalysis)

    @property
    def spring_damper_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6121.SpringDamperCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6121,
        )

        return self.__parent__._cast(_6121.SpringDamperCompoundHarmonicAnalysis)

    @property
    def straight_bevel_diff_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6126.StraightBevelDiffGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6126,
        )

        return self.__parent__._cast(
            _6126.StraightBevelDiffGearSetCompoundHarmonicAnalysis
        )

    @property
    def straight_bevel_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6129.StraightBevelGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6129,
        )

        return self.__parent__._cast(_6129.StraightBevelGearSetCompoundHarmonicAnalysis)

    @property
    def synchroniser_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6132.SynchroniserCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6132,
        )

        return self.__parent__._cast(_6132.SynchroniserCompoundHarmonicAnalysis)

    @property
    def torque_converter_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6136.TorqueConverterCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6136,
        )

        return self.__parent__._cast(_6136.TorqueConverterCompoundHarmonicAnalysis)

    @property
    def worm_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6144.WormGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6144,
        )

        return self.__parent__._cast(_6144.WormGearSetCompoundHarmonicAnalysis)

    @property
    def zerol_bevel_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6147.ZerolBevelGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6147,
        )

        return self.__parent__._cast(_6147.ZerolBevelGearSetCompoundHarmonicAnalysis)

    @property
    def specialised_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "SpecialisedAssemblyCompoundHarmonicAnalysis":
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
class SpecialisedAssemblyCompoundHarmonicAnalysis(
    _6017.AbstractAssemblyCompoundHarmonicAnalysis
):
    """SpecialisedAssemblyCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPECIALISED_ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_5948.SpecialisedAssemblyHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.SpecialisedAssemblyHarmonicAnalysis]

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
    ) -> "List[_5948.SpecialisedAssemblyHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.SpecialisedAssemblyHarmonicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_SpecialisedAssemblyCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_SpecialisedAssemblyCompoundHarmonicAnalysis
        """
        return _Cast_SpecialisedAssemblyCompoundHarmonicAnalysis(self)
