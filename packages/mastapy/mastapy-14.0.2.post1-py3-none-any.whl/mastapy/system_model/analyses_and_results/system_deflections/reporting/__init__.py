"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._2933 import (
        CylindricalGearMeshMisalignmentValue,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._2934 import (
        FlexibleGearChart,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._2935 import (
        GearInMeshDeflectionResults,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._2936 import (
        MeshDeflectionResults,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._2937 import (
        PlanetCarrierWindup,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._2938 import (
        PlanetPinWindup,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._2939 import (
        RigidlyConnectedComponentGroupSystemDeflection,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._2940 import (
        ShaftSystemDeflectionSectionsReport,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._2941 import (
        SplineFlankContactReporting,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.system_deflections.reporting._2933": [
            "CylindricalGearMeshMisalignmentValue"
        ],
        "_private.system_model.analyses_and_results.system_deflections.reporting._2934": [
            "FlexibleGearChart"
        ],
        "_private.system_model.analyses_and_results.system_deflections.reporting._2935": [
            "GearInMeshDeflectionResults"
        ],
        "_private.system_model.analyses_and_results.system_deflections.reporting._2936": [
            "MeshDeflectionResults"
        ],
        "_private.system_model.analyses_and_results.system_deflections.reporting._2937": [
            "PlanetCarrierWindup"
        ],
        "_private.system_model.analyses_and_results.system_deflections.reporting._2938": [
            "PlanetPinWindup"
        ],
        "_private.system_model.analyses_and_results.system_deflections.reporting._2939": [
            "RigidlyConnectedComponentGroupSystemDeflection"
        ],
        "_private.system_model.analyses_and_results.system_deflections.reporting._2940": [
            "ShaftSystemDeflectionSectionsReport"
        ],
        "_private.system_model.analyses_and_results.system_deflections.reporting._2941": [
            "SplineFlankContactReporting"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CylindricalGearMeshMisalignmentValue",
    "FlexibleGearChart",
    "GearInMeshDeflectionResults",
    "MeshDeflectionResults",
    "PlanetCarrierWindup",
    "PlanetPinWindup",
    "RigidlyConnectedComponentGroupSystemDeflection",
    "ShaftSystemDeflectionSectionsReport",
    "SplineFlankContactReporting",
)
