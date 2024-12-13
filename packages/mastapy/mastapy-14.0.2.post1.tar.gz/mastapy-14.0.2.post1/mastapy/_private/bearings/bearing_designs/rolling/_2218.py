"""RollerBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import enum_with_selected_value, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings import _1946
from mastapy._private.bearings.bearing_designs.rolling import _2221

_ROLLER_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "RollerBearing"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings.bearing_designs import _2186, _2187, _2190
    from mastapy._private.bearings.bearing_designs.rolling import (
        _2193,
        _2194,
        _2195,
        _2198,
        _2204,
        _2205,
        _2216,
        _2217,
        _2226,
        _2227,
        _2228,
        _2231,
    )
    from mastapy._private.bearings.roller_bearing_profiles import _1983, _1994

    Self = TypeVar("Self", bound="RollerBearing")
    CastSelf = TypeVar("CastSelf", bound="RollerBearing._Cast_RollerBearing")


__docformat__ = "restructuredtext en"
__all__ = ("RollerBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollerBearing:
    """Special nested class for casting RollerBearing to subclasses."""

    __parent__: "RollerBearing"

    @property
    def rolling_bearing(self: "CastSelf") -> "_2221.RollingBearing":
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
    def asymmetric_spherical_roller_bearing(
        self: "CastSelf",
    ) -> "_2193.AsymmetricSphericalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2193

        return self.__parent__._cast(_2193.AsymmetricSphericalRollerBearing)

    @property
    def axial_thrust_cylindrical_roller_bearing(
        self: "CastSelf",
    ) -> "_2194.AxialThrustCylindricalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2194

        return self.__parent__._cast(_2194.AxialThrustCylindricalRollerBearing)

    @property
    def axial_thrust_needle_roller_bearing(
        self: "CastSelf",
    ) -> "_2195.AxialThrustNeedleRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2195

        return self.__parent__._cast(_2195.AxialThrustNeedleRollerBearing)

    @property
    def barrel_roller_bearing(self: "CastSelf") -> "_2198.BarrelRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2198

        return self.__parent__._cast(_2198.BarrelRollerBearing)

    @property
    def crossed_roller_bearing(self: "CastSelf") -> "_2204.CrossedRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2204

        return self.__parent__._cast(_2204.CrossedRollerBearing)

    @property
    def cylindrical_roller_bearing(
        self: "CastSelf",
    ) -> "_2205.CylindricalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2205

        return self.__parent__._cast(_2205.CylindricalRollerBearing)

    @property
    def needle_roller_bearing(self: "CastSelf") -> "_2216.NeedleRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2216

        return self.__parent__._cast(_2216.NeedleRollerBearing)

    @property
    def non_barrel_roller_bearing(self: "CastSelf") -> "_2217.NonBarrelRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2217

        return self.__parent__._cast(_2217.NonBarrelRollerBearing)

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
    def taper_roller_bearing(self: "CastSelf") -> "_2228.TaperRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2228

        return self.__parent__._cast(_2228.TaperRollerBearing)

    @property
    def toroidal_roller_bearing(self: "CastSelf") -> "_2231.ToroidalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2231

        return self.__parent__._cast(_2231.ToroidalRollerBearing)

    @property
    def roller_bearing(self: "CastSelf") -> "RollerBearing":
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
class RollerBearing(_2221.RollingBearing):
    """RollerBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLER_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def corner_radii(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CornerRadii")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @corner_radii.setter
    @enforce_parameter_types
    def corner_radii(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CornerRadii", value)

    @property
    def effective_roller_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectiveRollerLength")

        if temp is None:
            return 0.0

        return temp

    @property
    def element_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ElementDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @element_diameter.setter
    @enforce_parameter_types
    def element_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ElementDiameter", value)

    @property
    def kl(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "KL")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @kl.setter
    @enforce_parameter_types
    def kl(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "KL", value)

    @property
    def roller_length(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RollerLength")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @roller_length.setter
    @enforce_parameter_types
    def roller_length(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RollerLength", value)

    @property
    def roller_profile(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_RollerBearingProfileTypes":
        """EnumWithSelectedValue[mastapy.bearings.RollerBearingProfileTypes]"""
        temp = pythonnet_property_get(self.wrapped, "RollerProfile")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_RollerBearingProfileTypes.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @roller_profile.setter
    @enforce_parameter_types
    def roller_profile(self: "Self", value: "_1946.RollerBearingProfileTypes") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RollerBearingProfileTypes.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "RollerProfile", value)

    @property
    def inner_race_profile_set(self: "Self") -> "_1983.ProfileSet":
        """mastapy.bearings.roller_bearing_profiles.ProfileSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerRaceProfileSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def outer_race_profile_set(self: "Self") -> "_1983.ProfileSet":
        """mastapy.bearings.roller_bearing_profiles.ProfileSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterRaceProfileSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def roller_profile_set(self: "Self") -> "_1983.ProfileSet":
        """mastapy.bearings.roller_bearing_profiles.ProfileSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollerProfileSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def inner_race_and_roller_profiles(
        self: "Self",
    ) -> "List[_1994.RollerRaceProfilePoint]":
        """List[mastapy.bearings.roller_bearing_profiles.RollerRaceProfilePoint]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerRaceAndRollerProfiles")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def inner_race_and_roller_profiles_for_first_row(
        self: "Self",
    ) -> "List[_1994.RollerRaceProfilePoint]":
        """List[mastapy.bearings.roller_bearing_profiles.RollerRaceProfilePoint]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "InnerRaceAndRollerProfilesForFirstRow"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def inner_race_and_roller_profiles_for_second_row(
        self: "Self",
    ) -> "List[_1994.RollerRaceProfilePoint]":
        """List[mastapy.bearings.roller_bearing_profiles.RollerRaceProfilePoint]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "InnerRaceAndRollerProfilesForSecondRow"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def outer_race_and_roller_profiles(
        self: "Self",
    ) -> "List[_1994.RollerRaceProfilePoint]":
        """List[mastapy.bearings.roller_bearing_profiles.RollerRaceProfilePoint]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterRaceAndRollerProfiles")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def outer_race_and_roller_profiles_for_first_row(
        self: "Self",
    ) -> "List[_1994.RollerRaceProfilePoint]":
        """List[mastapy.bearings.roller_bearing_profiles.RollerRaceProfilePoint]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "OuterRaceAndRollerProfilesForFirstRow"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def outer_race_and_roller_profiles_for_second_row(
        self: "Self",
    ) -> "List[_1994.RollerRaceProfilePoint]":
        """List[mastapy.bearings.roller_bearing_profiles.RollerRaceProfilePoint]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "OuterRaceAndRollerProfilesForSecondRow"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_RollerBearing":
        """Cast to another type.

        Returns:
            _Cast_RollerBearing
        """
        return _Cast_RollerBearing(self)
