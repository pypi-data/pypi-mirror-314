"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.modal_analysis.gears._1852 import GearMeshForTE
    from mastapy._private.utility.modal_analysis.gears._1853 import GearOrderForTE
    from mastapy._private.utility.modal_analysis.gears._1854 import GearPositions
    from mastapy._private.utility.modal_analysis.gears._1855 import HarmonicOrderForTE
    from mastapy._private.utility.modal_analysis.gears._1856 import LabelOnlyOrder
    from mastapy._private.utility.modal_analysis.gears._1857 import OrderForTE
    from mastapy._private.utility.modal_analysis.gears._1858 import OrderSelector
    from mastapy._private.utility.modal_analysis.gears._1859 import OrderWithRadius
    from mastapy._private.utility.modal_analysis.gears._1860 import RollingBearingOrder
    from mastapy._private.utility.modal_analysis.gears._1861 import ShaftOrderForTE
    from mastapy._private.utility.modal_analysis.gears._1862 import (
        UserDefinedOrderForTE,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.modal_analysis.gears._1852": ["GearMeshForTE"],
        "_private.utility.modal_analysis.gears._1853": ["GearOrderForTE"],
        "_private.utility.modal_analysis.gears._1854": ["GearPositions"],
        "_private.utility.modal_analysis.gears._1855": ["HarmonicOrderForTE"],
        "_private.utility.modal_analysis.gears._1856": ["LabelOnlyOrder"],
        "_private.utility.modal_analysis.gears._1857": ["OrderForTE"],
        "_private.utility.modal_analysis.gears._1858": ["OrderSelector"],
        "_private.utility.modal_analysis.gears._1859": ["OrderWithRadius"],
        "_private.utility.modal_analysis.gears._1860": ["RollingBearingOrder"],
        "_private.utility.modal_analysis.gears._1861": ["ShaftOrderForTE"],
        "_private.utility.modal_analysis.gears._1862": ["UserDefinedOrderForTE"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "GearMeshForTE",
    "GearOrderForTE",
    "GearPositions",
    "HarmonicOrderForTE",
    "LabelOnlyOrder",
    "OrderForTE",
    "OrderSelector",
    "OrderWithRadius",
    "RollingBearingOrder",
    "ShaftOrderForTE",
    "UserDefinedOrderForTE",
)
