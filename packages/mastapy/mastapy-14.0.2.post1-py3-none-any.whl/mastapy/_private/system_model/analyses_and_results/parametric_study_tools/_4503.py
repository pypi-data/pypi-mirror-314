"""ParametricStudyTool"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7709

_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "ParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2739
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4504,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6957,
        _6958,
    )

    Self = TypeVar("Self", bound="ParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf", bound="ParametricStudyTool._Cast_ParametricStudyTool"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ParametricStudyTool:
    """Special nested class for casting ParametricStudyTool to subclasses."""

    __parent__: "ParametricStudyTool"

    @property
    def analysis_case(self: "CastSelf") -> "_7709.AnalysisCase":
        return self.__parent__._cast(_7709.AnalysisCase)

    @property
    def context(self: "CastSelf") -> "_2739.Context":
        from mastapy._private.system_model.analyses_and_results import _2739

        return self.__parent__._cast(_2739.Context)

    @property
    def parametric_study_tool(self: "CastSelf") -> "ParametricStudyTool":
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
class ParametricStudyTool(_7709.AnalysisCase):
    """ParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def load_case(self: "Self") -> "_6957.StaticLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def parametric_analysis_options(self: "Self") -> "_4504.ParametricStudyToolOptions":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ParametricStudyToolOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ParametricAnalysisOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def time_series_load_case(self: "Self") -> "_6958.TimeSeriesLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.TimeSeriesLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeSeriesLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_ParametricStudyTool
        """
        return _Cast_ParametricStudyTool(self)
