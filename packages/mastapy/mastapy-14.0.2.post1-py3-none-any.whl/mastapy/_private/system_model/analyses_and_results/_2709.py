"""SingleAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _7727
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_TASK_PROGRESS = python_net_import("SMT.MastaAPIUtility", "TaskProgress")
_DESIGN_ENTITY = python_net_import("SMT.MastaAPI.SystemModel", "DesignEntity")
_DESIGN_ENTITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults", "DesignEntityAnalysis"
)
_SINGLE_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults", "SingleAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private import _7733
    from mastapy._private.system_model import _2260
    from mastapy._private.system_model.analyses_and_results import (
        _2710,
        _2711,
        _2712,
        _2713,
        _2714,
        _2715,
        _2716,
        _2717,
        _2718,
        _2719,
        _2720,
        _2721,
        _2722,
        _2723,
        _2724,
        _2725,
        _2726,
        _2727,
        _2728,
        _2729,
        _2730,
        _2731,
        _2732,
        _2733,
        _2734,
        _2735,
        _2736,
        _2740,
    )

    Self = TypeVar("Self", bound="SingleAnalysis")
    CastSelf = TypeVar("CastSelf", bound="SingleAnalysis._Cast_SingleAnalysis")


__docformat__ = "restructuredtext en"
__all__ = ("SingleAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SingleAnalysis:
    """Special nested class for casting SingleAnalysis to subclasses."""

    __parent__: "SingleAnalysis"

    @property
    def marshal_by_ref_object_permanent(
        self: "CastSelf",
    ) -> "_7727.MarshalByRefObjectPermanent":
        return self.__parent__._cast(_7727.MarshalByRefObjectPermanent)

    @property
    def advanced_system_deflection_analysis(
        self: "CastSelf",
    ) -> "_2710.AdvancedSystemDeflectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2710

        return self.__parent__._cast(_2710.AdvancedSystemDeflectionAnalysis)

    @property
    def advanced_system_deflection_sub_analysis(
        self: "CastSelf",
    ) -> "_2711.AdvancedSystemDeflectionSubAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2711

        return self.__parent__._cast(_2711.AdvancedSystemDeflectionSubAnalysis)

    @property
    def advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_2712.AdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results import _2712

        return self.__parent__._cast(_2712.AdvancedTimeSteppingAnalysisForModulation)

    @property
    def compound_parametric_study_tool_analysis(
        self: "CastSelf",
    ) -> "_2713.CompoundParametricStudyToolAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2713

        return self.__parent__._cast(_2713.CompoundParametricStudyToolAnalysis)

    @property
    def critical_speed_analysis(self: "CastSelf") -> "_2714.CriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2714

        return self.__parent__._cast(_2714.CriticalSpeedAnalysis)

    @property
    def dynamic_analysis(self: "CastSelf") -> "_2715.DynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2715

        return self.__parent__._cast(_2715.DynamicAnalysis)

    @property
    def dynamic_model_at_a_stiffness_analysis(
        self: "CastSelf",
    ) -> "_2716.DynamicModelAtAStiffnessAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2716

        return self.__parent__._cast(_2716.DynamicModelAtAStiffnessAnalysis)

    @property
    def dynamic_model_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "_2717.DynamicModelForHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2717

        return self.__parent__._cast(_2717.DynamicModelForHarmonicAnalysis)

    @property
    def dynamic_model_for_modal_analysis(
        self: "CastSelf",
    ) -> "_2718.DynamicModelForModalAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2718

        return self.__parent__._cast(_2718.DynamicModelForModalAnalysis)

    @property
    def dynamic_model_for_stability_analysis(
        self: "CastSelf",
    ) -> "_2719.DynamicModelForStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2719

        return self.__parent__._cast(_2719.DynamicModelForStabilityAnalysis)

    @property
    def dynamic_model_for_steady_state_synchronous_response_analysis(
        self: "CastSelf",
    ) -> "_2720.DynamicModelForSteadyStateSynchronousResponseAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2720

        return self.__parent__._cast(
            _2720.DynamicModelForSteadyStateSynchronousResponseAnalysis
        )

    @property
    def harmonic_analysis(self: "CastSelf") -> "_2721.HarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2721

        return self.__parent__._cast(_2721.HarmonicAnalysis)

    @property
    def harmonic_analysis_for_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_2722.HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results import _2722

        return self.__parent__._cast(
            _2722.HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def harmonic_analysis_of_single_excitation_analysis(
        self: "CastSelf",
    ) -> "_2723.HarmonicAnalysisOfSingleExcitationAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2723

        return self.__parent__._cast(_2723.HarmonicAnalysisOfSingleExcitationAnalysis)

    @property
    def modal_analysis(self: "CastSelf") -> "_2724.ModalAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2724

        return self.__parent__._cast(_2724.ModalAnalysis)

    @property
    def modal_analysis_at_a_speed(self: "CastSelf") -> "_2725.ModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results import _2725

        return self.__parent__._cast(_2725.ModalAnalysisAtASpeed)

    @property
    def modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_2726.ModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results import _2726

        return self.__parent__._cast(_2726.ModalAnalysisAtAStiffness)

    @property
    def modal_analysis_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "_2727.ModalAnalysisForHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2727

        return self.__parent__._cast(_2727.ModalAnalysisForHarmonicAnalysis)

    @property
    def multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_2728.MultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2728

        return self.__parent__._cast(_2728.MultibodyDynamicsAnalysis)

    @property
    def parametric_study_tool_analysis(
        self: "CastSelf",
    ) -> "_2729.ParametricStudyToolAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2729

        return self.__parent__._cast(_2729.ParametricStudyToolAnalysis)

    @property
    def power_flow_analysis(self: "CastSelf") -> "_2730.PowerFlowAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2730

        return self.__parent__._cast(_2730.PowerFlowAnalysis)

    @property
    def stability_analysis(self: "CastSelf") -> "_2731.StabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2731

        return self.__parent__._cast(_2731.StabilityAnalysis)

    @property
    def steady_state_synchronous_response_analysis(
        self: "CastSelf",
    ) -> "_2732.SteadyStateSynchronousResponseAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2732

        return self.__parent__._cast(_2732.SteadyStateSynchronousResponseAnalysis)

    @property
    def steady_state_synchronous_response_at_a_speed_analysis(
        self: "CastSelf",
    ) -> "_2733.SteadyStateSynchronousResponseAtASpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2733

        return self.__parent__._cast(
            _2733.SteadyStateSynchronousResponseAtASpeedAnalysis
        )

    @property
    def steady_state_synchronous_response_on_a_shaft_analysis(
        self: "CastSelf",
    ) -> "_2734.SteadyStateSynchronousResponseOnAShaftAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2734

        return self.__parent__._cast(
            _2734.SteadyStateSynchronousResponseOnAShaftAnalysis
        )

    @property
    def system_deflection_analysis(
        self: "CastSelf",
    ) -> "_2735.SystemDeflectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2735

        return self.__parent__._cast(_2735.SystemDeflectionAnalysis)

    @property
    def torsional_system_deflection_analysis(
        self: "CastSelf",
    ) -> "_2736.TorsionalSystemDeflectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2736

        return self.__parent__._cast(_2736.TorsionalSystemDeflectionAnalysis)

    @property
    def single_analysis(self: "CastSelf") -> "SingleAnalysis":
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
class SingleAnalysis(_7727.MarshalByRefObjectPermanent):
    """SingleAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SINGLE_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def results_ready(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsReady")

        if temp is None:
            return False

        return temp

    def perform_analysis(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "PerformAnalysis")

    @enforce_parameter_types
    def perform_analysis_with_progress(
        self: "Self", task_progress: "_7733.TaskProgress"
    ) -> None:
        """Method does not return.

        Args:
            task_progress (mastapy.TaskProgress)
        """
        pythonnet_method_call_overload(
            self.wrapped,
            "PerformAnalysis",
            [_TASK_PROGRESS],
            task_progress.wrapped if task_progress else None,
        )

    @enforce_parameter_types
    def results_for(
        self: "Self", design_entity: "_2260.DesignEntity"
    ) -> "_2740.DesignEntityAnalysis":
        """mastapy.system_model.analyses_and_results.DesignEntityAnalysis

        Args:
            design_entity (mastapy.system_model.DesignEntity)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_DESIGN_ENTITY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_design_entity_analysis(
        self: "Self", design_entity_analysis: "_2740.DesignEntityAnalysis"
    ) -> "_2740.DesignEntityAnalysis":
        """mastapy.system_model.analyses_and_results.DesignEntityAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.DesignEntityAnalysis)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_DESIGN_ENTITY_ANALYSIS],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_SingleAnalysis":
        """Cast to another type.

        Returns:
            _Cast_SingleAnalysis
        """
        return _Cast_SingleAnalysis(self)
