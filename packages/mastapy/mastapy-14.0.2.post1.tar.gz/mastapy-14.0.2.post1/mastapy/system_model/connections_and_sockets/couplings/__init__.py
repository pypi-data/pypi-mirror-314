"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.connections_and_sockets.couplings._2399 import (
        ClutchConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2400 import (
        ClutchSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2401 import (
        ConceptCouplingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2402 import (
        ConceptCouplingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2403 import (
        CouplingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2404 import (
        CouplingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2405 import (
        PartToPartShearCouplingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2406 import (
        PartToPartShearCouplingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2407 import (
        SpringDamperConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2408 import (
        SpringDamperSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2409 import (
        TorqueConverterConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2410 import (
        TorqueConverterPumpSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2411 import (
        TorqueConverterTurbineSocket,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.connections_and_sockets.couplings._2399": [
            "ClutchConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2400": [
            "ClutchSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2401": [
            "ConceptCouplingConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2402": [
            "ConceptCouplingSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2403": [
            "CouplingConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2404": [
            "CouplingSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2405": [
            "PartToPartShearCouplingConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2406": [
            "PartToPartShearCouplingSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2407": [
            "SpringDamperConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2408": [
            "SpringDamperSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2409": [
            "TorqueConverterConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2410": [
            "TorqueConverterPumpSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2411": [
            "TorqueConverterTurbineSocket"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ClutchConnection",
    "ClutchSocket",
    "ConceptCouplingConnection",
    "ConceptCouplingSocket",
    "CouplingConnection",
    "CouplingSocket",
    "PartToPartShearCouplingConnection",
    "PartToPartShearCouplingSocket",
    "SpringDamperConnection",
    "SpringDamperSocket",
    "TorqueConverterConnection",
    "TorqueConverterPumpSocket",
    "TorqueConverterTurbineSocket",
)
