"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bearings.tolerances._1956 import BearingConnectionComponent
    from mastapy._private.bearings.tolerances._1957 import InternalClearanceClass
    from mastapy._private.bearings.tolerances._1958 import BearingToleranceClass
    from mastapy._private.bearings.tolerances._1959 import (
        BearingToleranceDefinitionOptions,
    )
    from mastapy._private.bearings.tolerances._1960 import FitType
    from mastapy._private.bearings.tolerances._1961 import InnerRingTolerance
    from mastapy._private.bearings.tolerances._1962 import InnerSupportTolerance
    from mastapy._private.bearings.tolerances._1963 import InterferenceDetail
    from mastapy._private.bearings.tolerances._1964 import InterferenceTolerance
    from mastapy._private.bearings.tolerances._1965 import ITDesignation
    from mastapy._private.bearings.tolerances._1966 import MountingSleeveDiameterDetail
    from mastapy._private.bearings.tolerances._1967 import OuterRingTolerance
    from mastapy._private.bearings.tolerances._1968 import OuterSupportTolerance
    from mastapy._private.bearings.tolerances._1969 import RaceRoundnessAtAngle
    from mastapy._private.bearings.tolerances._1970 import RadialSpecificationMethod
    from mastapy._private.bearings.tolerances._1971 import RingDetail
    from mastapy._private.bearings.tolerances._1972 import RingTolerance
    from mastapy._private.bearings.tolerances._1973 import RoundnessSpecification
    from mastapy._private.bearings.tolerances._1974 import RoundnessSpecificationType
    from mastapy._private.bearings.tolerances._1975 import SupportDetail
    from mastapy._private.bearings.tolerances._1976 import SupportMaterialSource
    from mastapy._private.bearings.tolerances._1977 import SupportTolerance
    from mastapy._private.bearings.tolerances._1978 import (
        SupportToleranceLocationDesignation,
    )
    from mastapy._private.bearings.tolerances._1979 import ToleranceCombination
    from mastapy._private.bearings.tolerances._1980 import TypeOfFit
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bearings.tolerances._1956": ["BearingConnectionComponent"],
        "_private.bearings.tolerances._1957": ["InternalClearanceClass"],
        "_private.bearings.tolerances._1958": ["BearingToleranceClass"],
        "_private.bearings.tolerances._1959": ["BearingToleranceDefinitionOptions"],
        "_private.bearings.tolerances._1960": ["FitType"],
        "_private.bearings.tolerances._1961": ["InnerRingTolerance"],
        "_private.bearings.tolerances._1962": ["InnerSupportTolerance"],
        "_private.bearings.tolerances._1963": ["InterferenceDetail"],
        "_private.bearings.tolerances._1964": ["InterferenceTolerance"],
        "_private.bearings.tolerances._1965": ["ITDesignation"],
        "_private.bearings.tolerances._1966": ["MountingSleeveDiameterDetail"],
        "_private.bearings.tolerances._1967": ["OuterRingTolerance"],
        "_private.bearings.tolerances._1968": ["OuterSupportTolerance"],
        "_private.bearings.tolerances._1969": ["RaceRoundnessAtAngle"],
        "_private.bearings.tolerances._1970": ["RadialSpecificationMethod"],
        "_private.bearings.tolerances._1971": ["RingDetail"],
        "_private.bearings.tolerances._1972": ["RingTolerance"],
        "_private.bearings.tolerances._1973": ["RoundnessSpecification"],
        "_private.bearings.tolerances._1974": ["RoundnessSpecificationType"],
        "_private.bearings.tolerances._1975": ["SupportDetail"],
        "_private.bearings.tolerances._1976": ["SupportMaterialSource"],
        "_private.bearings.tolerances._1977": ["SupportTolerance"],
        "_private.bearings.tolerances._1978": ["SupportToleranceLocationDesignation"],
        "_private.bearings.tolerances._1979": ["ToleranceCombination"],
        "_private.bearings.tolerances._1980": ["TypeOfFit"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BearingConnectionComponent",
    "InternalClearanceClass",
    "BearingToleranceClass",
    "BearingToleranceDefinitionOptions",
    "FitType",
    "InnerRingTolerance",
    "InnerSupportTolerance",
    "InterferenceDetail",
    "InterferenceTolerance",
    "ITDesignation",
    "MountingSleeveDiameterDetail",
    "OuterRingTolerance",
    "OuterSupportTolerance",
    "RaceRoundnessAtAngle",
    "RadialSpecificationMethod",
    "RingDetail",
    "RingTolerance",
    "RoundnessSpecification",
    "RoundnessSpecificationType",
    "SupportDetail",
    "SupportMaterialSource",
    "SupportTolerance",
    "SupportToleranceLocationDesignation",
    "ToleranceCombination",
    "TypeOfFit",
)
