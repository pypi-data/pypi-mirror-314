"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.manufacturing.bevel.cutters._838 import (
        PinionFinishCutter,
    )
    from mastapy._private.gears.manufacturing.bevel.cutters._839 import (
        PinionRoughCutter,
    )
    from mastapy._private.gears.manufacturing.bevel.cutters._840 import (
        WheelFinishCutter,
    )
    from mastapy._private.gears.manufacturing.bevel.cutters._841 import WheelRoughCutter
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.manufacturing.bevel.cutters._838": ["PinionFinishCutter"],
        "_private.gears.manufacturing.bevel.cutters._839": ["PinionRoughCutter"],
        "_private.gears.manufacturing.bevel.cutters._840": ["WheelFinishCutter"],
        "_private.gears.manufacturing.bevel.cutters._841": ["WheelRoughCutter"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "PinionFinishCutter",
    "PinionRoughCutter",
    "WheelFinishCutter",
    "WheelRoughCutter",
)
