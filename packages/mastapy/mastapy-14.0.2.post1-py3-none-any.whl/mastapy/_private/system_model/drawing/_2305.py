"""DynamicAnalysisViewable"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.system_model.drawing import _2310

_DYNAMIC_ANALYSIS_VIEWABLE = python_net_import(
    "SMT.MastaAPI.SystemModel.Drawing", "DynamicAnalysisViewable"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6474,
    )
    from mastapy._private.system_model.drawing import _2303, _2306, _2308

    Self = TypeVar("Self", bound="DynamicAnalysisViewable")
    CastSelf = TypeVar(
        "CastSelf", bound="DynamicAnalysisViewable._Cast_DynamicAnalysisViewable"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DynamicAnalysisViewable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DynamicAnalysisViewable:
    """Special nested class for casting DynamicAnalysisViewable to subclasses."""

    __parent__: "DynamicAnalysisViewable"

    @property
    def part_analysis_case_with_contour_viewable(
        self: "CastSelf",
    ) -> "_2310.PartAnalysisCaseWithContourViewable":
        return self.__parent__._cast(_2310.PartAnalysisCaseWithContourViewable)

    @property
    def harmonic_analysis_viewable(
        self: "CastSelf",
    ) -> "_2306.HarmonicAnalysisViewable":
        from mastapy._private.system_model.drawing import _2306

        return self.__parent__._cast(_2306.HarmonicAnalysisViewable)

    @property
    def modal_analysis_viewable(self: "CastSelf") -> "_2308.ModalAnalysisViewable":
        from mastapy._private.system_model.drawing import _2308

        return self.__parent__._cast(_2308.ModalAnalysisViewable)

    @property
    def dynamic_analysis_viewable(self: "CastSelf") -> "DynamicAnalysisViewable":
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
class DynamicAnalysisViewable(_2310.PartAnalysisCaseWithContourViewable):
    """DynamicAnalysisViewable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DYNAMIC_ANALYSIS_VIEWABLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def contour_draw_style(self: "Self") -> "_2303.ContourDrawStyle":
        """mastapy.system_model.drawing.ContourDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContourDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def dynamic_analysis_draw_style(self: "Self") -> "_6474.DynamicAnalysisDrawStyle":
        """mastapy.system_model.analyses_and_results.dynamic_analyses.DynamicAnalysisDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicAnalysisDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    def fe_results(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "FEResults")

    @property
    def cast_to(self: "Self") -> "_Cast_DynamicAnalysisViewable":
        """Cast to another type.

        Returns:
            _Cast_DynamicAnalysisViewable
        """
        return _Cast_DynamicAnalysisViewable(self)
