"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.acoustics._2686 import (
        AcousticAnalysisOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2687 import (
        AcousticAnalysisSetup,
    )
    from mastapy._private.system_model.part_model.acoustics._2688 import (
        AcousticAnalysisSetupCacheReporting,
    )
    from mastapy._private.system_model.part_model.acoustics._2689 import (
        AcousticAnalysisSetupCollection,
    )
    from mastapy._private.system_model.part_model.acoustics._2690 import (
        AcousticEnvelopeType,
    )
    from mastapy._private.system_model.part_model.acoustics._2691 import (
        AcousticInputSurfaceOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2692 import (
        CacheMemoryEstimates,
    )
    from mastapy._private.system_model.part_model.acoustics._2693 import (
        FEPartInputSurfaceOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2694 import (
        FESurfaceSelectionForAcousticEnvelope,
    )
    from mastapy._private.system_model.part_model.acoustics._2695 import HoleInFaceGroup
    from mastapy._private.system_model.part_model.acoustics._2696 import (
        MeshedResultPlane,
    )
    from mastapy._private.system_model.part_model.acoustics._2697 import (
        MeshedResultSphere,
    )
    from mastapy._private.system_model.part_model.acoustics._2698 import (
        MeshedResultSurface,
    )
    from mastapy._private.system_model.part_model.acoustics._2699 import (
        MeshedResultSurfaceBase,
    )
    from mastapy._private.system_model.part_model.acoustics._2700 import (
        MicrophoneArrayDesign,
    )
    from mastapy._private.system_model.part_model.acoustics._2701 import (
        PartSelectionForAcousticEnvelope,
    )
    from mastapy._private.system_model.part_model.acoustics._2702 import (
        ResultPlaneOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2703 import (
        ResultSphereOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2704 import (
        ResultSurfaceCollection,
    )
    from mastapy._private.system_model.part_model.acoustics._2705 import (
        ResultSurfaceOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2706 import (
        SphericalEnvelopeCentreDefinition,
    )
    from mastapy._private.system_model.part_model.acoustics._2707 import (
        SphericalEnvelopeType,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.acoustics._2686": ["AcousticAnalysisOptions"],
        "_private.system_model.part_model.acoustics._2687": ["AcousticAnalysisSetup"],
        "_private.system_model.part_model.acoustics._2688": [
            "AcousticAnalysisSetupCacheReporting"
        ],
        "_private.system_model.part_model.acoustics._2689": [
            "AcousticAnalysisSetupCollection"
        ],
        "_private.system_model.part_model.acoustics._2690": ["AcousticEnvelopeType"],
        "_private.system_model.part_model.acoustics._2691": [
            "AcousticInputSurfaceOptions"
        ],
        "_private.system_model.part_model.acoustics._2692": ["CacheMemoryEstimates"],
        "_private.system_model.part_model.acoustics._2693": [
            "FEPartInputSurfaceOptions"
        ],
        "_private.system_model.part_model.acoustics._2694": [
            "FESurfaceSelectionForAcousticEnvelope"
        ],
        "_private.system_model.part_model.acoustics._2695": ["HoleInFaceGroup"],
        "_private.system_model.part_model.acoustics._2696": ["MeshedResultPlane"],
        "_private.system_model.part_model.acoustics._2697": ["MeshedResultSphere"],
        "_private.system_model.part_model.acoustics._2698": ["MeshedResultSurface"],
        "_private.system_model.part_model.acoustics._2699": ["MeshedResultSurfaceBase"],
        "_private.system_model.part_model.acoustics._2700": ["MicrophoneArrayDesign"],
        "_private.system_model.part_model.acoustics._2701": [
            "PartSelectionForAcousticEnvelope"
        ],
        "_private.system_model.part_model.acoustics._2702": ["ResultPlaneOptions"],
        "_private.system_model.part_model.acoustics._2703": ["ResultSphereOptions"],
        "_private.system_model.part_model.acoustics._2704": ["ResultSurfaceCollection"],
        "_private.system_model.part_model.acoustics._2705": ["ResultSurfaceOptions"],
        "_private.system_model.part_model.acoustics._2706": [
            "SphericalEnvelopeCentreDefinition"
        ],
        "_private.system_model.part_model.acoustics._2707": ["SphericalEnvelopeType"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AcousticAnalysisOptions",
    "AcousticAnalysisSetup",
    "AcousticAnalysisSetupCacheReporting",
    "AcousticAnalysisSetupCollection",
    "AcousticEnvelopeType",
    "AcousticInputSurfaceOptions",
    "CacheMemoryEstimates",
    "FEPartInputSurfaceOptions",
    "FESurfaceSelectionForAcousticEnvelope",
    "HoleInFaceGroup",
    "MeshedResultPlane",
    "MeshedResultSphere",
    "MeshedResultSurface",
    "MeshedResultSurfaceBase",
    "MicrophoneArrayDesign",
    "PartSelectionForAcousticEnvelope",
    "ResultPlaneOptions",
    "ResultSphereOptions",
    "ResultSurfaceCollection",
    "ResultSurfaceOptions",
    "SphericalEnvelopeCentreDefinition",
    "SphericalEnvelopeType",
)
