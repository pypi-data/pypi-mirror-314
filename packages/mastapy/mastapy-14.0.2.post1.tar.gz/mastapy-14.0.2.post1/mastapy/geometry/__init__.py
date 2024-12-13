"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.geometry._318 import ClippingPlane
    from mastapy._private.geometry._319 import DrawStyle
    from mastapy._private.geometry._320 import DrawStyleBase
    from mastapy._private.geometry._321 import PackagingLimits
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.geometry._318": ["ClippingPlane"],
        "_private.geometry._319": ["DrawStyle"],
        "_private.geometry._320": ["DrawStyleBase"],
        "_private.geometry._321": ["PackagingLimits"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ClippingPlane",
    "DrawStyle",
    "DrawStyleBase",
    "PackagingLimits",
)
