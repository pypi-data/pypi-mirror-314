"""CouplingConnectionCriticalSpeedAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
    _6759,
)

_COUPLING_CONNECTION_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses",
    "CouplingConnectionCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2742
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6712,
        _6717,
        _6726,
        _6776,
        _6798,
        _6813,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import _2403

    Self = TypeVar("Self", bound="CouplingConnectionCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingConnectionCriticalSpeedAnalysis._Cast_CouplingConnectionCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingConnectionCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingConnectionCriticalSpeedAnalysis:
    """Special nested class for casting CouplingConnectionCriticalSpeedAnalysis to subclasses."""

    __parent__: "CouplingConnectionCriticalSpeedAnalysis"

    @property
    def inter_mountable_component_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6759.InterMountableComponentConnectionCriticalSpeedAnalysis":
        return self.__parent__._cast(
            _6759.InterMountableComponentConnectionCriticalSpeedAnalysis
        )

    @property
    def connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6726.ConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6726,
        )

        return self.__parent__._cast(_6726.ConnectionCriticalSpeedAnalysis)

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
    def clutch_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6712.ClutchConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6712,
        )

        return self.__parent__._cast(_6712.ClutchConnectionCriticalSpeedAnalysis)

    @property
    def concept_coupling_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6717.ConceptCouplingConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6717,
        )

        return self.__parent__._cast(
            _6717.ConceptCouplingConnectionCriticalSpeedAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6776.PartToPartShearCouplingConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6776,
        )

        return self.__parent__._cast(
            _6776.PartToPartShearCouplingConnectionCriticalSpeedAnalysis
        )

    @property
    def spring_damper_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6798.SpringDamperConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6798,
        )

        return self.__parent__._cast(_6798.SpringDamperConnectionCriticalSpeedAnalysis)

    @property
    def torque_converter_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6813.TorqueConverterConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6813,
        )

        return self.__parent__._cast(
            _6813.TorqueConverterConnectionCriticalSpeedAnalysis
        )

    @property
    def coupling_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "CouplingConnectionCriticalSpeedAnalysis":
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
class CouplingConnectionCriticalSpeedAnalysis(
    _6759.InterMountableComponentConnectionCriticalSpeedAnalysis
):
    """CouplingConnectionCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_CONNECTION_CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2403.CouplingConnection":
        """mastapy.system_model.connections_and_sockets.couplings.CouplingConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingConnectionCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CouplingConnectionCriticalSpeedAnalysis
        """
        return _Cast_CouplingConnectionCriticalSpeedAnalysis(self)
