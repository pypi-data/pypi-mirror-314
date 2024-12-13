"""LinearBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.bearing_designs import _2186

_LINEAR_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns", "LinearBearing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _1937

    Self = TypeVar("Self", bound="LinearBearing")
    CastSelf = TypeVar("CastSelf", bound="LinearBearing._Cast_LinearBearing")


__docformat__ = "restructuredtext en"
__all__ = ("LinearBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LinearBearing:
    """Special nested class for casting LinearBearing to subclasses."""

    __parent__: "LinearBearing"

    @property
    def bearing_design(self: "CastSelf") -> "_2186.BearingDesign":
        return self.__parent__._cast(_2186.BearingDesign)

    @property
    def linear_bearing(self: "CastSelf") -> "LinearBearing":
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
class LinearBearing(_2186.BearingDesign):
    """LinearBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LINEAR_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def axial_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AxialStiffness")

        if temp is None:
            return 0.0

        return temp

    @axial_stiffness.setter
    @enforce_parameter_types
    def axial_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "AxialStiffness", float(value) if value is not None else 0.0
        )

    @property
    def bore(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Bore")

        if temp is None:
            return 0.0

        return temp

    @bore.setter
    @enforce_parameter_types
    def bore(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Bore", float(value) if value is not None else 0.0
        )

    @property
    def outer_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @outer_diameter.setter
    @enforce_parameter_types
    def outer_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "OuterDiameter", float(value) if value is not None else 0.0
        )

    @property
    def radial_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialStiffness")

        if temp is None:
            return 0.0

        return temp

    @radial_stiffness.setter
    @enforce_parameter_types
    def radial_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RadialStiffness", float(value) if value is not None else 0.0
        )

    @property
    def stiffness_options(self: "Self") -> "_1937.BearingStiffnessMatrixOption":
        """mastapy.bearings.BearingStiffnessMatrixOption"""
        temp = pythonnet_property_get(self.wrapped, "StiffnessOptions")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.BearingStiffnessMatrixOption"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._1937", "BearingStiffnessMatrixOption"
        )(value)

    @stiffness_options.setter
    @enforce_parameter_types
    def stiffness_options(
        self: "Self", value: "_1937.BearingStiffnessMatrixOption"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.BearingStiffnessMatrixOption"
        )
        pythonnet_property_set(self.wrapped, "StiffnessOptions", value)

    @property
    def tilt_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TiltStiffness")

        if temp is None:
            return 0.0

        return temp

    @tilt_stiffness.setter
    @enforce_parameter_types
    def tilt_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TiltStiffness", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_LinearBearing":
        """Cast to another type.

        Returns:
            _Cast_LinearBearing
        """
        return _Cast_LinearBearing(self)
