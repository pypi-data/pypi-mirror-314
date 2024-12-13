"""TransientSolver"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.nodal_analysis.system_solvers import _106

_TRANSIENT_SOLVER = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.SystemSolvers", "TransientSolver"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.nodal_analysis import _92
    from mastapy._private.nodal_analysis.system_solvers import (
        _103,
        _105,
        _107,
        _108,
        _109,
        _112,
        _116,
        _117,
        _118,
        _120,
    )

    Self = TypeVar("Self", bound="TransientSolver")
    CastSelf = TypeVar("CastSelf", bound="TransientSolver._Cast_TransientSolver")


__docformat__ = "restructuredtext en"
__all__ = ("TransientSolver",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TransientSolver:
    """Special nested class for casting TransientSolver to subclasses."""

    __parent__: "TransientSolver"

    @property
    def dynamic_solver(self: "CastSelf") -> "_106.DynamicSolver":
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
    def dirk_transient_solver(self: "CastSelf") -> "_105.DirkTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _105

        return self.__parent__._cast(_105.DirkTransientSolver)

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
    def wilson_theta_transient_solver(
        self: "CastSelf",
    ) -> "_120.WilsonThetaTransientSolver":
        from mastapy._private.nodal_analysis.system_solvers import _120

        return self.__parent__._cast(_120.WilsonThetaTransientSolver)

    @property
    def transient_solver(self: "CastSelf") -> "TransientSolver":
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
class TransientSolver(_106.DynamicSolver):
    """TransientSolver

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TRANSIENT_SOLVER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def average_number_of_jacobian_evaluations_per_newton_raphson_solve(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AverageNumberOfJacobianEvaluationsPerNewtonRaphsonSolve"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def interface_analysis_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InterfaceAnalysisTime")

        if temp is None:
            return 0.0

        return temp

    @property
    def number_of_attempted_single_steps(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfAttemptedSingleSteps")

        if temp is None:
            return 0

        return temp

    @property
    def number_of_failed_newton_raphson_solves(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfFailedNewtonRaphsonSolves")

        if temp is None:
            return 0

        return temp

    @property
    def number_of_failed_time_steps(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfFailedTimeSteps")

        if temp is None:
            return 0

        return temp

    @property
    def number_of_failed_time_steps_at_minimum_time_step(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfFailedTimeStepsAtMinimumTimeStep"
        )

        if temp is None:
            return 0

        return temp

    @property
    def number_of_interface_time_steps(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfInterfaceTimeSteps")

        if temp is None:
            return 0

        return temp

    @property
    def number_of_newton_raphson_jacobian_evaluations(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfNewtonRaphsonJacobianEvaluations"
        )

        if temp is None:
            return 0

        return temp

    @property
    def number_of_newton_raphson_maximum_iterations_reached(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfNewtonRaphsonMaximumIterationsReached"
        )

        if temp is None:
            return 0

        return temp

    @property
    def number_of_newton_raphson_other_status_results(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfNewtonRaphsonOtherStatusResults"
        )

        if temp is None:
            return 0

        return temp

    @property
    def number_of_newton_raphson_residual_evaluations(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfNewtonRaphsonResidualEvaluations"
        )

        if temp is None:
            return 0

        return temp

    @property
    def number_of_newton_raphson_residual_tolerance_met(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfNewtonRaphsonResidualToleranceMet"
        )

        if temp is None:
            return 0

        return temp

    @property
    def number_of_newton_raphson_solves(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfNewtonRaphsonSolves")

        if temp is None:
            return 0

        return temp

    @property
    def number_of_newton_raphson_values_not_changing(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfNewtonRaphsonValuesNotChanging"
        )

        if temp is None:
            return 0

        return temp

    @property
    def number_of_successful_single_steps(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfSuccessfulSingleSteps")

        if temp is None:
            return 0

        return temp

    @property
    def number_of_time_steps_taken(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfTimeStepsTaken")

        if temp is None:
            return 0

        return temp

    @property
    def number_of_times_single_step_function_failed(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfTimesSingleStepFunctionFailed"
        )

        if temp is None:
            return 0

        return temp

    @property
    def number_of_times_step_error_tolerance_not_met(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfTimesStepErrorToleranceNotMet"
        )

        if temp is None:
            return 0

        return temp

    @property
    def solver_status(self: "Self") -> "_92.TransientSolverStatus":
        """mastapy.nodal_analysis.TransientSolverStatus"""
        temp = pythonnet_property_get(self.wrapped, "SolverStatus")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.TransientSolverStatus"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis._92", "TransientSolverStatus"
        )(value)

    @solver_status.setter
    @enforce_parameter_types
    def solver_status(self: "Self", value: "_92.TransientSolverStatus") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.TransientSolverStatus"
        )
        pythonnet_property_set(self.wrapped, "SolverStatus", value)

    def times_of_logged_results(self: "Self") -> "List[float]":
        """List[float]"""
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(self.wrapped, "TimesOfLoggedResults"), float
        )

    @property
    def cast_to(self: "Self") -> "_Cast_TransientSolver":
        """Cast to another type.

        Returns:
            _Cast_TransientSolver
        """
        return _Cast_TransientSolver(self)
