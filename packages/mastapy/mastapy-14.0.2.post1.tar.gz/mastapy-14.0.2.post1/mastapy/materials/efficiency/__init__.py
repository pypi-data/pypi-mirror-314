"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.materials.efficiency._305 import BearingEfficiencyRatingMethod
    from mastapy._private.materials.efficiency._306 import CombinedResistiveTorque
    from mastapy._private.materials.efficiency._307 import IndependentPowerLoss
    from mastapy._private.materials.efficiency._308 import IndependentResistiveTorque
    from mastapy._private.materials.efficiency._309 import LoadAndSpeedCombinedPowerLoss
    from mastapy._private.materials.efficiency._310 import OilPumpDetail
    from mastapy._private.materials.efficiency._311 import OilPumpDriveType
    from mastapy._private.materials.efficiency._312 import OilSealLossCalculationMethod
    from mastapy._private.materials.efficiency._313 import OilSealMaterialType
    from mastapy._private.materials.efficiency._314 import PowerLoss
    from mastapy._private.materials.efficiency._315 import ResistiveTorque
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.materials.efficiency._305": ["BearingEfficiencyRatingMethod"],
        "_private.materials.efficiency._306": ["CombinedResistiveTorque"],
        "_private.materials.efficiency._307": ["IndependentPowerLoss"],
        "_private.materials.efficiency._308": ["IndependentResistiveTorque"],
        "_private.materials.efficiency._309": ["LoadAndSpeedCombinedPowerLoss"],
        "_private.materials.efficiency._310": ["OilPumpDetail"],
        "_private.materials.efficiency._311": ["OilPumpDriveType"],
        "_private.materials.efficiency._312": ["OilSealLossCalculationMethod"],
        "_private.materials.efficiency._313": ["OilSealMaterialType"],
        "_private.materials.efficiency._314": ["PowerLoss"],
        "_private.materials.efficiency._315": ["ResistiveTorque"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BearingEfficiencyRatingMethod",
    "CombinedResistiveTorque",
    "IndependentPowerLoss",
    "IndependentResistiveTorque",
    "LoadAndSpeedCombinedPowerLoss",
    "OilPumpDetail",
    "OilPumpDriveType",
    "OilSealLossCalculationMethod",
    "OilSealMaterialType",
    "PowerLoss",
    "ResistiveTorque",
)
