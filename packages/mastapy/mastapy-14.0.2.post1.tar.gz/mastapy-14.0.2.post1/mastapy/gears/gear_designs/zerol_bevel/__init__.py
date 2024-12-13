"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.zerol_bevel._978 import (
        ZerolBevelGearDesign,
    )
    from mastapy._private.gears.gear_designs.zerol_bevel._979 import (
        ZerolBevelGearMeshDesign,
    )
    from mastapy._private.gears.gear_designs.zerol_bevel._980 import (
        ZerolBevelGearSetDesign,
    )
    from mastapy._private.gears.gear_designs.zerol_bevel._981 import (
        ZerolBevelMeshedGearDesign,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.zerol_bevel._978": ["ZerolBevelGearDesign"],
        "_private.gears.gear_designs.zerol_bevel._979": ["ZerolBevelGearMeshDesign"],
        "_private.gears.gear_designs.zerol_bevel._980": ["ZerolBevelGearSetDesign"],
        "_private.gears.gear_designs.zerol_bevel._981": ["ZerolBevelMeshedGearDesign"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ZerolBevelGearDesign",
    "ZerolBevelGearMeshDesign",
    "ZerolBevelGearSetDesign",
    "ZerolBevelMeshedGearDesign",
)
