"""MeasurementSettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import list_with_selected_item, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility import _1645
from mastapy._private.utility.units_and_measurements import _1657

_MEASUREMENT_SETTINGS = python_net_import(
    "SMT.MastaAPI.Utility.UnitsAndMeasurements", "MeasurementSettings"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.units_and_measurements import _7734
    from mastapy._private.utility import _1646

    Self = TypeVar("Self", bound="MeasurementSettings")
    CastSelf = TypeVar(
        "CastSelf", bound="MeasurementSettings._Cast_MeasurementSettings"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MeasurementSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MeasurementSettings:
    """Special nested class for casting MeasurementSettings to subclasses."""

    __parent__: "MeasurementSettings"

    @property
    def per_machine_settings(self: "CastSelf") -> "_1645.PerMachineSettings":
        return self.__parent__._cast(_1645.PerMachineSettings)

    @property
    def persistent_singleton(self: "CastSelf") -> "_1646.PersistentSingleton":
        from mastapy._private.utility import _1646

        return self.__parent__._cast(_1646.PersistentSingleton)

    @property
    def measurement_settings(self: "CastSelf") -> "MeasurementSettings":
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
class MeasurementSettings(_1645.PerMachineSettings):
    """MeasurementSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MEASUREMENT_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def large_number_cutoff(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LargeNumberCutoff")

        if temp is None:
            return 0.0

        return temp

    @large_number_cutoff.setter
    @enforce_parameter_types
    def large_number_cutoff(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LargeNumberCutoff",
            float(value) if value is not None else 0.0,
        )

    @property
    def number_decimal_separator(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "NumberDecimalSeparator")

        if temp is None:
            return ""

        return temp

    @number_decimal_separator.setter
    @enforce_parameter_types
    def number_decimal_separator(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberDecimalSeparator",
            str(value) if value is not None else "",
        )

    @property
    def number_group_separator(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "NumberGroupSeparator")

        if temp is None:
            return ""

        return temp

    @number_group_separator.setter
    @enforce_parameter_types
    def number_group_separator(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberGroupSeparator",
            str(value) if value is not None else "",
        )

    @property
    def sample_input(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SampleInput")

        if temp is None:
            return ""

        return temp

    @property
    def sample_output(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SampleOutput")

        if temp is None:
            return ""

        return temp

    @property
    def selected_measurement(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_MeasurementBase":
        """ListWithSelectedItem[mastapy.utility.units_and_measurements.MeasurementBase]"""
        temp = pythonnet_property_get(self.wrapped, "SelectedMeasurement")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_MeasurementBase",
        )(temp)

    @selected_measurement.setter
    @enforce_parameter_types
    def selected_measurement(self: "Self", value: "_1657.MeasurementBase") -> None:
        wrapper_type = (
            list_with_selected_item.ListWithSelectedItem_MeasurementBase.wrapper_type()
        )
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_MeasurementBase.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "SelectedMeasurement", value)

    @property
    def show_trailing_zeros(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowTrailingZeros")

        if temp is None:
            return False

        return temp

    @show_trailing_zeros.setter
    @enforce_parameter_types
    def show_trailing_zeros(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowTrailingZeros",
            bool(value) if value is not None else False,
        )

    @property
    def small_number_cutoff(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "SmallNumberCutoff")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @small_number_cutoff.setter
    @enforce_parameter_types
    def small_number_cutoff(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "SmallNumberCutoff", value)

    @property
    def current_selected_measurement(self: "Self") -> "_1657.MeasurementBase":
        """mastapy.utility.units_and_measurements.MeasurementBase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurrentSelectedMeasurement")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    def default_to_imperial(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "DefaultToImperial")

    def default_to_metric(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "DefaultToMetric")

    @enforce_parameter_types
    def find_measurement_by_name(self: "Self", name: "str") -> "_1657.MeasurementBase":
        """mastapy.utility.units_and_measurements.MeasurementBase

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "FindMeasurementByName", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def get_measurement(
        self: "Self", measurement_type: "_7734.MeasurementType"
    ) -> "_1657.MeasurementBase":
        """mastapy.utility.units_and_measurements.MeasurementBase

        Args:
            measurement_type (mastapy.units_and_measurements.MeasurementType)
        """
        measurement_type = conversion.mp_to_pn_enum(
            measurement_type, "SMT.MastaAPIUtility.UnitsAndMeasurements.MeasurementType"
        )
        method_result = pythonnet_method_call(
            self.wrapped, "GetMeasurement", measurement_type
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_MeasurementSettings":
        """Cast to another type.

        Returns:
            _Cast_MeasurementSettings
        """
        return _Cast_MeasurementSettings(self)
