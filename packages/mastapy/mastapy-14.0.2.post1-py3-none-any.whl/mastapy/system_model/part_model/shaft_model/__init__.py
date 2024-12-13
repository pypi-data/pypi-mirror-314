"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.shaft_model._2543 import Shaft
    from mastapy._private.system_model.part_model.shaft_model._2544 import ShaftBow
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.shaft_model._2543": ["Shaft"],
        "_private.system_model.part_model.shaft_model._2544": ["ShaftBow"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "Shaft",
    "ShaftBow",
)
