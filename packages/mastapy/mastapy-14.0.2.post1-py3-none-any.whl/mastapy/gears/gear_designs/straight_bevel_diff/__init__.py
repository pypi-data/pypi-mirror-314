"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.straight_bevel_diff._991 import (
        StraightBevelDiffGearDesign,
    )
    from mastapy._private.gears.gear_designs.straight_bevel_diff._992 import (
        StraightBevelDiffGearMeshDesign,
    )
    from mastapy._private.gears.gear_designs.straight_bevel_diff._993 import (
        StraightBevelDiffGearSetDesign,
    )
    from mastapy._private.gears.gear_designs.straight_bevel_diff._994 import (
        StraightBevelDiffMeshedGearDesign,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.straight_bevel_diff._991": [
            "StraightBevelDiffGearDesign"
        ],
        "_private.gears.gear_designs.straight_bevel_diff._992": [
            "StraightBevelDiffGearMeshDesign"
        ],
        "_private.gears.gear_designs.straight_bevel_diff._993": [
            "StraightBevelDiffGearSetDesign"
        ],
        "_private.gears.gear_designs.straight_bevel_diff._994": [
            "StraightBevelDiffMeshedGearDesign"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "StraightBevelDiffGearDesign",
    "StraightBevelDiffGearMeshDesign",
    "StraightBevelDiffGearSetDesign",
    "StraightBevelDiffMeshedGearDesign",
)
