"""BevelGearRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating.agma_gleason_conical import _579

_BEVEL_GEAR_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Bevel", "BevelGearRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1255
    from mastapy._private.gears.rating import _366, _374
    from mastapy._private.gears.rating.conical import _553
    from mastapy._private.gears.rating.spiral_bevel import _416
    from mastapy._private.gears.rating.straight_bevel import _409
    from mastapy._private.gears.rating.zerol_bevel import _383

    Self = TypeVar("Self", bound="BevelGearRating")
    CastSelf = TypeVar("CastSelf", bound="BevelGearRating._Cast_BevelGearRating")


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearRating:
    """Special nested class for casting BevelGearRating to subclasses."""

    __parent__: "BevelGearRating"

    @property
    def agma_gleason_conical_gear_rating(
        self: "CastSelf",
    ) -> "_579.AGMAGleasonConicalGearRating":
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
    def zerol_bevel_gear_rating(self: "CastSelf") -> "_383.ZerolBevelGearRating":
        from mastapy._private.gears.rating.zerol_bevel import _383

        return self.__parent__._cast(_383.ZerolBevelGearRating)

    @property
    def straight_bevel_gear_rating(self: "CastSelf") -> "_409.StraightBevelGearRating":
        from mastapy._private.gears.rating.straight_bevel import _409

        return self.__parent__._cast(_409.StraightBevelGearRating)

    @property
    def spiral_bevel_gear_rating(self: "CastSelf") -> "_416.SpiralBevelGearRating":
        from mastapy._private.gears.rating.spiral_bevel import _416

        return self.__parent__._cast(_416.SpiralBevelGearRating)

    @property
    def bevel_gear_rating(self: "CastSelf") -> "BevelGearRating":
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
class BevelGearRating(_579.AGMAGleasonConicalGearRating):
    """BevelGearRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_BevelGearRating":
        """Cast to another type.

        Returns:
            _Cast_BevelGearRating
        """
        return _Cast_BevelGearRating(self)
