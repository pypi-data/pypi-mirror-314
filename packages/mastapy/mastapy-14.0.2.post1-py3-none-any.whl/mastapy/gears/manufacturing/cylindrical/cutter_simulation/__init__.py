"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._756 import (
        CutterSimulationCalc,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._757 import (
        CylindricalCutterSimulatableGear,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._758 import (
        CylindricalGearSpecification,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._759 import (
        CylindricalManufacturedRealGearInMesh,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._760 import (
        CylindricalManufacturedVirtualGearInMesh,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._761 import (
        FinishCutterSimulation,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._762 import (
        FinishStockPoint,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._763 import (
        FormWheelGrindingSimulationCalculator,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._764 import (
        GearCutterSimulation,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._765 import (
        HobSimulationCalculator,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._766 import (
        ManufacturingOperationConstraints,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._767 import (
        ManufacturingProcessControls,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._768 import (
        RackSimulationCalculator,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._769 import (
        RoughCutterSimulation,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._770 import (
        ShaperSimulationCalculator,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._771 import (
        ShavingSimulationCalculator,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._772 import (
        VirtualSimulationCalculator,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._773 import (
        WormGrinderSimulationCalculator,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.manufacturing.cylindrical.cutter_simulation._756": [
            "CutterSimulationCalc"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._757": [
            "CylindricalCutterSimulatableGear"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._758": [
            "CylindricalGearSpecification"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._759": [
            "CylindricalManufacturedRealGearInMesh"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._760": [
            "CylindricalManufacturedVirtualGearInMesh"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._761": [
            "FinishCutterSimulation"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._762": [
            "FinishStockPoint"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._763": [
            "FormWheelGrindingSimulationCalculator"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._764": [
            "GearCutterSimulation"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._765": [
            "HobSimulationCalculator"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._766": [
            "ManufacturingOperationConstraints"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._767": [
            "ManufacturingProcessControls"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._768": [
            "RackSimulationCalculator"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._769": [
            "RoughCutterSimulation"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._770": [
            "ShaperSimulationCalculator"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._771": [
            "ShavingSimulationCalculator"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._772": [
            "VirtualSimulationCalculator"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._773": [
            "WormGrinderSimulationCalculator"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CutterSimulationCalc",
    "CylindricalCutterSimulatableGear",
    "CylindricalGearSpecification",
    "CylindricalManufacturedRealGearInMesh",
    "CylindricalManufacturedVirtualGearInMesh",
    "FinishCutterSimulation",
    "FinishStockPoint",
    "FormWheelGrindingSimulationCalculator",
    "GearCutterSimulation",
    "HobSimulationCalculator",
    "ManufacturingOperationConstraints",
    "ManufacturingProcessControls",
    "RackSimulationCalculator",
    "RoughCutterSimulation",
    "ShaperSimulationCalculator",
    "ShavingSimulationCalculator",
    "VirtualSimulationCalculator",
    "WormGrinderSimulationCalculator",
)
