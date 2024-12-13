"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bearings.bearing_designs.rolling.xml_import._2233 import (
        AbstractXmlVariableAssignment,
    )
    from mastapy._private.bearings.bearing_designs.rolling.xml_import._2234 import (
        BearingImportFile,
    )
    from mastapy._private.bearings.bearing_designs.rolling.xml_import._2235 import (
        RollingBearingImporter,
    )
    from mastapy._private.bearings.bearing_designs.rolling.xml_import._2236 import (
        XmlBearingTypeMapping,
    )
    from mastapy._private.bearings.bearing_designs.rolling.xml_import._2237 import (
        XMLVariableAssignment,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bearings.bearing_designs.rolling.xml_import._2233": [
            "AbstractXmlVariableAssignment"
        ],
        "_private.bearings.bearing_designs.rolling.xml_import._2234": [
            "BearingImportFile"
        ],
        "_private.bearings.bearing_designs.rolling.xml_import._2235": [
            "RollingBearingImporter"
        ],
        "_private.bearings.bearing_designs.rolling.xml_import._2236": [
            "XmlBearingTypeMapping"
        ],
        "_private.bearings.bearing_designs.rolling.xml_import._2237": [
            "XMLVariableAssignment"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractXmlVariableAssignment",
    "BearingImportFile",
    "RollingBearingImporter",
    "XmlBearingTypeMapping",
    "XMLVariableAssignment",
)
