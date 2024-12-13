"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.ltca.cylindrical._876 import (
        CylindricalGearBendingStiffness,
    )
    from mastapy._private.gears.ltca.cylindrical._877 import (
        CylindricalGearBendingStiffnessNode,
    )
    from mastapy._private.gears.ltca.cylindrical._878 import (
        CylindricalGearContactStiffness,
    )
    from mastapy._private.gears.ltca.cylindrical._879 import (
        CylindricalGearContactStiffnessNode,
    )
    from mastapy._private.gears.ltca.cylindrical._880 import CylindricalGearFESettings
    from mastapy._private.gears.ltca.cylindrical._881 import (
        CylindricalGearLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca.cylindrical._882 import (
        CylindricalGearMeshLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca.cylindrical._883 import (
        CylindricalGearMeshLoadedContactLine,
    )
    from mastapy._private.gears.ltca.cylindrical._884 import (
        CylindricalGearMeshLoadedContactPoint,
    )
    from mastapy._private.gears.ltca.cylindrical._885 import (
        CylindricalGearSetLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca.cylindrical._886 import (
        CylindricalMeshLoadDistributionAtRotation,
    )
    from mastapy._private.gears.ltca.cylindrical._887 import (
        FaceGearSetLoadDistributionAnalysis,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.ltca.cylindrical._876": ["CylindricalGearBendingStiffness"],
        "_private.gears.ltca.cylindrical._877": ["CylindricalGearBendingStiffnessNode"],
        "_private.gears.ltca.cylindrical._878": ["CylindricalGearContactStiffness"],
        "_private.gears.ltca.cylindrical._879": ["CylindricalGearContactStiffnessNode"],
        "_private.gears.ltca.cylindrical._880": ["CylindricalGearFESettings"],
        "_private.gears.ltca.cylindrical._881": [
            "CylindricalGearLoadDistributionAnalysis"
        ],
        "_private.gears.ltca.cylindrical._882": [
            "CylindricalGearMeshLoadDistributionAnalysis"
        ],
        "_private.gears.ltca.cylindrical._883": [
            "CylindricalGearMeshLoadedContactLine"
        ],
        "_private.gears.ltca.cylindrical._884": [
            "CylindricalGearMeshLoadedContactPoint"
        ],
        "_private.gears.ltca.cylindrical._885": [
            "CylindricalGearSetLoadDistributionAnalysis"
        ],
        "_private.gears.ltca.cylindrical._886": [
            "CylindricalMeshLoadDistributionAtRotation"
        ],
        "_private.gears.ltca.cylindrical._887": ["FaceGearSetLoadDistributionAnalysis"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CylindricalGearBendingStiffness",
    "CylindricalGearBendingStiffnessNode",
    "CylindricalGearContactStiffness",
    "CylindricalGearContactStiffnessNode",
    "CylindricalGearFESettings",
    "CylindricalGearLoadDistributionAnalysis",
    "CylindricalGearMeshLoadDistributionAnalysis",
    "CylindricalGearMeshLoadedContactLine",
    "CylindricalGearMeshLoadedContactPoint",
    "CylindricalGearSetLoadDistributionAnalysis",
    "CylindricalMeshLoadDistributionAtRotation",
    "FaceGearSetLoadDistributionAnalysis",
)
