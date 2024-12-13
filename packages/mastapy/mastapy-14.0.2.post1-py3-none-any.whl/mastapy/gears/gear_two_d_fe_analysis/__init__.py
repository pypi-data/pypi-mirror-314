"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_two_d_fe_analysis._919 import (
        CylindricalGearMeshTIFFAnalysis,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._920 import (
        CylindricalGearMeshTIFFAnalysisDutyCycle,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._921 import (
        CylindricalGearSetTIFFAnalysis,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._922 import (
        CylindricalGearSetTIFFAnalysisDutyCycle,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._923 import (
        CylindricalGearTIFFAnalysis,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._924 import (
        CylindricalGearTIFFAnalysisDutyCycle,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._925 import (
        CylindricalGearTwoDimensionalFEAnalysis,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._926 import (
        FindleyCriticalPlaneAnalysis,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_two_d_fe_analysis._919": [
            "CylindricalGearMeshTIFFAnalysis"
        ],
        "_private.gears.gear_two_d_fe_analysis._920": [
            "CylindricalGearMeshTIFFAnalysisDutyCycle"
        ],
        "_private.gears.gear_two_d_fe_analysis._921": [
            "CylindricalGearSetTIFFAnalysis"
        ],
        "_private.gears.gear_two_d_fe_analysis._922": [
            "CylindricalGearSetTIFFAnalysisDutyCycle"
        ],
        "_private.gears.gear_two_d_fe_analysis._923": ["CylindricalGearTIFFAnalysis"],
        "_private.gears.gear_two_d_fe_analysis._924": [
            "CylindricalGearTIFFAnalysisDutyCycle"
        ],
        "_private.gears.gear_two_d_fe_analysis._925": [
            "CylindricalGearTwoDimensionalFEAnalysis"
        ],
        "_private.gears.gear_two_d_fe_analysis._926": ["FindleyCriticalPlaneAnalysis"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CylindricalGearMeshTIFFAnalysis",
    "CylindricalGearMeshTIFFAnalysisDutyCycle",
    "CylindricalGearSetTIFFAnalysis",
    "CylindricalGearSetTIFFAnalysisDutyCycle",
    "CylindricalGearTIFFAnalysis",
    "CylindricalGearTIFFAnalysisDutyCycle",
    "CylindricalGearTwoDimensionalFEAnalysis",
    "FindleyCriticalPlaneAnalysis",
)
