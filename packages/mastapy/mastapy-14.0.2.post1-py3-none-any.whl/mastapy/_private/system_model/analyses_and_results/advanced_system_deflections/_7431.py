"""AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
    _7466,
)

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_ADVANCED_SYSTEM_DEFLECTION = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections",
        "AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection",
    )
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2742
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7455,
        _7477,
        _7478,
        _7519,
        _7533,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.connections_and_sockets import _2322

    Self = TypeVar(
        "Self",
        bound="AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection._Cast_AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection:
    """Special nested class for casting AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection to subclasses."""

    __parent__: "AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection"

    @property
    def connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7466.ConnectionAdvancedSystemDeflection":
        return self.__parent__._cast(_7466.ConnectionAdvancedSystemDeflection)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7715.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7715,
        )

        return self.__parent__._cast(_7715.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7712.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7712,
        )

        return self.__parent__._cast(_7712.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2738.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2738

        return self.__parent__._cast(_2738.ConnectionAnalysis)

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
    def coaxial_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7455.CoaxialConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7455,
        )

        return self.__parent__._cast(_7455.CoaxialConnectionAdvancedSystemDeflection)

    @property
    def cycloidal_disc_central_bearing_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7477.CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7477,
        )

        return self.__parent__._cast(
            _7477.CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7478.CycloidalDiscPlanetaryBearingConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7478,
        )

        return self.__parent__._cast(
            _7478.CycloidalDiscPlanetaryBearingConnectionAdvancedSystemDeflection
        )

    @property
    def planetary_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7519.PlanetaryConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7519,
        )

        return self.__parent__._cast(_7519.PlanetaryConnectionAdvancedSystemDeflection)

    @property
    def shaft_to_mountable_component_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7533.ShaftToMountableComponentConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7533,
        )

        return self.__parent__._cast(
            _7533.ShaftToMountableComponentConnectionAdvancedSystemDeflection
        )

    @property
    def abstract_shaft_to_mountable_component_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection":
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
class AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection(
    _7466.ConnectionAdvancedSystemDeflection
):
    """AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_ADVANCED_SYSTEM_DEFLECTION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(
        self: "Self",
    ) -> "_2322.AbstractShaftToMountableComponentConnection":
        """mastapy.system_model.connections_and_sockets.AbstractShaftToMountableComponentConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection
        """
        return (
            _Cast_AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection(
                self
            )
        )
