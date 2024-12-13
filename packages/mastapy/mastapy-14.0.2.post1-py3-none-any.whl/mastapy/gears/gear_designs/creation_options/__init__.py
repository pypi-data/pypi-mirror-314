"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.creation_options._1186 import (
        CylindricalGearPairCreationOptions,
    )
    from mastapy._private.gears.gear_designs.creation_options._1187 import (
        GearSetCreationOptions,
    )
    from mastapy._private.gears.gear_designs.creation_options._1188 import (
        HypoidGearSetCreationOptions,
    )
    from mastapy._private.gears.gear_designs.creation_options._1189 import (
        SpiralBevelGearSetCreationOptions,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.creation_options._1186": [
            "CylindricalGearPairCreationOptions"
        ],
        "_private.gears.gear_designs.creation_options._1187": [
            "GearSetCreationOptions"
        ],
        "_private.gears.gear_designs.creation_options._1188": [
            "HypoidGearSetCreationOptions"
        ],
        "_private.gears.gear_designs.creation_options._1189": [
            "SpiralBevelGearSetCreationOptions"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CylindricalGearPairCreationOptions",
    "GearSetCreationOptions",
    "HypoidGearSetCreationOptions",
    "SpiralBevelGearSetCreationOptions",
)
