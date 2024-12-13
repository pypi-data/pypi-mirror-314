"""WilsonThetaTransientSolver"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.system_solvers import _117

_WILSON_THETA_TRANSIENT_SOLVER = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.SystemSolvers", "WilsonThetaTransientSolver"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.system_solvers import (
        _106,
        _107,
        _116,
        _118,
        _119,
    )

    Self = TypeVar("Self", bound="WilsonThetaTransientSolver")
    CastSelf = TypeVar(
        "CastSelf", bound="WilsonThetaTransientSolver._Cast_WilsonThetaTransientSolver"
    )


__docformat__ = "restructuredtext en"
__all__ = ("WilsonThetaTransientSolver",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WilsonThetaTransientSolver:
    """Special nested class for casting WilsonThetaTransientSolver to subclasses."""

    __parent__: "WilsonThetaTransientSolver"

    @property
    def step_halving_transient_solver(
        self: "CastSelf",
    ) -> "_117.StepHalvingTransientSolver":
        return self.__parent__._cast(_117.StepHalvingTransientSolver)

    @property
    def internal_transient_solver(self: "CastSelf") -> "_107.InternalTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _107

        return self.__parent__._cast(_107.InternalTransientSolver)

    @property
    def transient_solver(self: "CastSelf") -> "_119.TransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _119

        return self.__parent__._cast(_119.TransientSolver)

    @property
    def dynamic_solver(self: "CastSelf") -> "_106.DynamicSolver":
        from mastapy._private.nodal_analysis.system_solvers import _106

        return self.__parent__._cast(_106.DynamicSolver)

    @property
    def stiffness_solver(self: "CastSelf") -> "_118.StiffnessSolver":
        from mastapy._private.nodal_analysis.system_solvers import _118

        return self.__parent__._cast(_118.StiffnessSolver)

    @property
    def solver(self: "CastSelf") -> "_116.Solver":
        from mastapy._private.nodal_analysis.system_solvers import _116

        return self.__parent__._cast(_116.Solver)

    @property
    def wilson_theta_transient_solver(self: "CastSelf") -> "WilsonThetaTransientSolver":
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
class WilsonThetaTransientSolver(_117.StepHalvingTransientSolver):
    """WilsonThetaTransientSolver

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WILSON_THETA_TRANSIENT_SOLVER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_WilsonThetaTransientSolver":
        """Cast to another type.

        Returns:
            _Cast_WilsonThetaTransientSolver
        """
        return _Cast_WilsonThetaTransientSolver(self)
