"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.ltca.conical._888 import ConicalGearBendingStiffness
    from mastapy._private.gears.ltca.conical._889 import ConicalGearBendingStiffnessNode
    from mastapy._private.gears.ltca.conical._890 import ConicalGearContactStiffness
    from mastapy._private.gears.ltca.conical._891 import ConicalGearContactStiffnessNode
    from mastapy._private.gears.ltca.conical._892 import (
        ConicalGearLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca.conical._893 import (
        ConicalGearSetLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca.conical._894 import (
        ConicalMeshedGearLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca.conical._895 import (
        ConicalMeshLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca.conical._896 import (
        ConicalMeshLoadDistributionAtRotation,
    )
    from mastapy._private.gears.ltca.conical._897 import ConicalMeshLoadedContactLine
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.ltca.conical._888": ["ConicalGearBendingStiffness"],
        "_private.gears.ltca.conical._889": ["ConicalGearBendingStiffnessNode"],
        "_private.gears.ltca.conical._890": ["ConicalGearContactStiffness"],
        "_private.gears.ltca.conical._891": ["ConicalGearContactStiffnessNode"],
        "_private.gears.ltca.conical._892": ["ConicalGearLoadDistributionAnalysis"],
        "_private.gears.ltca.conical._893": ["ConicalGearSetLoadDistributionAnalysis"],
        "_private.gears.ltca.conical._894": [
            "ConicalMeshedGearLoadDistributionAnalysis"
        ],
        "_private.gears.ltca.conical._895": ["ConicalMeshLoadDistributionAnalysis"],
        "_private.gears.ltca.conical._896": ["ConicalMeshLoadDistributionAtRotation"],
        "_private.gears.ltca.conical._897": ["ConicalMeshLoadedContactLine"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConicalGearBendingStiffness",
    "ConicalGearBendingStiffnessNode",
    "ConicalGearContactStiffness",
    "ConicalGearContactStiffnessNode",
    "ConicalGearLoadDistributionAnalysis",
    "ConicalGearSetLoadDistributionAnalysis",
    "ConicalMeshedGearLoadDistributionAnalysis",
    "ConicalMeshLoadDistributionAnalysis",
    "ConicalMeshLoadDistributionAtRotation",
    "ConicalMeshLoadedContactLine",
)
