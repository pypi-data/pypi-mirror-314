"""GearOrderForTE"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.utility.modal_analysis.gears import _1859

_GEAR_ORDER_FOR_TE = python_net_import(
    "SMT.MastaAPI.Utility.ModalAnalysis.Gears", "GearOrderForTE"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.utility.modal_analysis.gears import _1854, _1857

    Self = TypeVar("Self", bound="GearOrderForTE")
    CastSelf = TypeVar("CastSelf", bound="GearOrderForTE._Cast_GearOrderForTE")


__docformat__ = "restructuredtext en"
__all__ = ("GearOrderForTE",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearOrderForTE:
    """Special nested class for casting GearOrderForTE to subclasses."""

    __parent__: "GearOrderForTE"

    @property
    def order_with_radius(self: "CastSelf") -> "_1859.OrderWithRadius":
        return self.__parent__._cast(_1859.OrderWithRadius)

    @property
    def order_for_te(self: "CastSelf") -> "_1857.OrderForTE":
        return self.__parent__._cast(_1857.OrderForTE)

    @property
    def gear_order_for_te(self: "CastSelf") -> "GearOrderForTE":
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
class GearOrderForTE(_1859.OrderWithRadius):
    """GearOrderForTE

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_ORDER_FOR_TE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def number_of_teeth(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @property
    def position(self: "Self") -> "_1854.GearPositions":
        """mastapy.utility.modal_analysis.gears.GearPositions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Position")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.ModalAnalysis.Gears.GearPositions"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility.modal_analysis.gears._1854", "GearPositions"
        )(value)

    @property
    def additional_orders_and_harmonics(self: "Self") -> "List[_1857.OrderForTE]":
        """List[mastapy.utility.modal_analysis.gears.OrderForTE]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AdditionalOrdersAndHarmonics")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_GearOrderForTE":
        """Cast to another type.

        Returns:
            _Cast_GearOrderForTE
        """
        return _Cast_GearOrderForTE(self)
