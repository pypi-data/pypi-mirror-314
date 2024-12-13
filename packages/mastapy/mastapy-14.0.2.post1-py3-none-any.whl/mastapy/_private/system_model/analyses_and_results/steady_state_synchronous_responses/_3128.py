"""DynamicModelForSteadyStateSynchronousResponse"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.dynamic_analyses import _6473

_DYNAMIC_MODEL_FOR_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
    "DynamicModelForSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2739
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7709,
        _7718,
        _7724,
    )

    Self = TypeVar("Self", bound="DynamicModelForSteadyStateSynchronousResponse")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DynamicModelForSteadyStateSynchronousResponse._Cast_DynamicModelForSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DynamicModelForSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DynamicModelForSteadyStateSynchronousResponse:
    """Special nested class for casting DynamicModelForSteadyStateSynchronousResponse to subclasses."""

    __parent__: "DynamicModelForSteadyStateSynchronousResponse"

    @property
    def dynamic_analysis(self: "CastSelf") -> "_6473.DynamicAnalysis":
        return self.__parent__._cast(_6473.DynamicAnalysis)

    @property
    def fe_analysis(self: "CastSelf") -> "_7718.FEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7718,
        )

        return self.__parent__._cast(_7718.FEAnalysis)

    @property
    def static_load_analysis_case(self: "CastSelf") -> "_7724.StaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7724,
        )

        return self.__parent__._cast(_7724.StaticLoadAnalysisCase)

    @property
    def analysis_case(self: "CastSelf") -> "_7709.AnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7709,
        )

        return self.__parent__._cast(_7709.AnalysisCase)

    @property
    def context(self: "CastSelf") -> "_2739.Context":
        from mastapy._private.system_model.analyses_and_results import _2739

        return self.__parent__._cast(_2739.Context)

    @property
    def dynamic_model_for_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "DynamicModelForSteadyStateSynchronousResponse":
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
class DynamicModelForSteadyStateSynchronousResponse(_6473.DynamicAnalysis):
    """DynamicModelForSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DYNAMIC_MODEL_FOR_STEADY_STATE_SYNCHRONOUS_RESPONSE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_DynamicModelForSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_DynamicModelForSteadyStateSynchronousResponse
        """
        return _Cast_DynamicModelForSteadyStateSynchronousResponse(self)
