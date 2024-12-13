"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4835 import (
        CalculateFullFEResultsForMode,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4836 import (
        CampbellDiagramReport,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4837 import (
        ComponentPerModeResult,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4838 import (
        DesignEntityModalAnalysisGroupResults,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4839 import (
        ModalCMSResultsForModeAndFE,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4840 import (
        PerModeResultsReport,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4841 import (
        RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4842 import (
        RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4843 import (
        RigidlyConnectedDesignEntityGroupModalAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4844 import (
        ShaftPerModeResult,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4845 import (
        SingleExcitationResultsModalAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4846 import (
        SingleModeResults,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4835": [
            "CalculateFullFEResultsForMode"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4836": [
            "CampbellDiagramReport"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4837": [
            "ComponentPerModeResult"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4838": [
            "DesignEntityModalAnalysisGroupResults"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4839": [
            "ModalCMSResultsForModeAndFE"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4840": [
            "PerModeResultsReport"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4841": [
            "RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4842": [
            "RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4843": [
            "RigidlyConnectedDesignEntityGroupModalAnalysis"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4844": [
            "ShaftPerModeResult"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4845": [
            "SingleExcitationResultsModalAnalysis"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4846": [
            "SingleModeResults"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CalculateFullFEResultsForMode",
    "CampbellDiagramReport",
    "ComponentPerModeResult",
    "DesignEntityModalAnalysisGroupResults",
    "ModalCMSResultsForModeAndFE",
    "PerModeResultsReport",
    "RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis",
    "RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis",
    "RigidlyConnectedDesignEntityGroupModalAnalysis",
    "ShaftPerModeResult",
    "SingleExcitationResultsModalAnalysis",
    "SingleModeResults",
)
