"""SpiralBevelGearRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.bevel import _568

_SPIRAL_BEVEL_GEAR_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.SpiralBevel", "SpiralBevelGearRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1255
    from mastapy._private.gears.gear_designs.spiral_bevel import _995
    from mastapy._private.gears.rating import _366, _374
    from mastapy._private.gears.rating.agma_gleason_conical import _579
    from mastapy._private.gears.rating.conical import _553

    Self = TypeVar("Self", bound="SpiralBevelGearRating")
    CastSelf = TypeVar(
        "CastSelf", bound="SpiralBevelGearRating._Cast_SpiralBevelGearRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpiralBevelGearRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpiralBevelGearRating:
    """Special nested class for casting SpiralBevelGearRating to subclasses."""

    __parent__: "SpiralBevelGearRating"

    @property
    def bevel_gear_rating(self: "CastSelf") -> "_568.BevelGearRating":
        return self.__parent__._cast(_568.BevelGearRating)

    @property
    def agma_gleason_conical_gear_rating(
        self: "CastSelf",
    ) -> "_579.AGMAGleasonConicalGearRating":
        from mastapy._private.gears.rating.agma_gleason_conical import _579

        return self.__parent__._cast(_579.AGMAGleasonConicalGearRating)

    @property
    def conical_gear_rating(self: "CastSelf") -> "_553.ConicalGearRating":
        from mastapy._private.gears.rating.conical import _553

        return self.__parent__._cast(_553.ConicalGearRating)

    @property
    def gear_rating(self: "CastSelf") -> "_374.GearRating":
        from mastapy._private.gears.rating import _374

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
    def spiral_bevel_gear_rating(self: "CastSelf") -> "SpiralBevelGearRating":
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
class SpiralBevelGearRating(_568.BevelGearRating):
    """SpiralBevelGearRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPIRAL_BEVEL_GEAR_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def spiral_bevel_gear(self: "Self") -> "_995.SpiralBevelGearDesign":
        """mastapy.gears.gear_designs.spiral_bevel.SpiralBevelGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpiralBevelGear")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SpiralBevelGearRating":
        """Cast to another type.

        Returns:
            _Cast_SpiralBevelGearRating
        """
        return _Cast_SpiralBevelGearRating(self)
