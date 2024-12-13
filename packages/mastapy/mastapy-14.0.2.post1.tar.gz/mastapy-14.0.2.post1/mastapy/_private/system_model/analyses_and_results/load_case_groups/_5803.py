"""SubGroupInSingleDesignState"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.load_case_groups import _5794

_SUB_GROUP_IN_SINGLE_DESIGN_STATE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups",
    "SubGroupInSingleDesignState",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.load_case_groups import (
        _5795,
        _5796,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _6957

    Self = TypeVar("Self", bound="SubGroupInSingleDesignState")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SubGroupInSingleDesignState._Cast_SubGroupInSingleDesignState",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SubGroupInSingleDesignState",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SubGroupInSingleDesignState:
    """Special nested class for casting SubGroupInSingleDesignState to subclasses."""

    __parent__: "SubGroupInSingleDesignState"

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
    def sub_group_in_single_design_state(
        self: "CastSelf",
    ) -> "SubGroupInSingleDesignState":
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
class SubGroupInSingleDesignState(_5794.AbstractDesignStateLoadCaseGroup):
    """SubGroupInSingleDesignState

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SUB_GROUP_IN_SINGLE_DESIGN_STATE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def cast_to(self: "Self") -> "_Cast_SubGroupInSingleDesignState":
        """Cast to another type.

        Returns:
            _Cast_SubGroupInSingleDesignState
        """
        return _Cast_SubGroupInSingleDesignState(self)
