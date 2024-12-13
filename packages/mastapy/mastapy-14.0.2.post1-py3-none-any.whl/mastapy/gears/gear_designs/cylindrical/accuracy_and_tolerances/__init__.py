"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1171 import (
        AGMA2000A88AccuracyGrader,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1172 import (
        AGMA20151A01AccuracyGrader,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1173 import (
        AGMA20151AccuracyGrades,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1174 import (
        AGMAISO13281B14AccuracyGrader,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1175 import (
        Customer102AGMA2000AccuracyGrader,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1176 import (
        CylindricalAccuracyGrader,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1177 import (
        CylindricalAccuracyGraderWithProfileFormAndSlope,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1178 import (
        CylindricalAccuracyGrades,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1179 import (
        CylindricalGearAccuracyTolerances,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1180 import (
        DIN3967SystemOfGearFits,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1181 import (
        ISO132811995AccuracyGrader,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1182 import (
        ISO132812013AccuracyGrader,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1183 import (
        ISO1328AccuracyGraderCommon,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1184 import (
        ISO1328AccuracyGrades,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1185 import (
        OverridableTolerance,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1171": [
            "AGMA2000A88AccuracyGrader"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1172": [
            "AGMA20151A01AccuracyGrader"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1173": [
            "AGMA20151AccuracyGrades"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1174": [
            "AGMAISO13281B14AccuracyGrader"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1175": [
            "Customer102AGMA2000AccuracyGrader"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1176": [
            "CylindricalAccuracyGrader"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1177": [
            "CylindricalAccuracyGraderWithProfileFormAndSlope"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1178": [
            "CylindricalAccuracyGrades"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1179": [
            "CylindricalGearAccuracyTolerances"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1180": [
            "DIN3967SystemOfGearFits"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1181": [
            "ISO132811995AccuracyGrader"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1182": [
            "ISO132812013AccuracyGrader"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1183": [
            "ISO1328AccuracyGraderCommon"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1184": [
            "ISO1328AccuracyGrades"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1185": [
            "OverridableTolerance"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AGMA2000A88AccuracyGrader",
    "AGMA20151A01AccuracyGrader",
    "AGMA20151AccuracyGrades",
    "AGMAISO13281B14AccuracyGrader",
    "Customer102AGMA2000AccuracyGrader",
    "CylindricalAccuracyGrader",
    "CylindricalAccuracyGraderWithProfileFormAndSlope",
    "CylindricalAccuracyGrades",
    "CylindricalGearAccuracyTolerances",
    "DIN3967SystemOfGearFits",
    "ISO132811995AccuracyGrader",
    "ISO132812013AccuracyGrader",
    "ISO1328AccuracyGraderCommon",
    "ISO1328AccuracyGrades",
    "OverridableTolerance",
)
