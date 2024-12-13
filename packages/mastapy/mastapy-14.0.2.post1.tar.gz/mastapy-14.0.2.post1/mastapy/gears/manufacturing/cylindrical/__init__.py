"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.manufacturing.cylindrical._634 import (
        CutterFlankSections,
    )
    from mastapy._private.gears.manufacturing.cylindrical._635 import (
        CylindricalCutterDatabase,
    )
    from mastapy._private.gears.manufacturing.cylindrical._636 import (
        CylindricalGearBlank,
    )
    from mastapy._private.gears.manufacturing.cylindrical._637 import (
        CylindricalGearManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.cylindrical._638 import (
        CylindricalGearSpecifiedMicroGeometry,
    )
    from mastapy._private.gears.manufacturing.cylindrical._639 import (
        CylindricalGearSpecifiedProfile,
    )
    from mastapy._private.gears.manufacturing.cylindrical._640 import (
        CylindricalHobDatabase,
    )
    from mastapy._private.gears.manufacturing.cylindrical._641 import (
        CylindricalManufacturedGearDutyCycle,
    )
    from mastapy._private.gears.manufacturing.cylindrical._642 import (
        CylindricalManufacturedGearLoadCase,
    )
    from mastapy._private.gears.manufacturing.cylindrical._643 import (
        CylindricalManufacturedGearMeshDutyCycle,
    )
    from mastapy._private.gears.manufacturing.cylindrical._644 import (
        CylindricalManufacturedGearMeshLoadCase,
    )
    from mastapy._private.gears.manufacturing.cylindrical._645 import (
        CylindricalManufacturedGearSetDutyCycle,
    )
    from mastapy._private.gears.manufacturing.cylindrical._646 import (
        CylindricalManufacturedGearSetLoadCase,
    )
    from mastapy._private.gears.manufacturing.cylindrical._647 import (
        CylindricalMeshManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.cylindrical._648 import (
        CylindricalMftFinishingMethods,
    )
    from mastapy._private.gears.manufacturing.cylindrical._649 import (
        CylindricalMftRoughingMethods,
    )
    from mastapy._private.gears.manufacturing.cylindrical._650 import (
        CylindricalSetManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.cylindrical._651 import (
        CylindricalShaperDatabase,
    )
    from mastapy._private.gears.manufacturing.cylindrical._652 import Flank
    from mastapy._private.gears.manufacturing.cylindrical._653 import (
        GearManufacturingConfigurationViewModel,
    )
    from mastapy._private.gears.manufacturing.cylindrical._654 import (
        GearManufacturingConfigurationViewModelPlaceholder,
    )
    from mastapy._private.gears.manufacturing.cylindrical._655 import (
        GearSetConfigViewModel,
    )
    from mastapy._private.gears.manufacturing.cylindrical._656 import HobEdgeTypes
    from mastapy._private.gears.manufacturing.cylindrical._657 import (
        LeadModificationSegment,
    )
    from mastapy._private.gears.manufacturing.cylindrical._658 import (
        MicroGeometryInputs,
    )
    from mastapy._private.gears.manufacturing.cylindrical._659 import (
        MicroGeometryInputsLead,
    )
    from mastapy._private.gears.manufacturing.cylindrical._660 import (
        MicroGeometryInputsProfile,
    )
    from mastapy._private.gears.manufacturing.cylindrical._661 import (
        ModificationSegment,
    )
    from mastapy._private.gears.manufacturing.cylindrical._662 import (
        ProfileModificationSegment,
    )
    from mastapy._private.gears.manufacturing.cylindrical._663 import (
        SuitableCutterSetup,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.manufacturing.cylindrical._634": ["CutterFlankSections"],
        "_private.gears.manufacturing.cylindrical._635": ["CylindricalCutterDatabase"],
        "_private.gears.manufacturing.cylindrical._636": ["CylindricalGearBlank"],
        "_private.gears.manufacturing.cylindrical._637": [
            "CylindricalGearManufacturingConfig"
        ],
        "_private.gears.manufacturing.cylindrical._638": [
            "CylindricalGearSpecifiedMicroGeometry"
        ],
        "_private.gears.manufacturing.cylindrical._639": [
            "CylindricalGearSpecifiedProfile"
        ],
        "_private.gears.manufacturing.cylindrical._640": ["CylindricalHobDatabase"],
        "_private.gears.manufacturing.cylindrical._641": [
            "CylindricalManufacturedGearDutyCycle"
        ],
        "_private.gears.manufacturing.cylindrical._642": [
            "CylindricalManufacturedGearLoadCase"
        ],
        "_private.gears.manufacturing.cylindrical._643": [
            "CylindricalManufacturedGearMeshDutyCycle"
        ],
        "_private.gears.manufacturing.cylindrical._644": [
            "CylindricalManufacturedGearMeshLoadCase"
        ],
        "_private.gears.manufacturing.cylindrical._645": [
            "CylindricalManufacturedGearSetDutyCycle"
        ],
        "_private.gears.manufacturing.cylindrical._646": [
            "CylindricalManufacturedGearSetLoadCase"
        ],
        "_private.gears.manufacturing.cylindrical._647": [
            "CylindricalMeshManufacturingConfig"
        ],
        "_private.gears.manufacturing.cylindrical._648": [
            "CylindricalMftFinishingMethods"
        ],
        "_private.gears.manufacturing.cylindrical._649": [
            "CylindricalMftRoughingMethods"
        ],
        "_private.gears.manufacturing.cylindrical._650": [
            "CylindricalSetManufacturingConfig"
        ],
        "_private.gears.manufacturing.cylindrical._651": ["CylindricalShaperDatabase"],
        "_private.gears.manufacturing.cylindrical._652": ["Flank"],
        "_private.gears.manufacturing.cylindrical._653": [
            "GearManufacturingConfigurationViewModel"
        ],
        "_private.gears.manufacturing.cylindrical._654": [
            "GearManufacturingConfigurationViewModelPlaceholder"
        ],
        "_private.gears.manufacturing.cylindrical._655": ["GearSetConfigViewModel"],
        "_private.gears.manufacturing.cylindrical._656": ["HobEdgeTypes"],
        "_private.gears.manufacturing.cylindrical._657": ["LeadModificationSegment"],
        "_private.gears.manufacturing.cylindrical._658": ["MicroGeometryInputs"],
        "_private.gears.manufacturing.cylindrical._659": ["MicroGeometryInputsLead"],
        "_private.gears.manufacturing.cylindrical._660": ["MicroGeometryInputsProfile"],
        "_private.gears.manufacturing.cylindrical._661": ["ModificationSegment"],
        "_private.gears.manufacturing.cylindrical._662": ["ProfileModificationSegment"],
        "_private.gears.manufacturing.cylindrical._663": ["SuitableCutterSetup"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CutterFlankSections",
    "CylindricalCutterDatabase",
    "CylindricalGearBlank",
    "CylindricalGearManufacturingConfig",
    "CylindricalGearSpecifiedMicroGeometry",
    "CylindricalGearSpecifiedProfile",
    "CylindricalHobDatabase",
    "CylindricalManufacturedGearDutyCycle",
    "CylindricalManufacturedGearLoadCase",
    "CylindricalManufacturedGearMeshDutyCycle",
    "CylindricalManufacturedGearMeshLoadCase",
    "CylindricalManufacturedGearSetDutyCycle",
    "CylindricalManufacturedGearSetLoadCase",
    "CylindricalMeshManufacturingConfig",
    "CylindricalMftFinishingMethods",
    "CylindricalMftRoughingMethods",
    "CylindricalSetManufacturingConfig",
    "CylindricalShaperDatabase",
    "Flank",
    "GearManufacturingConfigurationViewModel",
    "GearManufacturingConfigurationViewModelPlaceholder",
    "GearSetConfigViewModel",
    "HobEdgeTypes",
    "LeadModificationSegment",
    "MicroGeometryInputs",
    "MicroGeometryInputsLead",
    "MicroGeometryInputsProfile",
    "ModificationSegment",
    "ProfileModificationSegment",
    "SuitableCutterSetup",
)
