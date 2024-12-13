"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.scripting._7736 import ApiEnumForAttribute
    from mastapy._private.scripting._7737 import ApiVersion
    from mastapy._private.scripting._7738 import SMTBitmap
    from mastapy._private.scripting._7740 import MastaPropertyAttribute
    from mastapy._private.scripting._7741 import PythonCommand
    from mastapy._private.scripting._7742 import ScriptingCommand
    from mastapy._private.scripting._7743 import ScriptingExecutionCommand
    from mastapy._private.scripting._7744 import ScriptingObjectCommand
    from mastapy._private.scripting._7745 import ApiVersioning
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.scripting._7736": ["ApiEnumForAttribute"],
        "_private.scripting._7737": ["ApiVersion"],
        "_private.scripting._7738": ["SMTBitmap"],
        "_private.scripting._7740": ["MastaPropertyAttribute"],
        "_private.scripting._7741": ["PythonCommand"],
        "_private.scripting._7742": ["ScriptingCommand"],
        "_private.scripting._7743": ["ScriptingExecutionCommand"],
        "_private.scripting._7744": ["ScriptingObjectCommand"],
        "_private.scripting._7745": ["ApiVersioning"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ApiEnumForAttribute",
    "ApiVersion",
    "SMTBitmap",
    "MastaPropertyAttribute",
    "PythonCommand",
    "ScriptingCommand",
    "ScriptingExecutionCommand",
    "ScriptingObjectCommand",
    "ApiVersioning",
)
