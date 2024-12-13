"""CouplingCompoundStabilityAnalysis"""

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
    _4104,
)

_COUPLING_COMPOUND_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
    "CouplingCompoundStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3907,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
        _4004,
        _4025,
        _4030,
        _4085,
        _4086,
        _4108,
        _4123,
    )

    Self = TypeVar("Self", bound="CouplingCompoundStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingCompoundStabilityAnalysis._Cast_CouplingCompoundStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingCompoundStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingCompoundStabilityAnalysis:
    """Special nested class for casting CouplingCompoundStabilityAnalysis to subclasses."""

    __parent__: "CouplingCompoundStabilityAnalysis"

    @property
    def specialised_assembly_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4104.SpecialisedAssemblyCompoundStabilityAnalysis":
        return self.__parent__._cast(_4104.SpecialisedAssemblyCompoundStabilityAnalysis)

    @property
    def abstract_assembly_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4004.AbstractAssemblyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4004,
        )

        return self.__parent__._cast(_4004.AbstractAssemblyCompoundStabilityAnalysis)

    @property
    def part_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4085.PartCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4085,
        )

        return self.__parent__._cast(_4085.PartCompoundStabilityAnalysis)

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
    def clutch_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4025.ClutchCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4025,
        )

        return self.__parent__._cast(_4025.ClutchCompoundStabilityAnalysis)

    @property
    def concept_coupling_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4030.ConceptCouplingCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4030,
        )

        return self.__parent__._cast(_4030.ConceptCouplingCompoundStabilityAnalysis)

    @property
    def part_to_part_shear_coupling_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4086.PartToPartShearCouplingCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4086,
        )

        return self.__parent__._cast(
            _4086.PartToPartShearCouplingCompoundStabilityAnalysis
        )

    @property
    def spring_damper_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4108.SpringDamperCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4108,
        )

        return self.__parent__._cast(_4108.SpringDamperCompoundStabilityAnalysis)

    @property
    def torque_converter_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4123.TorqueConverterCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4123,
        )

        return self.__parent__._cast(_4123.TorqueConverterCompoundStabilityAnalysis)

    @property
    def coupling_compound_stability_analysis(
        self: "CastSelf",
    ) -> "CouplingCompoundStabilityAnalysis":
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
class CouplingCompoundStabilityAnalysis(
    _4104.SpecialisedAssemblyCompoundStabilityAnalysis
):
    """CouplingCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_COMPOUND_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_3907.CouplingStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.CouplingStabilityAnalysis]

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
    ) -> "List[_3907.CouplingStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.CouplingStabilityAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_CouplingCompoundStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CouplingCompoundStabilityAnalysis
        """
        return _Cast_CouplingCompoundStabilityAnalysis(self)
