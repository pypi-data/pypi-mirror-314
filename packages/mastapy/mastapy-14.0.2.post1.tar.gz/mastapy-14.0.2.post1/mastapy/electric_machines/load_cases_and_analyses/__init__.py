"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.electric_machines.load_cases_and_analyses._1396 import (
        BasicDynamicForceLoadCase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1397 import (
        DynamicForceAnalysis,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1398 import (
        DynamicForceLoadCase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1399 import (
        DynamicForcesOperatingPoint,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1400 import (
        EfficiencyMapAnalysis,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1401 import (
        EfficiencyMapLoadCase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1402 import (
        ElectricMachineAnalysis,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1403 import (
        ElectricMachineBasicMechanicalLossSettings,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1404 import (
        ElectricMachineControlStrategy,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1405 import (
        ElectricMachineEfficiencyMapSettings,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1406 import (
        ElectricMachineFEAnalysis,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1407 import (
        ElectricMachineFEMechanicalAnalysis,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1408 import (
        ElectricMachineLoadCase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1409 import (
        ElectricMachineLoadCaseBase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1410 import (
        ElectricMachineLoadCaseGroup,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1411 import (
        ElectricMachineMechanicalLoadCase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1412 import (
        EndWindingInductanceMethod,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1413 import (
        LeadingOrLagging,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1414 import (
        LoadCaseType,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1415 import (
        LoadCaseTypeSelector,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1416 import (
        MotoringOrGenerating,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1417 import (
        NonLinearDQModelMultipleOperatingPointsLoadCase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1418 import (
        NumberOfStepsPerOperatingPointSpecificationMethod,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1419 import (
        OperatingPointsSpecificationMethod,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1420 import (
        SingleOperatingPointAnalysis,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1421 import (
        SlotDetailForAnalysis,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1422 import (
        SpecifyTorqueOrCurrent,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1423 import (
        SpeedPointsDistribution,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1424 import (
        SpeedTorqueCurveAnalysis,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1425 import (
        SpeedTorqueCurveLoadCase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1426 import (
        SpeedTorqueLoadCase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1427 import (
        Temperatures,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.electric_machines.load_cases_and_analyses._1396": [
            "BasicDynamicForceLoadCase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1397": [
            "DynamicForceAnalysis"
        ],
        "_private.electric_machines.load_cases_and_analyses._1398": [
            "DynamicForceLoadCase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1399": [
            "DynamicForcesOperatingPoint"
        ],
        "_private.electric_machines.load_cases_and_analyses._1400": [
            "EfficiencyMapAnalysis"
        ],
        "_private.electric_machines.load_cases_and_analyses._1401": [
            "EfficiencyMapLoadCase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1402": [
            "ElectricMachineAnalysis"
        ],
        "_private.electric_machines.load_cases_and_analyses._1403": [
            "ElectricMachineBasicMechanicalLossSettings"
        ],
        "_private.electric_machines.load_cases_and_analyses._1404": [
            "ElectricMachineControlStrategy"
        ],
        "_private.electric_machines.load_cases_and_analyses._1405": [
            "ElectricMachineEfficiencyMapSettings"
        ],
        "_private.electric_machines.load_cases_and_analyses._1406": [
            "ElectricMachineFEAnalysis"
        ],
        "_private.electric_machines.load_cases_and_analyses._1407": [
            "ElectricMachineFEMechanicalAnalysis"
        ],
        "_private.electric_machines.load_cases_and_analyses._1408": [
            "ElectricMachineLoadCase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1409": [
            "ElectricMachineLoadCaseBase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1410": [
            "ElectricMachineLoadCaseGroup"
        ],
        "_private.electric_machines.load_cases_and_analyses._1411": [
            "ElectricMachineMechanicalLoadCase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1412": [
            "EndWindingInductanceMethod"
        ],
        "_private.electric_machines.load_cases_and_analyses._1413": [
            "LeadingOrLagging"
        ],
        "_private.electric_machines.load_cases_and_analyses._1414": ["LoadCaseType"],
        "_private.electric_machines.load_cases_and_analyses._1415": [
            "LoadCaseTypeSelector"
        ],
        "_private.electric_machines.load_cases_and_analyses._1416": [
            "MotoringOrGenerating"
        ],
        "_private.electric_machines.load_cases_and_analyses._1417": [
            "NonLinearDQModelMultipleOperatingPointsLoadCase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1418": [
            "NumberOfStepsPerOperatingPointSpecificationMethod"
        ],
        "_private.electric_machines.load_cases_and_analyses._1419": [
            "OperatingPointsSpecificationMethod"
        ],
        "_private.electric_machines.load_cases_and_analyses._1420": [
            "SingleOperatingPointAnalysis"
        ],
        "_private.electric_machines.load_cases_and_analyses._1421": [
            "SlotDetailForAnalysis"
        ],
        "_private.electric_machines.load_cases_and_analyses._1422": [
            "SpecifyTorqueOrCurrent"
        ],
        "_private.electric_machines.load_cases_and_analyses._1423": [
            "SpeedPointsDistribution"
        ],
        "_private.electric_machines.load_cases_and_analyses._1424": [
            "SpeedTorqueCurveAnalysis"
        ],
        "_private.electric_machines.load_cases_and_analyses._1425": [
            "SpeedTorqueCurveLoadCase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1426": [
            "SpeedTorqueLoadCase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1427": ["Temperatures"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BasicDynamicForceLoadCase",
    "DynamicForceAnalysis",
    "DynamicForceLoadCase",
    "DynamicForcesOperatingPoint",
    "EfficiencyMapAnalysis",
    "EfficiencyMapLoadCase",
    "ElectricMachineAnalysis",
    "ElectricMachineBasicMechanicalLossSettings",
    "ElectricMachineControlStrategy",
    "ElectricMachineEfficiencyMapSettings",
    "ElectricMachineFEAnalysis",
    "ElectricMachineFEMechanicalAnalysis",
    "ElectricMachineLoadCase",
    "ElectricMachineLoadCaseBase",
    "ElectricMachineLoadCaseGroup",
    "ElectricMachineMechanicalLoadCase",
    "EndWindingInductanceMethod",
    "LeadingOrLagging",
    "LoadCaseType",
    "LoadCaseTypeSelector",
    "MotoringOrGenerating",
    "NonLinearDQModelMultipleOperatingPointsLoadCase",
    "NumberOfStepsPerOperatingPointSpecificationMethod",
    "OperatingPointsSpecificationMethod",
    "SingleOperatingPointAnalysis",
    "SlotDetailForAnalysis",
    "SpecifyTorqueOrCurrent",
    "SpeedPointsDistribution",
    "SpeedTorqueCurveAnalysis",
    "SpeedTorqueCurveLoadCase",
    "SpeedTorqueLoadCase",
    "Temperatures",
)
