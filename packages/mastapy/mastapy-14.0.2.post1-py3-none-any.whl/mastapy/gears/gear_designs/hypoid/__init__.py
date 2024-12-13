"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.hypoid._1011 import HypoidGearDesign
    from mastapy._private.gears.gear_designs.hypoid._1012 import HypoidGearMeshDesign
    from mastapy._private.gears.gear_designs.hypoid._1013 import HypoidGearSetDesign
    from mastapy._private.gears.gear_designs.hypoid._1014 import HypoidMeshedGearDesign
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.hypoid._1011": ["HypoidGearDesign"],
        "_private.gears.gear_designs.hypoid._1012": ["HypoidGearMeshDesign"],
        "_private.gears.gear_designs.hypoid._1013": ["HypoidGearSetDesign"],
        "_private.gears.gear_designs.hypoid._1014": ["HypoidMeshedGearDesign"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "HypoidGearDesign",
    "HypoidGearMeshDesign",
    "HypoidGearSetDesign",
    "HypoidMeshedGearDesign",
)
