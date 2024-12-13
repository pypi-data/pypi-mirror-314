"""AbstractShaftToMountableComponentConnectionCompoundModalAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
    _4882,
)

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_MODAL_ANALYSIS = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound",
        "AbstractShaftToMountableComponentConnectionCompoundModalAnalysis",
    )
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7713,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4692
    from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
        _4871,
        _4891,
        _4893,
        _4932,
        _4946,
    )

    Self = TypeVar(
        "Self", bound="AbstractShaftToMountableComponentConnectionCompoundModalAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftToMountableComponentConnectionCompoundModalAnalysis._Cast_AbstractShaftToMountableComponentConnectionCompoundModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftToMountableComponentConnectionCompoundModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftToMountableComponentConnectionCompoundModalAnalysis:
    """Special nested class for casting AbstractShaftToMountableComponentConnectionCompoundModalAnalysis to subclasses."""

    __parent__: "AbstractShaftToMountableComponentConnectionCompoundModalAnalysis"

    @property
    def connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4882.ConnectionCompoundModalAnalysis":
        return self.__parent__._cast(_4882.ConnectionCompoundModalAnalysis)

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
    def coaxial_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4871.CoaxialConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4871,
        )

        return self.__parent__._cast(_4871.CoaxialConnectionCompoundModalAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4891.CycloidalDiscCentralBearingConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4891,
        )

        return self.__parent__._cast(
            _4891.CycloidalDiscCentralBearingConnectionCompoundModalAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4893.CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4893,
        )

        return self.__parent__._cast(
            _4893.CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysis
        )

    @property
    def planetary_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4932.PlanetaryConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4932,
        )

        return self.__parent__._cast(_4932.PlanetaryConnectionCompoundModalAnalysis)

    @property
    def shaft_to_mountable_component_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4946.ShaftToMountableComponentConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4946,
        )

        return self.__parent__._cast(
            _4946.ShaftToMountableComponentConnectionCompoundModalAnalysis
        )

    @property
    def abstract_shaft_to_mountable_component_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "AbstractShaftToMountableComponentConnectionCompoundModalAnalysis":
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
class AbstractShaftToMountableComponentConnectionCompoundModalAnalysis(
    _4882.ConnectionCompoundModalAnalysis
):
    """AbstractShaftToMountableComponentConnectionCompoundModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_MODAL_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_4692.AbstractShaftToMountableComponentConnectionModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.AbstractShaftToMountableComponentConnectionModalAnalysis]

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
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4692.AbstractShaftToMountableComponentConnectionModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.AbstractShaftToMountableComponentConnectionModalAnalysis]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_AbstractShaftToMountableComponentConnectionCompoundModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftToMountableComponentConnectionCompoundModalAnalysis
        """
        return _Cast_AbstractShaftToMountableComponentConnectionCompoundModalAnalysis(
            self
        )
