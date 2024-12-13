"""FaceGearSetMicroGeometry"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.gears.analysis import _1271

_FACE_GEAR_SET_MICRO_GEOMETRY = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Face", "FaceGearSetMicroGeometry"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1257, _1266
    from mastapy._private.gears.gear_designs.face import _1018, _1019, _1021

    Self = TypeVar("Self", bound="FaceGearSetMicroGeometry")
    CastSelf = TypeVar(
        "CastSelf", bound="FaceGearSetMicroGeometry._Cast_FaceGearSetMicroGeometry"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FaceGearSetMicroGeometry",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FaceGearSetMicroGeometry:
    """Special nested class for casting FaceGearSetMicroGeometry to subclasses."""

    __parent__: "FaceGearSetMicroGeometry"

    @property
    def gear_set_implementation_detail(
        self: "CastSelf",
    ) -> "_1271.GearSetImplementationDetail":
        return self.__parent__._cast(_1271.GearSetImplementationDetail)

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "_1266.GearSetDesignAnalysis":
        from mastapy._private.gears.analysis import _1266

        return self.__parent__._cast(_1266.GearSetDesignAnalysis)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1257.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1257

        return self.__parent__._cast(_1257.AbstractGearSetAnalysis)

    @property
    def face_gear_set_micro_geometry(self: "CastSelf") -> "FaceGearSetMicroGeometry":
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
class FaceGearSetMicroGeometry(_1271.GearSetImplementationDetail):
    """FaceGearSetMicroGeometry

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FACE_GEAR_SET_MICRO_GEOMETRY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def face_gear_set_design(self: "Self") -> "_1021.FaceGearSetDesign":
        """mastapy.gears.gear_designs.face.FaceGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def face_gear_micro_geometries(self: "Self") -> "List[_1019.FaceGearMicroGeometry]":
        """List[mastapy.gears.gear_designs.face.FaceGearMicroGeometry]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceGearMicroGeometries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def face_mesh_micro_geometries(
        self: "Self",
    ) -> "List[_1018.FaceGearMeshMicroGeometry]":
        """List[mastapy.gears.gear_designs.face.FaceGearMeshMicroGeometry]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceMeshMicroGeometries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    def duplicate(self: "Self") -> "FaceGearSetMicroGeometry":
        """mastapy.gears.gear_designs.face.FaceGearSetMicroGeometry"""
        method_result = pythonnet_method_call(self.wrapped, "Duplicate")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_FaceGearSetMicroGeometry":
        """Cast to another type.

        Returns:
            _Cast_FaceGearSetMicroGeometry
        """
        return _Cast_FaceGearSetMicroGeometry(self)
