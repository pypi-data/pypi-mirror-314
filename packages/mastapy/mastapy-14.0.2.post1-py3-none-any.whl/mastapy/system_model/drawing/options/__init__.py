"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.drawing.options._2318 import (
        AdvancedTimeSteppingAnalysisForModulationModeViewOptions,
    )
    from mastapy._private.system_model.drawing.options._2319 import (
        ExcitationAnalysisViewOption,
    )
    from mastapy._private.system_model.drawing.options._2320 import (
        ModalContributionViewOptions,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.drawing.options._2318": [
            "AdvancedTimeSteppingAnalysisForModulationModeViewOptions"
        ],
        "_private.system_model.drawing.options._2319": ["ExcitationAnalysisViewOption"],
        "_private.system_model.drawing.options._2320": ["ModalContributionViewOptions"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AdvancedTimeSteppingAnalysisForModulationModeViewOptions",
    "ExcitationAnalysisViewOption",
    "ModalContributionViewOptions",
)
