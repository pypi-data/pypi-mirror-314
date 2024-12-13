"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.optimization._2283 import (
        ConicalGearOptimisationStrategy,
    )
    from mastapy._private.system_model.optimization._2284 import (
        ConicalGearOptimizationStep,
    )
    from mastapy._private.system_model.optimization._2285 import (
        ConicalGearOptimizationStrategyDatabase,
    )
    from mastapy._private.system_model.optimization._2286 import (
        CylindricalGearOptimisationStrategy,
    )
    from mastapy._private.system_model.optimization._2287 import (
        CylindricalGearOptimizationStep,
    )
    from mastapy._private.system_model.optimization._2288 import (
        MeasuredAndFactorViewModel,
    )
    from mastapy._private.system_model.optimization._2289 import (
        MicroGeometryOptimisationTarget,
    )
    from mastapy._private.system_model.optimization._2290 import OptimizationStep
    from mastapy._private.system_model.optimization._2291 import OptimizationStrategy
    from mastapy._private.system_model.optimization._2292 import (
        OptimizationStrategyBase,
    )
    from mastapy._private.system_model.optimization._2293 import (
        OptimizationStrategyDatabase,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.optimization._2283": ["ConicalGearOptimisationStrategy"],
        "_private.system_model.optimization._2284": ["ConicalGearOptimizationStep"],
        "_private.system_model.optimization._2285": [
            "ConicalGearOptimizationStrategyDatabase"
        ],
        "_private.system_model.optimization._2286": [
            "CylindricalGearOptimisationStrategy"
        ],
        "_private.system_model.optimization._2287": ["CylindricalGearOptimizationStep"],
        "_private.system_model.optimization._2288": ["MeasuredAndFactorViewModel"],
        "_private.system_model.optimization._2289": ["MicroGeometryOptimisationTarget"],
        "_private.system_model.optimization._2290": ["OptimizationStep"],
        "_private.system_model.optimization._2291": ["OptimizationStrategy"],
        "_private.system_model.optimization._2292": ["OptimizationStrategyBase"],
        "_private.system_model.optimization._2293": ["OptimizationStrategyDatabase"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConicalGearOptimisationStrategy",
    "ConicalGearOptimizationStep",
    "ConicalGearOptimizationStrategyDatabase",
    "CylindricalGearOptimisationStrategy",
    "CylindricalGearOptimizationStep",
    "MeasuredAndFactorViewModel",
    "MicroGeometryOptimisationTarget",
    "OptimizationStep",
    "OptimizationStrategy",
    "OptimizationStrategyBase",
    "OptimizationStrategyDatabase",
)
