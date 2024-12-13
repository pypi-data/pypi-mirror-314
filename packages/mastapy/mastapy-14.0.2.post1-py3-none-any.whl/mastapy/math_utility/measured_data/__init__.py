"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.math_utility.measured_data._1615 import GriddedSurfaceAccessor
    from mastapy._private.math_utility.measured_data._1616 import LookupTableBase
    from mastapy._private.math_utility.measured_data._1617 import (
        OnedimensionalFunctionLookupTable,
    )
    from mastapy._private.math_utility.measured_data._1618 import (
        TwodimensionalFunctionLookupTable,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.math_utility.measured_data._1615": ["GriddedSurfaceAccessor"],
        "_private.math_utility.measured_data._1616": ["LookupTableBase"],
        "_private.math_utility.measured_data._1617": [
            "OnedimensionalFunctionLookupTable"
        ],
        "_private.math_utility.measured_data._1618": [
            "TwodimensionalFunctionLookupTable"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "GriddedSurfaceAccessor",
    "LookupTableBase",
    "OnedimensionalFunctionLookupTable",
    "TwodimensionalFunctionLookupTable",
)
