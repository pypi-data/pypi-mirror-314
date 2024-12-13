"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.bevel._1219 import (
        AGMAGleasonConicalGearGeometryMethods,
    )
    from mastapy._private.gears.gear_designs.bevel._1220 import BevelGearDesign
    from mastapy._private.gears.gear_designs.bevel._1221 import BevelGearMeshDesign
    from mastapy._private.gears.gear_designs.bevel._1222 import BevelGearSetDesign
    from mastapy._private.gears.gear_designs.bevel._1223 import BevelMeshedGearDesign
    from mastapy._private.gears.gear_designs.bevel._1224 import (
        DrivenMachineCharacteristicGleason,
    )
    from mastapy._private.gears.gear_designs.bevel._1225 import EdgeRadiusType
    from mastapy._private.gears.gear_designs.bevel._1226 import FinishingMethods
    from mastapy._private.gears.gear_designs.bevel._1227 import (
        MachineCharacteristicAGMAKlingelnberg,
    )
    from mastapy._private.gears.gear_designs.bevel._1228 import (
        PrimeMoverCharacteristicGleason,
    )
    from mastapy._private.gears.gear_designs.bevel._1229 import (
        ToothProportionsInputMethod,
    )
    from mastapy._private.gears.gear_designs.bevel._1230 import (
        ToothThicknessSpecificationMethod,
    )
    from mastapy._private.gears.gear_designs.bevel._1231 import (
        WheelFinishCutterPointWidthRestrictionMethod,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.bevel._1219": [
            "AGMAGleasonConicalGearGeometryMethods"
        ],
        "_private.gears.gear_designs.bevel._1220": ["BevelGearDesign"],
        "_private.gears.gear_designs.bevel._1221": ["BevelGearMeshDesign"],
        "_private.gears.gear_designs.bevel._1222": ["BevelGearSetDesign"],
        "_private.gears.gear_designs.bevel._1223": ["BevelMeshedGearDesign"],
        "_private.gears.gear_designs.bevel._1224": [
            "DrivenMachineCharacteristicGleason"
        ],
        "_private.gears.gear_designs.bevel._1225": ["EdgeRadiusType"],
        "_private.gears.gear_designs.bevel._1226": ["FinishingMethods"],
        "_private.gears.gear_designs.bevel._1227": [
            "MachineCharacteristicAGMAKlingelnberg"
        ],
        "_private.gears.gear_designs.bevel._1228": ["PrimeMoverCharacteristicGleason"],
        "_private.gears.gear_designs.bevel._1229": ["ToothProportionsInputMethod"],
        "_private.gears.gear_designs.bevel._1230": [
            "ToothThicknessSpecificationMethod"
        ],
        "_private.gears.gear_designs.bevel._1231": [
            "WheelFinishCutterPointWidthRestrictionMethod"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AGMAGleasonConicalGearGeometryMethods",
    "BevelGearDesign",
    "BevelGearMeshDesign",
    "BevelGearSetDesign",
    "BevelMeshedGearDesign",
    "DrivenMachineCharacteristicGleason",
    "EdgeRadiusType",
    "FinishingMethods",
    "MachineCharacteristicAGMAKlingelnberg",
    "PrimeMoverCharacteristicGleason",
    "ToothProportionsInputMethod",
    "ToothThicknessSpecificationMethod",
    "WheelFinishCutterPointWidthRestrictionMethod",
)
