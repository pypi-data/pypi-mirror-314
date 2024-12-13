"""AbstractShaftPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows import _4142

_ABSTRACT_SHAFT_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "AbstractShaftPowerFlow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740, _2742, _2746
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7719,
        _7722,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4166,
        _4187,
        _4225,
        _4244,
    )
    from mastapy._private.system_model.part_model import _2493

    Self = TypeVar("Self", bound="AbstractShaftPowerFlow")
    CastSelf = TypeVar(
        "CastSelf", bound="AbstractShaftPowerFlow._Cast_AbstractShaftPowerFlow"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftPowerFlow:
    """Special nested class for casting AbstractShaftPowerFlow to subclasses."""

    __parent__: "AbstractShaftPowerFlow"

    @property
    def abstract_shaft_or_housing_power_flow(
        self: "CastSelf",
    ) -> "_4142.AbstractShaftOrHousingPowerFlow":
        return self.__parent__._cast(_4142.AbstractShaftOrHousingPowerFlow)

    @property
    def component_power_flow(self: "CastSelf") -> "_4166.ComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4166

        return self.__parent__._cast(_4166.ComponentPowerFlow)

    @property
    def part_power_flow(self: "CastSelf") -> "_4225.PartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4225

        return self.__parent__._cast(_4225.PartPowerFlow)

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
    def cycloidal_disc_power_flow(self: "CastSelf") -> "_4187.CycloidalDiscPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4187

        return self.__parent__._cast(_4187.CycloidalDiscPowerFlow)

    @property
    def shaft_power_flow(self: "CastSelf") -> "_4244.ShaftPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4244

        return self.__parent__._cast(_4244.ShaftPowerFlow)

    @property
    def abstract_shaft_power_flow(self: "CastSelf") -> "AbstractShaftPowerFlow":
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
class AbstractShaftPowerFlow(_4142.AbstractShaftOrHousingPowerFlow):
    """AbstractShaftPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_SHAFT_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2493.AbstractShaft":
        """mastapy.system_model.part_model.AbstractShaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractShaftPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftPowerFlow
        """
        return _Cast_AbstractShaftPowerFlow(self)
