"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2616 import (
        BoostPressureInputOptions,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2617 import (
        InputPowerInputOptions,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2618 import (
        PressureRatioInputOptions,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2619 import (
        RotorSetDataInputFileOptions,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2620 import (
        RotorSetMeasuredPoint,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2621 import (
        RotorSpeedInputOptions,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2622 import (
        SuperchargerMap,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2623 import (
        SuperchargerMaps,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2624 import (
        SuperchargerRotorSet,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2625 import (
        SuperchargerRotorSetDatabase,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2626 import (
        YVariableForImportedData,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.gears.supercharger_rotor_set._2616": [
            "BoostPressureInputOptions"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2617": [
            "InputPowerInputOptions"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2618": [
            "PressureRatioInputOptions"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2619": [
            "RotorSetDataInputFileOptions"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2620": [
            "RotorSetMeasuredPoint"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2621": [
            "RotorSpeedInputOptions"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2622": [
            "SuperchargerMap"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2623": [
            "SuperchargerMaps"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2624": [
            "SuperchargerRotorSet"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2625": [
            "SuperchargerRotorSetDatabase"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2626": [
            "YVariableForImportedData"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BoostPressureInputOptions",
    "InputPowerInputOptions",
    "PressureRatioInputOptions",
    "RotorSetDataInputFileOptions",
    "RotorSetMeasuredPoint",
    "RotorSpeedInputOptions",
    "SuperchargerMap",
    "SuperchargerMaps",
    "SuperchargerRotorSet",
    "SuperchargerRotorSetDatabase",
    "YVariableForImportedData",
)
