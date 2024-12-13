"""ISO6336GeometryBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_ISO6336_GEOMETRY_BASE = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "ISO6336GeometryBase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1086, _1088, _1089

    Self = TypeVar("Self", bound="ISO6336GeometryBase")
    CastSelf = TypeVar(
        "CastSelf", bound="ISO6336GeometryBase._Cast_ISO6336GeometryBase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO6336GeometryBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO6336GeometryBase:
    """Special nested class for casting ISO6336GeometryBase to subclasses."""

    __parent__: "ISO6336GeometryBase"

    @property
    def iso6336_geometry(self: "CastSelf") -> "_1086.ISO6336Geometry":
        from mastapy._private.gears.gear_designs.cylindrical import _1086

        return self.__parent__._cast(_1086.ISO6336Geometry)

    @property
    def iso6336_geometry_for_shaped_gears(
        self: "CastSelf",
    ) -> "_1088.ISO6336GeometryForShapedGears":
        from mastapy._private.gears.gear_designs.cylindrical import _1088

        return self.__parent__._cast(_1088.ISO6336GeometryForShapedGears)

    @property
    def iso6336_geometry_manufactured(
        self: "CastSelf",
    ) -> "_1089.ISO6336GeometryManufactured":
        from mastapy._private.gears.gear_designs.cylindrical import _1089

        return self.__parent__._cast(_1089.ISO6336GeometryManufactured)

    @property
    def iso6336_geometry_base(self: "CastSelf") -> "ISO6336GeometryBase":
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
class ISO6336GeometryBase(_0.APIBase):
    """ISO6336GeometryBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO6336_GEOMETRY_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def iso6336_root_fillet_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO6336RootFilletRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    def iso6336_signed_virtual_base_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO6336SignedVirtualBaseDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def iso6336_tooth_root_chord(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO6336ToothRootChord")

        if temp is None:
            return 0.0

        return temp

    @property
    def iso6336_virtual_tip_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO6336VirtualTipDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def virtual_number_of_teeth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VirtualNumberOfTeeth")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ISO6336GeometryBase":
        """Cast to another type.

        Returns:
            _Cast_ISO6336GeometryBase
        """
        return _Cast_ISO6336GeometryBase(self)
