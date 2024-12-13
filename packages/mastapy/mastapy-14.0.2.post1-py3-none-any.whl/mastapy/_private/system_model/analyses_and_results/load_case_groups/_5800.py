"""DutyCycle"""

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
from mastapy._private.system_model.analyses_and_results.load_case_groups import _5796

_DUTY_CYCLE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups", "DutyCycle"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.load_case_groups import (
        _5795,
        _5803,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _6957
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
        _7156,
    )

    Self = TypeVar("Self", bound="DutyCycle")
    CastSelf = TypeVar("CastSelf", bound="DutyCycle._Cast_DutyCycle")


__docformat__ = "restructuredtext en"
__all__ = ("DutyCycle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DutyCycle:
    """Special nested class for casting DutyCycle to subclasses."""

    __parent__: "DutyCycle"

    @property
    def abstract_static_load_case_group(
        self: "CastSelf",
    ) -> "_5796.AbstractStaticLoadCaseGroup":
        return self.__parent__._cast(_5796.AbstractStaticLoadCaseGroup)

    @property
    def abstract_load_case_group(self: "CastSelf") -> "_5795.AbstractLoadCaseGroup":
        from mastapy._private.system_model.analyses_and_results.load_case_groups import (
            _5795,
        )

        return self.__parent__._cast(_5795.AbstractLoadCaseGroup)

    @property
    def duty_cycle(self: "CastSelf") -> "DutyCycle":
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
class DutyCycle(_5796.AbstractStaticLoadCaseGroup):
    """DutyCycle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DUTY_CYCLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def duty_cycle_design_states(
        self: "Self",
    ) -> "List[_5803.SubGroupInSingleDesignState]":
        """List[mastapy.system_model.analyses_and_results.load_case_groups.SubGroupInSingleDesignState]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DutyCycleDesignStates")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def time_series_importer(self: "Self") -> "_7156.TimeSeriesImporter":
        """mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition.TimeSeriesImporter

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeSeriesImporter")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    def convert_to_condensed_parametric_study_tool_duty_cycle(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "ConvertToCondensedParametricStudyToolDutyCycle"
        )

    @enforce_parameter_types
    def add_static_load(self: "Self", static_load: "_6957.StaticLoadCase") -> None:
        """Method does not return.

        Args:
            static_load (mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase)
        """
        pythonnet_method_call(
            self.wrapped, "AddStaticLoad", static_load.wrapped if static_load else None
        )

    def delete(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Delete")

    @enforce_parameter_types
    def remove_design_state_sub_group(
        self: "Self", sub_group: "_5803.SubGroupInSingleDesignState"
    ) -> None:
        """Method does not return.

        Args:
            sub_group (mastapy.system_model.analyses_and_results.load_case_groups.SubGroupInSingleDesignState)
        """
        pythonnet_method_call(
            self.wrapped,
            "RemoveDesignStateSubGroup",
            sub_group.wrapped if sub_group else None,
        )

    @enforce_parameter_types
    def remove_static_load(self: "Self", static_load: "_6957.StaticLoadCase") -> None:
        """Method does not return.

        Args:
            static_load (mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase)
        """
        pythonnet_method_call(
            self.wrapped,
            "RemoveStaticLoad",
            static_load.wrapped if static_load else None,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_DutyCycle":
        """Cast to another type.

        Returns:
            _Cast_DutyCycle
        """
        return _Cast_DutyCycle(self)
