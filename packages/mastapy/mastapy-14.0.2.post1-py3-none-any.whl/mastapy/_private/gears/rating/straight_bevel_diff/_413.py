"""StraightBevelDiffGearSetRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.conical import _555

_STRAIGHT_BEVEL_DIFF_GEAR_SET_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.StraightBevelDiff", "StraightBevelDiffGearSetRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1257
    from mastapy._private.gears.gear_designs.straight_bevel_diff import _993
    from mastapy._private.gears.rating import _367, _376
    from mastapy._private.gears.rating.straight_bevel_diff import _411, _412

    Self = TypeVar("Self", bound="StraightBevelDiffGearSetRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelDiffGearSetRating._Cast_StraightBevelDiffGearSetRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelDiffGearSetRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelDiffGearSetRating:
    """Special nested class for casting StraightBevelDiffGearSetRating to subclasses."""

    __parent__: "StraightBevelDiffGearSetRating"

    @property
    def conical_gear_set_rating(self: "CastSelf") -> "_555.ConicalGearSetRating":
        return self.__parent__._cast(_555.ConicalGearSetRating)

    @property
    def gear_set_rating(self: "CastSelf") -> "_376.GearSetRating":
        from mastapy._private.gears.rating import _376

        return self.__parent__._cast(_376.GearSetRating)

    @property
    def abstract_gear_set_rating(self: "CastSelf") -> "_367.AbstractGearSetRating":
        from mastapy._private.gears.rating import _367

        return self.__parent__._cast(_367.AbstractGearSetRating)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1257.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1257

        return self.__parent__._cast(_1257.AbstractGearSetAnalysis)

    @property
    def straight_bevel_diff_gear_set_rating(
        self: "CastSelf",
    ) -> "StraightBevelDiffGearSetRating":
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
class StraightBevelDiffGearSetRating(_555.ConicalGearSetRating):
    """StraightBevelDiffGearSetRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_DIFF_GEAR_SET_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def rating(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rating")

        if temp is None:
            return ""

        return temp

    @property
    def straight_bevel_diff_gear_set(
        self: "Self",
    ) -> "_993.StraightBevelDiffGearSetDesign":
        """mastapy.gears.gear_designs.straight_bevel_diff.StraightBevelDiffGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelDiffGearSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def straight_bevel_diff_gear_ratings(
        self: "Self",
    ) -> "List[_412.StraightBevelDiffGearRating]":
        """List[mastapy.gears.rating.straight_bevel_diff.StraightBevelDiffGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelDiffGearRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def straight_bevel_diff_mesh_ratings(
        self: "Self",
    ) -> "List[_411.StraightBevelDiffGearMeshRating]":
        """List[mastapy.gears.rating.straight_bevel_diff.StraightBevelDiffGearMeshRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelDiffMeshRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelDiffGearSetRating":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelDiffGearSetRating
        """
        return _Cast_StraightBevelDiffGearSetRating(self)
