"""WormGearMeshRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating import _373

_WORM_GEAR_MESH_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Worm", "WormGearMeshRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1256
    from mastapy._private.gears.gear_designs.worm import _984
    from mastapy._private.gears.rating import _365
    from mastapy._private.gears.rating.worm import _387

    Self = TypeVar("Self", bound="WormGearMeshRating")
    CastSelf = TypeVar("CastSelf", bound="WormGearMeshRating._Cast_WormGearMeshRating")


__docformat__ = "restructuredtext en"
__all__ = ("WormGearMeshRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormGearMeshRating:
    """Special nested class for casting WormGearMeshRating to subclasses."""

    __parent__: "WormGearMeshRating"

    @property
    def gear_mesh_rating(self: "CastSelf") -> "_373.GearMeshRating":
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
    def worm_gear_mesh_rating(self: "CastSelf") -> "WormGearMeshRating":
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
class WormGearMeshRating(_373.GearMeshRating):
    """WormGearMeshRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_GEAR_MESH_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def worm_gear_mesh(self: "Self") -> "_984.WormGearMeshDesign":
        """mastapy.gears.gear_designs.worm.WormGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormGearMesh")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def worm_gear_ratings(self: "Self") -> "List[_387.WormGearRating]":
        """List[mastapy.gears.rating.worm.WormGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormGearRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_WormGearMeshRating":
        """Cast to another type.

        Returns:
            _Cast_WormGearMeshRating
        """
        return _Cast_WormGearMeshRating(self)
