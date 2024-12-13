"""EigenvalueOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.nodal_analysis import _78

_EIGENVALUE_OPTIONS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses", "EigenvalueOptions"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    Self = TypeVar("Self", bound="EigenvalueOptions")
    CastSelf = TypeVar("CastSelf", bound="EigenvalueOptions._Cast_EigenvalueOptions")


__docformat__ = "restructuredtext en"
__all__ = ("EigenvalueOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_EigenvalueOptions:
    """Special nested class for casting EigenvalueOptions to subclasses."""

    __parent__: "EigenvalueOptions"

    @property
    def eigenvalue_options(self: "CastSelf") -> "EigenvalueOptions":
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
class EigenvalueOptions(_0.APIBase):
    """EigenvalueOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _EIGENVALUE_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def maximum_mode_frequency(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MaximumModeFrequency")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_mode_frequency.setter
    @enforce_parameter_types
    def maximum_mode_frequency(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaximumModeFrequency", value)

    @property
    def minimum_mode_frequency(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MinimumModeFrequency")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_mode_frequency.setter
    @enforce_parameter_types
    def minimum_mode_frequency(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MinimumModeFrequency", value)

    @property
    def mode_frequency_shift(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ModeFrequencyShift")

        if temp is None:
            return 0.0

        return temp

    @mode_frequency_shift.setter
    @enforce_parameter_types
    def mode_frequency_shift(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ModeFrequencyShift",
            float(value) if value is not None else 0.0,
        )

    @property
    def mode_input_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ModeInputType":
        """EnumWithSelectedValue[mastapy.nodal_analysis.ModeInputType]"""
        temp = pythonnet_property_get(self.wrapped, "ModeInputMethod")

        if temp is None:
            return None

        value = (
            enum_with_selected_value.EnumWithSelectedValue_ModeInputType.wrapped_type()
        )
        return enum_with_selected_value_runtime.create(temp, value)

    @mode_input_method.setter
    @enforce_parameter_types
    def mode_input_method(self: "Self", value: "_78.ModeInputType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = (
            enum_with_selected_value.EnumWithSelectedValue_ModeInputType.implicit_type()
        )
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ModeInputMethod", value)

    @property
    def number_of_modes(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfModes")

        if temp is None:
            return 0

        return temp

    @number_of_modes.setter
    @enforce_parameter_types
    def number_of_modes(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfModes", int(value) if value is not None else 0
        )

    @property
    def overall_amls_cutoff_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OverallAMLSCutoffFactor")

        if temp is None:
            return 0.0

        return temp

    @overall_amls_cutoff_factor.setter
    @enforce_parameter_types
    def overall_amls_cutoff_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverallAMLSCutoffFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def reduced_amls_cutoff_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ReducedAMLSCutoffFactor")

        if temp is None:
            return 0.0

        return temp

    @reduced_amls_cutoff_factor.setter
    @enforce_parameter_types
    def reduced_amls_cutoff_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReducedAMLSCutoffFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputDefaultReportTo", file_path if file_path else ""
        )

    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportTo", file_path if file_path else ""
        )

    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportAsTextTo", file_path if file_path else ""
        )

    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_EigenvalueOptions":
        """Cast to another type.

        Returns:
            _Cast_EigenvalueOptions
        """
        return _Cast_EigenvalueOptions(self)
