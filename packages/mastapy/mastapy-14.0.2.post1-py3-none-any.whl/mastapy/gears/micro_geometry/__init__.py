"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.micro_geometry._582 import BiasModification
    from mastapy._private.gears.micro_geometry._583 import FlankMicroGeometry
    from mastapy._private.gears.micro_geometry._584 import FlankSide
    from mastapy._private.gears.micro_geometry._585 import LeadModification
    from mastapy._private.gears.micro_geometry._586 import (
        LocationOfEvaluationLowerLimit,
    )
    from mastapy._private.gears.micro_geometry._587 import (
        LocationOfEvaluationUpperLimit,
    )
    from mastapy._private.gears.micro_geometry._588 import (
        LocationOfRootReliefEvaluation,
    )
    from mastapy._private.gears.micro_geometry._589 import LocationOfTipReliefEvaluation
    from mastapy._private.gears.micro_geometry._590 import (
        MainProfileReliefEndsAtTheStartOfRootReliefOption,
    )
    from mastapy._private.gears.micro_geometry._591 import (
        MainProfileReliefEndsAtTheStartOfTipReliefOption,
    )
    from mastapy._private.gears.micro_geometry._592 import Modification
    from mastapy._private.gears.micro_geometry._593 import (
        ParabolicRootReliefStartsTangentToMainProfileRelief,
    )
    from mastapy._private.gears.micro_geometry._594 import (
        ParabolicTipReliefStartsTangentToMainProfileRelief,
    )
    from mastapy._private.gears.micro_geometry._595 import ProfileModification
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.micro_geometry._582": ["BiasModification"],
        "_private.gears.micro_geometry._583": ["FlankMicroGeometry"],
        "_private.gears.micro_geometry._584": ["FlankSide"],
        "_private.gears.micro_geometry._585": ["LeadModification"],
        "_private.gears.micro_geometry._586": ["LocationOfEvaluationLowerLimit"],
        "_private.gears.micro_geometry._587": ["LocationOfEvaluationUpperLimit"],
        "_private.gears.micro_geometry._588": ["LocationOfRootReliefEvaluation"],
        "_private.gears.micro_geometry._589": ["LocationOfTipReliefEvaluation"],
        "_private.gears.micro_geometry._590": [
            "MainProfileReliefEndsAtTheStartOfRootReliefOption"
        ],
        "_private.gears.micro_geometry._591": [
            "MainProfileReliefEndsAtTheStartOfTipReliefOption"
        ],
        "_private.gears.micro_geometry._592": ["Modification"],
        "_private.gears.micro_geometry._593": [
            "ParabolicRootReliefStartsTangentToMainProfileRelief"
        ],
        "_private.gears.micro_geometry._594": [
            "ParabolicTipReliefStartsTangentToMainProfileRelief"
        ],
        "_private.gears.micro_geometry._595": ["ProfileModification"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BiasModification",
    "FlankMicroGeometry",
    "FlankSide",
    "LeadModification",
    "LocationOfEvaluationLowerLimit",
    "LocationOfEvaluationUpperLimit",
    "LocationOfRootReliefEvaluation",
    "LocationOfTipReliefEvaluation",
    "MainProfileReliefEndsAtTheStartOfRootReliefOption",
    "MainProfileReliefEndsAtTheStartOfTipReliefOption",
    "Modification",
    "ParabolicRootReliefStartsTangentToMainProfileRelief",
    "ParabolicTipReliefStartsTangentToMainProfileRelief",
    "ProfileModification",
)
