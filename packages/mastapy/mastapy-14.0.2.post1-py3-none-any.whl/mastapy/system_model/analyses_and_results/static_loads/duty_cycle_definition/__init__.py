"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7143 import (
        AdditionalForcesObtainedFrom,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7144 import (
        BoostPressureLoadCaseInputOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7145 import (
        DesignStateOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7146 import (
        DestinationDesignState,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7147 import (
        ForceInputOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7148 import (
        GearRatioInputOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7149 import (
        LoadCaseNameOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7150 import (
        MomentInputOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7151 import (
        MultiTimeSeriesDataInputFileOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7152 import (
        PointLoadInputOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7153 import (
        PowerLoadInputOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7154 import (
        RampOrSteadyStateInputOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7155 import (
        SpeedInputOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7156 import (
        TimeSeriesImporter,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7157 import (
        TimeStepInputOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7158 import (
        TorqueInputOptions,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7159 import (
        TorqueValuesObtainedFrom,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7143": [
            "AdditionalForcesObtainedFrom"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7144": [
            "BoostPressureLoadCaseInputOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7145": [
            "DesignStateOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7146": [
            "DestinationDesignState"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7147": [
            "ForceInputOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7148": [
            "GearRatioInputOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7149": [
            "LoadCaseNameOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7150": [
            "MomentInputOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7151": [
            "MultiTimeSeriesDataInputFileOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7152": [
            "PointLoadInputOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7153": [
            "PowerLoadInputOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7154": [
            "RampOrSteadyStateInputOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7155": [
            "SpeedInputOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7156": [
            "TimeSeriesImporter"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7157": [
            "TimeStepInputOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7158": [
            "TorqueInputOptions"
        ],
        "_private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7159": [
            "TorqueValuesObtainedFrom"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AdditionalForcesObtainedFrom",
    "BoostPressureLoadCaseInputOptions",
    "DesignStateOptions",
    "DestinationDesignState",
    "ForceInputOptions",
    "GearRatioInputOptions",
    "LoadCaseNameOptions",
    "MomentInputOptions",
    "MultiTimeSeriesDataInputFileOptions",
    "PointLoadInputOptions",
    "PowerLoadInputOptions",
    "RampOrSteadyStateInputOptions",
    "SpeedInputOptions",
    "TimeSeriesImporter",
    "TimeStepInputOptions",
    "TorqueInputOptions",
    "TorqueValuesObtainedFrom",
)
