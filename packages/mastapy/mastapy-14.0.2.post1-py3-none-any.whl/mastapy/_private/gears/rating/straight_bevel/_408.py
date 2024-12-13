"""StraightBevelGearMeshRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.bevel import _567

_STRAIGHT_BEVEL_GEAR_MESH_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.StraightBevel", "StraightBevelGearMeshRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1256
    from mastapy._private.gears.gear_designs.straight_bevel import _988
    from mastapy._private.gears.rating import _365, _373
    from mastapy._private.gears.rating.agma_gleason_conical import _578
    from mastapy._private.gears.rating.conical import _552
    from mastapy._private.gears.rating.straight_bevel import _409

    Self = TypeVar("Self", bound="StraightBevelGearMeshRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelGearMeshRating._Cast_StraightBevelGearMeshRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelGearMeshRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelGearMeshRating:
    """Special nested class for casting StraightBevelGearMeshRating to subclasses."""

    __parent__: "StraightBevelGearMeshRating"

    @property
    def bevel_gear_mesh_rating(self: "CastSelf") -> "_567.BevelGearMeshRating":
        return self.__parent__._cast(_567.BevelGearMeshRating)

    @property
    def agma_gleason_conical_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_578.AGMAGleasonConicalGearMeshRating":
        from mastapy._private.gears.rating.agma_gleason_conical import _578

        return self.__parent__._cast(_578.AGMAGleasonConicalGearMeshRating)

    @property
    def conical_gear_mesh_rating(self: "CastSelf") -> "_552.ConicalGearMeshRating":
        from mastapy._private.gears.rating.conical import _552

        return self.__parent__._cast(_552.ConicalGearMeshRating)

    @property
    def gear_mesh_rating(self: "CastSelf") -> "_373.GearMeshRating":
        from mastapy._private.gears.rating import _373

        return self.__parent__._cast(_373.GearMeshRating)

    @property
    def abstract_gear_mesh_rating(self: "CastSelf") -> "_365.AbstractGearMeshRating":
        from mastapy._private.gears.rating import _365

        return self.__parent__._cast(_365.AbstractGearMeshRating)

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1256.AbstractGearMeshAnalysis":
        from mastapy._private.gears.analysis import _1256

        return self.__parent__._cast(_1256.AbstractGearMeshAnalysis)

    @property
    def straight_bevel_gear_mesh_rating(
        self: "CastSelf",
    ) -> "StraightBevelGearMeshRating":
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
class StraightBevelGearMeshRating(_567.BevelGearMeshRating):
    """StraightBevelGearMeshRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_GEAR_MESH_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def straight_bevel_gear_mesh(self: "Self") -> "_988.StraightBevelGearMeshDesign":
        """mastapy.gears.gear_designs.straight_bevel.StraightBevelGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelGearMesh")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def straight_bevel_gear_ratings(
        self: "Self",
    ) -> "List[_409.StraightBevelGearRating]":
        """List[mastapy.gears.rating.straight_bevel.StraightBevelGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelGearRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelGearMeshRating":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelGearMeshRating
        """
        return _Cast_StraightBevelGearMeshRating(self)
