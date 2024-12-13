"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.face._458 import FaceGearDutyCycleRating
    from mastapy._private.gears.rating.face._459 import FaceGearMeshDutyCycleRating
    from mastapy._private.gears.rating.face._460 import FaceGearMeshRating
    from mastapy._private.gears.rating.face._461 import FaceGearRating
    from mastapy._private.gears.rating.face._462 import FaceGearSetDutyCycleRating
    from mastapy._private.gears.rating.face._463 import FaceGearSetRating
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.face._458": ["FaceGearDutyCycleRating"],
        "_private.gears.rating.face._459": ["FaceGearMeshDutyCycleRating"],
        "_private.gears.rating.face._460": ["FaceGearMeshRating"],
        "_private.gears.rating.face._461": ["FaceGearRating"],
        "_private.gears.rating.face._462": ["FaceGearSetDutyCycleRating"],
        "_private.gears.rating.face._463": ["FaceGearSetRating"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "FaceGearDutyCycleRating",
    "FaceGearMeshDutyCycleRating",
    "FaceGearMeshRating",
    "FaceGearRating",
    "FaceGearSetDutyCycleRating",
    "FaceGearSetRating",
)
