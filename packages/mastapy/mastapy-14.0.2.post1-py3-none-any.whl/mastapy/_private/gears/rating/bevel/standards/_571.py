"""AGMASpiralBevelMeshSingleFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.bevel.standards import _575

_AGMA_SPIRAL_BEVEL_MESH_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Bevel.Standards", "AGMASpiralBevelMeshSingleFlankRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating import _379
    from mastapy._private.gears.rating.bevel.standards import _570
    from mastapy._private.gears.rating.conical import _559

    Self = TypeVar("Self", bound="AGMASpiralBevelMeshSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMASpiralBevelMeshSingleFlankRating._Cast_AGMASpiralBevelMeshSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMASpiralBevelMeshSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMASpiralBevelMeshSingleFlankRating:
    """Special nested class for casting AGMASpiralBevelMeshSingleFlankRating to subclasses."""

    __parent__: "AGMASpiralBevelMeshSingleFlankRating"

    @property
    def spiral_bevel_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_575.SpiralBevelMeshSingleFlankRating":
        return self.__parent__._cast(_575.SpiralBevelMeshSingleFlankRating)

    @property
    def conical_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_559.ConicalMeshSingleFlankRating":
        from mastapy._private.gears.rating.conical import _559

        return self.__parent__._cast(_559.ConicalMeshSingleFlankRating)

    @property
    def mesh_single_flank_rating(self: "CastSelf") -> "_379.MeshSingleFlankRating":
        from mastapy._private.gears.rating import _379

        return self.__parent__._cast(_379.MeshSingleFlankRating)

    @property
    def agma_spiral_bevel_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "AGMASpiralBevelMeshSingleFlankRating":
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
class AGMASpiralBevelMeshSingleFlankRating(_575.SpiralBevelMeshSingleFlankRating):
    """AGMASpiralBevelMeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_SPIRAL_BEVEL_MESH_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def crowning_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CrowningFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    def rating_standard_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatingStandardName")

        if temp is None:
            return ""

        return temp

    @property
    def gear_single_flank_ratings(
        self: "Self",
    ) -> "List[_570.AGMASpiralBevelGearSingleFlankRating]":
        """List[mastapy.gears.rating.bevel.standards.AGMASpiralBevelGearSingleFlankRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSingleFlankRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def agma_bevel_gear_single_flank_ratings(
        self: "Self",
    ) -> "List[_570.AGMASpiralBevelGearSingleFlankRating]":
        """List[mastapy.gears.rating.bevel.standards.AGMASpiralBevelGearSingleFlankRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AGMABevelGearSingleFlankRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_AGMASpiralBevelMeshSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_AGMASpiralBevelMeshSingleFlankRating
        """
        return _Cast_AGMASpiralBevelMeshSingleFlankRating(self)
