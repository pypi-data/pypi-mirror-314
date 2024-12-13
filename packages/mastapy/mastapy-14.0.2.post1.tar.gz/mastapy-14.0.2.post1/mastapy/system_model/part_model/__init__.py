"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model._2491 import Assembly
    from mastapy._private.system_model.part_model._2492 import AbstractAssembly
    from mastapy._private.system_model.part_model._2493 import AbstractShaft
    from mastapy._private.system_model.part_model._2494 import AbstractShaftOrHousing
    from mastapy._private.system_model.part_model._2495 import (
        AGMALoadSharingTableApplicationLevel,
    )
    from mastapy._private.system_model.part_model._2496 import (
        AxialInternalClearanceTolerance,
    )
    from mastapy._private.system_model.part_model._2497 import Bearing
    from mastapy._private.system_model.part_model._2498 import BearingF0InputMethod
    from mastapy._private.system_model.part_model._2499 import (
        BearingRaceMountingOptions,
    )
    from mastapy._private.system_model.part_model._2500 import Bolt
    from mastapy._private.system_model.part_model._2501 import BoltedJoint
    from mastapy._private.system_model.part_model._2502 import Component
    from mastapy._private.system_model.part_model._2503 import ComponentsConnectedResult
    from mastapy._private.system_model.part_model._2504 import ConnectedSockets
    from mastapy._private.system_model.part_model._2505 import Connector
    from mastapy._private.system_model.part_model._2506 import Datum
    from mastapy._private.system_model.part_model._2507 import (
        ElectricMachineSearchRegionSpecificationMethod,
    )
    from mastapy._private.system_model.part_model._2508 import EnginePartLoad
    from mastapy._private.system_model.part_model._2509 import EngineSpeed
    from mastapy._private.system_model.part_model._2510 import ExternalCADModel
    from mastapy._private.system_model.part_model._2511 import FEPart
    from mastapy._private.system_model.part_model._2512 import FlexiblePinAssembly
    from mastapy._private.system_model.part_model._2513 import GuideDxfModel
    from mastapy._private.system_model.part_model._2514 import GuideImage
    from mastapy._private.system_model.part_model._2515 import GuideModelUsage
    from mastapy._private.system_model.part_model._2516 import (
        InnerBearingRaceMountingOptions,
    )
    from mastapy._private.system_model.part_model._2517 import (
        InternalClearanceTolerance,
    )
    from mastapy._private.system_model.part_model._2518 import LoadSharingModes
    from mastapy._private.system_model.part_model._2519 import LoadSharingSettings
    from mastapy._private.system_model.part_model._2520 import MassDisc
    from mastapy._private.system_model.part_model._2521 import MeasurementComponent
    from mastapy._private.system_model.part_model._2522 import Microphone
    from mastapy._private.system_model.part_model._2523 import MicrophoneArray
    from mastapy._private.system_model.part_model._2524 import MountableComponent
    from mastapy._private.system_model.part_model._2525 import OilLevelSpecification
    from mastapy._private.system_model.part_model._2526 import OilSeal
    from mastapy._private.system_model.part_model._2527 import (
        OuterBearingRaceMountingOptions,
    )
    from mastapy._private.system_model.part_model._2528 import Part
    from mastapy._private.system_model.part_model._2529 import PlanetCarrier
    from mastapy._private.system_model.part_model._2530 import PlanetCarrierSettings
    from mastapy._private.system_model.part_model._2531 import PointLoad
    from mastapy._private.system_model.part_model._2532 import PowerLoad
    from mastapy._private.system_model.part_model._2533 import (
        RadialInternalClearanceTolerance,
    )
    from mastapy._private.system_model.part_model._2534 import (
        RollingBearingElementLoadCase,
    )
    from mastapy._private.system_model.part_model._2535 import RootAssembly
    from mastapy._private.system_model.part_model._2536 import (
        ShaftDiameterModificationDueToRollingBearingRing,
    )
    from mastapy._private.system_model.part_model._2537 import SpecialisedAssembly
    from mastapy._private.system_model.part_model._2538 import UnbalancedMass
    from mastapy._private.system_model.part_model._2539 import (
        UnbalancedMassInclusionOption,
    )
    from mastapy._private.system_model.part_model._2540 import VirtualComponent
    from mastapy._private.system_model.part_model._2541 import (
        WindTurbineBladeModeDetails,
    )
    from mastapy._private.system_model.part_model._2542 import (
        WindTurbineSingleBladeDetails,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model._2491": ["Assembly"],
        "_private.system_model.part_model._2492": ["AbstractAssembly"],
        "_private.system_model.part_model._2493": ["AbstractShaft"],
        "_private.system_model.part_model._2494": ["AbstractShaftOrHousing"],
        "_private.system_model.part_model._2495": [
            "AGMALoadSharingTableApplicationLevel"
        ],
        "_private.system_model.part_model._2496": ["AxialInternalClearanceTolerance"],
        "_private.system_model.part_model._2497": ["Bearing"],
        "_private.system_model.part_model._2498": ["BearingF0InputMethod"],
        "_private.system_model.part_model._2499": ["BearingRaceMountingOptions"],
        "_private.system_model.part_model._2500": ["Bolt"],
        "_private.system_model.part_model._2501": ["BoltedJoint"],
        "_private.system_model.part_model._2502": ["Component"],
        "_private.system_model.part_model._2503": ["ComponentsConnectedResult"],
        "_private.system_model.part_model._2504": ["ConnectedSockets"],
        "_private.system_model.part_model._2505": ["Connector"],
        "_private.system_model.part_model._2506": ["Datum"],
        "_private.system_model.part_model._2507": [
            "ElectricMachineSearchRegionSpecificationMethod"
        ],
        "_private.system_model.part_model._2508": ["EnginePartLoad"],
        "_private.system_model.part_model._2509": ["EngineSpeed"],
        "_private.system_model.part_model._2510": ["ExternalCADModel"],
        "_private.system_model.part_model._2511": ["FEPart"],
        "_private.system_model.part_model._2512": ["FlexiblePinAssembly"],
        "_private.system_model.part_model._2513": ["GuideDxfModel"],
        "_private.system_model.part_model._2514": ["GuideImage"],
        "_private.system_model.part_model._2515": ["GuideModelUsage"],
        "_private.system_model.part_model._2516": ["InnerBearingRaceMountingOptions"],
        "_private.system_model.part_model._2517": ["InternalClearanceTolerance"],
        "_private.system_model.part_model._2518": ["LoadSharingModes"],
        "_private.system_model.part_model._2519": ["LoadSharingSettings"],
        "_private.system_model.part_model._2520": ["MassDisc"],
        "_private.system_model.part_model._2521": ["MeasurementComponent"],
        "_private.system_model.part_model._2522": ["Microphone"],
        "_private.system_model.part_model._2523": ["MicrophoneArray"],
        "_private.system_model.part_model._2524": ["MountableComponent"],
        "_private.system_model.part_model._2525": ["OilLevelSpecification"],
        "_private.system_model.part_model._2526": ["OilSeal"],
        "_private.system_model.part_model._2527": ["OuterBearingRaceMountingOptions"],
        "_private.system_model.part_model._2528": ["Part"],
        "_private.system_model.part_model._2529": ["PlanetCarrier"],
        "_private.system_model.part_model._2530": ["PlanetCarrierSettings"],
        "_private.system_model.part_model._2531": ["PointLoad"],
        "_private.system_model.part_model._2532": ["PowerLoad"],
        "_private.system_model.part_model._2533": ["RadialInternalClearanceTolerance"],
        "_private.system_model.part_model._2534": ["RollingBearingElementLoadCase"],
        "_private.system_model.part_model._2535": ["RootAssembly"],
        "_private.system_model.part_model._2536": [
            "ShaftDiameterModificationDueToRollingBearingRing"
        ],
        "_private.system_model.part_model._2537": ["SpecialisedAssembly"],
        "_private.system_model.part_model._2538": ["UnbalancedMass"],
        "_private.system_model.part_model._2539": ["UnbalancedMassInclusionOption"],
        "_private.system_model.part_model._2540": ["VirtualComponent"],
        "_private.system_model.part_model._2541": ["WindTurbineBladeModeDetails"],
        "_private.system_model.part_model._2542": ["WindTurbineSingleBladeDetails"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "Assembly",
    "AbstractAssembly",
    "AbstractShaft",
    "AbstractShaftOrHousing",
    "AGMALoadSharingTableApplicationLevel",
    "AxialInternalClearanceTolerance",
    "Bearing",
    "BearingF0InputMethod",
    "BearingRaceMountingOptions",
    "Bolt",
    "BoltedJoint",
    "Component",
    "ComponentsConnectedResult",
    "ConnectedSockets",
    "Connector",
    "Datum",
    "ElectricMachineSearchRegionSpecificationMethod",
    "EnginePartLoad",
    "EngineSpeed",
    "ExternalCADModel",
    "FEPart",
    "FlexiblePinAssembly",
    "GuideDxfModel",
    "GuideImage",
    "GuideModelUsage",
    "InnerBearingRaceMountingOptions",
    "InternalClearanceTolerance",
    "LoadSharingModes",
    "LoadSharingSettings",
    "MassDisc",
    "MeasurementComponent",
    "Microphone",
    "MicrophoneArray",
    "MountableComponent",
    "OilLevelSpecification",
    "OilSeal",
    "OuterBearingRaceMountingOptions",
    "Part",
    "PlanetCarrier",
    "PlanetCarrierSettings",
    "PointLoad",
    "PowerLoad",
    "RadialInternalClearanceTolerance",
    "RollingBearingElementLoadCase",
    "RootAssembly",
    "ShaftDiameterModificationDueToRollingBearingRing",
    "SpecialisedAssembly",
    "UnbalancedMass",
    "UnbalancedMassInclusionOption",
    "VirtualComponent",
    "WindTurbineBladeModeDetails",
    "WindTurbineSingleBladeDetails",
)
