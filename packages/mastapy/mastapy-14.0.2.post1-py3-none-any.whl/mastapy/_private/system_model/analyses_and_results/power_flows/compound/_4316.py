"""CouplingConnectionCompoundPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
    _4343,
)

_COUPLING_CONNECTION_COMPOUND_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound",
    "CouplingConnectionCompoundPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7713,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4178
    from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
        _4300,
        _4305,
        _4313,
        _4361,
        _4383,
        _4398,
    )

    Self = TypeVar("Self", bound="CouplingConnectionCompoundPowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingConnectionCompoundPowerFlow._Cast_CouplingConnectionCompoundPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingConnectionCompoundPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingConnectionCompoundPowerFlow:
    """Special nested class for casting CouplingConnectionCompoundPowerFlow to subclasses."""

    __parent__: "CouplingConnectionCompoundPowerFlow"

    @property
    def inter_mountable_component_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4343.InterMountableComponentConnectionCompoundPowerFlow":
        return self.__parent__._cast(
            _4343.InterMountableComponentConnectionCompoundPowerFlow
        )

    @property
    def connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4313.ConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4313,
        )

        return self.__parent__._cast(_4313.ConnectionCompoundPowerFlow)

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
    def clutch_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4300.ClutchConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4300,
        )

        return self.__parent__._cast(_4300.ClutchConnectionCompoundPowerFlow)

    @property
    def concept_coupling_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4305.ConceptCouplingConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4305,
        )

        return self.__parent__._cast(_4305.ConceptCouplingConnectionCompoundPowerFlow)

    @property
    def part_to_part_shear_coupling_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4361.PartToPartShearCouplingConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4361,
        )

        return self.__parent__._cast(
            _4361.PartToPartShearCouplingConnectionCompoundPowerFlow
        )

    @property
    def spring_damper_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4383.SpringDamperConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4383,
        )

        return self.__parent__._cast(_4383.SpringDamperConnectionCompoundPowerFlow)

    @property
    def torque_converter_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4398.TorqueConverterConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4398,
        )

        return self.__parent__._cast(_4398.TorqueConverterConnectionCompoundPowerFlow)

    @property
    def coupling_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "CouplingConnectionCompoundPowerFlow":
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
class CouplingConnectionCompoundPowerFlow(
    _4343.InterMountableComponentConnectionCompoundPowerFlow
):
    """CouplingConnectionCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_CONNECTION_COMPOUND_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_4178.CouplingConnectionPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.CouplingConnectionPowerFlow]

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
    ) -> "List[_4178.CouplingConnectionPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.CouplingConnectionPowerFlow]

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
    def cast_to(self: "Self") -> "_Cast_CouplingConnectionCompoundPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_CouplingConnectionCompoundPowerFlow
        """
        return _Cast_CouplingConnectionCompoundPowerFlow(self)
