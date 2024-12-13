"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears._326 import AccuracyGrades
    from mastapy._private.gears._327 import AGMAToleranceStandard
    from mastapy._private.gears._328 import BevelHypoidGearDesignSettings
    from mastapy._private.gears._329 import BevelHypoidGearRatingSettings
    from mastapy._private.gears._330 import CentreDistanceChangeMethod
    from mastapy._private.gears._331 import CoefficientOfFrictionCalculationMethod
    from mastapy._private.gears._332 import ConicalGearToothSurface
    from mastapy._private.gears._333 import ContactRatioDataSource
    from mastapy._private.gears._334 import ContactRatioRequirements
    from mastapy._private.gears._335 import CylindricalFlanks
    from mastapy._private.gears._336 import CylindricalMisalignmentDataSource
    from mastapy._private.gears._337 import DeflectionFromBendingOption
    from mastapy._private.gears._338 import GearFlanks
    from mastapy._private.gears._339 import GearNURBSSurface
    from mastapy._private.gears._340 import GearSetDesignGroup
    from mastapy._private.gears._341 import GearSetModes
    from mastapy._private.gears._342 import GearSetOptimisationResult
    from mastapy._private.gears._343 import GearSetOptimisationResults
    from mastapy._private.gears._344 import GearSetOptimiser
    from mastapy._private.gears._345 import Hand
    from mastapy._private.gears._346 import ISOToleranceStandard
    from mastapy._private.gears._347 import LubricationMethods
    from mastapy._private.gears._348 import MicroGeometryInputTypes
    from mastapy._private.gears._349 import MicroGeometryModel
    from mastapy._private.gears._350 import (
        MicropittingCoefficientOfFrictionCalculationMethod,
    )
    from mastapy._private.gears._351 import NamedPlanetAngle
    from mastapy._private.gears._352 import PlanetaryDetail
    from mastapy._private.gears._353 import PlanetaryRatingLoadSharingOption
    from mastapy._private.gears._354 import PocketingPowerLossCoefficients
    from mastapy._private.gears._355 import PocketingPowerLossCoefficientsDatabase
    from mastapy._private.gears._356 import QualityGradeTypes
    from mastapy._private.gears._357 import SafetyRequirementsAGMA
    from mastapy._private.gears._358 import (
        SpecificationForTheEffectOfOilKinematicViscosity,
    )
    from mastapy._private.gears._359 import SpiralBevelRootLineTilt
    from mastapy._private.gears._360 import SpiralBevelToothTaper
    from mastapy._private.gears._361 import TESpecificationType
    from mastapy._private.gears._362 import WormAddendumFactor
    from mastapy._private.gears._363 import WormType
    from mastapy._private.gears._364 import ZerolBevelGleasonToothTaperOption
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears._326": ["AccuracyGrades"],
        "_private.gears._327": ["AGMAToleranceStandard"],
        "_private.gears._328": ["BevelHypoidGearDesignSettings"],
        "_private.gears._329": ["BevelHypoidGearRatingSettings"],
        "_private.gears._330": ["CentreDistanceChangeMethod"],
        "_private.gears._331": ["CoefficientOfFrictionCalculationMethod"],
        "_private.gears._332": ["ConicalGearToothSurface"],
        "_private.gears._333": ["ContactRatioDataSource"],
        "_private.gears._334": ["ContactRatioRequirements"],
        "_private.gears._335": ["CylindricalFlanks"],
        "_private.gears._336": ["CylindricalMisalignmentDataSource"],
        "_private.gears._337": ["DeflectionFromBendingOption"],
        "_private.gears._338": ["GearFlanks"],
        "_private.gears._339": ["GearNURBSSurface"],
        "_private.gears._340": ["GearSetDesignGroup"],
        "_private.gears._341": ["GearSetModes"],
        "_private.gears._342": ["GearSetOptimisationResult"],
        "_private.gears._343": ["GearSetOptimisationResults"],
        "_private.gears._344": ["GearSetOptimiser"],
        "_private.gears._345": ["Hand"],
        "_private.gears._346": ["ISOToleranceStandard"],
        "_private.gears._347": ["LubricationMethods"],
        "_private.gears._348": ["MicroGeometryInputTypes"],
        "_private.gears._349": ["MicroGeometryModel"],
        "_private.gears._350": ["MicropittingCoefficientOfFrictionCalculationMethod"],
        "_private.gears._351": ["NamedPlanetAngle"],
        "_private.gears._352": ["PlanetaryDetail"],
        "_private.gears._353": ["PlanetaryRatingLoadSharingOption"],
        "_private.gears._354": ["PocketingPowerLossCoefficients"],
        "_private.gears._355": ["PocketingPowerLossCoefficientsDatabase"],
        "_private.gears._356": ["QualityGradeTypes"],
        "_private.gears._357": ["SafetyRequirementsAGMA"],
        "_private.gears._358": ["SpecificationForTheEffectOfOilKinematicViscosity"],
        "_private.gears._359": ["SpiralBevelRootLineTilt"],
        "_private.gears._360": ["SpiralBevelToothTaper"],
        "_private.gears._361": ["TESpecificationType"],
        "_private.gears._362": ["WormAddendumFactor"],
        "_private.gears._363": ["WormType"],
        "_private.gears._364": ["ZerolBevelGleasonToothTaperOption"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AccuracyGrades",
    "AGMAToleranceStandard",
    "BevelHypoidGearDesignSettings",
    "BevelHypoidGearRatingSettings",
    "CentreDistanceChangeMethod",
    "CoefficientOfFrictionCalculationMethod",
    "ConicalGearToothSurface",
    "ContactRatioDataSource",
    "ContactRatioRequirements",
    "CylindricalFlanks",
    "CylindricalMisalignmentDataSource",
    "DeflectionFromBendingOption",
    "GearFlanks",
    "GearNURBSSurface",
    "GearSetDesignGroup",
    "GearSetModes",
    "GearSetOptimisationResult",
    "GearSetOptimisationResults",
    "GearSetOptimiser",
    "Hand",
    "ISOToleranceStandard",
    "LubricationMethods",
    "MicroGeometryInputTypes",
    "MicroGeometryModel",
    "MicropittingCoefficientOfFrictionCalculationMethod",
    "NamedPlanetAngle",
    "PlanetaryDetail",
    "PlanetaryRatingLoadSharingOption",
    "PocketingPowerLossCoefficients",
    "PocketingPowerLossCoefficientsDatabase",
    "QualityGradeTypes",
    "SafetyRequirementsAGMA",
    "SpecificationForTheEffectOfOilKinematicViscosity",
    "SpiralBevelRootLineTilt",
    "SpiralBevelToothTaper",
    "TESpecificationType",
    "WormAddendumFactor",
    "WormType",
    "ZerolBevelGleasonToothTaperOption",
)
