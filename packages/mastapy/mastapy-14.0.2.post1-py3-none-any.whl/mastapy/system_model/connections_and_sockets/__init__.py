"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.connections_and_sockets._2322 import (
        AbstractShaftToMountableComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2323 import (
        BearingInnerSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2324 import (
        BearingOuterSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2325 import (
        BeltConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2326 import (
        CoaxialConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2327 import (
        ComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2328 import (
        ComponentMeasurer,
    )
    from mastapy._private.system_model.connections_and_sockets._2329 import Connection
    from mastapy._private.system_model.connections_and_sockets._2330 import (
        CVTBeltConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2331 import (
        CVTPulleySocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2332 import (
        CylindricalComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2333 import (
        CylindricalSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2334 import (
        DatumMeasurement,
    )
    from mastapy._private.system_model.connections_and_sockets._2335 import (
        ElectricMachineStatorSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2336 import (
        InnerShaftSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2337 import (
        InnerShaftSocketBase,
    )
    from mastapy._private.system_model.connections_and_sockets._2338 import (
        InterMountableComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2339 import (
        MountableComponentInnerSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2340 import (
        MountableComponentOuterSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2341 import (
        MountableComponentSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2342 import (
        OuterShaftSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2343 import (
        OuterShaftSocketBase,
    )
    from mastapy._private.system_model.connections_and_sockets._2344 import (
        PlanetaryConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2345 import (
        PlanetarySocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2346 import (
        PlanetarySocketBase,
    )
    from mastapy._private.system_model.connections_and_sockets._2347 import PulleySocket
    from mastapy._private.system_model.connections_and_sockets._2348 import (
        RealignmentResult,
    )
    from mastapy._private.system_model.connections_and_sockets._2349 import (
        RollingRingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2350 import (
        RollingRingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2351 import ShaftSocket
    from mastapy._private.system_model.connections_and_sockets._2352 import (
        ShaftToMountableComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2353 import Socket
    from mastapy._private.system_model.connections_and_sockets._2354 import (
        SocketConnectionOptions,
    )
    from mastapy._private.system_model.connections_and_sockets._2355 import (
        SocketConnectionSelection,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.connections_and_sockets._2322": [
            "AbstractShaftToMountableComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2323": ["BearingInnerSocket"],
        "_private.system_model.connections_and_sockets._2324": ["BearingOuterSocket"],
        "_private.system_model.connections_and_sockets._2325": ["BeltConnection"],
        "_private.system_model.connections_and_sockets._2326": ["CoaxialConnection"],
        "_private.system_model.connections_and_sockets._2327": ["ComponentConnection"],
        "_private.system_model.connections_and_sockets._2328": ["ComponentMeasurer"],
        "_private.system_model.connections_and_sockets._2329": ["Connection"],
        "_private.system_model.connections_and_sockets._2330": ["CVTBeltConnection"],
        "_private.system_model.connections_and_sockets._2331": ["CVTPulleySocket"],
        "_private.system_model.connections_and_sockets._2332": [
            "CylindricalComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2333": ["CylindricalSocket"],
        "_private.system_model.connections_and_sockets._2334": ["DatumMeasurement"],
        "_private.system_model.connections_and_sockets._2335": [
            "ElectricMachineStatorSocket"
        ],
        "_private.system_model.connections_and_sockets._2336": ["InnerShaftSocket"],
        "_private.system_model.connections_and_sockets._2337": ["InnerShaftSocketBase"],
        "_private.system_model.connections_and_sockets._2338": [
            "InterMountableComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2339": [
            "MountableComponentInnerSocket"
        ],
        "_private.system_model.connections_and_sockets._2340": [
            "MountableComponentOuterSocket"
        ],
        "_private.system_model.connections_and_sockets._2341": [
            "MountableComponentSocket"
        ],
        "_private.system_model.connections_and_sockets._2342": ["OuterShaftSocket"],
        "_private.system_model.connections_and_sockets._2343": ["OuterShaftSocketBase"],
        "_private.system_model.connections_and_sockets._2344": ["PlanetaryConnection"],
        "_private.system_model.connections_and_sockets._2345": ["PlanetarySocket"],
        "_private.system_model.connections_and_sockets._2346": ["PlanetarySocketBase"],
        "_private.system_model.connections_and_sockets._2347": ["PulleySocket"],
        "_private.system_model.connections_and_sockets._2348": ["RealignmentResult"],
        "_private.system_model.connections_and_sockets._2349": [
            "RollingRingConnection"
        ],
        "_private.system_model.connections_and_sockets._2350": ["RollingRingSocket"],
        "_private.system_model.connections_and_sockets._2351": ["ShaftSocket"],
        "_private.system_model.connections_and_sockets._2352": [
            "ShaftToMountableComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2353": ["Socket"],
        "_private.system_model.connections_and_sockets._2354": [
            "SocketConnectionOptions"
        ],
        "_private.system_model.connections_and_sockets._2355": [
            "SocketConnectionSelection"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractShaftToMountableComponentConnection",
    "BearingInnerSocket",
    "BearingOuterSocket",
    "BeltConnection",
    "CoaxialConnection",
    "ComponentConnection",
    "ComponentMeasurer",
    "Connection",
    "CVTBeltConnection",
    "CVTPulleySocket",
    "CylindricalComponentConnection",
    "CylindricalSocket",
    "DatumMeasurement",
    "ElectricMachineStatorSocket",
    "InnerShaftSocket",
    "InnerShaftSocketBase",
    "InterMountableComponentConnection",
    "MountableComponentInnerSocket",
    "MountableComponentOuterSocket",
    "MountableComponentSocket",
    "OuterShaftSocket",
    "OuterShaftSocketBase",
    "PlanetaryConnection",
    "PlanetarySocket",
    "PlanetarySocketBase",
    "PulleySocket",
    "RealignmentResult",
    "RollingRingConnection",
    "RollingRingSocket",
    "ShaftSocket",
    "ShaftToMountableComponentConnection",
    "Socket",
    "SocketConnectionOptions",
    "SocketConnectionSelection",
)
