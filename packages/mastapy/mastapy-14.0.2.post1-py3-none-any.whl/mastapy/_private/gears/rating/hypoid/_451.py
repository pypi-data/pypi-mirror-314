"""HypoidGearMeshRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.agma_gleason_conical import _578

_HYPOID_GEAR_MESH_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Hypoid", "HypoidGearMeshRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1256
    from mastapy._private.gears.gear_designs.hypoid import _1012
    from mastapy._private.gears.rating import _365, _373
    from mastapy._private.gears.rating.conical import _552, _558
    from mastapy._private.gears.rating.hypoid import _452
    from mastapy._private.gears.rating.hypoid.standards import _456
    from mastapy._private.gears.rating.iso_10300 import _437, _438

    Self = TypeVar("Self", bound="HypoidGearMeshRating")
    CastSelf = TypeVar(
        "CastSelf", bound="HypoidGearMeshRating._Cast_HypoidGearMeshRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("HypoidGearMeshRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HypoidGearMeshRating:
    """Special nested class for casting HypoidGearMeshRating to subclasses."""

    __parent__: "HypoidGearMeshRating"

    @property
    def agma_gleason_conical_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_578.AGMAGleasonConicalGearMeshRating":
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
    def hypoid_gear_mesh_rating(self: "CastSelf") -> "HypoidGearMeshRating":
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
class HypoidGearMeshRating(_578.AGMAGleasonConicalGearMeshRating):
    """HypoidGearMeshRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HYPOID_GEAR_MESH_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def gleason_hypoid_mesh_single_flank_rating(
        self: "Self",
    ) -> "_456.GleasonHypoidMeshSingleFlankRating":
        """mastapy.gears.rating.hypoid.standards.GleasonHypoidMeshSingleFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GleasonHypoidMeshSingleFlankRating"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def hypoid_gear_mesh(self: "Self") -> "_1012.HypoidGearMeshDesign":
        """mastapy.gears.gear_designs.hypoid.HypoidGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HypoidGearMesh")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def iso10300_hypoid_mesh_single_flank_rating_method_b1(
        self: "Self",
    ) -> "_438.ISO10300MeshSingleFlankRatingMethodB1":
        """mastapy.gears.rating.isoISO10300MeshSingleFlankRatingMethodB1

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO10300HypoidMeshSingleFlankRatingMethodB1"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def iso10300_hypoid_mesh_single_flank_rating_method_b2(
        self: "Self",
    ) -> "_437.ISO10300MeshSingleFlankRatingHypoidMethodB2":
        """mastapy.gears.rating.isoISO10300MeshSingleFlankRatingHypoidMethodB2

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO10300HypoidMeshSingleFlankRatingMethodB2"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def meshed_gears(self: "Self") -> "List[_558.ConicalMeshedGearRating]":
        """List[mastapy.gears.rating.conical.ConicalMeshedGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshedGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def gears_in_mesh(self: "Self") -> "List[_558.ConicalMeshedGearRating]":
        """List[mastapy.gears.rating.conical.ConicalMeshedGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearsInMesh")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def hypoid_gear_ratings(self: "Self") -> "List[_452.HypoidGearRating]":
        """List[mastapy.gears.rating.hypoid.HypoidGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HypoidGearRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_HypoidGearMeshRating":
        """Cast to another type.

        Returns:
            _Cast_HypoidGearMeshRating
        """
        return _Cast_HypoidGearMeshRating(self)
