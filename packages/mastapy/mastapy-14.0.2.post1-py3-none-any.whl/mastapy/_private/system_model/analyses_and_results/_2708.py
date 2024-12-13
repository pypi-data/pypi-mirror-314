"""CompoundAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _7727
from mastapy._private._internal import conversion, utility
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
_COMPOUND_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults", "CompoundAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Iterable, Type, TypeVar

    from mastapy._private import _7733
    from mastapy._private.system_model import _2260
    from mastapy._private.system_model.analyses_and_results import (
        _2747,
        _2748,
        _2749,
        _2750,
        _2751,
        _2752,
        _2753,
        _2754,
        _2755,
        _2756,
        _2757,
        _2758,
        _2759,
        _2760,
        _2761,
        _2762,
        _2763,
        _2764,
        _2765,
        _2766,
        _2767,
        _2768,
        _2769,
        _2770,
        _2771,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7717

    Self = TypeVar("Self", bound="CompoundAnalysis")
    CastSelf = TypeVar("CastSelf", bound="CompoundAnalysis._Cast_CompoundAnalysis")


__docformat__ = "restructuredtext en"
__all__ = ("CompoundAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CompoundAnalysis:
    """Special nested class for casting CompoundAnalysis to subclasses."""

    __parent__: "CompoundAnalysis"

    @property
    def marshal_by_ref_object_permanent(
        self: "CastSelf",
    ) -> "_7727.MarshalByRefObjectPermanent":
        return self.__parent__._cast(_7727.MarshalByRefObjectPermanent)

    @property
    def compound_advanced_system_deflection_analysis(
        self: "CastSelf",
    ) -> "_2747.CompoundAdvancedSystemDeflectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2747

        return self.__parent__._cast(_2747.CompoundAdvancedSystemDeflectionAnalysis)

    @property
    def compound_advanced_system_deflection_sub_analysis(
        self: "CastSelf",
    ) -> "_2748.CompoundAdvancedSystemDeflectionSubAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2748

        return self.__parent__._cast(_2748.CompoundAdvancedSystemDeflectionSubAnalysis)

    @property
    def compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_2749.CompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results import _2749

        return self.__parent__._cast(
            _2749.CompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_2750.CompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2750

        return self.__parent__._cast(_2750.CompoundCriticalSpeedAnalysis)

    @property
    def compound_dynamic_analysis(self: "CastSelf") -> "_2751.CompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2751

        return self.__parent__._cast(_2751.CompoundDynamicAnalysis)

    @property
    def compound_dynamic_model_at_a_stiffness_analysis(
        self: "CastSelf",
    ) -> "_2752.CompoundDynamicModelAtAStiffnessAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2752

        return self.__parent__._cast(_2752.CompoundDynamicModelAtAStiffnessAnalysis)

    @property
    def compound_dynamic_model_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "_2753.CompoundDynamicModelForHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2753

        return self.__parent__._cast(_2753.CompoundDynamicModelForHarmonicAnalysis)

    @property
    def compound_dynamic_model_for_modal_analysis(
        self: "CastSelf",
    ) -> "_2754.CompoundDynamicModelForModalAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2754

        return self.__parent__._cast(_2754.CompoundDynamicModelForModalAnalysis)

    @property
    def compound_dynamic_model_for_stability_analysis(
        self: "CastSelf",
    ) -> "_2755.CompoundDynamicModelForStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2755

        return self.__parent__._cast(_2755.CompoundDynamicModelForStabilityAnalysis)

    @property
    def compound_dynamic_model_for_steady_state_synchronous_response_analysis(
        self: "CastSelf",
    ) -> "_2756.CompoundDynamicModelForSteadyStateSynchronousResponseAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2756

        return self.__parent__._cast(
            _2756.CompoundDynamicModelForSteadyStateSynchronousResponseAnalysis
        )

    @property
    def compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_2757.CompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2757

        return self.__parent__._cast(_2757.CompoundHarmonicAnalysis)

    @property
    def compound_harmonic_analysis_for_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_2758.CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results import _2758

        return self.__parent__._cast(
            _2758.CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def compound_harmonic_analysis_of_single_excitation_analysis(
        self: "CastSelf",
    ) -> "_2759.CompoundHarmonicAnalysisOfSingleExcitationAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2759

        return self.__parent__._cast(
            _2759.CompoundHarmonicAnalysisOfSingleExcitationAnalysis
        )

    @property
    def compound_modal_analysis(self: "CastSelf") -> "_2760.CompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2760

        return self.__parent__._cast(_2760.CompoundModalAnalysis)

    @property
    def compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_2761.CompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results import _2761

        return self.__parent__._cast(_2761.CompoundModalAnalysisAtASpeed)

    @property
    def compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_2762.CompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results import _2762

        return self.__parent__._cast(_2762.CompoundModalAnalysisAtAStiffness)

    @property
    def compound_modal_analysis_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "_2763.CompoundModalAnalysisForHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2763

        return self.__parent__._cast(_2763.CompoundModalAnalysisForHarmonicAnalysis)

    @property
    def compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_2764.CompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2764

        return self.__parent__._cast(_2764.CompoundMultibodyDynamicsAnalysis)

    @property
    def compound_power_flow_analysis(
        self: "CastSelf",
    ) -> "_2765.CompoundPowerFlowAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2765

        return self.__parent__._cast(_2765.CompoundPowerFlowAnalysis)

    @property
    def compound_stability_analysis(
        self: "CastSelf",
    ) -> "_2766.CompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2766

        return self.__parent__._cast(_2766.CompoundStabilityAnalysis)

    @property
    def compound_steady_state_synchronous_response_analysis(
        self: "CastSelf",
    ) -> "_2767.CompoundSteadyStateSynchronousResponseAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2767

        return self.__parent__._cast(
            _2767.CompoundSteadyStateSynchronousResponseAnalysis
        )

    @property
    def compound_steady_state_synchronous_response_at_a_speed_analysis(
        self: "CastSelf",
    ) -> "_2768.CompoundSteadyStateSynchronousResponseAtASpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2768

        return self.__parent__._cast(
            _2768.CompoundSteadyStateSynchronousResponseAtASpeedAnalysis
        )

    @property
    def compound_steady_state_synchronous_response_on_a_shaft_analysis(
        self: "CastSelf",
    ) -> "_2769.CompoundSteadyStateSynchronousResponseOnAShaftAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2769

        return self.__parent__._cast(
            _2769.CompoundSteadyStateSynchronousResponseOnAShaftAnalysis
        )

    @property
    def compound_system_deflection_analysis(
        self: "CastSelf",
    ) -> "_2770.CompoundSystemDeflectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2770

        return self.__parent__._cast(_2770.CompoundSystemDeflectionAnalysis)

    @property
    def compound_torsional_system_deflection_analysis(
        self: "CastSelf",
    ) -> "_2771.CompoundTorsionalSystemDeflectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2771

        return self.__parent__._cast(_2771.CompoundTorsionalSystemDeflectionAnalysis)

    @property
    def compound_analysis(self: "CastSelf") -> "CompoundAnalysis":
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
class CompoundAnalysis(_7727.MarshalByRefObjectPermanent):
    """CompoundAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPOUND_ANALYSIS

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
        self: "Self", progress: "_7733.TaskProgress"
    ) -> None:
        """Method does not return.

        Args:
            progress (mastapy.TaskProgress)
        """
        pythonnet_method_call_overload(
            self.wrapped,
            "PerformAnalysis",
            [_TASK_PROGRESS],
            progress.wrapped if progress else None,
        )

    @enforce_parameter_types
    def results_for(
        self: "Self", design_entity: "_2260.DesignEntity"
    ) -> "Iterable[_7717.DesignEntityCompoundAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.analysis_cases.DesignEntityCompoundAnalysis]

        Args:
            design_entity (mastapy.system_model.DesignEntity)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call(
                self.wrapped,
                "ResultsFor",
                design_entity.wrapped if design_entity else None,
            )
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CompoundAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CompoundAnalysis
        """
        return _Cast_CompoundAnalysis(self)
