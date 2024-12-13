"""StiffnessSolver"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.system_solvers import _116

_STIFFNESS_SOLVER = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.SystemSolvers", "StiffnessSolver"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.system_solvers import (
        _103,
        _105,
        _106,
        _107,
        _108,
        _109,
        _112,
        _117,
        _119,
        _120,
    )

    Self = TypeVar("Self", bound="StiffnessSolver")
    CastSelf = TypeVar("CastSelf", bound="StiffnessSolver._Cast_StiffnessSolver")


__docformat__ = "restructuredtext en"
__all__ = ("StiffnessSolver",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StiffnessSolver:
    """Special nested class for casting StiffnessSolver to subclasses."""

    __parent__: "StiffnessSolver"

    @property
    def solver(self: "CastSelf") -> "_116.Solver":
        return self.__parent__._cast(_116.Solver)

    @property
    def backward_euler_transient_solver(
        self: "CastSelf",
    ) -> "_103.BackwardEulerTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _103

        return self.__parent__._cast(_103.BackwardEulerTransientSolver)

    @property
    def dirk_transient_solver(self: "CastSelf") -> "_105.DirkTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _105

        return self.__parent__._cast(_105.DirkTransientSolver)

    @property
    def dynamic_solver(self: "CastSelf") -> "_106.DynamicSolver":
        from mastapy._private.nodal_analysis.system_solvers import _106

        return self.__parent__._cast(_106.DynamicSolver)

    @property
    def internal_transient_solver(self: "CastSelf") -> "_107.InternalTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _107

        return self.__parent__._cast(_107.InternalTransientSolver)

    @property
    def lobatto_iiic_transient_solver(
        self: "CastSelf",
    ) -> "_108.LobattoIIICTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _108

        return self.__parent__._cast(_108.LobattoIIICTransientSolver)

    @property
    def newmark_transient_solver(self: "CastSelf") -> "_109.NewmarkTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _109

        return self.__parent__._cast(_109.NewmarkTransientSolver)

    @property
    def simple_velocity_based_step_halving_transient_solver(
        self: "CastSelf",
    ) -> "_112.SimpleVelocityBasedStepHalvingTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _112

        return self.__parent__._cast(_112.SimpleVelocityBasedStepHalvingTransientSolver)

    @property
    def step_halving_transient_solver(
        self: "CastSelf",
    ) -> "_117.StepHalvingTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _117

        return self.__parent__._cast(_117.StepHalvingTransientSolver)

    @property
    def transient_solver(self: "CastSelf") -> "_119.TransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _119

        return self.__parent__._cast(_119.TransientSolver)

    @property
    def wilson_theta_transient_solver(
        self: "CastSelf",
    ) -> "_120.WilsonThetaTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _120

        return self.__parent__._cast(_120.WilsonThetaTransientSolver)

    @property
    def stiffness_solver(self: "CastSelf") -> "StiffnessSolver":
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
class StiffnessSolver(_116.Solver):
    """StiffnessSolver

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STIFFNESS_SOLVER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_StiffnessSolver":
        """Cast to another type.

        Returns:
            _Cast_StiffnessSolver
        """
        return _Cast_StiffnessSolver(self)
