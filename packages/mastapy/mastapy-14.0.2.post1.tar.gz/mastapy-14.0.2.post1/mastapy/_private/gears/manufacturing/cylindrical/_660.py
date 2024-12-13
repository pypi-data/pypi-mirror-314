"""MicroGeometryInputsProfile"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.manufacturing.cylindrical import _658, _662

_MICRO_GEOMETRY_INPUTS_PROFILE = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical", "MicroGeometryInputsProfile"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1539

    Self = TypeVar("Self", bound="MicroGeometryInputsProfile")
    CastSelf = TypeVar(
        "CastSelf", bound="MicroGeometryInputsProfile._Cast_MicroGeometryInputsProfile"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MicroGeometryInputsProfile",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MicroGeometryInputsProfile:
    """Special nested class for casting MicroGeometryInputsProfile to subclasses."""

    __parent__: "MicroGeometryInputsProfile"

    @property
    def micro_geometry_inputs(self: "CastSelf") -> "_658.MicroGeometryInputs":
        return self.__parent__._cast(_658.MicroGeometryInputs)

    @property
    def micro_geometry_inputs_profile(self: "CastSelf") -> "MicroGeometryInputsProfile":
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
class MicroGeometryInputsProfile(
    _658.MicroGeometryInputs[_662.ProfileModificationSegment]
):
    """MicroGeometryInputsProfile

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MICRO_GEOMETRY_INPUTS_PROFILE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def number_of_profile_segments(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfProfileSegments")

        if temp is None:
            return 0

        return temp

    @number_of_profile_segments.setter
    @enforce_parameter_types
    def number_of_profile_segments(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfProfileSegments",
            int(value) if value is not None else 0,
        )

    @property
    def profile_micro_geometry_range(self: "Self") -> "_1539.Range":
        """mastapy.math_utility.Range

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileMicroGeometryRange")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def z_plane(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ZPlane")

        if temp is None:
            return 0.0

        return temp

    @z_plane.setter
    @enforce_parameter_types
    def z_plane(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ZPlane", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_MicroGeometryInputsProfile":
        """Cast to another type.

        Returns:
            _Cast_MicroGeometryInputsProfile
        """
        return _Cast_MicroGeometryInputsProfile(self)
