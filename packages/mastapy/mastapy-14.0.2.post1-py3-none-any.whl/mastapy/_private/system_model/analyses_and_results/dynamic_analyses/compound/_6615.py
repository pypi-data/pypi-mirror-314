"""GuideDxfModelCompoundDynamicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
    _6579,
)

_GUIDE_DXF_MODEL_COMPOUND_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound",
    "GuideDxfModelCompoundDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6484,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6635,
    )
    from mastapy._private.system_model.part_model import _2513

    Self = TypeVar("Self", bound="GuideDxfModelCompoundDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GuideDxfModelCompoundDynamicAnalysis._Cast_GuideDxfModelCompoundDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GuideDxfModelCompoundDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GuideDxfModelCompoundDynamicAnalysis:
    """Special nested class for casting GuideDxfModelCompoundDynamicAnalysis to subclasses."""

    __parent__: "GuideDxfModelCompoundDynamicAnalysis"

    @property
    def component_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6579.ComponentCompoundDynamicAnalysis":
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
    def guide_dxf_model_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "GuideDxfModelCompoundDynamicAnalysis":
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
class GuideDxfModelCompoundDynamicAnalysis(_6579.ComponentCompoundDynamicAnalysis):
    """GuideDxfModelCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GUIDE_DXF_MODEL_COMPOUND_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2513.GuideDxfModel":
        """mastapy.system_model.part_model.GuideDxfModel

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
    ) -> "List[_6484.GuideDxfModelDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.GuideDxfModelDynamicAnalysis]

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
    ) -> "List[_6484.GuideDxfModelDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.GuideDxfModelDynamicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_GuideDxfModelCompoundDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GuideDxfModelCompoundDynamicAnalysis
        """
        return _Cast_GuideDxfModelCompoundDynamicAnalysis(self)
