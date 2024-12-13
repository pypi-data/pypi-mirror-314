"""PlanetCarrierSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections import _2873

_PLANET_CARRIER_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "PlanetCarrierSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740, _2742, _2746
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7719,
        _7721,
        _7722,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4231
    from mastapy._private.system_model.analyses_and_results.static_loads import _7090
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2804,
        _2876,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
        _2937,
    )
    from mastapy._private.system_model.part_model import _2529

    Self = TypeVar("Self", bound="PlanetCarrierSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PlanetCarrierSystemDeflection._Cast_PlanetCarrierSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlanetCarrierSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlanetCarrierSystemDeflection:
    """Special nested class for casting PlanetCarrierSystemDeflection to subclasses."""

    __parent__: "PlanetCarrierSystemDeflection"

    @property
    def mountable_component_system_deflection(
        self: "CastSelf",
    ) -> "_2873.MountableComponentSystemDeflection":
        return self.__parent__._cast(_2873.MountableComponentSystemDeflection)

    @property
    def component_system_deflection(
        self: "CastSelf",
    ) -> "_2804.ComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2804,
        )

        return self.__parent__._cast(_2804.ComponentSystemDeflection)

    @property
    def part_system_deflection(self: "CastSelf") -> "_2876.PartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2876,
        )

        return self.__parent__._cast(_2876.PartSystemDeflection)

    @property
    def part_fe_analysis(self: "CastSelf") -> "_7721.PartFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7721,
        )

        return self.__parent__._cast(_7721.PartFEAnalysis)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7722.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7722,
        )

        return self.__parent__._cast(_7722.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7719.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7719,
        )

        return self.__parent__._cast(_7719.PartAnalysisCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2746.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2746

        return self.__parent__._cast(_2746.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2742.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2742

        return self.__parent__._cast(_2742.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2740.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2740

        return self.__parent__._cast(_2740.DesignEntityAnalysis)

    @property
    def planet_carrier_system_deflection(
        self: "CastSelf",
    ) -> "PlanetCarrierSystemDeflection":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class PlanetCarrierSystemDeflection(_2873.MountableComponentSystemDeflection):
    """PlanetCarrierSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANET_CARRIER_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2529.PlanetCarrier":
        """mastapy.system_model.part_model.PlanetCarrier

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: "Self") -> "_7090.PlanetCarrierLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def power_flow_results(self: "Self") -> "_4231.PlanetCarrierPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.PlanetCarrierPowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlowResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def windup(self: "Self") -> "List[_2937.PlanetCarrierWindup]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.reporting.PlanetCarrierWindup]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Windup")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_PlanetCarrierSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_PlanetCarrierSystemDeflection
        """
        return _Cast_PlanetCarrierSystemDeflection(self)
