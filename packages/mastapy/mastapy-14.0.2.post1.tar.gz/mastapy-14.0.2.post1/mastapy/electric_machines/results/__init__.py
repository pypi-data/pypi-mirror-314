"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.electric_machines.results._1371 import DynamicForceResults
    from mastapy._private.electric_machines.results._1372 import EfficiencyResults
    from mastapy._private.electric_machines.results._1373 import ElectricMachineDQModel
    from mastapy._private.electric_machines.results._1374 import (
        ElectricMachineMechanicalResults,
    )
    from mastapy._private.electric_machines.results._1375 import (
        ElectricMachineMechanicalResultsViewable,
    )
    from mastapy._private.electric_machines.results._1376 import ElectricMachineResults
    from mastapy._private.electric_machines.results._1377 import (
        ElectricMachineResultsForConductorTurn,
    )
    from mastapy._private.electric_machines.results._1378 import (
        ElectricMachineResultsForConductorTurnAtTimeStep,
    )
    from mastapy._private.electric_machines.results._1379 import (
        ElectricMachineResultsForLineToLine,
    )
    from mastapy._private.electric_machines.results._1380 import (
        ElectricMachineResultsForOpenCircuitAndOnLoad,
    )
    from mastapy._private.electric_machines.results._1381 import (
        ElectricMachineResultsForPhase,
    )
    from mastapy._private.electric_machines.results._1382 import (
        ElectricMachineResultsForPhaseAtTimeStep,
    )
    from mastapy._private.electric_machines.results._1383 import (
        ElectricMachineResultsForStatorToothAtTimeStep,
    )
    from mastapy._private.electric_machines.results._1384 import (
        ElectricMachineResultsLineToLineAtTimeStep,
    )
    from mastapy._private.electric_machines.results._1385 import (
        ElectricMachineResultsTimeStep,
    )
    from mastapy._private.electric_machines.results._1386 import (
        ElectricMachineResultsTimeStepAtLocation,
    )
    from mastapy._private.electric_machines.results._1387 import (
        ElectricMachineResultsViewable,
    )
    from mastapy._private.electric_machines.results._1388 import (
        ElectricMachineForceViewOptions,
    )
    from mastapy._private.electric_machines.results._1390 import LinearDQModel
    from mastapy._private.electric_machines.results._1391 import (
        MaximumTorqueResultsPoints,
    )
    from mastapy._private.electric_machines.results._1392 import NonLinearDQModel
    from mastapy._private.electric_machines.results._1393 import (
        NonLinearDQModelGeneratorSettings,
    )
    from mastapy._private.electric_machines.results._1394 import (
        OnLoadElectricMachineResults,
    )
    from mastapy._private.electric_machines.results._1395 import (
        OpenCircuitElectricMachineResults,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.electric_machines.results._1371": ["DynamicForceResults"],
        "_private.electric_machines.results._1372": ["EfficiencyResults"],
        "_private.electric_machines.results._1373": ["ElectricMachineDQModel"],
        "_private.electric_machines.results._1374": [
            "ElectricMachineMechanicalResults"
        ],
        "_private.electric_machines.results._1375": [
            "ElectricMachineMechanicalResultsViewable"
        ],
        "_private.electric_machines.results._1376": ["ElectricMachineResults"],
        "_private.electric_machines.results._1377": [
            "ElectricMachineResultsForConductorTurn"
        ],
        "_private.electric_machines.results._1378": [
            "ElectricMachineResultsForConductorTurnAtTimeStep"
        ],
        "_private.electric_machines.results._1379": [
            "ElectricMachineResultsForLineToLine"
        ],
        "_private.electric_machines.results._1380": [
            "ElectricMachineResultsForOpenCircuitAndOnLoad"
        ],
        "_private.electric_machines.results._1381": ["ElectricMachineResultsForPhase"],
        "_private.electric_machines.results._1382": [
            "ElectricMachineResultsForPhaseAtTimeStep"
        ],
        "_private.electric_machines.results._1383": [
            "ElectricMachineResultsForStatorToothAtTimeStep"
        ],
        "_private.electric_machines.results._1384": [
            "ElectricMachineResultsLineToLineAtTimeStep"
        ],
        "_private.electric_machines.results._1385": ["ElectricMachineResultsTimeStep"],
        "_private.electric_machines.results._1386": [
            "ElectricMachineResultsTimeStepAtLocation"
        ],
        "_private.electric_machines.results._1387": ["ElectricMachineResultsViewable"],
        "_private.electric_machines.results._1388": ["ElectricMachineForceViewOptions"],
        "_private.electric_machines.results._1390": ["LinearDQModel"],
        "_private.electric_machines.results._1391": ["MaximumTorqueResultsPoints"],
        "_private.electric_machines.results._1392": ["NonLinearDQModel"],
        "_private.electric_machines.results._1393": [
            "NonLinearDQModelGeneratorSettings"
        ],
        "_private.electric_machines.results._1394": ["OnLoadElectricMachineResults"],
        "_private.electric_machines.results._1395": [
            "OpenCircuitElectricMachineResults"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DynamicForceResults",
    "EfficiencyResults",
    "ElectricMachineDQModel",
    "ElectricMachineMechanicalResults",
    "ElectricMachineMechanicalResultsViewable",
    "ElectricMachineResults",
    "ElectricMachineResultsForConductorTurn",
    "ElectricMachineResultsForConductorTurnAtTimeStep",
    "ElectricMachineResultsForLineToLine",
    "ElectricMachineResultsForOpenCircuitAndOnLoad",
    "ElectricMachineResultsForPhase",
    "ElectricMachineResultsForPhaseAtTimeStep",
    "ElectricMachineResultsForStatorToothAtTimeStep",
    "ElectricMachineResultsLineToLineAtTimeStep",
    "ElectricMachineResultsTimeStep",
    "ElectricMachineResultsTimeStepAtLocation",
    "ElectricMachineResultsViewable",
    "ElectricMachineForceViewOptions",
    "LinearDQModel",
    "MaximumTorqueResultsPoints",
    "NonLinearDQModel",
    "NonLinearDQModelGeneratorSettings",
    "OnLoadElectricMachineResults",
    "OpenCircuitElectricMachineResults",
)
