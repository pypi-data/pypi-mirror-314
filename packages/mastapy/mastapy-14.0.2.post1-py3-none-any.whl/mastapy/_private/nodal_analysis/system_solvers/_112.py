"""SimpleVelocityBasedStepHalvingTransientSolver"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.system_solvers import _117

_SIMPLE_VELOCITY_BASED_STEP_HALVING_TRANSIENT_SOLVER = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.SystemSolvers",
    "SimpleVelocityBasedStepHalvingTransientSolver",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.system_solvers import (
        _103,
        _106,
        _107,
        _109,
        _116,
        _118,
        _119,
    )

    Self = TypeVar("Self", bound="SimpleVelocityBasedStepHalvingTransientSolver")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SimpleVelocityBasedStepHalvingTransientSolver._Cast_SimpleVelocityBasedStepHalvingTransientSolver",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SimpleVelocityBasedStepHalvingTransientSolver",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SimpleVelocityBasedStepHalvingTransientSolver:
    """Special nested class for casting SimpleVelocityBasedStepHalvingTransientSolver to subclasses."""

    __parent__: "SimpleVelocityBasedStepHalvingTransientSolver"

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
    def backward_euler_transient_solver(
        self: "CastSelf",
    ) -> "_103.BackwardEulerTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _103

        return self.__parent__._cast(_103.BackwardEulerTransientSolver)

    @property
    def newmark_transient_solver(self: "CastSelf") -> "_109.NewmarkTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _109

        return self.__parent__._cast(_109.NewmarkTransientSolver)

    @property
    def simple_velocity_based_step_halving_transient_solver(
        self: "CastSelf",
    ) -> "SimpleVelocityBasedStepHalvingTransientSolver":
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
class SimpleVelocityBasedStepHalvingTransientSolver(_117.StepHalvingTransientSolver):
    """SimpleVelocityBasedStepHalvingTransientSolver

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SIMPLE_VELOCITY_BASED_STEP_HALVING_TRANSIENT_SOLVER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_SimpleVelocityBasedStepHalvingTransientSolver":
        """Cast to another type.

        Returns:
            _Cast_SimpleVelocityBasedStepHalvingTransientSolver
        """
        return _Cast_SimpleVelocityBasedStepHalvingTransientSolver(self)
