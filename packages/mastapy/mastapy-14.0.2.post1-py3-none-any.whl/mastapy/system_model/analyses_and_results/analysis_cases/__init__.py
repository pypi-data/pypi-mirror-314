"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7709 import (
        AnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7710 import (
        AbstractAnalysisOptions,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7711 import (
        CompoundAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7712 import (
        ConnectionAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7713 import (
        ConnectionCompoundAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7714 import (
        ConnectionFEAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7715 import (
        ConnectionStaticLoadAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7716 import (
        ConnectionTimeSeriesLoadAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7717 import (
        DesignEntityCompoundAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7718 import (
        FEAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7719 import (
        PartAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7720 import (
        PartCompoundAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7721 import (
        PartFEAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7722 import (
        PartStaticLoadAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7723 import (
        PartTimeSeriesLoadAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7724 import (
        StaticLoadAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7725 import (
        TimeSeriesLoadAnalysisCase,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.analysis_cases._7709": [
            "AnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7710": [
            "AbstractAnalysisOptions"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7711": [
            "CompoundAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7712": [
            "ConnectionAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7713": [
            "ConnectionCompoundAnalysis"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7714": [
            "ConnectionFEAnalysis"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7715": [
            "ConnectionStaticLoadAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7716": [
            "ConnectionTimeSeriesLoadAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7717": [
            "DesignEntityCompoundAnalysis"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7718": [
            "FEAnalysis"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7719": [
            "PartAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7720": [
            "PartCompoundAnalysis"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7721": [
            "PartFEAnalysis"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7722": [
            "PartStaticLoadAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7723": [
            "PartTimeSeriesLoadAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7724": [
            "StaticLoadAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7725": [
            "TimeSeriesLoadAnalysisCase"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AnalysisCase",
    "AbstractAnalysisOptions",
    "CompoundAnalysisCase",
    "ConnectionAnalysisCase",
    "ConnectionCompoundAnalysis",
    "ConnectionFEAnalysis",
    "ConnectionStaticLoadAnalysisCase",
    "ConnectionTimeSeriesLoadAnalysisCase",
    "DesignEntityCompoundAnalysis",
    "FEAnalysis",
    "PartAnalysisCase",
    "PartCompoundAnalysis",
    "PartFEAnalysis",
    "PartStaticLoadAnalysisCase",
    "PartTimeSeriesLoadAnalysisCase",
    "StaticLoadAnalysisCase",
    "TimeSeriesLoadAnalysisCase",
)
