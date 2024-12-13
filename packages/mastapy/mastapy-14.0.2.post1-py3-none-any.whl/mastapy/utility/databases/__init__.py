"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.databases._1879 import Database
    from mastapy._private.utility.databases._1880 import DatabaseConnectionSettings
    from mastapy._private.utility.databases._1881 import DatabaseKey
    from mastapy._private.utility.databases._1882 import DatabaseSettings
    from mastapy._private.utility.databases._1883 import NamedDatabase
    from mastapy._private.utility.databases._1884 import NamedDatabaseItem
    from mastapy._private.utility.databases._1885 import NamedKey
    from mastapy._private.utility.databases._1886 import SQLDatabase
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.databases._1879": ["Database"],
        "_private.utility.databases._1880": ["DatabaseConnectionSettings"],
        "_private.utility.databases._1881": ["DatabaseKey"],
        "_private.utility.databases._1882": ["DatabaseSettings"],
        "_private.utility.databases._1883": ["NamedDatabase"],
        "_private.utility.databases._1884": ["NamedDatabaseItem"],
        "_private.utility.databases._1885": ["NamedKey"],
        "_private.utility.databases._1886": ["SQLDatabase"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "Database",
    "DatabaseConnectionSettings",
    "DatabaseKey",
    "DatabaseSettings",
    "NamedDatabase",
    "NamedDatabaseItem",
    "NamedKey",
    "SQLDatabase",
)
