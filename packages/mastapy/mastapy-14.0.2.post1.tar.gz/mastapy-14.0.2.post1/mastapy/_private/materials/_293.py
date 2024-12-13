"""SafetyFactorItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_SAFETY_FACTOR_ITEM = python_net_import("SMT.MastaAPI.Materials", "SafetyFactorItem")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.materials import _263, _266, _267

    Self = TypeVar("Self", bound="SafetyFactorItem")
    CastSelf = TypeVar("CastSelf", bound="SafetyFactorItem._Cast_SafetyFactorItem")


__docformat__ = "restructuredtext en"
__all__ = ("SafetyFactorItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SafetyFactorItem:
    """Special nested class for casting SafetyFactorItem to subclasses."""

    __parent__: "SafetyFactorItem"

    @property
    def composite_fatigue_safety_factor_item(
        self: "CastSelf",
    ) -> "_263.CompositeFatigueSafetyFactorItem":
        from mastapy._private.materials import _263

        return self.__parent__._cast(_263.CompositeFatigueSafetyFactorItem)

    @property
    def fatigue_safety_factor_item(self: "CastSelf") -> "_266.FatigueSafetyFactorItem":
        from mastapy._private.materials import _266

        return self.__parent__._cast(_266.FatigueSafetyFactorItem)

    @property
    def fatigue_safety_factor_item_base(
        self: "CastSelf",
    ) -> "_267.FatigueSafetyFactorItemBase":
        from mastapy._private.materials import _267

        return self.__parent__._cast(_267.FatigueSafetyFactorItemBase)

    @property
    def safety_factor_item(self: "CastSelf") -> "SafetyFactorItem":
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
class SafetyFactorItem(_0.APIBase):
    """SafetyFactorItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SAFETY_FACTOR_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Damage")

        if temp is None:
            return 0.0

        return temp

    @property
    def description(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Description")

        if temp is None:
            return ""

        return temp

    @property
    def minimum_required_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumRequiredSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Reliability")

        if temp is None:
            return 0.0

        return temp

    @property
    def safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def time_until_failure(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeUntilFailure")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_SafetyFactorItem":
        """Cast to another type.

        Returns:
            _Cast_SafetyFactorItem
        """
        return _Cast_SafetyFactorItem(self)
