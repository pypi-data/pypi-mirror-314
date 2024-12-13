"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.klingelnberg_hypoid._1003 import (
        KlingelnbergCycloPalloidHypoidGearDesign,
    )
    from mastapy._private.gears.gear_designs.klingelnberg_hypoid._1004 import (
        KlingelnbergCycloPalloidHypoidGearMeshDesign,
    )
    from mastapy._private.gears.gear_designs.klingelnberg_hypoid._1005 import (
        KlingelnbergCycloPalloidHypoidGearSetDesign,
    )
    from mastapy._private.gears.gear_designs.klingelnberg_hypoid._1006 import (
        KlingelnbergCycloPalloidHypoidMeshedGearDesign,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.klingelnberg_hypoid._1003": [
            "KlingelnbergCycloPalloidHypoidGearDesign"
        ],
        "_private.gears.gear_designs.klingelnberg_hypoid._1004": [
            "KlingelnbergCycloPalloidHypoidGearMeshDesign"
        ],
        "_private.gears.gear_designs.klingelnberg_hypoid._1005": [
            "KlingelnbergCycloPalloidHypoidGearSetDesign"
        ],
        "_private.gears.gear_designs.klingelnberg_hypoid._1006": [
            "KlingelnbergCycloPalloidHypoidMeshedGearDesign"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "KlingelnbergCycloPalloidHypoidGearDesign",
    "KlingelnbergCycloPalloidHypoidGearMeshDesign",
    "KlingelnbergCycloPalloidHypoidGearSetDesign",
    "KlingelnbergCycloPalloidHypoidMeshedGearDesign",
)
