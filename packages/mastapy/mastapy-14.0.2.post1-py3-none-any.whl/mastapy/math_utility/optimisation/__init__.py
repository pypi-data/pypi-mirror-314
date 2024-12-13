"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.math_utility.optimisation._1589 import AbstractOptimisable
    from mastapy._private.math_utility.optimisation._1590 import (
        DesignSpaceSearchStrategyDatabase,
    )
    from mastapy._private.math_utility.optimisation._1591 import InputSetter
    from mastapy._private.math_utility.optimisation._1592 import Optimisable
    from mastapy._private.math_utility.optimisation._1593 import OptimisationHistory
    from mastapy._private.math_utility.optimisation._1594 import OptimizationInput
    from mastapy._private.math_utility.optimisation._1595 import OptimizationVariable
    from mastapy._private.math_utility.optimisation._1596 import (
        ParetoOptimisationFilter,
    )
    from mastapy._private.math_utility.optimisation._1597 import ParetoOptimisationInput
    from mastapy._private.math_utility.optimisation._1598 import (
        ParetoOptimisationOutput,
    )
    from mastapy._private.math_utility.optimisation._1599 import (
        ParetoOptimisationStrategy,
    )
    from mastapy._private.math_utility.optimisation._1600 import (
        ParetoOptimisationStrategyBars,
    )
    from mastapy._private.math_utility.optimisation._1601 import (
        ParetoOptimisationStrategyChartInformation,
    )
    from mastapy._private.math_utility.optimisation._1602 import (
        ParetoOptimisationStrategyDatabase,
    )
    from mastapy._private.math_utility.optimisation._1603 import (
        ParetoOptimisationVariable,
    )
    from mastapy._private.math_utility.optimisation._1604 import (
        ParetoOptimisationVariableBase,
    )
    from mastapy._private.math_utility.optimisation._1605 import (
        PropertyTargetForDominantCandidateSearch,
    )
    from mastapy._private.math_utility.optimisation._1606 import (
        ReportingOptimizationInput,
    )
    from mastapy._private.math_utility.optimisation._1607 import (
        SpecifyOptimisationInputAs,
    )
    from mastapy._private.math_utility.optimisation._1608 import TargetingPropertyTo
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.math_utility.optimisation._1589": ["AbstractOptimisable"],
        "_private.math_utility.optimisation._1590": [
            "DesignSpaceSearchStrategyDatabase"
        ],
        "_private.math_utility.optimisation._1591": ["InputSetter"],
        "_private.math_utility.optimisation._1592": ["Optimisable"],
        "_private.math_utility.optimisation._1593": ["OptimisationHistory"],
        "_private.math_utility.optimisation._1594": ["OptimizationInput"],
        "_private.math_utility.optimisation._1595": ["OptimizationVariable"],
        "_private.math_utility.optimisation._1596": ["ParetoOptimisationFilter"],
        "_private.math_utility.optimisation._1597": ["ParetoOptimisationInput"],
        "_private.math_utility.optimisation._1598": ["ParetoOptimisationOutput"],
        "_private.math_utility.optimisation._1599": ["ParetoOptimisationStrategy"],
        "_private.math_utility.optimisation._1600": ["ParetoOptimisationStrategyBars"],
        "_private.math_utility.optimisation._1601": [
            "ParetoOptimisationStrategyChartInformation"
        ],
        "_private.math_utility.optimisation._1602": [
            "ParetoOptimisationStrategyDatabase"
        ],
        "_private.math_utility.optimisation._1603": ["ParetoOptimisationVariable"],
        "_private.math_utility.optimisation._1604": ["ParetoOptimisationVariableBase"],
        "_private.math_utility.optimisation._1605": [
            "PropertyTargetForDominantCandidateSearch"
        ],
        "_private.math_utility.optimisation._1606": ["ReportingOptimizationInput"],
        "_private.math_utility.optimisation._1607": ["SpecifyOptimisationInputAs"],
        "_private.math_utility.optimisation._1608": ["TargetingPropertyTo"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractOptimisable",
    "DesignSpaceSearchStrategyDatabase",
    "InputSetter",
    "Optimisable",
    "OptimisationHistory",
    "OptimizationInput",
    "OptimizationVariable",
    "ParetoOptimisationFilter",
    "ParetoOptimisationInput",
    "ParetoOptimisationOutput",
    "ParetoOptimisationStrategy",
    "ParetoOptimisationStrategyBars",
    "ParetoOptimisationStrategyChartInformation",
    "ParetoOptimisationStrategyDatabase",
    "ParetoOptimisationVariable",
    "ParetoOptimisationVariableBase",
    "PropertyTargetForDominantCandidateSearch",
    "ReportingOptimizationInput",
    "SpecifyOptimisationInputAs",
    "TargetingPropertyTo",
)
