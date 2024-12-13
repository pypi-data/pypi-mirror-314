"""CompositeFatigueSafetyFactorItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.materials import _266

_COMPOSITE_FATIGUE_SAFETY_FACTOR_ITEM = python_net_import(
    "SMT.MastaAPI.Materials", "CompositeFatigueSafetyFactorItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.materials import _267, _293

    Self = TypeVar("Self", bound="CompositeFatigueSafetyFactorItem")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CompositeFatigueSafetyFactorItem._Cast_CompositeFatigueSafetyFactorItem",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CompositeFatigueSafetyFactorItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CompositeFatigueSafetyFactorItem:
    """Special nested class for casting CompositeFatigueSafetyFactorItem to subclasses."""

    __parent__: "CompositeFatigueSafetyFactorItem"

    @property
    def fatigue_safety_factor_item(self: "CastSelf") -> "_266.FatigueSafetyFactorItem":
        return self.__parent__._cast(_266.FatigueSafetyFactorItem)

    @property
    def fatigue_safety_factor_item_base(
        self: "CastSelf",
    ) -> "_267.FatigueSafetyFactorItemBase":
        from mastapy._private.materials import _267

        return self.__parent__._cast(_267.FatigueSafetyFactorItemBase)

    @property
    def safety_factor_item(self: "CastSelf") -> "_293.SafetyFactorItem":
        from mastapy._private.materials import _293

        return self.__parent__._cast(_293.SafetyFactorItem)

    @property
    def composite_fatigue_safety_factor_item(
        self: "CastSelf",
    ) -> "CompositeFatigueSafetyFactorItem":
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
class CompositeFatigueSafetyFactorItem(_266.FatigueSafetyFactorItem):
    """CompositeFatigueSafetyFactorItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPOSITE_FATIGUE_SAFETY_FACTOR_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CompositeFatigueSafetyFactorItem":
        """Cast to another type.

        Returns:
            _Cast_CompositeFatigueSafetyFactorItem
        """
        return _Cast_CompositeFatigueSafetyFactorItem(self)
