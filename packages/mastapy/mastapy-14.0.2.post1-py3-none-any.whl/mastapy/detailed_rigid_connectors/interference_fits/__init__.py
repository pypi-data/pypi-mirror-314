"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.detailed_rigid_connectors.interference_fits._1493 import (
        AssemblyMethods,
    )
    from mastapy._private.detailed_rigid_connectors.interference_fits._1494 import (
        CalculationMethods,
    )
    from mastapy._private.detailed_rigid_connectors.interference_fits._1495 import (
        InterferenceFitDesign,
    )
    from mastapy._private.detailed_rigid_connectors.interference_fits._1496 import (
        InterferenceFitHalfDesign,
    )
    from mastapy._private.detailed_rigid_connectors.interference_fits._1497 import (
        StressRegions,
    )
    from mastapy._private.detailed_rigid_connectors.interference_fits._1498 import (
        Table4JointInterfaceTypes,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.detailed_rigid_connectors.interference_fits._1493": [
            "AssemblyMethods"
        ],
        "_private.detailed_rigid_connectors.interference_fits._1494": [
            "CalculationMethods"
        ],
        "_private.detailed_rigid_connectors.interference_fits._1495": [
            "InterferenceFitDesign"
        ],
        "_private.detailed_rigid_connectors.interference_fits._1496": [
            "InterferenceFitHalfDesign"
        ],
        "_private.detailed_rigid_connectors.interference_fits._1497": ["StressRegions"],
        "_private.detailed_rigid_connectors.interference_fits._1498": [
            "Table4JointInterfaceTypes"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AssemblyMethods",
    "CalculationMethods",
    "InterferenceFitDesign",
    "InterferenceFitHalfDesign",
    "StressRegions",
    "Table4JointInterfaceTypes",
)
