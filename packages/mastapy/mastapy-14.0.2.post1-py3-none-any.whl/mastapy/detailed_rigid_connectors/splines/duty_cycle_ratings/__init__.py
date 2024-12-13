"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.detailed_rigid_connectors.splines.duty_cycle_ratings._1483 import (
        AGMA6123SplineJointDutyCycleRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.duty_cycle_ratings._1484 import (
        GBT17855SplineJointDutyCycleRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.duty_cycle_ratings._1485 import (
        SAESplineJointDutyCycleRating,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.detailed_rigid_connectors.splines.duty_cycle_ratings._1483": [
            "AGMA6123SplineJointDutyCycleRating"
        ],
        "_private.detailed_rigid_connectors.splines.duty_cycle_ratings._1484": [
            "GBT17855SplineJointDutyCycleRating"
        ],
        "_private.detailed_rigid_connectors.splines.duty_cycle_ratings._1485": [
            "SAESplineJointDutyCycleRating"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AGMA6123SplineJointDutyCycleRating",
    "GBT17855SplineJointDutyCycleRating",
    "SAESplineJointDutyCycleRating",
)
