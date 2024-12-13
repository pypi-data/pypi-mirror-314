"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.nodal_analysis.system_solvers._103 import (
        BackwardEulerTransientSolver,
    )
    from mastapy._private.nodal_analysis.system_solvers._104 import DenseStiffnessSolver
    from mastapy._private.nodal_analysis.system_solvers._105 import DirkTransientSolver
    from mastapy._private.nodal_analysis.system_solvers._106 import DynamicSolver
    from mastapy._private.nodal_analysis.system_solvers._107 import (
        InternalTransientSolver,
    )
    from mastapy._private.nodal_analysis.system_solvers._108 import (
        LobattoIIICTransientSolver,
    )
    from mastapy._private.nodal_analysis.system_solvers._109 import (
        NewmarkTransientSolver,
    )
    from mastapy._private.nodal_analysis.system_solvers._110 import (
        NewtonRaphsonAnalysis,
    )
    from mastapy._private.nodal_analysis.system_solvers._111 import (
        NewtonRaphsonDegreeOfFreedomError,
    )
    from mastapy._private.nodal_analysis.system_solvers._112 import (
        SimpleVelocityBasedStepHalvingTransientSolver,
    )
    from mastapy._private.nodal_analysis.system_solvers._113 import (
        SingularDegreeOfFreedomAnalysis,
    )
    from mastapy._private.nodal_analysis.system_solvers._114 import (
        SingularValuesAnalysis,
    )
    from mastapy._private.nodal_analysis.system_solvers._115 import (
        SingularVectorAnalysis,
    )
    from mastapy._private.nodal_analysis.system_solvers._116 import Solver
    from mastapy._private.nodal_analysis.system_solvers._117 import (
        StepHalvingTransientSolver,
    )
    from mastapy._private.nodal_analysis.system_solvers._118 import StiffnessSolver
    from mastapy._private.nodal_analysis.system_solvers._119 import TransientSolver
    from mastapy._private.nodal_analysis.system_solvers._120 import (
        WilsonThetaTransientSolver,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.nodal_analysis.system_solvers._103": ["BackwardEulerTransientSolver"],
        "_private.nodal_analysis.system_solvers._104": ["DenseStiffnessSolver"],
        "_private.nodal_analysis.system_solvers._105": ["DirkTransientSolver"],
        "_private.nodal_analysis.system_solvers._106": ["DynamicSolver"],
        "_private.nodal_analysis.system_solvers._107": ["InternalTransientSolver"],
        "_private.nodal_analysis.system_solvers._108": ["LobattoIIICTransientSolver"],
        "_private.nodal_analysis.system_solvers._109": ["NewmarkTransientSolver"],
        "_private.nodal_analysis.system_solvers._110": ["NewtonRaphsonAnalysis"],
        "_private.nodal_analysis.system_solvers._111": [
            "NewtonRaphsonDegreeOfFreedomError"
        ],
        "_private.nodal_analysis.system_solvers._112": [
            "SimpleVelocityBasedStepHalvingTransientSolver"
        ],
        "_private.nodal_analysis.system_solvers._113": [
            "SingularDegreeOfFreedomAnalysis"
        ],
        "_private.nodal_analysis.system_solvers._114": ["SingularValuesAnalysis"],
        "_private.nodal_analysis.system_solvers._115": ["SingularVectorAnalysis"],
        "_private.nodal_analysis.system_solvers._116": ["Solver"],
        "_private.nodal_analysis.system_solvers._117": ["StepHalvingTransientSolver"],
        "_private.nodal_analysis.system_solvers._118": ["StiffnessSolver"],
        "_private.nodal_analysis.system_solvers._119": ["TransientSolver"],
        "_private.nodal_analysis.system_solvers._120": ["WilsonThetaTransientSolver"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BackwardEulerTransientSolver",
    "DenseStiffnessSolver",
    "DirkTransientSolver",
    "DynamicSolver",
    "InternalTransientSolver",
    "LobattoIIICTransientSolver",
    "NewmarkTransientSolver",
    "NewtonRaphsonAnalysis",
    "NewtonRaphsonDegreeOfFreedomError",
    "SimpleVelocityBasedStepHalvingTransientSolver",
    "SingularDegreeOfFreedomAnalysis",
    "SingularValuesAnalysis",
    "SingularVectorAnalysis",
    "Solver",
    "StepHalvingTransientSolver",
    "StiffnessSolver",
    "TransientSolver",
    "WilsonThetaTransientSolver",
)
