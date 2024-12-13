"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles._748 import (
        CutterShapeDefinition,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles._749 import (
        CylindricalGearFormedWheelGrinderTangible,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles._750 import (
        CylindricalGearHobShape,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles._751 import (
        CylindricalGearShaperTangible,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles._752 import (
        CylindricalGearShaverTangible,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles._753 import (
        CylindricalGearWormGrinderShape,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles._754 import (
        NamedPoint,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles._755 import (
        RackShape,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.manufacturing.cylindrical.cutters.tangibles._748": [
            "CutterShapeDefinition"
        ],
        "_private.gears.manufacturing.cylindrical.cutters.tangibles._749": [
            "CylindricalGearFormedWheelGrinderTangible"
        ],
        "_private.gears.manufacturing.cylindrical.cutters.tangibles._750": [
            "CylindricalGearHobShape"
        ],
        "_private.gears.manufacturing.cylindrical.cutters.tangibles._751": [
            "CylindricalGearShaperTangible"
        ],
        "_private.gears.manufacturing.cylindrical.cutters.tangibles._752": [
            "CylindricalGearShaverTangible"
        ],
        "_private.gears.manufacturing.cylindrical.cutters.tangibles._753": [
            "CylindricalGearWormGrinderShape"
        ],
        "_private.gears.manufacturing.cylindrical.cutters.tangibles._754": [
            "NamedPoint"
        ],
        "_private.gears.manufacturing.cylindrical.cutters.tangibles._755": [
            "RackShape"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CutterShapeDefinition",
    "CylindricalGearFormedWheelGrinderTangible",
    "CylindricalGearHobShape",
    "CylindricalGearShaperTangible",
    "CylindricalGearShaverTangible",
    "CylindricalGearWormGrinderShape",
    "NamedPoint",
    "RackShape",
)
