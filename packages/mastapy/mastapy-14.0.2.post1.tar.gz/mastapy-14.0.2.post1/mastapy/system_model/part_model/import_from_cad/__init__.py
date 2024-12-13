"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.import_from_cad._2554 import (
        AbstractShaftFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2555 import (
        ClutchFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2556 import (
        ComponentFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2557 import (
        ConceptBearingFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2558 import (
        ConnectorFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2559 import (
        CylindricalGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2560 import (
        CylindricalGearInPlanetarySetFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2561 import (
        CylindricalPlanetGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2562 import (
        CylindricalRingGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2563 import (
        CylindricalSunGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2564 import (
        HousedOrMounted,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2565 import (
        MountableComponentFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2566 import (
        PlanetShaftFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2567 import (
        PulleyFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2568 import (
        RigidConnectorFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2569 import (
        RollingBearingFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2570 import (
        ShaftFromCAD,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.import_from_cad._2554": [
            "AbstractShaftFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2555": ["ClutchFromCAD"],
        "_private.system_model.part_model.import_from_cad._2556": ["ComponentFromCAD"],
        "_private.system_model.part_model.import_from_cad._2557": [
            "ConceptBearingFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2558": ["ConnectorFromCAD"],
        "_private.system_model.part_model.import_from_cad._2559": [
            "CylindricalGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2560": [
            "CylindricalGearInPlanetarySetFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2561": [
            "CylindricalPlanetGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2562": [
            "CylindricalRingGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2563": [
            "CylindricalSunGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2564": ["HousedOrMounted"],
        "_private.system_model.part_model.import_from_cad._2565": [
            "MountableComponentFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2566": [
            "PlanetShaftFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2567": ["PulleyFromCAD"],
        "_private.system_model.part_model.import_from_cad._2568": [
            "RigidConnectorFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2569": [
            "RollingBearingFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2570": ["ShaftFromCAD"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractShaftFromCAD",
    "ClutchFromCAD",
    "ComponentFromCAD",
    "ConceptBearingFromCAD",
    "ConnectorFromCAD",
    "CylindricalGearFromCAD",
    "CylindricalGearInPlanetarySetFromCAD",
    "CylindricalPlanetGearFromCAD",
    "CylindricalRingGearFromCAD",
    "CylindricalSunGearFromCAD",
    "HousedOrMounted",
    "MountableComponentFromCAD",
    "PlanetShaftFromCAD",
    "PulleyFromCAD",
    "RigidConnectorFromCAD",
    "RollingBearingFromCAD",
    "ShaftFromCAD",
)
