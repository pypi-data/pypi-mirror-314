"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.manufacturing.bevel._797 import AbstractTCA
    from mastapy._private.gears.manufacturing.bevel._798 import (
        BevelMachineSettingOptimizationResult,
    )
    from mastapy._private.gears.manufacturing.bevel._799 import (
        ConicalFlankDeviationsData,
    )
    from mastapy._private.gears.manufacturing.bevel._800 import (
        ConicalGearManufacturingAnalysis,
    )
    from mastapy._private.gears.manufacturing.bevel._801 import (
        ConicalGearManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._802 import (
        ConicalGearMicroGeometryConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._803 import (
        ConicalGearMicroGeometryConfigBase,
    )
    from mastapy._private.gears.manufacturing.bevel._804 import (
        ConicalMeshedGearManufacturingAnalysis,
    )
    from mastapy._private.gears.manufacturing.bevel._805 import (
        ConicalMeshedWheelFlankManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._806 import (
        ConicalMeshFlankManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._807 import (
        ConicalMeshFlankMicroGeometryConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._808 import (
        ConicalMeshFlankNURBSMicroGeometryConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._809 import (
        ConicalMeshManufacturingAnalysis,
    )
    from mastapy._private.gears.manufacturing.bevel._810 import (
        ConicalMeshManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._811 import (
        ConicalMeshMicroGeometryConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._812 import (
        ConicalMeshMicroGeometryConfigBase,
    )
    from mastapy._private.gears.manufacturing.bevel._813 import (
        ConicalPinionManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._814 import (
        ConicalPinionMicroGeometryConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._815 import (
        ConicalSetManufacturingAnalysis,
    )
    from mastapy._private.gears.manufacturing.bevel._816 import (
        ConicalSetManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._817 import (
        ConicalSetMicroGeometryConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._818 import (
        ConicalSetMicroGeometryConfigBase,
    )
    from mastapy._private.gears.manufacturing.bevel._819 import (
        ConicalWheelManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._820 import EaseOffBasedTCA
    from mastapy._private.gears.manufacturing.bevel._821 import FlankMeasurementBorder
    from mastapy._private.gears.manufacturing.bevel._822 import HypoidAdvancedLibrary
    from mastapy._private.gears.manufacturing.bevel._823 import MachineTypes
    from mastapy._private.gears.manufacturing.bevel._824 import ManufacturingMachine
    from mastapy._private.gears.manufacturing.bevel._825 import (
        ManufacturingMachineDatabase,
    )
    from mastapy._private.gears.manufacturing.bevel._826 import (
        PinionBevelGeneratingModifiedRollMachineSettings,
    )
    from mastapy._private.gears.manufacturing.bevel._827 import (
        PinionBevelGeneratingTiltMachineSettings,
    )
    from mastapy._private.gears.manufacturing.bevel._828 import PinionConcave
    from mastapy._private.gears.manufacturing.bevel._829 import (
        PinionConicalMachineSettingsSpecified,
    )
    from mastapy._private.gears.manufacturing.bevel._830 import PinionConvex
    from mastapy._private.gears.manufacturing.bevel._831 import (
        PinionFinishMachineSettings,
    )
    from mastapy._private.gears.manufacturing.bevel._832 import (
        PinionHypoidFormateTiltMachineSettings,
    )
    from mastapy._private.gears.manufacturing.bevel._833 import (
        PinionHypoidGeneratingTiltMachineSettings,
    )
    from mastapy._private.gears.manufacturing.bevel._834 import PinionMachineSettingsSMT
    from mastapy._private.gears.manufacturing.bevel._835 import (
        PinionRoughMachineSetting,
    )
    from mastapy._private.gears.manufacturing.bevel._836 import Wheel
    from mastapy._private.gears.manufacturing.bevel._837 import WheelFormatMachineTypes
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.manufacturing.bevel._797": ["AbstractTCA"],
        "_private.gears.manufacturing.bevel._798": [
            "BevelMachineSettingOptimizationResult"
        ],
        "_private.gears.manufacturing.bevel._799": ["ConicalFlankDeviationsData"],
        "_private.gears.manufacturing.bevel._800": ["ConicalGearManufacturingAnalysis"],
        "_private.gears.manufacturing.bevel._801": ["ConicalGearManufacturingConfig"],
        "_private.gears.manufacturing.bevel._802": ["ConicalGearMicroGeometryConfig"],
        "_private.gears.manufacturing.bevel._803": [
            "ConicalGearMicroGeometryConfigBase"
        ],
        "_private.gears.manufacturing.bevel._804": [
            "ConicalMeshedGearManufacturingAnalysis"
        ],
        "_private.gears.manufacturing.bevel._805": [
            "ConicalMeshedWheelFlankManufacturingConfig"
        ],
        "_private.gears.manufacturing.bevel._806": [
            "ConicalMeshFlankManufacturingConfig"
        ],
        "_private.gears.manufacturing.bevel._807": [
            "ConicalMeshFlankMicroGeometryConfig"
        ],
        "_private.gears.manufacturing.bevel._808": [
            "ConicalMeshFlankNURBSMicroGeometryConfig"
        ],
        "_private.gears.manufacturing.bevel._809": ["ConicalMeshManufacturingAnalysis"],
        "_private.gears.manufacturing.bevel._810": ["ConicalMeshManufacturingConfig"],
        "_private.gears.manufacturing.bevel._811": ["ConicalMeshMicroGeometryConfig"],
        "_private.gears.manufacturing.bevel._812": [
            "ConicalMeshMicroGeometryConfigBase"
        ],
        "_private.gears.manufacturing.bevel._813": ["ConicalPinionManufacturingConfig"],
        "_private.gears.manufacturing.bevel._814": ["ConicalPinionMicroGeometryConfig"],
        "_private.gears.manufacturing.bevel._815": ["ConicalSetManufacturingAnalysis"],
        "_private.gears.manufacturing.bevel._816": ["ConicalSetManufacturingConfig"],
        "_private.gears.manufacturing.bevel._817": ["ConicalSetMicroGeometryConfig"],
        "_private.gears.manufacturing.bevel._818": [
            "ConicalSetMicroGeometryConfigBase"
        ],
        "_private.gears.manufacturing.bevel._819": ["ConicalWheelManufacturingConfig"],
        "_private.gears.manufacturing.bevel._820": ["EaseOffBasedTCA"],
        "_private.gears.manufacturing.bevel._821": ["FlankMeasurementBorder"],
        "_private.gears.manufacturing.bevel._822": ["HypoidAdvancedLibrary"],
        "_private.gears.manufacturing.bevel._823": ["MachineTypes"],
        "_private.gears.manufacturing.bevel._824": ["ManufacturingMachine"],
        "_private.gears.manufacturing.bevel._825": ["ManufacturingMachineDatabase"],
        "_private.gears.manufacturing.bevel._826": [
            "PinionBevelGeneratingModifiedRollMachineSettings"
        ],
        "_private.gears.manufacturing.bevel._827": [
            "PinionBevelGeneratingTiltMachineSettings"
        ],
        "_private.gears.manufacturing.bevel._828": ["PinionConcave"],
        "_private.gears.manufacturing.bevel._829": [
            "PinionConicalMachineSettingsSpecified"
        ],
        "_private.gears.manufacturing.bevel._830": ["PinionConvex"],
        "_private.gears.manufacturing.bevel._831": ["PinionFinishMachineSettings"],
        "_private.gears.manufacturing.bevel._832": [
            "PinionHypoidFormateTiltMachineSettings"
        ],
        "_private.gears.manufacturing.bevel._833": [
            "PinionHypoidGeneratingTiltMachineSettings"
        ],
        "_private.gears.manufacturing.bevel._834": ["PinionMachineSettingsSMT"],
        "_private.gears.manufacturing.bevel._835": ["PinionRoughMachineSetting"],
        "_private.gears.manufacturing.bevel._836": ["Wheel"],
        "_private.gears.manufacturing.bevel._837": ["WheelFormatMachineTypes"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractTCA",
    "BevelMachineSettingOptimizationResult",
    "ConicalFlankDeviationsData",
    "ConicalGearManufacturingAnalysis",
    "ConicalGearManufacturingConfig",
    "ConicalGearMicroGeometryConfig",
    "ConicalGearMicroGeometryConfigBase",
    "ConicalMeshedGearManufacturingAnalysis",
    "ConicalMeshedWheelFlankManufacturingConfig",
    "ConicalMeshFlankManufacturingConfig",
    "ConicalMeshFlankMicroGeometryConfig",
    "ConicalMeshFlankNURBSMicroGeometryConfig",
    "ConicalMeshManufacturingAnalysis",
    "ConicalMeshManufacturingConfig",
    "ConicalMeshMicroGeometryConfig",
    "ConicalMeshMicroGeometryConfigBase",
    "ConicalPinionManufacturingConfig",
    "ConicalPinionMicroGeometryConfig",
    "ConicalSetManufacturingAnalysis",
    "ConicalSetManufacturingConfig",
    "ConicalSetMicroGeometryConfig",
    "ConicalSetMicroGeometryConfigBase",
    "ConicalWheelManufacturingConfig",
    "EaseOffBasedTCA",
    "FlankMeasurementBorder",
    "HypoidAdvancedLibrary",
    "MachineTypes",
    "ManufacturingMachine",
    "ManufacturingMachineDatabase",
    "PinionBevelGeneratingModifiedRollMachineSettings",
    "PinionBevelGeneratingTiltMachineSettings",
    "PinionConcave",
    "PinionConicalMachineSettingsSpecified",
    "PinionConvex",
    "PinionFinishMachineSettings",
    "PinionHypoidFormateTiltMachineSettings",
    "PinionHypoidGeneratingTiltMachineSettings",
    "PinionMachineSettingsSMT",
    "PinionRoughMachineSetting",
    "Wheel",
    "WheelFormatMachineTypes",
)
