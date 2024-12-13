"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving._667 import (
        CalculationError,
    )
    from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving._668 import (
        ChartType,
    )
    from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving._669 import (
        GearPointCalculationError,
    )
    from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving._670 import (
        MicroGeometryDefinitionMethod,
    )
    from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving._671 import (
        MicroGeometryDefinitionType,
    )
    from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving._672 import (
        PlungeShaverCalculation,
    )
    from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving._673 import (
        PlungeShaverCalculationInputs,
    )
    from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving._674 import (
        PlungeShaverGeneration,
    )
    from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving._675 import (
        PlungeShaverInputsAndMicroGeometry,
    )
    from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving._676 import (
        PlungeShaverOutputs,
    )
    from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving._677 import (
        PlungeShaverSettings,
    )
    from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving._678 import (
        PointOfInterest,
    )
    from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving._679 import (
        RealPlungeShaverOutputs,
    )
    from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving._680 import (
        ShaverPointCalculationError,
    )
    from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving._681 import (
        ShaverPointOfInterest,
    )
    from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving._682 import (
        VirtualPlungeShaverOutputs,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.manufacturing.cylindrical.plunge_shaving._667": [
            "CalculationError"
        ],
        "_private.gears.manufacturing.cylindrical.plunge_shaving._668": ["ChartType"],
        "_private.gears.manufacturing.cylindrical.plunge_shaving._669": [
            "GearPointCalculationError"
        ],
        "_private.gears.manufacturing.cylindrical.plunge_shaving._670": [
            "MicroGeometryDefinitionMethod"
        ],
        "_private.gears.manufacturing.cylindrical.plunge_shaving._671": [
            "MicroGeometryDefinitionType"
        ],
        "_private.gears.manufacturing.cylindrical.plunge_shaving._672": [
            "PlungeShaverCalculation"
        ],
        "_private.gears.manufacturing.cylindrical.plunge_shaving._673": [
            "PlungeShaverCalculationInputs"
        ],
        "_private.gears.manufacturing.cylindrical.plunge_shaving._674": [
            "PlungeShaverGeneration"
        ],
        "_private.gears.manufacturing.cylindrical.plunge_shaving._675": [
            "PlungeShaverInputsAndMicroGeometry"
        ],
        "_private.gears.manufacturing.cylindrical.plunge_shaving._676": [
            "PlungeShaverOutputs"
        ],
        "_private.gears.manufacturing.cylindrical.plunge_shaving._677": [
            "PlungeShaverSettings"
        ],
        "_private.gears.manufacturing.cylindrical.plunge_shaving._678": [
            "PointOfInterest"
        ],
        "_private.gears.manufacturing.cylindrical.plunge_shaving._679": [
            "RealPlungeShaverOutputs"
        ],
        "_private.gears.manufacturing.cylindrical.plunge_shaving._680": [
            "ShaverPointCalculationError"
        ],
        "_private.gears.manufacturing.cylindrical.plunge_shaving._681": [
            "ShaverPointOfInterest"
        ],
        "_private.gears.manufacturing.cylindrical.plunge_shaving._682": [
            "VirtualPlungeShaverOutputs"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CalculationError",
    "ChartType",
    "GearPointCalculationError",
    "MicroGeometryDefinitionMethod",
    "MicroGeometryDefinitionType",
    "PlungeShaverCalculation",
    "PlungeShaverCalculationInputs",
    "PlungeShaverGeneration",
    "PlungeShaverInputsAndMicroGeometry",
    "PlungeShaverOutputs",
    "PlungeShaverSettings",
    "PointOfInterest",
    "RealPlungeShaverOutputs",
    "ShaverPointCalculationError",
    "ShaverPointOfInterest",
    "VirtualPlungeShaverOutputs",
)
