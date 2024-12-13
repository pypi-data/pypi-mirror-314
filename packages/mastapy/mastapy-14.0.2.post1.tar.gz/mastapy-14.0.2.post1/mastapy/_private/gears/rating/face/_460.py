"""FaceGearMeshRating"""

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

_FACE_GEAR_MESH_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Face", "FaceGearMeshRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears import _338
    from mastapy._private.gears.analysis import _1256
    from mastapy._private.gears.gear_designs.face import _1017
    from mastapy._private.gears.load_case.face import _906
    from mastapy._private.gears.rating import _365
    from mastapy._private.gears.rating.cylindrical.iso6336 import _527
    from mastapy._private.gears.rating.face import _461, _463

    Self = TypeVar("Self", bound="FaceGearMeshRating")
    CastSelf = TypeVar("CastSelf", bound="FaceGearMeshRating._Cast_FaceGearMeshRating")


__docformat__ = "restructuredtext en"
__all__ = ("FaceGearMeshRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FaceGearMeshRating:
    """Special nested class for casting FaceGearMeshRating to subclasses."""

    __parent__: "FaceGearMeshRating"

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
    def face_gear_mesh_rating(self: "CastSelf") -> "FaceGearMeshRating":
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
class FaceGearMeshRating(_373.GearMeshRating):
    """FaceGearMeshRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FACE_GEAR_MESH_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def active_flank(self: "Self") -> "_338.GearFlanks":
        """mastapy.gears.GearFlanks

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveFlank")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Gears.GearFlanks")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._338", "GearFlanks"
        )(value)

    @property
    def face_gear_mesh(self: "Self") -> "_1017.FaceGearMeshDesign":
        """mastapy.gears.gear_designs.face.FaceGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceGearMesh")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gear_set_rating(self: "Self") -> "_463.FaceGearSetRating":
        """mastapy.gears.rating.face.FaceGearSetRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSetRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def mesh_load_case(self: "Self") -> "_906.FaceMeshLoadCase":
        """mastapy.gears.load_case.face.FaceMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def mesh_single_flank_rating(
        self: "Self",
    ) -> "_527.ISO63362006MeshSingleFlankRating":
        """mastapy.gears.rating.cylindrical.iso6336.ISO63362006MeshSingleFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshSingleFlankRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def face_gear_ratings(self: "Self") -> "List[_461.FaceGearRating]":
        """List[mastapy.gears.rating.face.FaceGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceGearRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_FaceGearMeshRating":
        """Cast to another type.

        Returns:
            _Cast_FaceGearMeshRating
        """
        return _Cast_FaceGearMeshRating(self)
