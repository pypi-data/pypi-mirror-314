"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.fe_model._1237 import GearFEModel
    from mastapy._private.gears.fe_model._1238 import GearMeshFEModel
    from mastapy._private.gears.fe_model._1239 import GearMeshingElementOptions
    from mastapy._private.gears.fe_model._1240 import GearSetFEModel
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.fe_model._1237": ["GearFEModel"],
        "_private.gears.fe_model._1238": ["GearMeshFEModel"],
        "_private.gears.fe_model._1239": ["GearMeshingElementOptions"],
        "_private.gears.fe_model._1240": ["GearSetFEModel"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "GearFEModel",
    "GearMeshFEModel",
    "GearMeshingElementOptions",
    "GearSetFEModel",
)
