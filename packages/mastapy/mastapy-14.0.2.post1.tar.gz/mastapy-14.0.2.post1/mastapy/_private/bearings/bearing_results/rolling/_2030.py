"""ISO14179Settings"""

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
from mastapy._private.utility.databases import _1884

_ISO14179_SETTINGS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "ISO14179Settings"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2121
    from mastapy._private.math_utility.measured_data import _1617, _1618

    Self = TypeVar("Self", bound="ISO14179Settings")
    CastSelf = TypeVar("CastSelf", bound="ISO14179Settings._Cast_ISO14179Settings")


__docformat__ = "restructuredtext en"
__all__ = ("ISO14179Settings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO14179Settings:
    """Special nested class for casting ISO14179Settings to subclasses."""

    __parent__: "ISO14179Settings"

    @property
    def named_database_item(self: "CastSelf") -> "_1884.NamedDatabaseItem":
        return self.__parent__._cast(_1884.NamedDatabaseItem)

    @property
    def iso14179_settings(self: "CastSelf") -> "ISO14179Settings":
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
class ISO14179Settings(_1884.NamedDatabaseItem):
    """ISO14179Settings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO14179_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def isotr141792001f1_specification_method(
        self: "Self",
    ) -> "_2121.PowerRatingF1EstimationMethod":
        """mastapy.bearings.bearing_results.rolling.PowerRatingF1EstimationMethod"""
        temp = pythonnet_property_get(
            self.wrapped, "ISOTR141792001F1SpecificationMethod"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Bearings.BearingResults.Rolling.PowerRatingF1EstimationMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.bearing_results.rolling._2121",
            "PowerRatingF1EstimationMethod",
        )(value)

    @isotr141792001f1_specification_method.setter
    @enforce_parameter_types
    def isotr141792001f1_specification_method(
        self: "Self", value: "_2121.PowerRatingF1EstimationMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Bearings.BearingResults.Rolling.PowerRatingF1EstimationMethod",
        )
        pythonnet_property_set(
            self.wrapped, "ISOTR141792001F1SpecificationMethod", value
        )

    @property
    def user_specified_f1_for_isotr141792001(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedF1ForISOTR141792001")

        if temp is None:
            return 0.0

        return temp

    @user_specified_f1_for_isotr141792001.setter
    @enforce_parameter_types
    def user_specified_f1_for_isotr141792001(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UserSpecifiedF1ForISOTR141792001",
            float(value) if value is not None else 0.0,
        )

    @property
    def power_rating_f0_scaling_factor_one_dimensional_lookup_table(
        self: "Self",
    ) -> "_1617.OnedimensionalFunctionLookupTable":
        """mastapy.math_utility.measured_data.OnedimensionalFunctionLookupTable

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerRatingF0ScalingFactorOneDimensionalLookupTable"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def power_rating_f1_one_dimensional_lookup_table(
        self: "Self",
    ) -> "_1617.OnedimensionalFunctionLookupTable":
        """mastapy.math_utility.measured_data.OnedimensionalFunctionLookupTable

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerRatingF1OneDimensionalLookupTable"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def power_rating_f1_scaling_factor_one_dimensional_lookup_table(
        self: "Self",
    ) -> "_1617.OnedimensionalFunctionLookupTable":
        """mastapy.math_utility.measured_data.OnedimensionalFunctionLookupTable

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerRatingF1ScalingFactorOneDimensionalLookupTable"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def power_rating_f1_two_dimensional_lookup_table(
        self: "Self",
    ) -> "_1618.TwodimensionalFunctionLookupTable":
        """mastapy.math_utility.measured_data.TwodimensionalFunctionLookupTable

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerRatingF1TwoDimensionalLookupTable"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ISO14179Settings":
        """Cast to another type.

        Returns:
            _Cast_ISO14179Settings
        """
        return _Cast_ISO14179Settings(self)
