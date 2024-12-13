"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results._2708 import (
        CompoundAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2709 import SingleAnalysis
    from mastapy._private.system_model.analyses_and_results._2710 import (
        AdvancedSystemDeflectionAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2711 import (
        AdvancedSystemDeflectionSubAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2712 import (
        AdvancedTimeSteppingAnalysisForModulation,
    )
    from mastapy._private.system_model.analyses_and_results._2713 import (
        CompoundParametricStudyToolAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2714 import (
        CriticalSpeedAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2715 import DynamicAnalysis
    from mastapy._private.system_model.analyses_and_results._2716 import (
        DynamicModelAtAStiffnessAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2717 import (
        DynamicModelForHarmonicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2718 import (
        DynamicModelForModalAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2719 import (
        DynamicModelForStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2720 import (
        DynamicModelForSteadyStateSynchronousResponseAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2721 import (
        HarmonicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2722 import (
        HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation,
    )
    from mastapy._private.system_model.analyses_and_results._2723 import (
        HarmonicAnalysisOfSingleExcitationAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2724 import ModalAnalysis
    from mastapy._private.system_model.analyses_and_results._2725 import (
        ModalAnalysisAtASpeed,
    )
    from mastapy._private.system_model.analyses_and_results._2726 import (
        ModalAnalysisAtAStiffness,
    )
    from mastapy._private.system_model.analyses_and_results._2727 import (
        ModalAnalysisForHarmonicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2728 import (
        MultibodyDynamicsAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2729 import (
        ParametricStudyToolAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2730 import (
        PowerFlowAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2731 import (
        StabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2732 import (
        SteadyStateSynchronousResponseAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2733 import (
        SteadyStateSynchronousResponseAtASpeedAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2734 import (
        SteadyStateSynchronousResponseOnAShaftAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2735 import (
        SystemDeflectionAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2736 import (
        TorsionalSystemDeflectionAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2737 import (
        AnalysisCaseVariable,
    )
    from mastapy._private.system_model.analyses_and_results._2738 import (
        ConnectionAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2739 import Context
    from mastapy._private.system_model.analyses_and_results._2740 import (
        DesignEntityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2741 import (
        DesignEntityGroupAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2742 import (
        DesignEntitySingleContextAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2746 import PartAnalysis
    from mastapy._private.system_model.analyses_and_results._2747 import (
        CompoundAdvancedSystemDeflectionAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2748 import (
        CompoundAdvancedSystemDeflectionSubAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2749 import (
        CompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from mastapy._private.system_model.analyses_and_results._2750 import (
        CompoundCriticalSpeedAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2751 import (
        CompoundDynamicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2752 import (
        CompoundDynamicModelAtAStiffnessAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2753 import (
        CompoundDynamicModelForHarmonicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2754 import (
        CompoundDynamicModelForModalAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2755 import (
        CompoundDynamicModelForStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2756 import (
        CompoundDynamicModelForSteadyStateSynchronousResponseAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2757 import (
        CompoundHarmonicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2758 import (
        CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation,
    )
    from mastapy._private.system_model.analyses_and_results._2759 import (
        CompoundHarmonicAnalysisOfSingleExcitationAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2760 import (
        CompoundModalAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2761 import (
        CompoundModalAnalysisAtASpeed,
    )
    from mastapy._private.system_model.analyses_and_results._2762 import (
        CompoundModalAnalysisAtAStiffness,
    )
    from mastapy._private.system_model.analyses_and_results._2763 import (
        CompoundModalAnalysisForHarmonicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2764 import (
        CompoundMultibodyDynamicsAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2765 import (
        CompoundPowerFlowAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2766 import (
        CompoundStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2767 import (
        CompoundSteadyStateSynchronousResponseAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2768 import (
        CompoundSteadyStateSynchronousResponseAtASpeedAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2769 import (
        CompoundSteadyStateSynchronousResponseOnAShaftAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2770 import (
        CompoundSystemDeflectionAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2771 import (
        CompoundTorsionalSystemDeflectionAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2772 import (
        TESetUpForDynamicAnalysisOptions,
    )
    from mastapy._private.system_model.analyses_and_results._2773 import TimeOptions
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results._2708": ["CompoundAnalysis"],
        "_private.system_model.analyses_and_results._2709": ["SingleAnalysis"],
        "_private.system_model.analyses_and_results._2710": [
            "AdvancedSystemDeflectionAnalysis"
        ],
        "_private.system_model.analyses_and_results._2711": [
            "AdvancedSystemDeflectionSubAnalysis"
        ],
        "_private.system_model.analyses_and_results._2712": [
            "AdvancedTimeSteppingAnalysisForModulation"
        ],
        "_private.system_model.analyses_and_results._2713": [
            "CompoundParametricStudyToolAnalysis"
        ],
        "_private.system_model.analyses_and_results._2714": ["CriticalSpeedAnalysis"],
        "_private.system_model.analyses_and_results._2715": ["DynamicAnalysis"],
        "_private.system_model.analyses_and_results._2716": [
            "DynamicModelAtAStiffnessAnalysis"
        ],
        "_private.system_model.analyses_and_results._2717": [
            "DynamicModelForHarmonicAnalysis"
        ],
        "_private.system_model.analyses_and_results._2718": [
            "DynamicModelForModalAnalysis"
        ],
        "_private.system_model.analyses_and_results._2719": [
            "DynamicModelForStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results._2720": [
            "DynamicModelForSteadyStateSynchronousResponseAnalysis"
        ],
        "_private.system_model.analyses_and_results._2721": ["HarmonicAnalysis"],
        "_private.system_model.analyses_and_results._2722": [
            "HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_private.system_model.analyses_and_results._2723": [
            "HarmonicAnalysisOfSingleExcitationAnalysis"
        ],
        "_private.system_model.analyses_and_results._2724": ["ModalAnalysis"],
        "_private.system_model.analyses_and_results._2725": ["ModalAnalysisAtASpeed"],
        "_private.system_model.analyses_and_results._2726": [
            "ModalAnalysisAtAStiffness"
        ],
        "_private.system_model.analyses_and_results._2727": [
            "ModalAnalysisForHarmonicAnalysis"
        ],
        "_private.system_model.analyses_and_results._2728": [
            "MultibodyDynamicsAnalysis"
        ],
        "_private.system_model.analyses_and_results._2729": [
            "ParametricStudyToolAnalysis"
        ],
        "_private.system_model.analyses_and_results._2730": ["PowerFlowAnalysis"],
        "_private.system_model.analyses_and_results._2731": ["StabilityAnalysis"],
        "_private.system_model.analyses_and_results._2732": [
            "SteadyStateSynchronousResponseAnalysis"
        ],
        "_private.system_model.analyses_and_results._2733": [
            "SteadyStateSynchronousResponseAtASpeedAnalysis"
        ],
        "_private.system_model.analyses_and_results._2734": [
            "SteadyStateSynchronousResponseOnAShaftAnalysis"
        ],
        "_private.system_model.analyses_and_results._2735": [
            "SystemDeflectionAnalysis"
        ],
        "_private.system_model.analyses_and_results._2736": [
            "TorsionalSystemDeflectionAnalysis"
        ],
        "_private.system_model.analyses_and_results._2737": ["AnalysisCaseVariable"],
        "_private.system_model.analyses_and_results._2738": ["ConnectionAnalysis"],
        "_private.system_model.analyses_and_results._2739": ["Context"],
        "_private.system_model.analyses_and_results._2740": ["DesignEntityAnalysis"],
        "_private.system_model.analyses_and_results._2741": [
            "DesignEntityGroupAnalysis"
        ],
        "_private.system_model.analyses_and_results._2742": [
            "DesignEntitySingleContextAnalysis"
        ],
        "_private.system_model.analyses_and_results._2746": ["PartAnalysis"],
        "_private.system_model.analyses_and_results._2747": [
            "CompoundAdvancedSystemDeflectionAnalysis"
        ],
        "_private.system_model.analyses_and_results._2748": [
            "CompoundAdvancedSystemDeflectionSubAnalysis"
        ],
        "_private.system_model.analyses_and_results._2749": [
            "CompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_private.system_model.analyses_and_results._2750": [
            "CompoundCriticalSpeedAnalysis"
        ],
        "_private.system_model.analyses_and_results._2751": ["CompoundDynamicAnalysis"],
        "_private.system_model.analyses_and_results._2752": [
            "CompoundDynamicModelAtAStiffnessAnalysis"
        ],
        "_private.system_model.analyses_and_results._2753": [
            "CompoundDynamicModelForHarmonicAnalysis"
        ],
        "_private.system_model.analyses_and_results._2754": [
            "CompoundDynamicModelForModalAnalysis"
        ],
        "_private.system_model.analyses_and_results._2755": [
            "CompoundDynamicModelForStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results._2756": [
            "CompoundDynamicModelForSteadyStateSynchronousResponseAnalysis"
        ],
        "_private.system_model.analyses_and_results._2757": [
            "CompoundHarmonicAnalysis"
        ],
        "_private.system_model.analyses_and_results._2758": [
            "CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_private.system_model.analyses_and_results._2759": [
            "CompoundHarmonicAnalysisOfSingleExcitationAnalysis"
        ],
        "_private.system_model.analyses_and_results._2760": ["CompoundModalAnalysis"],
        "_private.system_model.analyses_and_results._2761": [
            "CompoundModalAnalysisAtASpeed"
        ],
        "_private.system_model.analyses_and_results._2762": [
            "CompoundModalAnalysisAtAStiffness"
        ],
        "_private.system_model.analyses_and_results._2763": [
            "CompoundModalAnalysisForHarmonicAnalysis"
        ],
        "_private.system_model.analyses_and_results._2764": [
            "CompoundMultibodyDynamicsAnalysis"
        ],
        "_private.system_model.analyses_and_results._2765": [
            "CompoundPowerFlowAnalysis"
        ],
        "_private.system_model.analyses_and_results._2766": [
            "CompoundStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results._2767": [
            "CompoundSteadyStateSynchronousResponseAnalysis"
        ],
        "_private.system_model.analyses_and_results._2768": [
            "CompoundSteadyStateSynchronousResponseAtASpeedAnalysis"
        ],
        "_private.system_model.analyses_and_results._2769": [
            "CompoundSteadyStateSynchronousResponseOnAShaftAnalysis"
        ],
        "_private.system_model.analyses_and_results._2770": [
            "CompoundSystemDeflectionAnalysis"
        ],
        "_private.system_model.analyses_and_results._2771": [
            "CompoundTorsionalSystemDeflectionAnalysis"
        ],
        "_private.system_model.analyses_and_results._2772": [
            "TESetUpForDynamicAnalysisOptions"
        ],
        "_private.system_model.analyses_and_results._2773": ["TimeOptions"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CompoundAnalysis",
    "SingleAnalysis",
    "AdvancedSystemDeflectionAnalysis",
    "AdvancedSystemDeflectionSubAnalysis",
    "AdvancedTimeSteppingAnalysisForModulation",
    "CompoundParametricStudyToolAnalysis",
    "CriticalSpeedAnalysis",
    "DynamicAnalysis",
    "DynamicModelAtAStiffnessAnalysis",
    "DynamicModelForHarmonicAnalysis",
    "DynamicModelForModalAnalysis",
    "DynamicModelForStabilityAnalysis",
    "DynamicModelForSteadyStateSynchronousResponseAnalysis",
    "HarmonicAnalysis",
    "HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation",
    "HarmonicAnalysisOfSingleExcitationAnalysis",
    "ModalAnalysis",
    "ModalAnalysisAtASpeed",
    "ModalAnalysisAtAStiffness",
    "ModalAnalysisForHarmonicAnalysis",
    "MultibodyDynamicsAnalysis",
    "ParametricStudyToolAnalysis",
    "PowerFlowAnalysis",
    "StabilityAnalysis",
    "SteadyStateSynchronousResponseAnalysis",
    "SteadyStateSynchronousResponseAtASpeedAnalysis",
    "SteadyStateSynchronousResponseOnAShaftAnalysis",
    "SystemDeflectionAnalysis",
    "TorsionalSystemDeflectionAnalysis",
    "AnalysisCaseVariable",
    "ConnectionAnalysis",
    "Context",
    "DesignEntityAnalysis",
    "DesignEntityGroupAnalysis",
    "DesignEntitySingleContextAnalysis",
    "PartAnalysis",
    "CompoundAdvancedSystemDeflectionAnalysis",
    "CompoundAdvancedSystemDeflectionSubAnalysis",
    "CompoundAdvancedTimeSteppingAnalysisForModulation",
    "CompoundCriticalSpeedAnalysis",
    "CompoundDynamicAnalysis",
    "CompoundDynamicModelAtAStiffnessAnalysis",
    "CompoundDynamicModelForHarmonicAnalysis",
    "CompoundDynamicModelForModalAnalysis",
    "CompoundDynamicModelForStabilityAnalysis",
    "CompoundDynamicModelForSteadyStateSynchronousResponseAnalysis",
    "CompoundHarmonicAnalysis",
    "CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation",
    "CompoundHarmonicAnalysisOfSingleExcitationAnalysis",
    "CompoundModalAnalysis",
    "CompoundModalAnalysisAtASpeed",
    "CompoundModalAnalysisAtAStiffness",
    "CompoundModalAnalysisForHarmonicAnalysis",
    "CompoundMultibodyDynamicsAnalysis",
    "CompoundPowerFlowAnalysis",
    "CompoundStabilityAnalysis",
    "CompoundSteadyStateSynchronousResponseAnalysis",
    "CompoundSteadyStateSynchronousResponseAtASpeedAnalysis",
    "CompoundSteadyStateSynchronousResponseOnAShaftAnalysis",
    "CompoundSystemDeflectionAnalysis",
    "CompoundTorsionalSystemDeflectionAnalysis",
    "TESetUpForDynamicAnalysisOptions",
    "TimeOptions",
)
