"""SpiralBevelGearSetRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.bevel import _569

_SPIRAL_BEVEL_GEAR_SET_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.SpiralBevel", "SpiralBevelGearSetRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1257
    from mastapy._private.gears.gear_designs.spiral_bevel import _997
    from mastapy._private.gears.rating import _367, _376
    from mastapy._private.gears.rating.agma_gleason_conical import _580
    from mastapy._private.gears.rating.conical import _555
    from mastapy._private.gears.rating.spiral_bevel import _415, _416

    Self = TypeVar("Self", bound="SpiralBevelGearSetRating")
    CastSelf = TypeVar(
        "CastSelf", bound="SpiralBevelGearSetRating._Cast_SpiralBevelGearSetRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpiralBevelGearSetRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpiralBevelGearSetRating:
    """Special nested class for casting SpiralBevelGearSetRating to subclasses."""

    __parent__: "SpiralBevelGearSetRating"

    @property
    def bevel_gear_set_rating(self: "CastSelf") -> "_569.BevelGearSetRating":
        return self.__parent__._cast(_569.BevelGearSetRating)

    @property
    def agma_gleason_conical_gear_set_rating(
        self: "CastSelf",
    ) -> "_580.AGMAGleasonConicalGearSetRating":
        from mastapy._private.gears.rating.agma_gleason_conical import _580

        return self.__parent__._cast(_580.AGMAGleasonConicalGearSetRating)

    @property
    def conical_gear_set_rating(self: "CastSelf") -> "_555.ConicalGearSetRating":
        from mastapy._private.gears.rating.conical import _555

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
    def spiral_bevel_gear_set_rating(self: "CastSelf") -> "SpiralBevelGearSetRating":
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
class SpiralBevelGearSetRating(_569.BevelGearSetRating):
    """SpiralBevelGearSetRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPIRAL_BEVEL_GEAR_SET_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def spiral_bevel_gear_set(self: "Self") -> "_997.SpiralBevelGearSetDesign":
        """mastapy.gears.gear_designs.spiral_bevel.SpiralBevelGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpiralBevelGearSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def spiral_bevel_gear_ratings(self: "Self") -> "List[_416.SpiralBevelGearRating]":
        """List[mastapy.gears.rating.spiral_bevel.SpiralBevelGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpiralBevelGearRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def spiral_bevel_mesh_ratings(
        self: "Self",
    ) -> "List[_415.SpiralBevelGearMeshRating]":
        """List[mastapy.gears.rating.spiral_bevel.SpiralBevelGearMeshRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpiralBevelMeshRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_SpiralBevelGearSetRating":
        """Cast to another type.

        Returns:
            _Cast_SpiralBevelGearSetRating
        """
        return _Cast_SpiralBevelGearSetRating(self)
