"""DrawStyleForFE"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_DRAW_STYLE_FOR_FE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses", "DrawStyleForFE"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.nodal_analysis import _59

    Self = TypeVar("Self", bound="DrawStyleForFE")
    CastSelf = TypeVar("CastSelf", bound="DrawStyleForFE._Cast_DrawStyleForFE")


__docformat__ = "restructuredtext en"
__all__ = ("DrawStyleForFE",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DrawStyleForFE:
    """Special nested class for casting DrawStyleForFE to subclasses."""

    __parent__: "DrawStyleForFE"

    @property
    def draw_style_for_fe(self: "CastSelf") -> "DrawStyleForFE":
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
class DrawStyleForFE(_0.APIBase):
    """DrawStyleForFE

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DRAW_STYLE_FOR_FE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def grounded_nodes(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "GroundedNodes")

        if temp is None:
            return False

        return temp

    @grounded_nodes.setter
    @enforce_parameter_types
    def grounded_nodes(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "GroundedNodes", bool(value) if value is not None else False
        )

    @property
    def highlight_bad_elements(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HighlightBadElements")

        if temp is None:
            return False

        return temp

    @highlight_bad_elements.setter
    @enforce_parameter_types
    def highlight_bad_elements(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HighlightBadElements",
            bool(value) if value is not None else False,
        )

    @property
    def line_option(self: "Self") -> "_59.FEMeshElementEntityOption":
        """mastapy.nodal_analysis.FEMeshElementEntityOption"""
        temp = pythonnet_property_get(self.wrapped, "LineOption")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.FEMeshElementEntityOption"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis._59", "FEMeshElementEntityOption"
        )(value)

    @line_option.setter
    @enforce_parameter_types
    def line_option(self: "Self", value: "_59.FEMeshElementEntityOption") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.FEMeshElementEntityOption"
        )
        pythonnet_property_set(self.wrapped, "LineOption", value)

    @property
    def node_size(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NodeSize")

        if temp is None:
            return 0

        return temp

    @node_size.setter
    @enforce_parameter_types
    def node_size(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NodeSize", int(value) if value is not None else 0
        )

    @property
    def rigid_elements(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "RigidElements")

        if temp is None:
            return False

        return temp

    @rigid_elements.setter
    @enforce_parameter_types
    def rigid_elements(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "RigidElements", bool(value) if value is not None else False
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
    def cast_to(self: "Self") -> "_Cast_DrawStyleForFE":
        """Cast to another type.

        Returns:
            _Cast_DrawStyleForFE
        """
        return _Cast_DrawStyleForFE(self)
