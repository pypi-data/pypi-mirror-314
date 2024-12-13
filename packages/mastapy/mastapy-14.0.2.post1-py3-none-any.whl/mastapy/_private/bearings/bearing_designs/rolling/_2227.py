"""SphericalRollerThrustBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.bearing_designs.rolling import _2198

_SPHERICAL_ROLLER_THRUST_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "SphericalRollerThrustBearing"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings.bearing_designs import _2186, _2187, _2190
    from mastapy._private.bearings.bearing_designs.rolling import _2218, _2221

    Self = TypeVar("Self", bound="SphericalRollerThrustBearing")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SphericalRollerThrustBearing._Cast_SphericalRollerThrustBearing",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SphericalRollerThrustBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SphericalRollerThrustBearing:
    """Special nested class for casting SphericalRollerThrustBearing to subclasses."""

    __parent__: "SphericalRollerThrustBearing"

    @property
    def barrel_roller_bearing(self: "CastSelf") -> "_2198.BarrelRollerBearing":
        return self.__parent__._cast(_2198.BarrelRollerBearing)

    @property
    def roller_bearing(self: "CastSelf") -> "_2218.RollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2218

        return self.__parent__._cast(_2218.RollerBearing)

    @property
    def rolling_bearing(self: "CastSelf") -> "_2221.RollingBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2221

        return self.__parent__._cast(_2221.RollingBearing)

    @property
    def detailed_bearing(self: "CastSelf") -> "_2187.DetailedBearing":
        from mastapy._private.bearings.bearing_designs import _2187

        return self.__parent__._cast(_2187.DetailedBearing)

    @property
    def non_linear_bearing(self: "CastSelf") -> "_2190.NonLinearBearing":
        from mastapy._private.bearings.bearing_designs import _2190

        return self.__parent__._cast(_2190.NonLinearBearing)

    @property
    def bearing_design(self: "CastSelf") -> "_2186.BearingDesign":
        from mastapy._private.bearings.bearing_designs import _2186

        return self.__parent__._cast(_2186.BearingDesign)

    @property
    def spherical_roller_thrust_bearing(
        self: "CastSelf",
    ) -> "SphericalRollerThrustBearing":
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
class SphericalRollerThrustBearing(_2198.BarrelRollerBearing):
    """SphericalRollerThrustBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPHERICAL_ROLLER_THRUST_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def angle_between_roller_end_and_bearing_axis(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AngleBetweenRollerEndAndBearingAxis"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def distance_to_pressure_point_from_left_face(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "DistanceToPressurePointFromLeftFace"
        )

        if temp is None:
            return 0.0

        return temp

    @distance_to_pressure_point_from_left_face.setter
    @enforce_parameter_types
    def distance_to_pressure_point_from_left_face(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DistanceToPressurePointFromLeftFace",
            float(value) if value is not None else 0.0,
        )

    @property
    def effective_taper_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectiveTaperAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def element_centre_point_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementCentrePointDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def major_diameter_offset_from_roller_centre(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "MajorDiameterOffsetFromRollerCentre"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @major_diameter_offset_from_roller_centre.setter
    @enforce_parameter_types
    def major_diameter_offset_from_roller_centre(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MajorDiameterOffsetFromRollerCentre", value
        )

    @property
    def width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return temp

    @width.setter
    @enforce_parameter_types
    def width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_SphericalRollerThrustBearing":
        """Cast to another type.

        Returns:
            _Cast_SphericalRollerThrustBearing
        """
        return _Cast_SphericalRollerThrustBearing(self)
