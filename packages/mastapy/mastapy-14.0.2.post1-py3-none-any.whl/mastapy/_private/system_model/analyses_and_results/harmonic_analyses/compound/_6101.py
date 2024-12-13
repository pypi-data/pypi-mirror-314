"""PartToPartShearCouplingHalfCompoundHarmonicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
    _6056,
)

_PART_TO_PART_SHEAR_COUPLING_HALF_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "PartToPartShearCouplingHalfCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5928,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6042,
        _6096,
        _6098,
    )
    from mastapy._private.system_model.part_model.couplings import _2652

    Self = TypeVar("Self", bound="PartToPartShearCouplingHalfCompoundHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PartToPartShearCouplingHalfCompoundHarmonicAnalysis._Cast_PartToPartShearCouplingHalfCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartToPartShearCouplingHalfCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartToPartShearCouplingHalfCompoundHarmonicAnalysis:
    """Special nested class for casting PartToPartShearCouplingHalfCompoundHarmonicAnalysis to subclasses."""

    __parent__: "PartToPartShearCouplingHalfCompoundHarmonicAnalysis"

    @property
    def coupling_half_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6056.CouplingHalfCompoundHarmonicAnalysis":
        return self.__parent__._cast(_6056.CouplingHalfCompoundHarmonicAnalysis)

    @property
    def mountable_component_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6096.MountableComponentCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6096,
        )

        return self.__parent__._cast(_6096.MountableComponentCompoundHarmonicAnalysis)

    @property
    def component_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6042.ComponentCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6042,
        )

        return self.__parent__._cast(_6042.ComponentCompoundHarmonicAnalysis)

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
    def part_to_part_shear_coupling_half_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "PartToPartShearCouplingHalfCompoundHarmonicAnalysis":
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
class PartToPartShearCouplingHalfCompoundHarmonicAnalysis(
    _6056.CouplingHalfCompoundHarmonicAnalysis
):
    """PartToPartShearCouplingHalfCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _PART_TO_PART_SHEAR_COUPLING_HALF_COMPOUND_HARMONIC_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2652.PartToPartShearCouplingHalf":
        """mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5928.PartToPartShearCouplingHalfHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.PartToPartShearCouplingHalfHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_5928.PartToPartShearCouplingHalfHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.PartToPartShearCouplingHalfHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_PartToPartShearCouplingHalfCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_PartToPartShearCouplingHalfCompoundHarmonicAnalysis
        """
        return _Cast_PartToPartShearCouplingHalfCompoundHarmonicAnalysis(self)
