"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.zerol_bevel._382 import ZerolBevelGearMeshRating
    from mastapy._private.gears.rating.zerol_bevel._383 import ZerolBevelGearRating
    from mastapy._private.gears.rating.zerol_bevel._384 import ZerolBevelGearSetRating
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.zerol_bevel._382": ["ZerolBevelGearMeshRating"],
        "_private.gears.rating.zerol_bevel._383": ["ZerolBevelGearRating"],
        "_private.gears.rating.zerol_bevel._384": ["ZerolBevelGearSetRating"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ZerolBevelGearMeshRating",
    "ZerolBevelGearRating",
    "ZerolBevelGearSetRating",
)
