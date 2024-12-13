"""BarrelRollerBearing"""

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
from mastapy._private.bearings.bearing_designs.rolling import _2218

_BARREL_ROLLER_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "BarrelRollerBearing"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings.bearing_designs import _2186, _2187, _2190
    from mastapy._private.bearings.bearing_designs.rolling import (
        _2221,
        _2226,
        _2227,
        _2231,
    )

    Self = TypeVar("Self", bound="BarrelRollerBearing")
    CastSelf = TypeVar(
        "CastSelf", bound="BarrelRollerBearing._Cast_BarrelRollerBearing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BarrelRollerBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BarrelRollerBearing:
    """Special nested class for casting BarrelRollerBearing to subclasses."""

    __parent__: "BarrelRollerBearing"

    @property
    def roller_bearing(self: "CastSelf") -> "_2218.RollerBearing":
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
    def spherical_roller_bearing(self: "CastSelf") -> "_2226.SphericalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2226

        return self.__parent__._cast(_2226.SphericalRollerBearing)

    @property
    def spherical_roller_thrust_bearing(
        self: "CastSelf",
    ) -> "_2227.SphericalRollerThrustBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2227

        return self.__parent__._cast(_2227.SphericalRollerThrustBearing)

    @property
    def toroidal_roller_bearing(self: "CastSelf") -> "_2231.ToroidalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2231

        return self.__parent__._cast(_2231.ToroidalRollerBearing)

    @property
    def barrel_roller_bearing(self: "CastSelf") -> "BarrelRollerBearing":
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
class BarrelRollerBearing(_2218.RollerBearing):
    """BarrelRollerBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BARREL_ROLLER_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def element_profile_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ElementProfileRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @element_profile_radius.setter
    @enforce_parameter_types
    def element_profile_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ElementProfileRadius", value)

    @property
    def groove_radius_inner(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "GrooveRadiusInner")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @groove_radius_inner.setter
    @enforce_parameter_types
    def groove_radius_inner(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "GrooveRadiusInner", value)

    @property
    def groove_radius_outer(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "GrooveRadiusOuter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @groove_radius_outer.setter
    @enforce_parameter_types
    def groove_radius_outer(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "GrooveRadiusOuter", value)

    @property
    def roller_race_radius_ratio(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RollerRaceRadiusRatio")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @roller_race_radius_ratio.setter
    @enforce_parameter_types
    def roller_race_radius_ratio(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RollerRaceRadiusRatio", value)

    @property
    def cast_to(self: "Self") -> "_Cast_BarrelRollerBearing":
        """Cast to another type.

        Returns:
            _Cast_BarrelRollerBearing
        """
        return _Cast_BarrelRollerBearing(self)
