"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.fe.links._2476 import FELink
    from mastapy._private.system_model.fe.links._2477 import ElectricMachineStatorFELink
    from mastapy._private.system_model.fe.links._2478 import FELinkWithSelection
    from mastapy._private.system_model.fe.links._2479 import GearMeshFELink
    from mastapy._private.system_model.fe.links._2480 import (
        GearWithDuplicatedMeshesFELink,
    )
    from mastapy._private.system_model.fe.links._2481 import MultiAngleConnectionFELink
    from mastapy._private.system_model.fe.links._2482 import MultiNodeConnectorFELink
    from mastapy._private.system_model.fe.links._2483 import MultiNodeFELink
    from mastapy._private.system_model.fe.links._2484 import (
        PlanetaryConnectorMultiNodeFELink,
    )
    from mastapy._private.system_model.fe.links._2485 import PlanetBasedFELink
    from mastapy._private.system_model.fe.links._2486 import PlanetCarrierFELink
    from mastapy._private.system_model.fe.links._2487 import PointLoadFELink
    from mastapy._private.system_model.fe.links._2488 import RollingRingConnectionFELink
    from mastapy._private.system_model.fe.links._2489 import ShaftHubConnectionFELink
    from mastapy._private.system_model.fe.links._2490 import SingleNodeFELink
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.fe.links._2476": ["FELink"],
        "_private.system_model.fe.links._2477": ["ElectricMachineStatorFELink"],
        "_private.system_model.fe.links._2478": ["FELinkWithSelection"],
        "_private.system_model.fe.links._2479": ["GearMeshFELink"],
        "_private.system_model.fe.links._2480": ["GearWithDuplicatedMeshesFELink"],
        "_private.system_model.fe.links._2481": ["MultiAngleConnectionFELink"],
        "_private.system_model.fe.links._2482": ["MultiNodeConnectorFELink"],
        "_private.system_model.fe.links._2483": ["MultiNodeFELink"],
        "_private.system_model.fe.links._2484": ["PlanetaryConnectorMultiNodeFELink"],
        "_private.system_model.fe.links._2485": ["PlanetBasedFELink"],
        "_private.system_model.fe.links._2486": ["PlanetCarrierFELink"],
        "_private.system_model.fe.links._2487": ["PointLoadFELink"],
        "_private.system_model.fe.links._2488": ["RollingRingConnectionFELink"],
        "_private.system_model.fe.links._2489": ["ShaftHubConnectionFELink"],
        "_private.system_model.fe.links._2490": ["SingleNodeFELink"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "FELink",
    "ElectricMachineStatorFELink",
    "FELinkWithSelection",
    "GearMeshFELink",
    "GearWithDuplicatedMeshesFELink",
    "MultiAngleConnectionFELink",
    "MultiNodeConnectorFELink",
    "MultiNodeFELink",
    "PlanetaryConnectorMultiNodeFELink",
    "PlanetBasedFELink",
    "PlanetCarrierFELink",
    "PointLoadFELink",
    "RollingRingConnectionFELink",
    "ShaftHubConnectionFELink",
    "SingleNodeFELink",
)
