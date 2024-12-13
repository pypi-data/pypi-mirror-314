"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.conical._551 import ConicalGearDutyCycleRating
    from mastapy._private.gears.rating.conical._552 import ConicalGearMeshRating
    from mastapy._private.gears.rating.conical._553 import ConicalGearRating
    from mastapy._private.gears.rating.conical._554 import ConicalGearSetDutyCycleRating
    from mastapy._private.gears.rating.conical._555 import ConicalGearSetRating
    from mastapy._private.gears.rating.conical._556 import ConicalGearSingleFlankRating
    from mastapy._private.gears.rating.conical._557 import ConicalMeshDutyCycleRating
    from mastapy._private.gears.rating.conical._558 import ConicalMeshedGearRating
    from mastapy._private.gears.rating.conical._559 import ConicalMeshSingleFlankRating
    from mastapy._private.gears.rating.conical._560 import ConicalRateableMesh
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.conical._551": ["ConicalGearDutyCycleRating"],
        "_private.gears.rating.conical._552": ["ConicalGearMeshRating"],
        "_private.gears.rating.conical._553": ["ConicalGearRating"],
        "_private.gears.rating.conical._554": ["ConicalGearSetDutyCycleRating"],
        "_private.gears.rating.conical._555": ["ConicalGearSetRating"],
        "_private.gears.rating.conical._556": ["ConicalGearSingleFlankRating"],
        "_private.gears.rating.conical._557": ["ConicalMeshDutyCycleRating"],
        "_private.gears.rating.conical._558": ["ConicalMeshedGearRating"],
        "_private.gears.rating.conical._559": ["ConicalMeshSingleFlankRating"],
        "_private.gears.rating.conical._560": ["ConicalRateableMesh"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConicalGearDutyCycleRating",
    "ConicalGearMeshRating",
    "ConicalGearRating",
    "ConicalGearSetDutyCycleRating",
    "ConicalGearSetRating",
    "ConicalGearSingleFlankRating",
    "ConicalMeshDutyCycleRating",
    "ConicalMeshedGearRating",
    "ConicalMeshSingleFlankRating",
    "ConicalRateableMesh",
)
