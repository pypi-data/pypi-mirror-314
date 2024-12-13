"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.materials._596 import AGMACylindricalGearMaterial
    from mastapy._private.gears.materials._597 import (
        BenedictAndKelleyCoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._598 import BevelGearAbstractMaterialDatabase
    from mastapy._private.gears.materials._599 import BevelGearISOMaterial
    from mastapy._private.gears.materials._600 import BevelGearISOMaterialDatabase
    from mastapy._private.gears.materials._601 import BevelGearMaterial
    from mastapy._private.gears.materials._602 import BevelGearMaterialDatabase
    from mastapy._private.gears.materials._603 import CoefficientOfFrictionCalculator
    from mastapy._private.gears.materials._604 import (
        CylindricalGearAGMAMaterialDatabase,
    )
    from mastapy._private.gears.materials._605 import CylindricalGearISOMaterialDatabase
    from mastapy._private.gears.materials._606 import CylindricalGearMaterial
    from mastapy._private.gears.materials._607 import CylindricalGearMaterialDatabase
    from mastapy._private.gears.materials._608 import (
        CylindricalGearPlasticMaterialDatabase,
    )
    from mastapy._private.gears.materials._609 import (
        DrozdovAndGavrikovCoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._610 import GearMaterial
    from mastapy._private.gears.materials._611 import GearMaterialDatabase
    from mastapy._private.gears.materials._612 import (
        GearMaterialExpertSystemFactorSettings,
    )
    from mastapy._private.gears.materials._613 import (
        InstantaneousCoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._614 import (
        ISO14179Part1CoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._615 import (
        ISO14179Part2CoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._616 import (
        ISO14179Part2CoefficientOfFrictionCalculatorBase,
    )
    from mastapy._private.gears.materials._617 import (
        ISO14179Part2CoefficientOfFrictionCalculatorWithMartinsModification,
    )
    from mastapy._private.gears.materials._618 import ISOCylindricalGearMaterial
    from mastapy._private.gears.materials._619 import (
        ISOTC60CoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._620 import (
        ISOTR1417912001CoefficientOfFrictionConstants,
    )
    from mastapy._private.gears.materials._621 import (
        ISOTR1417912001CoefficientOfFrictionConstantsDatabase,
    )
    from mastapy._private.gears.materials._622 import (
        KlingelnbergConicalGearMaterialDatabase,
    )
    from mastapy._private.gears.materials._623 import (
        KlingelnbergCycloPalloidConicalGearMaterial,
    )
    from mastapy._private.gears.materials._624 import ManufactureRating
    from mastapy._private.gears.materials._625 import (
        MisharinCoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._626 import (
        ODonoghueAndCameronCoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._627 import PlasticCylindricalGearMaterial
    from mastapy._private.gears.materials._628 import PlasticSNCurve
    from mastapy._private.gears.materials._629 import RatingMethods
    from mastapy._private.gears.materials._630 import RawMaterial
    from mastapy._private.gears.materials._631 import RawMaterialDatabase
    from mastapy._private.gears.materials._632 import (
        ScriptCoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._633 import SNCurveDefinition
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.materials._596": ["AGMACylindricalGearMaterial"],
        "_private.gears.materials._597": [
            "BenedictAndKelleyCoefficientOfFrictionCalculator"
        ],
        "_private.gears.materials._598": ["BevelGearAbstractMaterialDatabase"],
        "_private.gears.materials._599": ["BevelGearISOMaterial"],
        "_private.gears.materials._600": ["BevelGearISOMaterialDatabase"],
        "_private.gears.materials._601": ["BevelGearMaterial"],
        "_private.gears.materials._602": ["BevelGearMaterialDatabase"],
        "_private.gears.materials._603": ["CoefficientOfFrictionCalculator"],
        "_private.gears.materials._604": ["CylindricalGearAGMAMaterialDatabase"],
        "_private.gears.materials._605": ["CylindricalGearISOMaterialDatabase"],
        "_private.gears.materials._606": ["CylindricalGearMaterial"],
        "_private.gears.materials._607": ["CylindricalGearMaterialDatabase"],
        "_private.gears.materials._608": ["CylindricalGearPlasticMaterialDatabase"],
        "_private.gears.materials._609": [
            "DrozdovAndGavrikovCoefficientOfFrictionCalculator"
        ],
        "_private.gears.materials._610": ["GearMaterial"],
        "_private.gears.materials._611": ["GearMaterialDatabase"],
        "_private.gears.materials._612": ["GearMaterialExpertSystemFactorSettings"],
        "_private.gears.materials._613": [
            "InstantaneousCoefficientOfFrictionCalculator"
        ],
        "_private.gears.materials._614": [
            "ISO14179Part1CoefficientOfFrictionCalculator"
        ],
        "_private.gears.materials._615": [
            "ISO14179Part2CoefficientOfFrictionCalculator"
        ],
        "_private.gears.materials._616": [
            "ISO14179Part2CoefficientOfFrictionCalculatorBase"
        ],
        "_private.gears.materials._617": [
            "ISO14179Part2CoefficientOfFrictionCalculatorWithMartinsModification"
        ],
        "_private.gears.materials._618": ["ISOCylindricalGearMaterial"],
        "_private.gears.materials._619": ["ISOTC60CoefficientOfFrictionCalculator"],
        "_private.gears.materials._620": [
            "ISOTR1417912001CoefficientOfFrictionConstants"
        ],
        "_private.gears.materials._621": [
            "ISOTR1417912001CoefficientOfFrictionConstantsDatabase"
        ],
        "_private.gears.materials._622": ["KlingelnbergConicalGearMaterialDatabase"],
        "_private.gears.materials._623": [
            "KlingelnbergCycloPalloidConicalGearMaterial"
        ],
        "_private.gears.materials._624": ["ManufactureRating"],
        "_private.gears.materials._625": ["MisharinCoefficientOfFrictionCalculator"],
        "_private.gears.materials._626": [
            "ODonoghueAndCameronCoefficientOfFrictionCalculator"
        ],
        "_private.gears.materials._627": ["PlasticCylindricalGearMaterial"],
        "_private.gears.materials._628": ["PlasticSNCurve"],
        "_private.gears.materials._629": ["RatingMethods"],
        "_private.gears.materials._630": ["RawMaterial"],
        "_private.gears.materials._631": ["RawMaterialDatabase"],
        "_private.gears.materials._632": ["ScriptCoefficientOfFrictionCalculator"],
        "_private.gears.materials._633": ["SNCurveDefinition"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AGMACylindricalGearMaterial",
    "BenedictAndKelleyCoefficientOfFrictionCalculator",
    "BevelGearAbstractMaterialDatabase",
    "BevelGearISOMaterial",
    "BevelGearISOMaterialDatabase",
    "BevelGearMaterial",
    "BevelGearMaterialDatabase",
    "CoefficientOfFrictionCalculator",
    "CylindricalGearAGMAMaterialDatabase",
    "CylindricalGearISOMaterialDatabase",
    "CylindricalGearMaterial",
    "CylindricalGearMaterialDatabase",
    "CylindricalGearPlasticMaterialDatabase",
    "DrozdovAndGavrikovCoefficientOfFrictionCalculator",
    "GearMaterial",
    "GearMaterialDatabase",
    "GearMaterialExpertSystemFactorSettings",
    "InstantaneousCoefficientOfFrictionCalculator",
    "ISO14179Part1CoefficientOfFrictionCalculator",
    "ISO14179Part2CoefficientOfFrictionCalculator",
    "ISO14179Part2CoefficientOfFrictionCalculatorBase",
    "ISO14179Part2CoefficientOfFrictionCalculatorWithMartinsModification",
    "ISOCylindricalGearMaterial",
    "ISOTC60CoefficientOfFrictionCalculator",
    "ISOTR1417912001CoefficientOfFrictionConstants",
    "ISOTR1417912001CoefficientOfFrictionConstantsDatabase",
    "KlingelnbergConicalGearMaterialDatabase",
    "KlingelnbergCycloPalloidConicalGearMaterial",
    "ManufactureRating",
    "MisharinCoefficientOfFrictionCalculator",
    "ODonoghueAndCameronCoefficientOfFrictionCalculator",
    "PlasticCylindricalGearMaterial",
    "PlasticSNCurve",
    "RatingMethods",
    "RawMaterial",
    "RawMaterialDatabase",
    "ScriptCoefficientOfFrictionCalculator",
    "SNCurveDefinition",
)
