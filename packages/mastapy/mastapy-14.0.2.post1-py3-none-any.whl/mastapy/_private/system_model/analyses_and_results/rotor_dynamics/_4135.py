"""RotorDynamicsDrawStyle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.drawing import _2303

_ROTOR_DYNAMICS_DRAW_STYLE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.RotorDynamics",
    "RotorDynamicsDrawStyle",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.geometry import _320
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6732,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3978,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3185,
    )

    Self = TypeVar("Self", bound="RotorDynamicsDrawStyle")
    CastSelf = TypeVar(
        "CastSelf", bound="RotorDynamicsDrawStyle._Cast_RotorDynamicsDrawStyle"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RotorDynamicsDrawStyle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RotorDynamicsDrawStyle:
    """Special nested class for casting RotorDynamicsDrawStyle to subclasses."""

    __parent__: "RotorDynamicsDrawStyle"

    @property
    def contour_draw_style(self: "CastSelf") -> "_2303.ContourDrawStyle":
        return self.__parent__._cast(_2303.ContourDrawStyle)

    @property
    def draw_style_base(self: "CastSelf") -> "_320.DrawStyleBase":
        from mastapy._private.geometry import _320

        return self.__parent__._cast(_320.DrawStyleBase)

    @property
    def steady_state_synchronous_response_draw_style(
        self: "CastSelf",
    ) -> "_3185.SteadyStateSynchronousResponseDrawStyle":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3185,
        )

        return self.__parent__._cast(_3185.SteadyStateSynchronousResponseDrawStyle)

    @property
    def stability_analysis_draw_style(
        self: "CastSelf",
    ) -> "_3978.StabilityAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3978,
        )

        return self.__parent__._cast(_3978.StabilityAnalysisDrawStyle)

    @property
    def critical_speed_analysis_draw_style(
        self: "CastSelf",
    ) -> "_6732.CriticalSpeedAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6732,
        )

        return self.__parent__._cast(_6732.CriticalSpeedAnalysisDrawStyle)

    @property
    def rotor_dynamics_draw_style(self: "CastSelf") -> "RotorDynamicsDrawStyle":
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
class RotorDynamicsDrawStyle(_2303.ContourDrawStyle):
    """RotorDynamicsDrawStyle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROTOR_DYNAMICS_DRAW_STYLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def show_whirl_orbits(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowWhirlOrbits")

        if temp is None:
            return False

        return temp

    @show_whirl_orbits.setter
    @enforce_parameter_types
    def show_whirl_orbits(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowWhirlOrbits", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_RotorDynamicsDrawStyle":
        """Cast to another type.

        Returns:
            _Cast_RotorDynamicsDrawStyle
        """
        return _Cast_RotorDynamicsDrawStyle(self)
