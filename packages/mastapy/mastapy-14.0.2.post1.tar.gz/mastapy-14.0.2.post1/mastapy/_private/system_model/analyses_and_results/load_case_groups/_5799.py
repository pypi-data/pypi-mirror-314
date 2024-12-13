"""DesignState"""

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
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.load_case_groups import _5794

_DESIGN_STATE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups", "DesignState"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.load_case_groups import (
        _5795,
        _5796,
        _5797,
        _5798,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _6957
    from mastapy._private.system_model.connections_and_sockets.couplings import _2399
    from mastapy._private.system_model.part_model.gears import _2586

    Self = TypeVar("Self", bound="DesignState")
    CastSelf = TypeVar("CastSelf", bound="DesignState._Cast_DesignState")


__docformat__ = "restructuredtext en"
__all__ = ("DesignState",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DesignState:
    """Special nested class for casting DesignState to subclasses."""

    __parent__: "DesignState"

    @property
    def abstract_design_state_load_case_group(
        self: "CastSelf",
    ) -> "_5794.AbstractDesignStateLoadCaseGroup":
        return self.__parent__._cast(_5794.AbstractDesignStateLoadCaseGroup)

    @property
    def abstract_static_load_case_group(
        self: "CastSelf",
    ) -> "_5796.AbstractStaticLoadCaseGroup":
        from mastapy._private.system_model.analyses_and_results.load_case_groups import (
            _5796,
        )

        return self.__parent__._cast(_5796.AbstractStaticLoadCaseGroup)

    @property
    def abstract_load_case_group(self: "CastSelf") -> "_5795.AbstractLoadCaseGroup":
        from mastapy._private.system_model.analyses_and_results.load_case_groups import (
            _5795,
        )

        return self.__parent__._cast(_5795.AbstractLoadCaseGroup)

    @property
    def design_state(self: "CastSelf") -> "DesignState":
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
class DesignState(_5794.AbstractDesignStateLoadCaseGroup):
    """DesignState

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DESIGN_STATE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def clutches(self: "Self") -> "List[_5797.ClutchEngagementStatus]":
        """List[mastapy.system_model.analyses_and_results.load_case_groups.ClutchEngagementStatus]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Clutches")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def concept_synchro_mounted_gears(
        self: "Self",
    ) -> "List[_5798.ConceptSynchroGearEngagementStatus]":
        """List[mastapy.system_model.analyses_and_results.load_case_groups.ConceptSynchroGearEngagementStatus]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConceptSynchroMountedGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @enforce_parameter_types
    def clutch_engagement_status_for(
        self: "Self", clutch_connection: "_2399.ClutchConnection"
    ) -> "_5797.ClutchEngagementStatus":
        """mastapy.system_model.analyses_and_results.load_case_groups.ClutchEngagementStatus

        Args:
            clutch_connection (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "ClutchEngagementStatusFor",
            clutch_connection.wrapped if clutch_connection else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def concept_synchro_gear_engagement_status_for(
        self: "Self", gear: "_2586.CylindricalGear"
    ) -> "_5798.ConceptSynchroGearEngagementStatus":
        """mastapy.system_model.analyses_and_results.load_case_groups.ConceptSynchroGearEngagementStatus

        Args:
            gear (mastapy.system_model.part_model.gears.CylindricalGear)
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "ConceptSynchroGearEngagementStatusFor",
            gear.wrapped if gear else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def create_load_case(
        self: "Self", name: "str" = "New Static Load"
    ) -> "_6957.StaticLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "CreateLoadCase", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    def delete(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Delete")

    @enforce_parameter_types
    def duplicate(self: "Self", duplicate_static_loads: "bool" = True) -> "DesignState":
        """mastapy.system_model.analyses_and_results.load_case_groups.DesignState

        Args:
            duplicate_static_loads (bool, optional)
        """
        duplicate_static_loads = bool(duplicate_static_loads)
        method_result = pythonnet_method_call(
            self.wrapped,
            "Duplicate",
            duplicate_static_loads if duplicate_static_loads else False,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_DesignState":
        """Cast to another type.

        Returns:
            _Cast_DesignState
        """
        return _Cast_DesignState(self)
