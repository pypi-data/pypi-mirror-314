"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.concept._561 import ConceptGearDutyCycleRating
    from mastapy._private.gears.rating.concept._562 import (
        ConceptGearMeshDutyCycleRating,
    )
    from mastapy._private.gears.rating.concept._563 import ConceptGearMeshRating
    from mastapy._private.gears.rating.concept._564 import ConceptGearRating
    from mastapy._private.gears.rating.concept._565 import ConceptGearSetDutyCycleRating
    from mastapy._private.gears.rating.concept._566 import ConceptGearSetRating
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.concept._561": ["ConceptGearDutyCycleRating"],
        "_private.gears.rating.concept._562": ["ConceptGearMeshDutyCycleRating"],
        "_private.gears.rating.concept._563": ["ConceptGearMeshRating"],
        "_private.gears.rating.concept._564": ["ConceptGearRating"],
        "_private.gears.rating.concept._565": ["ConceptGearSetDutyCycleRating"],
        "_private.gears.rating.concept._566": ["ConceptGearSetRating"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConceptGearDutyCycleRating",
    "ConceptGearMeshDutyCycleRating",
    "ConceptGearMeshRating",
    "ConceptGearRating",
    "ConceptGearSetDutyCycleRating",
    "ConceptGearSetRating",
)
