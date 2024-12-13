"""FEPartDRIVASurfaceSelection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.nodal_analysis.component_mode_synthesis import _237
from mastapy._private.system_model.fe import _2441

_FE_PART_DRIVA_SURFACE_SELECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "FEPartDRIVASurfaceSelection"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="FEPartDRIVASurfaceSelection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FEPartDRIVASurfaceSelection._Cast_FEPartDRIVASurfaceSelection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FEPartDRIVASurfaceSelection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEPartDRIVASurfaceSelection:
    """Special nested class for casting FEPartDRIVASurfaceSelection to subclasses."""

    __parent__: "FEPartDRIVASurfaceSelection"

    @property
    def fe_part_driva_surface_selection(
        self: "CastSelf",
    ) -> "FEPartDRIVASurfaceSelection":
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
class FEPartDRIVASurfaceSelection(_0.APIBase):
    """FEPartDRIVASurfaceSelection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_PART_DRIVA_SURFACE_SELECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def fe_substructures(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_FESubstructure":
        """ListWithSelectedItem[mastapy.system_model.fe.FESubstructure]"""
        temp = pythonnet_property_get(self.wrapped, "FESubstructures")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_FESubstructure",
        )(temp)

    @fe_substructures.setter
    @enforce_parameter_types
    def fe_substructures(self: "Self", value: "_2441.FESubstructure") -> None:
        wrapper_type = (
            list_with_selected_item.ListWithSelectedItem_FESubstructure.wrapper_type()
        )
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_FESubstructure.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "FESubstructures", value)

    @property
    def is_included(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsIncluded")

        if temp is None:
            return False

        return temp

    @is_included.setter
    @enforce_parameter_types
    def is_included(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IsIncluded", bool(value) if value is not None else False
        )

    @property
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def surfaces(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_CMSElementFaceGroup":
        """ListWithSelectedItem[mastapy.nodal_analysis.component_mode_synthesis.CMSElementFaceGroup]"""
        temp = pythonnet_property_get(self.wrapped, "Surfaces")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_CMSElementFaceGroup",
        )(temp)

    @surfaces.setter
    @enforce_parameter_types
    def surfaces(self: "Self", value: "_237.CMSElementFaceGroup") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_CMSElementFaceGroup.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_CMSElementFaceGroup.implicit_type()
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "Surfaces", value)

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
    def cast_to(self: "Self") -> "_Cast_FEPartDRIVASurfaceSelection":
        """Cast to another type.

        Returns:
            _Cast_FEPartDRIVASurfaceSelection
        """
        return _Cast_FEPartDRIVASurfaceSelection(self)
