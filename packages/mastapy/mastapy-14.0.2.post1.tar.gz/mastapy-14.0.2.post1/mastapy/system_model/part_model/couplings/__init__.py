"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.couplings._2638 import BeltDrive
    from mastapy._private.system_model.part_model.couplings._2639 import BeltDriveType
    from mastapy._private.system_model.part_model.couplings._2640 import Clutch
    from mastapy._private.system_model.part_model.couplings._2641 import ClutchHalf
    from mastapy._private.system_model.part_model.couplings._2642 import ClutchType
    from mastapy._private.system_model.part_model.couplings._2643 import ConceptCoupling
    from mastapy._private.system_model.part_model.couplings._2644 import (
        ConceptCouplingHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2645 import (
        ConceptCouplingHalfPositioning,
    )
    from mastapy._private.system_model.part_model.couplings._2646 import Coupling
    from mastapy._private.system_model.part_model.couplings._2647 import CouplingHalf
    from mastapy._private.system_model.part_model.couplings._2648 import (
        CrowningSpecification,
    )
    from mastapy._private.system_model.part_model.couplings._2649 import CVT
    from mastapy._private.system_model.part_model.couplings._2650 import CVTPulley
    from mastapy._private.system_model.part_model.couplings._2651 import (
        PartToPartShearCoupling,
    )
    from mastapy._private.system_model.part_model.couplings._2652 import (
        PartToPartShearCouplingHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2653 import (
        PitchErrorFlankOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2654 import Pulley
    from mastapy._private.system_model.part_model.couplings._2655 import (
        RigidConnectorStiffnessType,
    )
    from mastapy._private.system_model.part_model.couplings._2656 import (
        RigidConnectorTiltStiffnessTypes,
    )
    from mastapy._private.system_model.part_model.couplings._2657 import (
        RigidConnectorToothLocation,
    )
    from mastapy._private.system_model.part_model.couplings._2658 import (
        RigidConnectorToothSpacingType,
    )
    from mastapy._private.system_model.part_model.couplings._2659 import (
        RigidConnectorTypes,
    )
    from mastapy._private.system_model.part_model.couplings._2660 import RollingRing
    from mastapy._private.system_model.part_model.couplings._2661 import (
        RollingRingAssembly,
    )
    from mastapy._private.system_model.part_model.couplings._2662 import (
        ShaftHubConnection,
    )
    from mastapy._private.system_model.part_model.couplings._2663 import (
        SplineFitOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2664 import (
        SplineLeadRelief,
    )
    from mastapy._private.system_model.part_model.couplings._2665 import (
        SplinePitchErrorInputType,
    )
    from mastapy._private.system_model.part_model.couplings._2666 import (
        SplinePitchErrorOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2667 import SpringDamper
    from mastapy._private.system_model.part_model.couplings._2668 import (
        SpringDamperHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2669 import Synchroniser
    from mastapy._private.system_model.part_model.couplings._2670 import (
        SynchroniserCone,
    )
    from mastapy._private.system_model.part_model.couplings._2671 import (
        SynchroniserHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2672 import (
        SynchroniserPart,
    )
    from mastapy._private.system_model.part_model.couplings._2673 import (
        SynchroniserSleeve,
    )
    from mastapy._private.system_model.part_model.couplings._2674 import TorqueConverter
    from mastapy._private.system_model.part_model.couplings._2675 import (
        TorqueConverterPump,
    )
    from mastapy._private.system_model.part_model.couplings._2676 import (
        TorqueConverterSpeedRatio,
    )
    from mastapy._private.system_model.part_model.couplings._2677 import (
        TorqueConverterTurbine,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.couplings._2638": ["BeltDrive"],
        "_private.system_model.part_model.couplings._2639": ["BeltDriveType"],
        "_private.system_model.part_model.couplings._2640": ["Clutch"],
        "_private.system_model.part_model.couplings._2641": ["ClutchHalf"],
        "_private.system_model.part_model.couplings._2642": ["ClutchType"],
        "_private.system_model.part_model.couplings._2643": ["ConceptCoupling"],
        "_private.system_model.part_model.couplings._2644": ["ConceptCouplingHalf"],
        "_private.system_model.part_model.couplings._2645": [
            "ConceptCouplingHalfPositioning"
        ],
        "_private.system_model.part_model.couplings._2646": ["Coupling"],
        "_private.system_model.part_model.couplings._2647": ["CouplingHalf"],
        "_private.system_model.part_model.couplings._2648": ["CrowningSpecification"],
        "_private.system_model.part_model.couplings._2649": ["CVT"],
        "_private.system_model.part_model.couplings._2650": ["CVTPulley"],
        "_private.system_model.part_model.couplings._2651": ["PartToPartShearCoupling"],
        "_private.system_model.part_model.couplings._2652": [
            "PartToPartShearCouplingHalf"
        ],
        "_private.system_model.part_model.couplings._2653": ["PitchErrorFlankOptions"],
        "_private.system_model.part_model.couplings._2654": ["Pulley"],
        "_private.system_model.part_model.couplings._2655": [
            "RigidConnectorStiffnessType"
        ],
        "_private.system_model.part_model.couplings._2656": [
            "RigidConnectorTiltStiffnessTypes"
        ],
        "_private.system_model.part_model.couplings._2657": [
            "RigidConnectorToothLocation"
        ],
        "_private.system_model.part_model.couplings._2658": [
            "RigidConnectorToothSpacingType"
        ],
        "_private.system_model.part_model.couplings._2659": ["RigidConnectorTypes"],
        "_private.system_model.part_model.couplings._2660": ["RollingRing"],
        "_private.system_model.part_model.couplings._2661": ["RollingRingAssembly"],
        "_private.system_model.part_model.couplings._2662": ["ShaftHubConnection"],
        "_private.system_model.part_model.couplings._2663": ["SplineFitOptions"],
        "_private.system_model.part_model.couplings._2664": ["SplineLeadRelief"],
        "_private.system_model.part_model.couplings._2665": [
            "SplinePitchErrorInputType"
        ],
        "_private.system_model.part_model.couplings._2666": ["SplinePitchErrorOptions"],
        "_private.system_model.part_model.couplings._2667": ["SpringDamper"],
        "_private.system_model.part_model.couplings._2668": ["SpringDamperHalf"],
        "_private.system_model.part_model.couplings._2669": ["Synchroniser"],
        "_private.system_model.part_model.couplings._2670": ["SynchroniserCone"],
        "_private.system_model.part_model.couplings._2671": ["SynchroniserHalf"],
        "_private.system_model.part_model.couplings._2672": ["SynchroniserPart"],
        "_private.system_model.part_model.couplings._2673": ["SynchroniserSleeve"],
        "_private.system_model.part_model.couplings._2674": ["TorqueConverter"],
        "_private.system_model.part_model.couplings._2675": ["TorqueConverterPump"],
        "_private.system_model.part_model.couplings._2676": [
            "TorqueConverterSpeedRatio"
        ],
        "_private.system_model.part_model.couplings._2677": ["TorqueConverterTurbine"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BeltDrive",
    "BeltDriveType",
    "Clutch",
    "ClutchHalf",
    "ClutchType",
    "ConceptCoupling",
    "ConceptCouplingHalf",
    "ConceptCouplingHalfPositioning",
    "Coupling",
    "CouplingHalf",
    "CrowningSpecification",
    "CVT",
    "CVTPulley",
    "PartToPartShearCoupling",
    "PartToPartShearCouplingHalf",
    "PitchErrorFlankOptions",
    "Pulley",
    "RigidConnectorStiffnessType",
    "RigidConnectorTiltStiffnessTypes",
    "RigidConnectorToothLocation",
    "RigidConnectorToothSpacingType",
    "RigidConnectorTypes",
    "RollingRing",
    "RollingRingAssembly",
    "ShaftHubConnection",
    "SplineFitOptions",
    "SplineLeadRelief",
    "SplinePitchErrorInputType",
    "SplinePitchErrorOptions",
    "SpringDamper",
    "SpringDamperHalf",
    "Synchroniser",
    "SynchroniserCone",
    "SynchroniserHalf",
    "SynchroniserPart",
    "SynchroniserSleeve",
    "TorqueConverter",
    "TorqueConverterPump",
    "TorqueConverterSpeedRatio",
    "TorqueConverterTurbine",
)
