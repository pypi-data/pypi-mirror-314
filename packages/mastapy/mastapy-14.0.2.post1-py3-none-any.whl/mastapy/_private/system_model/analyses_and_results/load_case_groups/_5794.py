"""AbstractDesignStateLoadCaseGroup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.load_case_groups import _5796

_ABSTRACT_DESIGN_STATE_LOAD_CASE_GROUP = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups",
    "AbstractDesignStateLoadCaseGroup",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.load_case_groups import (
        _5795,
        _5799,
        _5803,
    )

    Self = TypeVar("Self", bound="AbstractDesignStateLoadCaseGroup")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractDesignStateLoadCaseGroup._Cast_AbstractDesignStateLoadCaseGroup",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractDesignStateLoadCaseGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractDesignStateLoadCaseGroup:
    """Special nested class for casting AbstractDesignStateLoadCaseGroup to subclasses."""

    __parent__: "AbstractDesignStateLoadCaseGroup"

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
    def design_state(self: "CastSelf") -> "_5799.DesignState":
        from mastapy._private.system_model.analyses_and_results.load_case_groups import (
            _5799,
        )

        return self.__parent__._cast(_5799.DesignState)

    @property
    def sub_group_in_single_design_state(
        self: "CastSelf",
    ) -> "_5803.SubGroupInSingleDesignState":
        from mastapy._private.system_model.analyses_and_results.load_case_groups import (
            _5803,
        )

        return self.__parent__._cast(_5803.SubGroupInSingleDesignState)

    @property
    def abstract_design_state_load_case_group(
        self: "CastSelf",
    ) -> "AbstractDesignStateLoadCaseGroup":
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
class AbstractDesignStateLoadCaseGroup(_5796.AbstractStaticLoadCaseGroup):
    """AbstractDesignStateLoadCaseGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_DESIGN_STATE_LOAD_CASE_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def two_d_drawing_showing_power_flow(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TwoDDrawingShowingPowerFlow")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Ratio")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractDesignStateLoadCaseGroup":
        """Cast to another type.

        Returns:
            _Cast_AbstractDesignStateLoadCaseGroup
        """
        return _Cast_AbstractDesignStateLoadCaseGroup(self)
