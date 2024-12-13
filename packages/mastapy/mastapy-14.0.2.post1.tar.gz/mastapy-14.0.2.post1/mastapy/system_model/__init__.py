"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model._2257 import Design
    from mastapy._private.system_model._2258 import ComponentDampingOption
    from mastapy._private.system_model._2259 import (
        ConceptCouplingSpeedRatioSpecificationMethod,
    )
    from mastapy._private.system_model._2260 import DesignEntity
    from mastapy._private.system_model._2261 import DesignEntityId
    from mastapy._private.system_model._2262 import DesignSettings
    from mastapy._private.system_model._2263 import DutyCycleImporter
    from mastapy._private.system_model._2264 import DutyCycleImporterDesignEntityMatch
    from mastapy._private.system_model._2265 import ExternalFullFELoader
    from mastapy._private.system_model._2266 import HypoidWindUpRemovalMethod
    from mastapy._private.system_model._2267 import IncludeDutyCycleOption
    from mastapy._private.system_model._2268 import MAAElectricMachineGroup
    from mastapy._private.system_model._2269 import MASTASettings
    from mastapy._private.system_model._2270 import MemorySummary
    from mastapy._private.system_model._2271 import MeshStiffnessModel
    from mastapy._private.system_model._2272 import (
        PlanetPinManufacturingErrorsCoordinateSystem,
    )
    from mastapy._private.system_model._2273 import (
        PowerLoadDragTorqueSpecificationMethod,
    )
    from mastapy._private.system_model._2274 import (
        PowerLoadInputTorqueSpecificationMethod,
    )
    from mastapy._private.system_model._2275 import PowerLoadPIDControlSpeedInputType
    from mastapy._private.system_model._2276 import PowerLoadType
    from mastapy._private.system_model._2277 import RelativeComponentAlignment
    from mastapy._private.system_model._2278 import RelativeOffsetOption
    from mastapy._private.system_model._2279 import SystemReporting
    from mastapy._private.system_model._2280 import (
        ThermalExpansionOptionForGroundedNodes,
    )
    from mastapy._private.system_model._2281 import TransmissionTemperatureSet
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model._2257": ["Design"],
        "_private.system_model._2258": ["ComponentDampingOption"],
        "_private.system_model._2259": ["ConceptCouplingSpeedRatioSpecificationMethod"],
        "_private.system_model._2260": ["DesignEntity"],
        "_private.system_model._2261": ["DesignEntityId"],
        "_private.system_model._2262": ["DesignSettings"],
        "_private.system_model._2263": ["DutyCycleImporter"],
        "_private.system_model._2264": ["DutyCycleImporterDesignEntityMatch"],
        "_private.system_model._2265": ["ExternalFullFELoader"],
        "_private.system_model._2266": ["HypoidWindUpRemovalMethod"],
        "_private.system_model._2267": ["IncludeDutyCycleOption"],
        "_private.system_model._2268": ["MAAElectricMachineGroup"],
        "_private.system_model._2269": ["MASTASettings"],
        "_private.system_model._2270": ["MemorySummary"],
        "_private.system_model._2271": ["MeshStiffnessModel"],
        "_private.system_model._2272": ["PlanetPinManufacturingErrorsCoordinateSystem"],
        "_private.system_model._2273": ["PowerLoadDragTorqueSpecificationMethod"],
        "_private.system_model._2274": ["PowerLoadInputTorqueSpecificationMethod"],
        "_private.system_model._2275": ["PowerLoadPIDControlSpeedInputType"],
        "_private.system_model._2276": ["PowerLoadType"],
        "_private.system_model._2277": ["RelativeComponentAlignment"],
        "_private.system_model._2278": ["RelativeOffsetOption"],
        "_private.system_model._2279": ["SystemReporting"],
        "_private.system_model._2280": ["ThermalExpansionOptionForGroundedNodes"],
        "_private.system_model._2281": ["TransmissionTemperatureSet"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "Design",
    "ComponentDampingOption",
    "ConceptCouplingSpeedRatioSpecificationMethod",
    "DesignEntity",
    "DesignEntityId",
    "DesignSettings",
    "DutyCycleImporter",
    "DutyCycleImporterDesignEntityMatch",
    "ExternalFullFELoader",
    "HypoidWindUpRemovalMethod",
    "IncludeDutyCycleOption",
    "MAAElectricMachineGroup",
    "MASTASettings",
    "MemorySummary",
    "MeshStiffnessModel",
    "PlanetPinManufacturingErrorsCoordinateSystem",
    "PowerLoadDragTorqueSpecificationMethod",
    "PowerLoadInputTorqueSpecificationMethod",
    "PowerLoadPIDControlSpeedInputType",
    "PowerLoadType",
    "RelativeComponentAlignment",
    "RelativeOffsetOption",
    "SystemReporting",
    "ThermalExpansionOptionForGroundedNodes",
    "TransmissionTemperatureSet",
)
