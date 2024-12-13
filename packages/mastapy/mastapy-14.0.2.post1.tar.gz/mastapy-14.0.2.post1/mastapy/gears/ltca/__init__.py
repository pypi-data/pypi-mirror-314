"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.ltca._850 import ConicalGearFilletStressResults
    from mastapy._private.gears.ltca._851 import ConicalGearRootFilletStressResults
    from mastapy._private.gears.ltca._852 import ContactResultType
    from mastapy._private.gears.ltca._853 import CylindricalGearFilletNodeStressResults
    from mastapy._private.gears.ltca._854 import (
        CylindricalGearFilletNodeStressResultsColumn,
    )
    from mastapy._private.gears.ltca._855 import (
        CylindricalGearFilletNodeStressResultsRow,
    )
    from mastapy._private.gears.ltca._856 import CylindricalGearRootFilletStressResults
    from mastapy._private.gears.ltca._857 import (
        CylindricalMeshedGearLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca._858 import GearBendingStiffness
    from mastapy._private.gears.ltca._859 import GearBendingStiffnessNode
    from mastapy._private.gears.ltca._860 import GearContactStiffness
    from mastapy._private.gears.ltca._861 import GearContactStiffnessNode
    from mastapy._private.gears.ltca._862 import GearFilletNodeStressResults
    from mastapy._private.gears.ltca._863 import GearFilletNodeStressResultsColumn
    from mastapy._private.gears.ltca._864 import GearFilletNodeStressResultsRow
    from mastapy._private.gears.ltca._865 import GearLoadDistributionAnalysis
    from mastapy._private.gears.ltca._866 import GearMeshLoadDistributionAnalysis
    from mastapy._private.gears.ltca._867 import GearMeshLoadDistributionAtRotation
    from mastapy._private.gears.ltca._868 import GearMeshLoadedContactLine
    from mastapy._private.gears.ltca._869 import GearMeshLoadedContactPoint
    from mastapy._private.gears.ltca._870 import GearRootFilletStressResults
    from mastapy._private.gears.ltca._871 import GearSetLoadDistributionAnalysis
    from mastapy._private.gears.ltca._872 import GearStiffness
    from mastapy._private.gears.ltca._873 import GearStiffnessNode
    from mastapy._private.gears.ltca._874 import (
        MeshedGearLoadDistributionAnalysisAtRotation,
    )
    from mastapy._private.gears.ltca._875 import UseAdvancedLTCAOptions
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.ltca._850": ["ConicalGearFilletStressResults"],
        "_private.gears.ltca._851": ["ConicalGearRootFilletStressResults"],
        "_private.gears.ltca._852": ["ContactResultType"],
        "_private.gears.ltca._853": ["CylindricalGearFilletNodeStressResults"],
        "_private.gears.ltca._854": ["CylindricalGearFilletNodeStressResultsColumn"],
        "_private.gears.ltca._855": ["CylindricalGearFilletNodeStressResultsRow"],
        "_private.gears.ltca._856": ["CylindricalGearRootFilletStressResults"],
        "_private.gears.ltca._857": ["CylindricalMeshedGearLoadDistributionAnalysis"],
        "_private.gears.ltca._858": ["GearBendingStiffness"],
        "_private.gears.ltca._859": ["GearBendingStiffnessNode"],
        "_private.gears.ltca._860": ["GearContactStiffness"],
        "_private.gears.ltca._861": ["GearContactStiffnessNode"],
        "_private.gears.ltca._862": ["GearFilletNodeStressResults"],
        "_private.gears.ltca._863": ["GearFilletNodeStressResultsColumn"],
        "_private.gears.ltca._864": ["GearFilletNodeStressResultsRow"],
        "_private.gears.ltca._865": ["GearLoadDistributionAnalysis"],
        "_private.gears.ltca._866": ["GearMeshLoadDistributionAnalysis"],
        "_private.gears.ltca._867": ["GearMeshLoadDistributionAtRotation"],
        "_private.gears.ltca._868": ["GearMeshLoadedContactLine"],
        "_private.gears.ltca._869": ["GearMeshLoadedContactPoint"],
        "_private.gears.ltca._870": ["GearRootFilletStressResults"],
        "_private.gears.ltca._871": ["GearSetLoadDistributionAnalysis"],
        "_private.gears.ltca._872": ["GearStiffness"],
        "_private.gears.ltca._873": ["GearStiffnessNode"],
        "_private.gears.ltca._874": ["MeshedGearLoadDistributionAnalysisAtRotation"],
        "_private.gears.ltca._875": ["UseAdvancedLTCAOptions"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConicalGearFilletStressResults",
    "ConicalGearRootFilletStressResults",
    "ContactResultType",
    "CylindricalGearFilletNodeStressResults",
    "CylindricalGearFilletNodeStressResultsColumn",
    "CylindricalGearFilletNodeStressResultsRow",
    "CylindricalGearRootFilletStressResults",
    "CylindricalMeshedGearLoadDistributionAnalysis",
    "GearBendingStiffness",
    "GearBendingStiffnessNode",
    "GearContactStiffness",
    "GearContactStiffnessNode",
    "GearFilletNodeStressResults",
    "GearFilletNodeStressResultsColumn",
    "GearFilletNodeStressResultsRow",
    "GearLoadDistributionAnalysis",
    "GearMeshLoadDistributionAnalysis",
    "GearMeshLoadDistributionAtRotation",
    "GearMeshLoadedContactLine",
    "GearMeshLoadedContactPoint",
    "GearRootFilletStressResults",
    "GearSetLoadDistributionAnalysis",
    "GearStiffness",
    "GearStiffnessNode",
    "MeshedGearLoadDistributionAnalysisAtRotation",
    "UseAdvancedLTCAOptions",
)
