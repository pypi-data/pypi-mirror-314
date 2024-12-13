"""StraightBevelDiffGearRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.conical import _553

_STRAIGHT_BEVEL_DIFF_GEAR_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.StraightBevelDiff", "StraightBevelDiffGearRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1255
    from mastapy._private.gears.gear_designs.straight_bevel_diff import _991
    from mastapy._private.gears.rating import _366, _374

    Self = TypeVar("Self", bound="StraightBevelDiffGearRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelDiffGearRating._Cast_StraightBevelDiffGearRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelDiffGearRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelDiffGearRating:
    """Special nested class for casting StraightBevelDiffGearRating to subclasses."""

    __parent__: "StraightBevelDiffGearRating"

    @property
    def conical_gear_rating(self: "CastSelf") -> "_553.ConicalGearRating":
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
    def straight_bevel_diff_gear_rating(
        self: "CastSelf",
    ) -> "StraightBevelDiffGearRating":
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
class StraightBevelDiffGearRating(_553.ConicalGearRating):
    """StraightBevelDiffGearRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_DIFF_GEAR_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cycles_to_fail(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CyclesToFail")

        if temp is None:
            return 0.0

        return temp

    @property
    def cycles_to_fail_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CyclesToFailBending")

        if temp is None:
            return 0.0

        return temp

    @property
    def cycles_to_fail_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CyclesToFailContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def time_to_fail(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeToFail")

        if temp is None:
            return 0.0

        return temp

    @property
    def time_to_fail_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeToFailBending")

        if temp is None:
            return 0.0

        return temp

    @property
    def time_to_fail_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeToFailContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def straight_bevel_diff_gear(self: "Self") -> "_991.StraightBevelDiffGearDesign":
        """mastapy.gears.gear_designs.straight_bevel_diff.StraightBevelDiffGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelDiffGear")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelDiffGearRating":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelDiffGearRating
        """
        return _Cast_StraightBevelDiffGearRating(self)
