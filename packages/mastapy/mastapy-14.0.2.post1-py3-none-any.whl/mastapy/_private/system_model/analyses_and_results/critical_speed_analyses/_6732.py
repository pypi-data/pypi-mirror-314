"""CriticalSpeedAnalysisDrawStyle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.rotor_dynamics import _4135

_CRITICAL_SPEED_ANALYSIS_DRAW_STYLE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses",
    "CriticalSpeedAnalysisDrawStyle",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.geometry import _320
    from mastapy._private.system_model.drawing import _2303

    Self = TypeVar("Self", bound="CriticalSpeedAnalysisDrawStyle")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CriticalSpeedAnalysisDrawStyle._Cast_CriticalSpeedAnalysisDrawStyle",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CriticalSpeedAnalysisDrawStyle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CriticalSpeedAnalysisDrawStyle:
    """Special nested class for casting CriticalSpeedAnalysisDrawStyle to subclasses."""

    __parent__: "CriticalSpeedAnalysisDrawStyle"

    @property
    def rotor_dynamics_draw_style(self: "CastSelf") -> "_4135.RotorDynamicsDrawStyle":
        return self.__parent__._cast(_4135.RotorDynamicsDrawStyle)

    @property
    def contour_draw_style(self: "CastSelf") -> "_2303.ContourDrawStyle":
        from mastapy._private.system_model.drawing import _2303

        return self.__parent__._cast(_2303.ContourDrawStyle)

    @property
    def draw_style_base(self: "CastSelf") -> "_320.DrawStyleBase":
        from mastapy._private.geometry import _320

        return self.__parent__._cast(_320.DrawStyleBase)

    @property
    def critical_speed_analysis_draw_style(
        self: "CastSelf",
    ) -> "CriticalSpeedAnalysisDrawStyle":
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
class CriticalSpeedAnalysisDrawStyle(_4135.RotorDynamicsDrawStyle):
    """CriticalSpeedAnalysisDrawStyle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CRITICAL_SPEED_ANALYSIS_DRAW_STYLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CriticalSpeedAnalysisDrawStyle":
        """Cast to another type.

        Returns:
            _Cast_CriticalSpeedAnalysisDrawStyle
        """
        return _Cast_CriticalSpeedAnalysisDrawStyle(self)
