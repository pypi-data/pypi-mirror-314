"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.load_case.cylindrical._907 import (
        CylindricalGearLoadCase,
    )
    from mastapy._private.gears.load_case.cylindrical._908 import (
        CylindricalGearSetLoadCase,
    )
    from mastapy._private.gears.load_case.cylindrical._909 import (
        CylindricalMeshLoadCase,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.load_case.cylindrical._907": ["CylindricalGearLoadCase"],
        "_private.gears.load_case.cylindrical._908": ["CylindricalGearSetLoadCase"],
        "_private.gears.load_case.cylindrical._909": ["CylindricalMeshLoadCase"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CylindricalGearLoadCase",
    "CylindricalGearSetLoadCase",
    "CylindricalMeshLoadCase",
)
