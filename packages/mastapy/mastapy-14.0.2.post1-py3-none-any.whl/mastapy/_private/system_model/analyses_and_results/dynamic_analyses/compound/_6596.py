"""CVTPulleyCompoundDynamicAnalysis"""

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
    _6644,
)

_CVT_PULLEY_COMPOUND_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound",
    "CVTPulleyCompoundDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6463,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6579,
        _6593,
        _6633,
        _6635,
    )

    Self = TypeVar("Self", bound="CVTPulleyCompoundDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CVTPulleyCompoundDynamicAnalysis._Cast_CVTPulleyCompoundDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CVTPulleyCompoundDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CVTPulleyCompoundDynamicAnalysis:
    """Special nested class for casting CVTPulleyCompoundDynamicAnalysis to subclasses."""

    __parent__: "CVTPulleyCompoundDynamicAnalysis"

    @property
    def pulley_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6644.PulleyCompoundDynamicAnalysis":
        return self.__parent__._cast(_6644.PulleyCompoundDynamicAnalysis)

    @property
    def coupling_half_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6593.CouplingHalfCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6593,
        )

        return self.__parent__._cast(_6593.CouplingHalfCompoundDynamicAnalysis)

    @property
    def mountable_component_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6633.MountableComponentCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6633,
        )

        return self.__parent__._cast(_6633.MountableComponentCompoundDynamicAnalysis)

    @property
    def component_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6579.ComponentCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6579,
        )

        return self.__parent__._cast(_6579.ComponentCompoundDynamicAnalysis)

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
    def cvt_pulley_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "CVTPulleyCompoundDynamicAnalysis":
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
class CVTPulleyCompoundDynamicAnalysis(_6644.PulleyCompoundDynamicAnalysis):
    """CVTPulleyCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CVT_PULLEY_COMPOUND_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6463.CVTPulleyDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.CVTPulleyDynamicAnalysis]

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
    ) -> "List[_6463.CVTPulleyDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.CVTPulleyDynamicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_CVTPulleyCompoundDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CVTPulleyCompoundDynamicAnalysis
        """
        return _Cast_CVTPulleyCompoundDynamicAnalysis(self)
