"""PartAnalysisCaseWithContourViewable"""

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
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.enums import _1877, _1878

_PART_ANALYSIS_CASE_WITH_CONTOUR_VIEWABLE = python_net_import(
    "SMT.MastaAPI.SystemModel.Drawing", "PartAnalysisCaseWithContourViewable"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.drawing import (
        _2300,
        _2301,
        _2303,
        _2305,
        _2306,
        _2308,
        _2317,
    )

    Self = TypeVar("Self", bound="PartAnalysisCaseWithContourViewable")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PartAnalysisCaseWithContourViewable._Cast_PartAnalysisCaseWithContourViewable",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartAnalysisCaseWithContourViewable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartAnalysisCaseWithContourViewable:
    """Special nested class for casting PartAnalysisCaseWithContourViewable to subclasses."""

    __parent__: "PartAnalysisCaseWithContourViewable"

    @property
    def abstract_system_deflection_viewable(
        self: "CastSelf",
    ) -> "_2300.AbstractSystemDeflectionViewable":
        from mastapy._private.system_model.drawing import _2300

        return self.__parent__._cast(_2300.AbstractSystemDeflectionViewable)

    @property
    def advanced_system_deflection_viewable(
        self: "CastSelf",
    ) -> "_2301.AdvancedSystemDeflectionViewable":
        from mastapy._private.system_model.drawing import _2301

        return self.__parent__._cast(_2301.AdvancedSystemDeflectionViewable)

    @property
    def dynamic_analysis_viewable(self: "CastSelf") -> "_2305.DynamicAnalysisViewable":
        from mastapy._private.system_model.drawing import _2305

        return self.__parent__._cast(_2305.DynamicAnalysisViewable)

    @property
    def harmonic_analysis_viewable(
        self: "CastSelf",
    ) -> "_2306.HarmonicAnalysisViewable":
        from mastapy._private.system_model.drawing import _2306

        return self.__parent__._cast(_2306.HarmonicAnalysisViewable)

    @property
    def modal_analysis_viewable(self: "CastSelf") -> "_2308.ModalAnalysisViewable":
        from mastapy._private.system_model.drawing import _2308

        return self.__parent__._cast(_2308.ModalAnalysisViewable)

    @property
    def system_deflection_viewable(
        self: "CastSelf",
    ) -> "_2317.SystemDeflectionViewable":
        from mastapy._private.system_model.drawing import _2317

        return self.__parent__._cast(_2317.SystemDeflectionViewable)

    @property
    def part_analysis_case_with_contour_viewable(
        self: "CastSelf",
    ) -> "PartAnalysisCaseWithContourViewable":
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
class PartAnalysisCaseWithContourViewable(_0.APIBase):
    """PartAnalysisCaseWithContourViewable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_ANALYSIS_CASE_WITH_CONTOUR_VIEWABLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def contour(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOptionFirstSelection":
        """EnumWithSelectedValue[mastapy.utility.enums.ThreeDViewContourOptionFirstSelection]"""
        temp = pythonnet_property_get(self.wrapped, "Contour")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOptionFirstSelection.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @contour.setter
    @enforce_parameter_types
    def contour(
        self: "Self", value: "_1877.ThreeDViewContourOptionFirstSelection"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOptionFirstSelection.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "Contour", value)

    @property
    def contour_secondary(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOptionSecondSelection":
        """EnumWithSelectedValue[mastapy.utility.enums.ThreeDViewContourOptionSecondSelection]"""
        temp = pythonnet_property_get(self.wrapped, "ContourSecondary")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOptionSecondSelection.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @contour_secondary.setter
    @enforce_parameter_types
    def contour_secondary(
        self: "Self", value: "_1878.ThreeDViewContourOptionSecondSelection"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOptionSecondSelection.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ContourSecondary", value)

    @property
    def contour_draw_style(self: "Self") -> "_2303.ContourDrawStyle":
        """mastapy.system_model.drawing.ContourDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContourDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

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
    def cast_to(self: "Self") -> "_Cast_PartAnalysisCaseWithContourViewable":
        """Cast to another type.

        Returns:
            _Cast_PartAnalysisCaseWithContourViewable
        """
        return _Cast_PartAnalysisCaseWithContourViewable(self)
