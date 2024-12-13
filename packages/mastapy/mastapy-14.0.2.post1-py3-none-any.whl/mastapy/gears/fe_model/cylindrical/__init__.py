"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.fe_model.cylindrical._1241 import CylindricalGearFEModel
    from mastapy._private.gears.fe_model.cylindrical._1242 import (
        CylindricalGearMeshFEModel,
    )
    from mastapy._private.gears.fe_model.cylindrical._1243 import (
        CylindricalGearSetFEModel,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.fe_model.cylindrical._1241": ["CylindricalGearFEModel"],
        "_private.gears.fe_model.cylindrical._1242": ["CylindricalGearMeshFEModel"],
        "_private.gears.fe_model.cylindrical._1243": ["CylindricalGearSetFEModel"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CylindricalGearFEModel",
    "CylindricalGearMeshFEModel",
    "CylindricalGearSetFEModel",
)
