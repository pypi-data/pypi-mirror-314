"""MultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7725

_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "MultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.system_solvers import _119
    from mastapy._private.system_model.analyses_and_results import _2739
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7709
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5591

    Self = TypeVar("Self", bound="MultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="MultibodyDynamicsAnalysis._Cast_MultibodyDynamicsAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MultibodyDynamicsAnalysis:
    """Special nested class for casting MultibodyDynamicsAnalysis to subclasses."""

    __parent__: "MultibodyDynamicsAnalysis"

    @property
    def time_series_load_analysis_case(
        self: "CastSelf",
    ) -> "_7725.TimeSeriesLoadAnalysisCase":
        return self.__parent__._cast(_7725.TimeSeriesLoadAnalysisCase)

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
    def multibody_dynamics_analysis(self: "CastSelf") -> "MultibodyDynamicsAnalysis":
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
class MultibodyDynamicsAnalysis(_7725.TimeSeriesLoadAnalysisCase):
    """MultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MULTIBODY_DYNAMICS_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def has_interface_analysis_results_available(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HasInterfaceAnalysisResultsAvailable"
        )

        if temp is None:
            return False

        return temp

    @property
    def percentage_time_spent_in_masta_solver(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PercentageTimeSpentInMASTASolver")

        if temp is None:
            return 0.0

        return temp

    @property
    def mbd_options(self: "Self") -> "_5591.MBDAnalysisOptions":
        """mastapy.system_model.analyses_and_results.mbd_analyses.MBDAnalysisOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MBDOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def transient_solver(self: "Self") -> "_119.TransientSolver":
        """mastapy.nodal_analysis.system_solvers.TransientSolver

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransientSolver")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_MultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_MultibodyDynamicsAnalysis
        """
        return _Cast_MultibodyDynamicsAnalysis(self)
