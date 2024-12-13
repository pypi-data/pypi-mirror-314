"""RootAssemblyCompoundPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
    _4285,
)

_ROOT_ASSEMBLY_COMPOUND_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound",
    "RootAssemblyCompoundPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups import (
        _5796,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4242
    from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
        _4278,
        _4359,
    )

    Self = TypeVar("Self", bound="RootAssemblyCompoundPowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RootAssemblyCompoundPowerFlow._Cast_RootAssemblyCompoundPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RootAssemblyCompoundPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RootAssemblyCompoundPowerFlow:
    """Special nested class for casting RootAssemblyCompoundPowerFlow to subclasses."""

    __parent__: "RootAssemblyCompoundPowerFlow"

    @property
    def assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "_4285.AssemblyCompoundPowerFlow":
        return self.__parent__._cast(_4285.AssemblyCompoundPowerFlow)

    @property
    def abstract_assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "_4278.AbstractAssemblyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4278,
        )

        return self.__parent__._cast(_4278.AbstractAssemblyCompoundPowerFlow)

    @property
    def part_compound_power_flow(self: "CastSelf") -> "_4359.PartCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4359,
        )

        return self.__parent__._cast(_4359.PartCompoundPowerFlow)

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
    def root_assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "RootAssemblyCompoundPowerFlow":
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
class RootAssemblyCompoundPowerFlow(_4285.AssemblyCompoundPowerFlow):
    """RootAssemblyCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROOT_ASSEMBLY_COMPOUND_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def compound_static_load(self: "Self") -> "_5796.AbstractStaticLoadCaseGroup":
        """mastapy.system_model.analyses_and_results.load_case_groups.AbstractStaticLoadCaseGroup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CompoundStaticLoad")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4242.RootAssemblyPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.RootAssemblyPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases(self: "Self") -> "List[_4242.RootAssemblyPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.RootAssemblyPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    def set_face_widths_for_specified_safety_factors(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SetFaceWidthsForSpecifiedSafetyFactors")

    @property
    def cast_to(self: "Self") -> "_Cast_RootAssemblyCompoundPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_RootAssemblyCompoundPowerFlow
        """
        return _Cast_RootAssemblyCompoundPowerFlow(self)
