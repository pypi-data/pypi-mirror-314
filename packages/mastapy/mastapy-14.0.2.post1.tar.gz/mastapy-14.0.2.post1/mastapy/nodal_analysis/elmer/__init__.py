"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.nodal_analysis.elmer._176 import ContactType
    from mastapy._private.nodal_analysis.elmer._177 import ElectricMachineAnalysisPeriod
    from mastapy._private.nodal_analysis.elmer._178 import ElmerResultEntityType
    from mastapy._private.nodal_analysis.elmer._179 import ElmerResults
    from mastapy._private.nodal_analysis.elmer._180 import (
        ElmerResultsFromElectromagneticAnalysis,
    )
    from mastapy._private.nodal_analysis.elmer._181 import (
        ElmerResultsFromMechanicalAnalysis,
    )
    from mastapy._private.nodal_analysis.elmer._182 import ElmerResultsViewable
    from mastapy._private.nodal_analysis.elmer._183 import ElmerResultType
    from mastapy._private.nodal_analysis.elmer._184 import (
        MechanicalContactSpecification,
    )
    from mastapy._private.nodal_analysis.elmer._185 import MechanicalSolverType
    from mastapy._private.nodal_analysis.elmer._186 import NodalAverageType
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.nodal_analysis.elmer._176": ["ContactType"],
        "_private.nodal_analysis.elmer._177": ["ElectricMachineAnalysisPeriod"],
        "_private.nodal_analysis.elmer._178": ["ElmerResultEntityType"],
        "_private.nodal_analysis.elmer._179": ["ElmerResults"],
        "_private.nodal_analysis.elmer._180": [
            "ElmerResultsFromElectromagneticAnalysis"
        ],
        "_private.nodal_analysis.elmer._181": ["ElmerResultsFromMechanicalAnalysis"],
        "_private.nodal_analysis.elmer._182": ["ElmerResultsViewable"],
        "_private.nodal_analysis.elmer._183": ["ElmerResultType"],
        "_private.nodal_analysis.elmer._184": ["MechanicalContactSpecification"],
        "_private.nodal_analysis.elmer._185": ["MechanicalSolverType"],
        "_private.nodal_analysis.elmer._186": ["NodalAverageType"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ContactType",
    "ElectricMachineAnalysisPeriod",
    "ElmerResultEntityType",
    "ElmerResults",
    "ElmerResultsFromElectromagneticAnalysis",
    "ElmerResultsFromMechanicalAnalysis",
    "ElmerResultsViewable",
    "ElmerResultType",
    "MechanicalContactSpecification",
    "MechanicalSolverType",
    "NodalAverageType",
)
