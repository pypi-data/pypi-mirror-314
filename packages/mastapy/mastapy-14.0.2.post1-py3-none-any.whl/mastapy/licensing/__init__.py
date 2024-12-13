"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.licensing._1538 import LicenceServer
    from mastapy._private.licensing._7746 import LicenceServerDetails
    from mastapy._private.licensing._7747 import ModuleDetails
    from mastapy._private.licensing._7748 import ModuleLicenceStatus
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.licensing._1538": ["LicenceServer"],
        "_private.licensing._7746": ["LicenceServerDetails"],
        "_private.licensing._7747": ["ModuleDetails"],
        "_private.licensing._7748": ["ModuleLicenceStatus"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "LicenceServer",
    "LicenceServerDetails",
    "ModuleDetails",
    "ModuleLicenceStatus",
)
