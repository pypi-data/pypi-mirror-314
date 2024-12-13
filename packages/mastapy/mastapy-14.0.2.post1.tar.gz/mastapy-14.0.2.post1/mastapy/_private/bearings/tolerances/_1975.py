"""SupportDetail"""

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
from mastapy._private.bearings.tolerances import _1963

_SUPPORT_DETAIL = python_net_import("SMT.MastaAPI.Bearings.Tolerances", "SupportDetail")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.tolerances import _1956, _1970, _1976

    Self = TypeVar("Self", bound="SupportDetail")
    CastSelf = TypeVar("CastSelf", bound="SupportDetail._Cast_SupportDetail")


__docformat__ = "restructuredtext en"
__all__ = ("SupportDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SupportDetail:
    """Special nested class for casting SupportDetail to subclasses."""

    __parent__: "SupportDetail"

    @property
    def interference_detail(self: "CastSelf") -> "_1963.InterferenceDetail":
        return self.__parent__._cast(_1963.InterferenceDetail)

    @property
    def bearing_connection_component(
        self: "CastSelf",
    ) -> "_1956.BearingConnectionComponent":
        from mastapy._private.bearings.tolerances import _1956

        return self.__parent__._cast(_1956.BearingConnectionComponent)

    @property
    def support_detail(self: "CastSelf") -> "SupportDetail":
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
class SupportDetail(_1963.InterferenceDetail):
    """SupportDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SUPPORT_DETAIL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def angle_of_radial_error(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AngleOfRadialError")

        if temp is None:
            return 0.0

        return temp

    @angle_of_radial_error.setter
    @enforce_parameter_types
    def angle_of_radial_error(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AngleOfRadialError",
            float(value) if value is not None else 0.0,
        )

    @property
    def material_source(self: "Self") -> "_1976.SupportMaterialSource":
        """mastapy.bearings.tolerances.SupportMaterialSource

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaterialSource")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.Tolerances.SupportMaterialSource"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.tolerances._1976", "SupportMaterialSource"
        )(value)

    @property
    def radial_error_magnitude(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialErrorMagnitude")

        if temp is None:
            return 0.0

        return temp

    @radial_error_magnitude.setter
    @enforce_parameter_types
    def radial_error_magnitude(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RadialErrorMagnitude",
            float(value) if value is not None else 0.0,
        )

    @property
    def radial_specification_method(self: "Self") -> "_1970.RadialSpecificationMethod":
        """mastapy.bearings.tolerances.RadialSpecificationMethod"""
        temp = pythonnet_property_get(self.wrapped, "RadialSpecificationMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.Tolerances.RadialSpecificationMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.tolerances._1970", "RadialSpecificationMethod"
        )(value)

    @radial_specification_method.setter
    @enforce_parameter_types
    def radial_specification_method(
        self: "Self", value: "_1970.RadialSpecificationMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.Tolerances.RadialSpecificationMethod"
        )
        pythonnet_property_set(self.wrapped, "RadialSpecificationMethod", value)

    @property
    def theta_x(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ThetaX")

        if temp is None:
            return 0.0

        return temp

    @theta_x.setter
    @enforce_parameter_types
    def theta_x(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ThetaX", float(value) if value is not None else 0.0
        )

    @property
    def theta_y(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ThetaY")

        if temp is None:
            return 0.0

        return temp

    @theta_y.setter
    @enforce_parameter_types
    def theta_y(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ThetaY", float(value) if value is not None else 0.0
        )

    @property
    def x(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "X")

        if temp is None:
            return 0.0

        return temp

    @x.setter
    @enforce_parameter_types
    def x(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "X", float(value) if value is not None else 0.0
        )

    @property
    def y(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Y")

        if temp is None:
            return 0.0

        return temp

    @y.setter
    @enforce_parameter_types
    def y(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Y", float(value) if value is not None else 0.0
        )

    @property
    def z(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Z")

        if temp is None:
            return 0.0

        return temp

    @z.setter
    @enforce_parameter_types
    def z(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Z", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_SupportDetail":
        """Cast to another type.

        Returns:
            _Cast_SupportDetail
        """
        return _Cast_SupportDetail(self)
