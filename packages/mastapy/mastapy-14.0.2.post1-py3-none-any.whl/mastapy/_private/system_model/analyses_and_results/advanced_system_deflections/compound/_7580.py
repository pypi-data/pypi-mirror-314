"""BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
    _7577,
)

_BEVEL_DIFFERENTIAL_PLANET_GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound",
    "BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7445,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
        _7570,
        _7582,
        _7591,
        _7598,
        _7624,
        _7645,
        _7647,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )

    Self = TypeVar(
        "Self", bound="BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection._Cast_BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection:
    """Special nested class for casting BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection to subclasses."""

    __parent__: "BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection"

    @property
    def bevel_differential_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7577.BevelDifferentialGearCompoundAdvancedSystemDeflection":
        return self.__parent__._cast(
            _7577.BevelDifferentialGearCompoundAdvancedSystemDeflection
        )

    @property
    def bevel_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7582.BevelGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7582,
        )

        return self.__parent__._cast(_7582.BevelGearCompoundAdvancedSystemDeflection)

    @property
    def agma_gleason_conical_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7570.AGMAGleasonConicalGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7570,
        )

        return self.__parent__._cast(
            _7570.AGMAGleasonConicalGearCompoundAdvancedSystemDeflection
        )

    @property
    def conical_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7598.ConicalGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7598,
        )

        return self.__parent__._cast(_7598.ConicalGearCompoundAdvancedSystemDeflection)

    @property
    def gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7624.GearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7624,
        )

        return self.__parent__._cast(_7624.GearCompoundAdvancedSystemDeflection)

    @property
    def mountable_component_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7645.MountableComponentCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7645,
        )

        return self.__parent__._cast(
            _7645.MountableComponentCompoundAdvancedSystemDeflection
        )

    @property
    def component_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7591.ComponentCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7591,
        )

        return self.__parent__._cast(_7591.ComponentCompoundAdvancedSystemDeflection)

    @property
    def part_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7647.PartCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7647,
        )

        return self.__parent__._cast(_7647.PartCompoundAdvancedSystemDeflection)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7720.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7720,
        )

        return self.__parent__._cast(_7720.PartCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7717.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7717,
        )

        return self.__parent__._cast(_7717.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2740.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2740

        return self.__parent__._cast(_2740.DesignEntityAnalysis)

    @property
    def bevel_differential_planet_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection":
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
class BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection(
    _7577.BevelDifferentialGearCompoundAdvancedSystemDeflection
):
    """BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _BEVEL_DIFFERENTIAL_PLANET_GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_7445.BevelDifferentialPlanetGearAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialPlanetGearAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_7445.BevelDifferentialPlanetGearAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialPlanetGearAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection
        """
        return _Cast_BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection(self)
