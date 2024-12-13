"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.virtual_cylindrical_gears._391 import (
        BevelVirtualCylindricalGearISO10300MethodB2,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._392 import (
        BevelVirtualCylindricalGearSetISO10300MethodB1,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._393 import (
        BevelVirtualCylindricalGearSetISO10300MethodB2,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._394 import (
        HypoidVirtualCylindricalGearISO10300MethodB2,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._395 import (
        HypoidVirtualCylindricalGearSetISO10300MethodB1,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._396 import (
        HypoidVirtualCylindricalGearSetISO10300MethodB2,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._397 import (
        KlingelnbergHypoidVirtualCylindricalGear,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._398 import (
        KlingelnbergSpiralBevelVirtualCylindricalGear,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._399 import (
        KlingelnbergVirtualCylindricalGear,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._400 import (
        KlingelnbergVirtualCylindricalGearSet,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._401 import (
        VirtualCylindricalGear,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._402 import (
        VirtualCylindricalGearBasic,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._403 import (
        VirtualCylindricalGearISO10300MethodB1,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._404 import (
        VirtualCylindricalGearISO10300MethodB2,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._405 import (
        VirtualCylindricalGearSet,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._406 import (
        VirtualCylindricalGearSetISO10300MethodB1,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._407 import (
        VirtualCylindricalGearSetISO10300MethodB2,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.virtual_cylindrical_gears._391": [
            "BevelVirtualCylindricalGearISO10300MethodB2"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._392": [
            "BevelVirtualCylindricalGearSetISO10300MethodB1"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._393": [
            "BevelVirtualCylindricalGearSetISO10300MethodB2"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._394": [
            "HypoidVirtualCylindricalGearISO10300MethodB2"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._395": [
            "HypoidVirtualCylindricalGearSetISO10300MethodB1"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._396": [
            "HypoidVirtualCylindricalGearSetISO10300MethodB2"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._397": [
            "KlingelnbergHypoidVirtualCylindricalGear"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._398": [
            "KlingelnbergSpiralBevelVirtualCylindricalGear"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._399": [
            "KlingelnbergVirtualCylindricalGear"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._400": [
            "KlingelnbergVirtualCylindricalGearSet"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._401": [
            "VirtualCylindricalGear"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._402": [
            "VirtualCylindricalGearBasic"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._403": [
            "VirtualCylindricalGearISO10300MethodB1"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._404": [
            "VirtualCylindricalGearISO10300MethodB2"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._405": [
            "VirtualCylindricalGearSet"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._406": [
            "VirtualCylindricalGearSetISO10300MethodB1"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._407": [
            "VirtualCylindricalGearSetISO10300MethodB2"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BevelVirtualCylindricalGearISO10300MethodB2",
    "BevelVirtualCylindricalGearSetISO10300MethodB1",
    "BevelVirtualCylindricalGearSetISO10300MethodB2",
    "HypoidVirtualCylindricalGearISO10300MethodB2",
    "HypoidVirtualCylindricalGearSetISO10300MethodB1",
    "HypoidVirtualCylindricalGearSetISO10300MethodB2",
    "KlingelnbergHypoidVirtualCylindricalGear",
    "KlingelnbergSpiralBevelVirtualCylindricalGear",
    "KlingelnbergVirtualCylindricalGear",
    "KlingelnbergVirtualCylindricalGearSet",
    "VirtualCylindricalGear",
    "VirtualCylindricalGearBasic",
    "VirtualCylindricalGearISO10300MethodB1",
    "VirtualCylindricalGearISO10300MethodB2",
    "VirtualCylindricalGearSet",
    "VirtualCylindricalGearSetISO10300MethodB1",
    "VirtualCylindricalGearSetISO10300MethodB2",
)
