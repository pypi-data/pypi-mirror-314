"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs._966 import (
        BevelHypoidGearDesignSettingsDatabase,
    )
    from mastapy._private.gears.gear_designs._967 import (
        BevelHypoidGearDesignSettingsItem,
    )
    from mastapy._private.gears.gear_designs._968 import (
        BevelHypoidGearRatingSettingsDatabase,
    )
    from mastapy._private.gears.gear_designs._969 import (
        BevelHypoidGearRatingSettingsItem,
    )
    from mastapy._private.gears.gear_designs._970 import DesignConstraint
    from mastapy._private.gears.gear_designs._971 import (
        DesignConstraintCollectionDatabase,
    )
    from mastapy._private.gears.gear_designs._972 import DesignConstraintsCollection
    from mastapy._private.gears.gear_designs._973 import GearDesign
    from mastapy._private.gears.gear_designs._974 import GearDesignComponent
    from mastapy._private.gears.gear_designs._975 import GearMeshDesign
    from mastapy._private.gears.gear_designs._976 import GearSetDesign
    from mastapy._private.gears.gear_designs._977 import (
        SelectedDesignConstraintsCollection,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs._966": ["BevelHypoidGearDesignSettingsDatabase"],
        "_private.gears.gear_designs._967": ["BevelHypoidGearDesignSettingsItem"],
        "_private.gears.gear_designs._968": ["BevelHypoidGearRatingSettingsDatabase"],
        "_private.gears.gear_designs._969": ["BevelHypoidGearRatingSettingsItem"],
        "_private.gears.gear_designs._970": ["DesignConstraint"],
        "_private.gears.gear_designs._971": ["DesignConstraintCollectionDatabase"],
        "_private.gears.gear_designs._972": ["DesignConstraintsCollection"],
        "_private.gears.gear_designs._973": ["GearDesign"],
        "_private.gears.gear_designs._974": ["GearDesignComponent"],
        "_private.gears.gear_designs._975": ["GearMeshDesign"],
        "_private.gears.gear_designs._976": ["GearSetDesign"],
        "_private.gears.gear_designs._977": ["SelectedDesignConstraintsCollection"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BevelHypoidGearDesignSettingsDatabase",
    "BevelHypoidGearDesignSettingsItem",
    "BevelHypoidGearRatingSettingsDatabase",
    "BevelHypoidGearRatingSettingsItem",
    "DesignConstraint",
    "DesignConstraintCollectionDatabase",
    "DesignConstraintsCollection",
    "GearDesign",
    "GearDesignComponent",
    "GearMeshDesign",
    "GearSetDesign",
    "SelectedDesignConstraintsCollection",
)
