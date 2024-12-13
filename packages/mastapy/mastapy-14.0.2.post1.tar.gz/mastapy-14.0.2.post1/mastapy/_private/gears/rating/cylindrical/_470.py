"""CylindricalGearFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating import _371

_CYLINDRICAL_GEAR_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "CylindricalGearFlankRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalGearFlankRating")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalGearFlankRating._Cast_CylindricalGearFlankRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearFlankRating:
    """Special nested class for casting CylindricalGearFlankRating to subclasses."""

    __parent__: "CylindricalGearFlankRating"

    @property
    def gear_flank_rating(self: "CastSelf") -> "_371.GearFlankRating":
        return self.__parent__._cast(_371.GearFlankRating)

    @property
    def cylindrical_gear_flank_rating(self: "CastSelf") -> "CylindricalGearFlankRating":
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
class CylindricalGearFlankRating(_371.GearFlankRating):
    """CylindricalGearFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def worst_dynamic_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorstDynamicFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def worst_face_load_factor_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorstFaceLoadFactorContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def worst_load_sharing_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorstLoadSharingFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearFlankRating":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearFlankRating
        """
        return _Cast_CylindricalGearFlankRating(self)
