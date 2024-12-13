"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.cylindrical._464 import AGMAScuffingResultsRow
    from mastapy._private.gears.rating.cylindrical._465 import (
        CylindricalGearDesignAndRatingSettings,
    )
    from mastapy._private.gears.rating.cylindrical._466 import (
        CylindricalGearDesignAndRatingSettingsDatabase,
    )
    from mastapy._private.gears.rating.cylindrical._467 import (
        CylindricalGearDesignAndRatingSettingsItem,
    )
    from mastapy._private.gears.rating.cylindrical._468 import (
        CylindricalGearDutyCycleRating,
    )
    from mastapy._private.gears.rating.cylindrical._469 import (
        CylindricalGearFlankDutyCycleRating,
    )
    from mastapy._private.gears.rating.cylindrical._470 import (
        CylindricalGearFlankRating,
    )
    from mastapy._private.gears.rating.cylindrical._471 import CylindricalGearMeshRating
    from mastapy._private.gears.rating.cylindrical._472 import (
        CylindricalGearMicroPittingResults,
    )
    from mastapy._private.gears.rating.cylindrical._473 import CylindricalGearRating
    from mastapy._private.gears.rating.cylindrical._474 import (
        CylindricalGearRatingGeometryDataSource,
    )
    from mastapy._private.gears.rating.cylindrical._475 import (
        CylindricalGearScuffingResults,
    )
    from mastapy._private.gears.rating.cylindrical._476 import (
        CylindricalGearSetDutyCycleRating,
    )
    from mastapy._private.gears.rating.cylindrical._477 import CylindricalGearSetRating
    from mastapy._private.gears.rating.cylindrical._478 import (
        CylindricalGearSingleFlankRating,
    )
    from mastapy._private.gears.rating.cylindrical._479 import (
        CylindricalMeshDutyCycleRating,
    )
    from mastapy._private.gears.rating.cylindrical._480 import (
        CylindricalMeshSingleFlankRating,
    )
    from mastapy._private.gears.rating.cylindrical._481 import (
        CylindricalPlasticGearRatingSettings,
    )
    from mastapy._private.gears.rating.cylindrical._482 import (
        CylindricalPlasticGearRatingSettingsDatabase,
    )
    from mastapy._private.gears.rating.cylindrical._483 import (
        CylindricalPlasticGearRatingSettingsItem,
    )
    from mastapy._private.gears.rating.cylindrical._484 import CylindricalRateableMesh
    from mastapy._private.gears.rating.cylindrical._485 import DynamicFactorMethods
    from mastapy._private.gears.rating.cylindrical._486 import (
        GearBlankFactorCalculationOptions,
    )
    from mastapy._private.gears.rating.cylindrical._487 import ISOScuffingResultsRow
    from mastapy._private.gears.rating.cylindrical._488 import MeshRatingForReports
    from mastapy._private.gears.rating.cylindrical._489 import MicropittingRatingMethod
    from mastapy._private.gears.rating.cylindrical._490 import MicroPittingResultsRow
    from mastapy._private.gears.rating.cylindrical._491 import (
        MisalignmentContactPatternEnhancements,
    )
    from mastapy._private.gears.rating.cylindrical._492 import RatingMethod
    from mastapy._private.gears.rating.cylindrical._493 import (
        ReducedCylindricalGearSetDutyCycleRating,
    )
    from mastapy._private.gears.rating.cylindrical._494 import (
        ScuffingFlashTemperatureRatingMethod,
    )
    from mastapy._private.gears.rating.cylindrical._495 import (
        ScuffingIntegralTemperatureRatingMethod,
    )
    from mastapy._private.gears.rating.cylindrical._496 import ScuffingMethods
    from mastapy._private.gears.rating.cylindrical._497 import ScuffingResultsRow
    from mastapy._private.gears.rating.cylindrical._498 import ScuffingResultsRowGear
    from mastapy._private.gears.rating.cylindrical._499 import TipReliefScuffingOptions
    from mastapy._private.gears.rating.cylindrical._500 import ToothThicknesses
    from mastapy._private.gears.rating.cylindrical._501 import (
        VDI2737SafetyFactorReportingObject,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.cylindrical._464": ["AGMAScuffingResultsRow"],
        "_private.gears.rating.cylindrical._465": [
            "CylindricalGearDesignAndRatingSettings"
        ],
        "_private.gears.rating.cylindrical._466": [
            "CylindricalGearDesignAndRatingSettingsDatabase"
        ],
        "_private.gears.rating.cylindrical._467": [
            "CylindricalGearDesignAndRatingSettingsItem"
        ],
        "_private.gears.rating.cylindrical._468": ["CylindricalGearDutyCycleRating"],
        "_private.gears.rating.cylindrical._469": [
            "CylindricalGearFlankDutyCycleRating"
        ],
        "_private.gears.rating.cylindrical._470": ["CylindricalGearFlankRating"],
        "_private.gears.rating.cylindrical._471": ["CylindricalGearMeshRating"],
        "_private.gears.rating.cylindrical._472": [
            "CylindricalGearMicroPittingResults"
        ],
        "_private.gears.rating.cylindrical._473": ["CylindricalGearRating"],
        "_private.gears.rating.cylindrical._474": [
            "CylindricalGearRatingGeometryDataSource"
        ],
        "_private.gears.rating.cylindrical._475": ["CylindricalGearScuffingResults"],
        "_private.gears.rating.cylindrical._476": ["CylindricalGearSetDutyCycleRating"],
        "_private.gears.rating.cylindrical._477": ["CylindricalGearSetRating"],
        "_private.gears.rating.cylindrical._478": ["CylindricalGearSingleFlankRating"],
        "_private.gears.rating.cylindrical._479": ["CylindricalMeshDutyCycleRating"],
        "_private.gears.rating.cylindrical._480": ["CylindricalMeshSingleFlankRating"],
        "_private.gears.rating.cylindrical._481": [
            "CylindricalPlasticGearRatingSettings"
        ],
        "_private.gears.rating.cylindrical._482": [
            "CylindricalPlasticGearRatingSettingsDatabase"
        ],
        "_private.gears.rating.cylindrical._483": [
            "CylindricalPlasticGearRatingSettingsItem"
        ],
        "_private.gears.rating.cylindrical._484": ["CylindricalRateableMesh"],
        "_private.gears.rating.cylindrical._485": ["DynamicFactorMethods"],
        "_private.gears.rating.cylindrical._486": ["GearBlankFactorCalculationOptions"],
        "_private.gears.rating.cylindrical._487": ["ISOScuffingResultsRow"],
        "_private.gears.rating.cylindrical._488": ["MeshRatingForReports"],
        "_private.gears.rating.cylindrical._489": ["MicropittingRatingMethod"],
        "_private.gears.rating.cylindrical._490": ["MicroPittingResultsRow"],
        "_private.gears.rating.cylindrical._491": [
            "MisalignmentContactPatternEnhancements"
        ],
        "_private.gears.rating.cylindrical._492": ["RatingMethod"],
        "_private.gears.rating.cylindrical._493": [
            "ReducedCylindricalGearSetDutyCycleRating"
        ],
        "_private.gears.rating.cylindrical._494": [
            "ScuffingFlashTemperatureRatingMethod"
        ],
        "_private.gears.rating.cylindrical._495": [
            "ScuffingIntegralTemperatureRatingMethod"
        ],
        "_private.gears.rating.cylindrical._496": ["ScuffingMethods"],
        "_private.gears.rating.cylindrical._497": ["ScuffingResultsRow"],
        "_private.gears.rating.cylindrical._498": ["ScuffingResultsRowGear"],
        "_private.gears.rating.cylindrical._499": ["TipReliefScuffingOptions"],
        "_private.gears.rating.cylindrical._500": ["ToothThicknesses"],
        "_private.gears.rating.cylindrical._501": [
            "VDI2737SafetyFactorReportingObject"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AGMAScuffingResultsRow",
    "CylindricalGearDesignAndRatingSettings",
    "CylindricalGearDesignAndRatingSettingsDatabase",
    "CylindricalGearDesignAndRatingSettingsItem",
    "CylindricalGearDutyCycleRating",
    "CylindricalGearFlankDutyCycleRating",
    "CylindricalGearFlankRating",
    "CylindricalGearMeshRating",
    "CylindricalGearMicroPittingResults",
    "CylindricalGearRating",
    "CylindricalGearRatingGeometryDataSource",
    "CylindricalGearScuffingResults",
    "CylindricalGearSetDutyCycleRating",
    "CylindricalGearSetRating",
    "CylindricalGearSingleFlankRating",
    "CylindricalMeshDutyCycleRating",
    "CylindricalMeshSingleFlankRating",
    "CylindricalPlasticGearRatingSettings",
    "CylindricalPlasticGearRatingSettingsDatabase",
    "CylindricalPlasticGearRatingSettingsItem",
    "CylindricalRateableMesh",
    "DynamicFactorMethods",
    "GearBlankFactorCalculationOptions",
    "ISOScuffingResultsRow",
    "MeshRatingForReports",
    "MicropittingRatingMethod",
    "MicroPittingResultsRow",
    "MisalignmentContactPatternEnhancements",
    "RatingMethod",
    "ReducedCylindricalGearSetDutyCycleRating",
    "ScuffingFlashTemperatureRatingMethod",
    "ScuffingIntegralTemperatureRatingMethod",
    "ScuffingMethods",
    "ScuffingResultsRow",
    "ScuffingResultsRowGear",
    "TipReliefScuffingOptions",
    "ToothThicknesses",
    "VDI2737SafetyFactorReportingObject",
)
