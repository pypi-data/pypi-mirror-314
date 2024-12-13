"""Root of the mastapy package."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private._0 import APIBase
    from mastapy._private._1 import Initialiser
    from mastapy._private._2 import LegacyV2RuntimeActivationPolicyAttributeSetter
    from mastapy._private._3 import PythonUtility
    from mastapy._private._4 import UtilityMethods
    from mastapy._private._5 import Versioning
    from mastapy._private._7726 import ConsoleProgress
    from mastapy._private._7727 import MarshalByRefObjectPermanent
    from mastapy._private._7728 import MarshalByRefObjects
    from mastapy._private._7729 import EnvironmentVariableUtility
    from mastapy._private._7730 import Remoting
    from mastapy._private._7731 import ScriptedPropertyNameAttribute
    from mastapy._private._7732 import SimpleTaskProgress
    from mastapy._private._7733 import TaskProgress
    from mastapy._private._internal import (
        AssemblyLoadError,
        CastException,
        DebugEnvironment,
        Examples,
        MastaInitException,
        MastaPropertyException,
        MastaPropertyTypeException,
        MastapyImportException,
        MeasurementType,
        TupleWithName,
        TypeCheckException,
        UnavailableMethodError,
        __api_version__,
        __version__,
        init,
        masta_after,
        masta_before,
        masta_licences,
        masta_property,
        overridable,
        start_debugging,
    )
    from mastapy._private._math import (
        Color,
        Long,
        Matrix2x2,
        Matrix3x3,
        Matrix4x4,
        MatrixException,
        Vector2D,
        Vector3D,
        Vector4D,
        VectorException,
        approximately_equal,
        clamp,
        fract,
        sign,
        smoothstep,
        step,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private._internal": [
            "DebugEnvironment",
            "MastaInitException",
            "MastaPropertyException",
            "MastaPropertyTypeException",
            "masta_property",
            "masta_before",
            "masta_after",
            "init",
            "start_debugging",
            "__version__",
            "__api_version__",
            "TupleWithName",
            "CastException",
            "MastapyImportException",
            "overridable",
            "MeasurementType",
            "TypeCheckException",
            "masta_licences",
            "AssemblyLoadError",
            "UnavailableMethodError",
            "Examples",
        ],
        "_private._math": [
            "clamp",
            "sign",
            "fract",
            "step",
            "smoothstep",
            "approximately_equal",
            "Long",
            "Vector2D",
            "Vector3D",
            "Vector4D",
            "Color",
            "VectorException",
            "Matrix2x2",
            "Matrix3x3",
            "Matrix4x4",
            "MatrixException",
        ],
        "_private._0": ["APIBase"],
        "_private._1": ["Initialiser"],
        "_private._2": ["LegacyV2RuntimeActivationPolicyAttributeSetter"],
        "_private._3": ["PythonUtility"],
        "_private._4": ["UtilityMethods"],
        "_private._5": ["Versioning"],
        "_private._7726": ["ConsoleProgress"],
        "_private._7727": ["MarshalByRefObjectPermanent"],
        "_private._7728": ["MarshalByRefObjects"],
        "_private._7729": ["EnvironmentVariableUtility"],
        "_private._7730": ["Remoting"],
        "_private._7731": ["ScriptedPropertyNameAttribute"],
        "_private._7732": ["SimpleTaskProgress"],
        "_private._7733": ["TaskProgress"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

    from mastapy._private._internal import mastafile_hook as __mh

    __mh()


__all__ = (
    "DebugEnvironment",
    "MastaInitException",
    "MastaPropertyException",
    "MastaPropertyTypeException",
    "masta_property",
    "masta_before",
    "masta_after",
    "init",
    "start_debugging",
    "__version__",
    "__api_version__",
    "TupleWithName",
    "CastException",
    "MastapyImportException",
    "overridable",
    "MeasurementType",
    "TypeCheckException",
    "masta_licences",
    "AssemblyLoadError",
    "UnavailableMethodError",
    "Examples",
    "clamp",
    "sign",
    "fract",
    "step",
    "smoothstep",
    "approximately_equal",
    "Long",
    "Vector2D",
    "Vector3D",
    "Vector4D",
    "Color",
    "VectorException",
    "Matrix2x2",
    "Matrix3x3",
    "Matrix4x4",
    "MatrixException",
    "APIBase",
    "Initialiser",
    "LegacyV2RuntimeActivationPolicyAttributeSetter",
    "PythonUtility",
    "UtilityMethods",
    "Versioning",
    "ConsoleProgress",
    "MarshalByRefObjectPermanent",
    "MarshalByRefObjects",
    "EnvironmentVariableUtility",
    "Remoting",
    "ScriptedPropertyNameAttribute",
    "SimpleTaskProgress",
    "TaskProgress",
)
