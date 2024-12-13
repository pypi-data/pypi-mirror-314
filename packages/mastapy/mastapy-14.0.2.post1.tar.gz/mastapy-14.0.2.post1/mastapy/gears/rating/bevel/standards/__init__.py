"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.bevel.standards._570 import (
        AGMASpiralBevelGearSingleFlankRating,
    )
    from mastapy._private.gears.rating.bevel.standards._571 import (
        AGMASpiralBevelMeshSingleFlankRating,
    )
    from mastapy._private.gears.rating.bevel.standards._572 import (
        GleasonSpiralBevelGearSingleFlankRating,
    )
    from mastapy._private.gears.rating.bevel.standards._573 import (
        GleasonSpiralBevelMeshSingleFlankRating,
    )
    from mastapy._private.gears.rating.bevel.standards._574 import (
        SpiralBevelGearSingleFlankRating,
    )
    from mastapy._private.gears.rating.bevel.standards._575 import (
        SpiralBevelMeshSingleFlankRating,
    )
    from mastapy._private.gears.rating.bevel.standards._576 import (
        SpiralBevelRateableGear,
    )
    from mastapy._private.gears.rating.bevel.standards._577 import (
        SpiralBevelRateableMesh,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.bevel.standards._570": [
            "AGMASpiralBevelGearSingleFlankRating"
        ],
        "_private.gears.rating.bevel.standards._571": [
            "AGMASpiralBevelMeshSingleFlankRating"
        ],
        "_private.gears.rating.bevel.standards._572": [
            "GleasonSpiralBevelGearSingleFlankRating"
        ],
        "_private.gears.rating.bevel.standards._573": [
            "GleasonSpiralBevelMeshSingleFlankRating"
        ],
        "_private.gears.rating.bevel.standards._574": [
            "SpiralBevelGearSingleFlankRating"
        ],
        "_private.gears.rating.bevel.standards._575": [
            "SpiralBevelMeshSingleFlankRating"
        ],
        "_private.gears.rating.bevel.standards._576": ["SpiralBevelRateableGear"],
        "_private.gears.rating.bevel.standards._577": ["SpiralBevelRateableMesh"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AGMASpiralBevelGearSingleFlankRating",
    "AGMASpiralBevelMeshSingleFlankRating",
    "GleasonSpiralBevelGearSingleFlankRating",
    "GleasonSpiralBevelMeshSingleFlankRating",
    "SpiralBevelGearSingleFlankRating",
    "SpiralBevelMeshSingleFlankRating",
    "SpiralBevelRateableGear",
    "SpiralBevelRateableMesh",
)
