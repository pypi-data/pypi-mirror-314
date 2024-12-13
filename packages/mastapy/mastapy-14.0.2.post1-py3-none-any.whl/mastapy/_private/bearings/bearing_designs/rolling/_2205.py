"""CylindricalRollerBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
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
from mastapy._private.bearings.bearing_designs.rolling import _2217

_CYLINDRICAL_ROLLER_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "CylindricalRollerBearing"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings.bearing_designs import _2186, _2187, _2190
    from mastapy._private.bearings.bearing_designs.rolling import _2216, _2218, _2221
    from mastapy._private.bearings.bearing_results import _1998

    Self = TypeVar("Self", bound="CylindricalRollerBearing")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalRollerBearing._Cast_CylindricalRollerBearing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalRollerBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalRollerBearing:
    """Special nested class for casting CylindricalRollerBearing to subclasses."""

    __parent__: "CylindricalRollerBearing"

    @property
    def non_barrel_roller_bearing(self: "CastSelf") -> "_2217.NonBarrelRollerBearing":
        return self.__parent__._cast(_2217.NonBarrelRollerBearing)

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
    def needle_roller_bearing(self: "CastSelf") -> "_2216.NeedleRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2216

        return self.__parent__._cast(_2216.NeedleRollerBearing)

    @property
    def cylindrical_roller_bearing(self: "CastSelf") -> "CylindricalRollerBearing":
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
class CylindricalRollerBearing(_2217.NonBarrelRollerBearing):
    """CylindricalRollerBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_ROLLER_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def allowable_axial_load_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "AllowableAxialLoadFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @allowable_axial_load_factor.setter
    @enforce_parameter_types
    def allowable_axial_load_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AllowableAxialLoadFactor", value)

    @property
    def capacity_lubrication_factor_for_permissible_axial_load_grease(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "CapacityLubricationFactorForPermissibleAxialLoadGrease"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @capacity_lubrication_factor_for_permissible_axial_load_grease.setter
    @enforce_parameter_types
    def capacity_lubrication_factor_for_permissible_axial_load_grease(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped,
            "CapacityLubricationFactorForPermissibleAxialLoadGrease",
            value,
        )

    @property
    def capacity_lubrication_factor_for_permissible_axial_load_oil(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "CapacityLubricationFactorForPermissibleAxialLoadOil"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @capacity_lubrication_factor_for_permissible_axial_load_oil.setter
    @enforce_parameter_types
    def capacity_lubrication_factor_for_permissible_axial_load_oil(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "CapacityLubricationFactorForPermissibleAxialLoadOil", value
        )

    @property
    def diameter_exponent_factor_for_permissible_axial_load(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "DiameterExponentFactorForPermissibleAxialLoad"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @diameter_exponent_factor_for_permissible_axial_load.setter
    @enforce_parameter_types
    def diameter_exponent_factor_for_permissible_axial_load(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "DiameterExponentFactorForPermissibleAxialLoad", value
        )

    @property
    def diameter_scaling_factor_for_permissible_axial_load(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "DiameterScalingFactorForPermissibleAxialLoad"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @diameter_scaling_factor_for_permissible_axial_load.setter
    @enforce_parameter_types
    def diameter_scaling_factor_for_permissible_axial_load(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "DiameterScalingFactorForPermissibleAxialLoad", value
        )

    @property
    def permissible_axial_load_default_calculation_method(
        self: "Self",
    ) -> "_1998.CylindricalRollerMaxAxialLoadMethod":
        """mastapy.bearings.bearing_results.CylindricalRollerMaxAxialLoadMethod"""
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleAxialLoadDefaultCalculationMethod"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Bearings.BearingResults.CylindricalRollerMaxAxialLoadMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.bearing_results._1998",
            "CylindricalRollerMaxAxialLoadMethod",
        )(value)

    @permissible_axial_load_default_calculation_method.setter
    @enforce_parameter_types
    def permissible_axial_load_default_calculation_method(
        self: "Self", value: "_1998.CylindricalRollerMaxAxialLoadMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Bearings.BearingResults.CylindricalRollerMaxAxialLoadMethod",
        )
        pythonnet_property_set(
            self.wrapped, "PermissibleAxialLoadDefaultCalculationMethod", value
        )

    @property
    def permissible_axial_load_dimension_factor(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleAxialLoadDimensionFactor"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @permissible_axial_load_dimension_factor.setter
    @enforce_parameter_types
    def permissible_axial_load_dimension_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "PermissibleAxialLoadDimensionFactor", value
        )

    @property
    def permissible_axial_load_internal_dimension_factor(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleAxialLoadInternalDimensionFactor"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @permissible_axial_load_internal_dimension_factor.setter
    @enforce_parameter_types
    def permissible_axial_load_internal_dimension_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "PermissibleAxialLoadInternalDimensionFactor", value
        )

    @property
    def radial_load_lubrication_factor_for_permissible_axial_load_grease(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "RadialLoadLubricationFactorForPermissibleAxialLoadGrease"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @radial_load_lubrication_factor_for_permissible_axial_load_grease.setter
    @enforce_parameter_types
    def radial_load_lubrication_factor_for_permissible_axial_load_grease(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped,
            "RadialLoadLubricationFactorForPermissibleAxialLoadGrease",
            value,
        )

    @property
    def radial_load_lubrication_factor_for_permissible_axial_load_oil(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "RadialLoadLubricationFactorForPermissibleAxialLoadOil"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @radial_load_lubrication_factor_for_permissible_axial_load_oil.setter
    @enforce_parameter_types
    def radial_load_lubrication_factor_for_permissible_axial_load_oil(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "RadialLoadLubricationFactorForPermissibleAxialLoadOil", value
        )

    @property
    def reference_rotation_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ReferenceRotationSpeed")

        if temp is None:
            return 0.0

        return temp

    @reference_rotation_speed.setter
    @enforce_parameter_types
    def reference_rotation_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReferenceRotationSpeed",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalRollerBearing":
        """Cast to another type.

        Returns:
            _Cast_CylindricalRollerBearing
        """
        return _Cast_CylindricalRollerBearing(self)
