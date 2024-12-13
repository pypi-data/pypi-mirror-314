"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.generics._1865 import NamedTuple1
    from mastapy._private.utility.generics._1866 import NamedTuple2
    from mastapy._private.utility.generics._1867 import NamedTuple3
    from mastapy._private.utility.generics._1868 import NamedTuple4
    from mastapy._private.utility.generics._1869 import NamedTuple5
    from mastapy._private.utility.generics._1870 import NamedTuple6
    from mastapy._private.utility.generics._1871 import NamedTuple7
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.generics._1865": ["NamedTuple1"],
        "_private.utility.generics._1866": ["NamedTuple2"],
        "_private.utility.generics._1867": ["NamedTuple3"],
        "_private.utility.generics._1868": ["NamedTuple4"],
        "_private.utility.generics._1869": ["NamedTuple5"],
        "_private.utility.generics._1870": ["NamedTuple6"],
        "_private.utility.generics._1871": ["NamedTuple7"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "NamedTuple1",
    "NamedTuple2",
    "NamedTuple3",
    "NamedTuple4",
    "NamedTuple5",
    "NamedTuple6",
    "NamedTuple7",
)
