"""ISO63362019GearSingleFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.cylindrical.iso6336 import _526

_ISO63362019_GEAR_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336", "ISO63362019GearSingleFlankRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _377
    from mastapy._private.gears.rating.cylindrical import _478
    from mastapy._private.gears.rating.cylindrical.iso6336 import _530, _532

    Self = TypeVar("Self", bound="ISO63362019GearSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO63362019GearSingleFlankRating._Cast_ISO63362019GearSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO63362019GearSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO63362019GearSingleFlankRating:
    """Special nested class for casting ISO63362019GearSingleFlankRating to subclasses."""

    __parent__: "ISO63362019GearSingleFlankRating"

    @property
    def iso63362006_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_526.ISO63362006GearSingleFlankRating":
        return self.__parent__._cast(_526.ISO63362006GearSingleFlankRating)

    @property
    def iso6336_abstract_metal_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_532.ISO6336AbstractMetalGearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _532

        return self.__parent__._cast(_532.ISO6336AbstractMetalGearSingleFlankRating)

    @property
    def iso6336_abstract_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_530.ISO6336AbstractGearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _530

        return self.__parent__._cast(_530.ISO6336AbstractGearSingleFlankRating)

    @property
    def cylindrical_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_478.CylindricalGearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical import _478

        return self.__parent__._cast(_478.CylindricalGearSingleFlankRating)

    @property
    def gear_single_flank_rating(self: "CastSelf") -> "_377.GearSingleFlankRating":
        from mastapy._private.gears.rating import _377

        return self.__parent__._cast(_377.GearSingleFlankRating)

    @property
    def iso63362019_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "ISO63362019GearSingleFlankRating":
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
class ISO63362019GearSingleFlankRating(_526.ISO63362006GearSingleFlankRating):
    """ISO63362019GearSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO63362019_GEAR_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def load_distribution_influence_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadDistributionInfluenceFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ISO63362019GearSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_ISO63362019GearSingleFlankRating
        """
        return _Cast_ISO63362019GearSingleFlankRating(self)
