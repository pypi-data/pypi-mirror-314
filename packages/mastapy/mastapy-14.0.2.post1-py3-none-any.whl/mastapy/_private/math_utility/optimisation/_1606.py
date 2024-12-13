"""ReportingOptimizationInput"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.math_utility.optimisation import _1594

_REPORTING_OPTIMIZATION_INPUT = python_net_import(
    "SMT.MastaAPI.MathUtility.Optimisation", "ReportingOptimizationInput"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility.optimisation import _1595

    Self = TypeVar("Self", bound="ReportingOptimizationInput")
    CastSelf = TypeVar(
        "CastSelf", bound="ReportingOptimizationInput._Cast_ReportingOptimizationInput"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ReportingOptimizationInput",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ReportingOptimizationInput:
    """Special nested class for casting ReportingOptimizationInput to subclasses."""

    __parent__: "ReportingOptimizationInput"

    @property
    def optimization_input(self: "CastSelf") -> "_1594.OptimizationInput":
        return self.__parent__._cast(_1594.OptimizationInput)

    @property
    def optimization_variable(self: "CastSelf") -> "_1595.OptimizationVariable":
        from mastapy._private.math_utility.optimisation import _1595

        return self.__parent__._cast(_1595.OptimizationVariable)

    @property
    def reporting_optimization_input(self: "CastSelf") -> "ReportingOptimizationInput":
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
class ReportingOptimizationInput(_1594.OptimizationInput):
    """ReportingOptimizationInput

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _REPORTING_OPTIMIZATION_INPUT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ReportingOptimizationInput":
        """Cast to another type.

        Returns:
            _Cast_ReportingOptimizationInput
        """
        return _Cast_ReportingOptimizationInput(self)
