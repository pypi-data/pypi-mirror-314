"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.fe._2412 import AlignConnectedComponentOptions
    from mastapy._private.system_model.fe._2413 import AlignmentMethod
    from mastapy._private.system_model.fe._2414 import AlignmentMethodForRaceBearing
    from mastapy._private.system_model.fe._2415 import AlignmentUsingAxialNodePositions
    from mastapy._private.system_model.fe._2416 import AngleSource
    from mastapy._private.system_model.fe._2417 import BaseFEWithSelection
    from mastapy._private.system_model.fe._2418 import BatchOperations
    from mastapy._private.system_model.fe._2419 import BearingNodeAlignmentOption
    from mastapy._private.system_model.fe._2420 import BearingNodeOption
    from mastapy._private.system_model.fe._2421 import BearingRaceNodeLink
    from mastapy._private.system_model.fe._2422 import BearingRacePosition
    from mastapy._private.system_model.fe._2423 import ComponentOrientationOption
    from mastapy._private.system_model.fe._2424 import ContactPairWithSelection
    from mastapy._private.system_model.fe._2425 import CoordinateSystemWithSelection
    from mastapy._private.system_model.fe._2426 import CreateConnectedComponentOptions
    from mastapy._private.system_model.fe._2427 import (
        CreateMicrophoneNormalToSurfaceOptions,
    )
    from mastapy._private.system_model.fe._2428 import DegreeOfFreedomBoundaryCondition
    from mastapy._private.system_model.fe._2429 import (
        DegreeOfFreedomBoundaryConditionAngular,
    )
    from mastapy._private.system_model.fe._2430 import (
        DegreeOfFreedomBoundaryConditionLinear,
    )
    from mastapy._private.system_model.fe._2431 import ElectricMachineDataSet
    from mastapy._private.system_model.fe._2432 import ElectricMachineDynamicLoadData
    from mastapy._private.system_model.fe._2433 import ElementFaceGroupWithSelection
    from mastapy._private.system_model.fe._2434 import ElementPropertiesWithSelection
    from mastapy._private.system_model.fe._2435 import FEEntityGroupWithSelection
    from mastapy._private.system_model.fe._2436 import FEExportSettings
    from mastapy._private.system_model.fe._2437 import FEPartDRIVASurfaceSelection
    from mastapy._private.system_model.fe._2438 import FEPartWithBatchOptions
    from mastapy._private.system_model.fe._2439 import FEStiffnessGeometry
    from mastapy._private.system_model.fe._2440 import FEStiffnessTester
    from mastapy._private.system_model.fe._2441 import FESubstructure
    from mastapy._private.system_model.fe._2442 import FESubstructureExportOptions
    from mastapy._private.system_model.fe._2443 import FESubstructureNode
    from mastapy._private.system_model.fe._2444 import FESubstructureNodeModeShape
    from mastapy._private.system_model.fe._2445 import FESubstructureNodeModeShapes
    from mastapy._private.system_model.fe._2446 import FESubstructureType
    from mastapy._private.system_model.fe._2447 import FESubstructureWithBatchOptions
    from mastapy._private.system_model.fe._2448 import FESubstructureWithSelection
    from mastapy._private.system_model.fe._2449 import (
        FESubstructureWithSelectionComponents,
    )
    from mastapy._private.system_model.fe._2450 import (
        FESubstructureWithSelectionForHarmonicAnalysis,
    )
    from mastapy._private.system_model.fe._2451 import (
        FESubstructureWithSelectionForModalAnalysis,
    )
    from mastapy._private.system_model.fe._2452 import (
        FESubstructureWithSelectionForStaticAnalysis,
    )
    from mastapy._private.system_model.fe._2453 import GearMeshingOptions
    from mastapy._private.system_model.fe._2454 import (
        IndependentMASTACreatedCondensationNode,
    )
    from mastapy._private.system_model.fe._2455 import (
        LinkComponentAxialPositionErrorReporter,
    )
    from mastapy._private.system_model.fe._2456 import LinkNodeSource
    from mastapy._private.system_model.fe._2457 import MaterialPropertiesWithSelection
    from mastapy._private.system_model.fe._2458 import (
        NodeBoundaryConditionStaticAnalysis,
    )
    from mastapy._private.system_model.fe._2459 import NodeGroupWithSelection
    from mastapy._private.system_model.fe._2460 import NodeSelectionDepthOption
    from mastapy._private.system_model.fe._2461 import (
        OptionsWhenExternalFEFileAlreadyExists,
    )
    from mastapy._private.system_model.fe._2462 import PerLinkExportOptions
    from mastapy._private.system_model.fe._2463 import PerNodeExportOptions
    from mastapy._private.system_model.fe._2464 import RaceBearingFE
    from mastapy._private.system_model.fe._2465 import RaceBearingFESystemDeflection
    from mastapy._private.system_model.fe._2466 import RaceBearingFEWithSelection
    from mastapy._private.system_model.fe._2467 import ReplacedShaftSelectionHelper
    from mastapy._private.system_model.fe._2468 import SystemDeflectionFEExportOptions
    from mastapy._private.system_model.fe._2469 import ThermalExpansionOption
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.fe._2412": ["AlignConnectedComponentOptions"],
        "_private.system_model.fe._2413": ["AlignmentMethod"],
        "_private.system_model.fe._2414": ["AlignmentMethodForRaceBearing"],
        "_private.system_model.fe._2415": ["AlignmentUsingAxialNodePositions"],
        "_private.system_model.fe._2416": ["AngleSource"],
        "_private.system_model.fe._2417": ["BaseFEWithSelection"],
        "_private.system_model.fe._2418": ["BatchOperations"],
        "_private.system_model.fe._2419": ["BearingNodeAlignmentOption"],
        "_private.system_model.fe._2420": ["BearingNodeOption"],
        "_private.system_model.fe._2421": ["BearingRaceNodeLink"],
        "_private.system_model.fe._2422": ["BearingRacePosition"],
        "_private.system_model.fe._2423": ["ComponentOrientationOption"],
        "_private.system_model.fe._2424": ["ContactPairWithSelection"],
        "_private.system_model.fe._2425": ["CoordinateSystemWithSelection"],
        "_private.system_model.fe._2426": ["CreateConnectedComponentOptions"],
        "_private.system_model.fe._2427": ["CreateMicrophoneNormalToSurfaceOptions"],
        "_private.system_model.fe._2428": ["DegreeOfFreedomBoundaryCondition"],
        "_private.system_model.fe._2429": ["DegreeOfFreedomBoundaryConditionAngular"],
        "_private.system_model.fe._2430": ["DegreeOfFreedomBoundaryConditionLinear"],
        "_private.system_model.fe._2431": ["ElectricMachineDataSet"],
        "_private.system_model.fe._2432": ["ElectricMachineDynamicLoadData"],
        "_private.system_model.fe._2433": ["ElementFaceGroupWithSelection"],
        "_private.system_model.fe._2434": ["ElementPropertiesWithSelection"],
        "_private.system_model.fe._2435": ["FEEntityGroupWithSelection"],
        "_private.system_model.fe._2436": ["FEExportSettings"],
        "_private.system_model.fe._2437": ["FEPartDRIVASurfaceSelection"],
        "_private.system_model.fe._2438": ["FEPartWithBatchOptions"],
        "_private.system_model.fe._2439": ["FEStiffnessGeometry"],
        "_private.system_model.fe._2440": ["FEStiffnessTester"],
        "_private.system_model.fe._2441": ["FESubstructure"],
        "_private.system_model.fe._2442": ["FESubstructureExportOptions"],
        "_private.system_model.fe._2443": ["FESubstructureNode"],
        "_private.system_model.fe._2444": ["FESubstructureNodeModeShape"],
        "_private.system_model.fe._2445": ["FESubstructureNodeModeShapes"],
        "_private.system_model.fe._2446": ["FESubstructureType"],
        "_private.system_model.fe._2447": ["FESubstructureWithBatchOptions"],
        "_private.system_model.fe._2448": ["FESubstructureWithSelection"],
        "_private.system_model.fe._2449": ["FESubstructureWithSelectionComponents"],
        "_private.system_model.fe._2450": [
            "FESubstructureWithSelectionForHarmonicAnalysis"
        ],
        "_private.system_model.fe._2451": [
            "FESubstructureWithSelectionForModalAnalysis"
        ],
        "_private.system_model.fe._2452": [
            "FESubstructureWithSelectionForStaticAnalysis"
        ],
        "_private.system_model.fe._2453": ["GearMeshingOptions"],
        "_private.system_model.fe._2454": ["IndependentMASTACreatedCondensationNode"],
        "_private.system_model.fe._2455": ["LinkComponentAxialPositionErrorReporter"],
        "_private.system_model.fe._2456": ["LinkNodeSource"],
        "_private.system_model.fe._2457": ["MaterialPropertiesWithSelection"],
        "_private.system_model.fe._2458": ["NodeBoundaryConditionStaticAnalysis"],
        "_private.system_model.fe._2459": ["NodeGroupWithSelection"],
        "_private.system_model.fe._2460": ["NodeSelectionDepthOption"],
        "_private.system_model.fe._2461": ["OptionsWhenExternalFEFileAlreadyExists"],
        "_private.system_model.fe._2462": ["PerLinkExportOptions"],
        "_private.system_model.fe._2463": ["PerNodeExportOptions"],
        "_private.system_model.fe._2464": ["RaceBearingFE"],
        "_private.system_model.fe._2465": ["RaceBearingFESystemDeflection"],
        "_private.system_model.fe._2466": ["RaceBearingFEWithSelection"],
        "_private.system_model.fe._2467": ["ReplacedShaftSelectionHelper"],
        "_private.system_model.fe._2468": ["SystemDeflectionFEExportOptions"],
        "_private.system_model.fe._2469": ["ThermalExpansionOption"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AlignConnectedComponentOptions",
    "AlignmentMethod",
    "AlignmentMethodForRaceBearing",
    "AlignmentUsingAxialNodePositions",
    "AngleSource",
    "BaseFEWithSelection",
    "BatchOperations",
    "BearingNodeAlignmentOption",
    "BearingNodeOption",
    "BearingRaceNodeLink",
    "BearingRacePosition",
    "ComponentOrientationOption",
    "ContactPairWithSelection",
    "CoordinateSystemWithSelection",
    "CreateConnectedComponentOptions",
    "CreateMicrophoneNormalToSurfaceOptions",
    "DegreeOfFreedomBoundaryCondition",
    "DegreeOfFreedomBoundaryConditionAngular",
    "DegreeOfFreedomBoundaryConditionLinear",
    "ElectricMachineDataSet",
    "ElectricMachineDynamicLoadData",
    "ElementFaceGroupWithSelection",
    "ElementPropertiesWithSelection",
    "FEEntityGroupWithSelection",
    "FEExportSettings",
    "FEPartDRIVASurfaceSelection",
    "FEPartWithBatchOptions",
    "FEStiffnessGeometry",
    "FEStiffnessTester",
    "FESubstructure",
    "FESubstructureExportOptions",
    "FESubstructureNode",
    "FESubstructureNodeModeShape",
    "FESubstructureNodeModeShapes",
    "FESubstructureType",
    "FESubstructureWithBatchOptions",
    "FESubstructureWithSelection",
    "FESubstructureWithSelectionComponents",
    "FESubstructureWithSelectionForHarmonicAnalysis",
    "FESubstructureWithSelectionForModalAnalysis",
    "FESubstructureWithSelectionForStaticAnalysis",
    "GearMeshingOptions",
    "IndependentMASTACreatedCondensationNode",
    "LinkComponentAxialPositionErrorReporter",
    "LinkNodeSource",
    "MaterialPropertiesWithSelection",
    "NodeBoundaryConditionStaticAnalysis",
    "NodeGroupWithSelection",
    "NodeSelectionDepthOption",
    "OptionsWhenExternalFEFileAlreadyExists",
    "PerLinkExportOptions",
    "PerNodeExportOptions",
    "RaceBearingFE",
    "RaceBearingFESystemDeflection",
    "RaceBearingFEWithSelection",
    "ReplacedShaftSelectionHelper",
    "SystemDeflectionFEExportOptions",
    "ThermalExpansionOption",
)
