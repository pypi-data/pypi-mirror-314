"""StraightBevelSunGearSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections import _2906

_STRAIGHT_BEVEL_SUN_GEAR_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "StraightBevelSunGearSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740, _2742, _2746
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7719,
        _7721,
        _7722,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4260
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2780,
        _2797,
        _2804,
        _2815,
        _2850,
        _2873,
        _2876,
    )
    from mastapy._private.system_model.part_model.gears import _2611

    Self = TypeVar("Self", bound="StraightBevelSunGearSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelSunGearSystemDeflection._Cast_StraightBevelSunGearSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelSunGearSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelSunGearSystemDeflection:
    """Special nested class for casting StraightBevelSunGearSystemDeflection to subclasses."""

    __parent__: "StraightBevelSunGearSystemDeflection"

    @property
    def straight_bevel_diff_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2906.StraightBevelDiffGearSystemDeflection":
        return self.__parent__._cast(_2906.StraightBevelDiffGearSystemDeflection)

    @property
    def bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2797.BevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2797,
        )

        return self.__parent__._cast(_2797.BevelGearSystemDeflection)

    @property
    def agma_gleason_conical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2780.AGMAGleasonConicalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2780,
        )

        return self.__parent__._cast(_2780.AGMAGleasonConicalGearSystemDeflection)

    @property
    def conical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2815.ConicalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2815,
        )

        return self.__parent__._cast(_2815.ConicalGearSystemDeflection)

    @property
    def gear_system_deflection(self: "CastSelf") -> "_2850.GearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2850,
        )

        return self.__parent__._cast(_2850.GearSystemDeflection)

    @property
    def mountable_component_system_deflection(
        self: "CastSelf",
    ) -> "_2873.MountableComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2873,
        )

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
    def straight_bevel_sun_gear_system_deflection(
        self: "CastSelf",
    ) -> "StraightBevelSunGearSystemDeflection":
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
class StraightBevelSunGearSystemDeflection(_2906.StraightBevelDiffGearSystemDeflection):
    """StraightBevelSunGearSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_SUN_GEAR_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2611.StraightBevelSunGear":
        """mastapy.system_model.part_model.gears.StraightBevelSunGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def power_flow_results(self: "Self") -> "_4260.StraightBevelSunGearPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.StraightBevelSunGearPowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlowResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelSunGearSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelSunGearSystemDeflection
        """
        return _Cast_StraightBevelSunGearSystemDeflection(self)
