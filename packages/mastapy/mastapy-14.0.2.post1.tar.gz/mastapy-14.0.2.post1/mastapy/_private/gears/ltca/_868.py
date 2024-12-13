"""GearMeshLoadedContactLine"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_GEAR_MESH_LOADED_CONTACT_LINE = python_net_import(
    "SMT.MastaAPI.Gears.LTCA", "GearMeshLoadedContactLine"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.ltca import _869
    from mastapy._private.gears.ltca.conical import _897
    from mastapy._private.gears.ltca.cylindrical import _883

    Self = TypeVar("Self", bound="GearMeshLoadedContactLine")
    CastSelf = TypeVar(
        "CastSelf", bound="GearMeshLoadedContactLine._Cast_GearMeshLoadedContactLine"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshLoadedContactLine",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshLoadedContactLine:
    """Special nested class for casting GearMeshLoadedContactLine to subclasses."""

    __parent__: "GearMeshLoadedContactLine"

    @property
    def cylindrical_gear_mesh_loaded_contact_line(
        self: "CastSelf",
    ) -> "_883.CylindricalGearMeshLoadedContactLine":
        from mastapy._private.gears.ltca.cylindrical import _883

        return self.__parent__._cast(_883.CylindricalGearMeshLoadedContactLine)

    @property
    def conical_mesh_loaded_contact_line(
        self: "CastSelf",
    ) -> "_897.ConicalMeshLoadedContactLine":
        from mastapy._private.gears.ltca.conical import _897

        return self.__parent__._cast(_897.ConicalMeshLoadedContactLine)

    @property
    def gear_mesh_loaded_contact_line(self: "CastSelf") -> "GearMeshLoadedContactLine":
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
class GearMeshLoadedContactLine(_0.APIBase):
    """GearMeshLoadedContactLine

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_LOADED_CONTACT_LINE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def contact_line_index(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactLineIndex")

        if temp is None:
            return 0

        return temp

    @property
    def mesh_position_index(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshPositionIndex")

        if temp is None:
            return 0

        return temp

    @property
    def tooth_number_of_gear_a(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothNumberOfGearA")

        if temp is None:
            return 0

        return temp

    @property
    def tooth_number_of_gear_b(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothNumberOfGearB")

        if temp is None:
            return 0

        return temp

    @property
    def loaded_contact_strip_end_points(
        self: "Self",
    ) -> "List[_869.GearMeshLoadedContactPoint]":
        """List[mastapy.gears.ltca.GearMeshLoadedContactPoint]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadedContactStripEndPoints")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshLoadedContactLine":
        """Cast to another type.

        Returns:
            _Cast_GearMeshLoadedContactLine
        """
        return _Cast_GearMeshLoadedContactLine(self)
