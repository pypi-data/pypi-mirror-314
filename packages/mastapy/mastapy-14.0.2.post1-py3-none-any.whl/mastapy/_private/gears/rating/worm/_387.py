"""WormGearRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating import _374

_WORM_GEAR_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Worm", "WormGearRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1255
    from mastapy._private.gears.gear_designs.worm import _983
    from mastapy._private.gears.rating import _366, _371

    Self = TypeVar("Self", bound="WormGearRating")
    CastSelf = TypeVar("CastSelf", bound="WormGearRating._Cast_WormGearRating")


__docformat__ = "restructuredtext en"
__all__ = ("WormGearRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormGearRating:
    """Special nested class for casting WormGearRating to subclasses."""

    __parent__: "WormGearRating"

    @property
    def gear_rating(self: "CastSelf") -> "_374.GearRating":
        return self.__parent__._cast(_374.GearRating)

    @property
    def abstract_gear_rating(self: "CastSelf") -> "_366.AbstractGearRating":
        from mastapy._private.gears.rating import _366

        return self.__parent__._cast(_366.AbstractGearRating)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1255.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1255

        return self.__parent__._cast(_1255.AbstractGearAnalysis)

    @property
    def worm_gear_rating(self: "CastSelf") -> "WormGearRating":
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
class WormGearRating(_374.GearRating):
    """WormGearRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_GEAR_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def left_flank_rating(self: "Self") -> "_371.GearFlankRating":
        """mastapy.gears.rating.GearFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftFlankRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def right_flank_rating(self: "Self") -> "_371.GearFlankRating":
        """mastapy.gears.rating.GearFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightFlankRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def worm_gear(self: "Self") -> "_983.WormGearDesign":
        """mastapy.gears.gear_designs.worm.WormGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormGear")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_WormGearRating":
        """Cast to another type.

        Returns:
            _Cast_WormGearRating
        """
        return _Cast_WormGearRating(self)
