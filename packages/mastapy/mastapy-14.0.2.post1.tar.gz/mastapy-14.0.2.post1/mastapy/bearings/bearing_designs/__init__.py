"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bearings.bearing_designs._2186 import BearingDesign
    from mastapy._private.bearings.bearing_designs._2187 import DetailedBearing
    from mastapy._private.bearings.bearing_designs._2188 import DummyRollingBearing
    from mastapy._private.bearings.bearing_designs._2189 import LinearBearing
    from mastapy._private.bearings.bearing_designs._2190 import NonLinearBearing
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bearings.bearing_designs._2186": ["BearingDesign"],
        "_private.bearings.bearing_designs._2187": ["DetailedBearing"],
        "_private.bearings.bearing_designs._2188": ["DummyRollingBearing"],
        "_private.bearings.bearing_designs._2189": ["LinearBearing"],
        "_private.bearings.bearing_designs._2190": ["NonLinearBearing"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BearingDesign",
    "DetailedBearing",
    "DummyRollingBearing",
    "LinearBearing",
    "NonLinearBearing",
)
