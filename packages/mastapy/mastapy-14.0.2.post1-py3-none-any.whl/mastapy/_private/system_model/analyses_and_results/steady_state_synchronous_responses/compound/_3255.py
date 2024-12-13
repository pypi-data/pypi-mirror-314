"""CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponse"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
    _3235,
)

_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound",
    "CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7713,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3120,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
        _3214,
        _3246,
        _3310,
    )

    Self = TypeVar(
        "Self",
        bound="CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponse",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponse._Cast_CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = (
    "CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponse",
)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponse:
    """Special nested class for casting CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponse to subclasses."""

    __parent__: (
        "CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponse"
    )

    @property
    def coaxial_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3235.CoaxialConnectionCompoundSteadyStateSynchronousResponse":
        return self.__parent__._cast(
            _3235.CoaxialConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def shaft_to_mountable_component_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3310.ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3310,
        )

        return self.__parent__._cast(
            _3310.ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def abstract_shaft_to_mountable_component_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3214.AbstractShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3214,
        )

        return self.__parent__._cast(
            _3214.AbstractShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3246.ConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3246,
        )

        return self.__parent__._cast(
            _3246.ConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7713.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7713,
        )

        return self.__parent__._cast(_7713.ConnectionCompoundAnalysis)

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
    def cycloidal_disc_central_bearing_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponse":
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
class CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponse(
    _3235.CoaxialConnectionCompoundSteadyStateSynchronousResponse
):
    """CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_3120.CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_3120.CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponse
        """
        return _Cast_CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponse(
            self
        )
