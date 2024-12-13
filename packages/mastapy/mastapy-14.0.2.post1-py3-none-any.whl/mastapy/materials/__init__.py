"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.materials._249 import (
        AbstractStressCyclesDataForAnSNCurveOfAPlasticMaterial,
    )
    from mastapy._private.materials._250 import AcousticRadiationEfficiency
    from mastapy._private.materials._251 import AcousticRadiationEfficiencyInputType
    from mastapy._private.materials._252 import AGMALubricantType
    from mastapy._private.materials._253 import AGMAMaterialApplications
    from mastapy._private.materials._254 import AGMAMaterialClasses
    from mastapy._private.materials._255 import AGMAMaterialGrade
    from mastapy._private.materials._256 import AirProperties
    from mastapy._private.materials._257 import BearingLubricationCondition
    from mastapy._private.materials._258 import BearingMaterial
    from mastapy._private.materials._259 import BearingMaterialDatabase
    from mastapy._private.materials._260 import BHCurveExtrapolationMethod
    from mastapy._private.materials._261 import BHCurveSpecification
    from mastapy._private.materials._262 import ComponentMaterialDatabase
    from mastapy._private.materials._263 import CompositeFatigueSafetyFactorItem
    from mastapy._private.materials._264 import CylindricalGearRatingMethods
    from mastapy._private.materials._265 import DensitySpecificationMethod
    from mastapy._private.materials._266 import FatigueSafetyFactorItem
    from mastapy._private.materials._267 import FatigueSafetyFactorItemBase
    from mastapy._private.materials._268 import GearingTypes
    from mastapy._private.materials._269 import GeneralTransmissionProperties
    from mastapy._private.materials._270 import GreaseContaminationOptions
    from mastapy._private.materials._271 import HardnessType
    from mastapy._private.materials._272 import ISO76StaticSafetyFactorLimits
    from mastapy._private.materials._273 import ISOLubricantType
    from mastapy._private.materials._274 import LubricantDefinition
    from mastapy._private.materials._275 import LubricantDelivery
    from mastapy._private.materials._276 import LubricantViscosityClassAGMA
    from mastapy._private.materials._277 import LubricantViscosityClassification
    from mastapy._private.materials._278 import LubricantViscosityClassISO
    from mastapy._private.materials._279 import LubricantViscosityClassSAE
    from mastapy._private.materials._280 import LubricationDetail
    from mastapy._private.materials._281 import LubricationDetailDatabase
    from mastapy._private.materials._282 import Material
    from mastapy._private.materials._283 import MaterialDatabase
    from mastapy._private.materials._284 import MaterialsSettings
    from mastapy._private.materials._285 import MaterialsSettingsDatabase
    from mastapy._private.materials._286 import MaterialsSettingsItem
    from mastapy._private.materials._287 import MaterialStandards
    from mastapy._private.materials._288 import MetalPlasticType
    from mastapy._private.materials._289 import OilFiltrationOptions
    from mastapy._private.materials._290 import PressureViscosityCoefficientMethod
    from mastapy._private.materials._291 import QualityGrade
    from mastapy._private.materials._292 import SafetyFactorGroup
    from mastapy._private.materials._293 import SafetyFactorItem
    from mastapy._private.materials._294 import SNCurve
    from mastapy._private.materials._295 import SNCurvePoint
    from mastapy._private.materials._296 import SoundPressureEnclosure
    from mastapy._private.materials._297 import SoundPressureEnclosureType
    from mastapy._private.materials._298 import (
        StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial,
    )
    from mastapy._private.materials._299 import (
        StressCyclesDataForTheContactSNCurveOfAPlasticMaterial,
    )
    from mastapy._private.materials._300 import TransmissionApplications
    from mastapy._private.materials._301 import VDI2736LubricantType
    from mastapy._private.materials._302 import VehicleDynamicsProperties
    from mastapy._private.materials._303 import WindTurbineStandards
    from mastapy._private.materials._304 import WorkingCharacteristics
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.materials._249": [
            "AbstractStressCyclesDataForAnSNCurveOfAPlasticMaterial"
        ],
        "_private.materials._250": ["AcousticRadiationEfficiency"],
        "_private.materials._251": ["AcousticRadiationEfficiencyInputType"],
        "_private.materials._252": ["AGMALubricantType"],
        "_private.materials._253": ["AGMAMaterialApplications"],
        "_private.materials._254": ["AGMAMaterialClasses"],
        "_private.materials._255": ["AGMAMaterialGrade"],
        "_private.materials._256": ["AirProperties"],
        "_private.materials._257": ["BearingLubricationCondition"],
        "_private.materials._258": ["BearingMaterial"],
        "_private.materials._259": ["BearingMaterialDatabase"],
        "_private.materials._260": ["BHCurveExtrapolationMethod"],
        "_private.materials._261": ["BHCurveSpecification"],
        "_private.materials._262": ["ComponentMaterialDatabase"],
        "_private.materials._263": ["CompositeFatigueSafetyFactorItem"],
        "_private.materials._264": ["CylindricalGearRatingMethods"],
        "_private.materials._265": ["DensitySpecificationMethod"],
        "_private.materials._266": ["FatigueSafetyFactorItem"],
        "_private.materials._267": ["FatigueSafetyFactorItemBase"],
        "_private.materials._268": ["GearingTypes"],
        "_private.materials._269": ["GeneralTransmissionProperties"],
        "_private.materials._270": ["GreaseContaminationOptions"],
        "_private.materials._271": ["HardnessType"],
        "_private.materials._272": ["ISO76StaticSafetyFactorLimits"],
        "_private.materials._273": ["ISOLubricantType"],
        "_private.materials._274": ["LubricantDefinition"],
        "_private.materials._275": ["LubricantDelivery"],
        "_private.materials._276": ["LubricantViscosityClassAGMA"],
        "_private.materials._277": ["LubricantViscosityClassification"],
        "_private.materials._278": ["LubricantViscosityClassISO"],
        "_private.materials._279": ["LubricantViscosityClassSAE"],
        "_private.materials._280": ["LubricationDetail"],
        "_private.materials._281": ["LubricationDetailDatabase"],
        "_private.materials._282": ["Material"],
        "_private.materials._283": ["MaterialDatabase"],
        "_private.materials._284": ["MaterialsSettings"],
        "_private.materials._285": ["MaterialsSettingsDatabase"],
        "_private.materials._286": ["MaterialsSettingsItem"],
        "_private.materials._287": ["MaterialStandards"],
        "_private.materials._288": ["MetalPlasticType"],
        "_private.materials._289": ["OilFiltrationOptions"],
        "_private.materials._290": ["PressureViscosityCoefficientMethod"],
        "_private.materials._291": ["QualityGrade"],
        "_private.materials._292": ["SafetyFactorGroup"],
        "_private.materials._293": ["SafetyFactorItem"],
        "_private.materials._294": ["SNCurve"],
        "_private.materials._295": ["SNCurvePoint"],
        "_private.materials._296": ["SoundPressureEnclosure"],
        "_private.materials._297": ["SoundPressureEnclosureType"],
        "_private.materials._298": [
            "StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial"
        ],
        "_private.materials._299": [
            "StressCyclesDataForTheContactSNCurveOfAPlasticMaterial"
        ],
        "_private.materials._300": ["TransmissionApplications"],
        "_private.materials._301": ["VDI2736LubricantType"],
        "_private.materials._302": ["VehicleDynamicsProperties"],
        "_private.materials._303": ["WindTurbineStandards"],
        "_private.materials._304": ["WorkingCharacteristics"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractStressCyclesDataForAnSNCurveOfAPlasticMaterial",
    "AcousticRadiationEfficiency",
    "AcousticRadiationEfficiencyInputType",
    "AGMALubricantType",
    "AGMAMaterialApplications",
    "AGMAMaterialClasses",
    "AGMAMaterialGrade",
    "AirProperties",
    "BearingLubricationCondition",
    "BearingMaterial",
    "BearingMaterialDatabase",
    "BHCurveExtrapolationMethod",
    "BHCurveSpecification",
    "ComponentMaterialDatabase",
    "CompositeFatigueSafetyFactorItem",
    "CylindricalGearRatingMethods",
    "DensitySpecificationMethod",
    "FatigueSafetyFactorItem",
    "FatigueSafetyFactorItemBase",
    "GearingTypes",
    "GeneralTransmissionProperties",
    "GreaseContaminationOptions",
    "HardnessType",
    "ISO76StaticSafetyFactorLimits",
    "ISOLubricantType",
    "LubricantDefinition",
    "LubricantDelivery",
    "LubricantViscosityClassAGMA",
    "LubricantViscosityClassification",
    "LubricantViscosityClassISO",
    "LubricantViscosityClassSAE",
    "LubricationDetail",
    "LubricationDetailDatabase",
    "Material",
    "MaterialDatabase",
    "MaterialsSettings",
    "MaterialsSettingsDatabase",
    "MaterialsSettingsItem",
    "MaterialStandards",
    "MetalPlasticType",
    "OilFiltrationOptions",
    "PressureViscosityCoefficientMethod",
    "QualityGrade",
    "SafetyFactorGroup",
    "SafetyFactorItem",
    "SNCurve",
    "SNCurvePoint",
    "SoundPressureEnclosure",
    "SoundPressureEnclosureType",
    "StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial",
    "StressCyclesDataForTheContactSNCurveOfAPlasticMaterial",
    "TransmissionApplications",
    "VDI2736LubricantType",
    "VehicleDynamicsProperties",
    "WindTurbineStandards",
    "WorkingCharacteristics",
)
