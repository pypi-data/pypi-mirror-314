"""SystemDeflectionFEExportOptions"""

from __future__ import annotations

from enum import Enum
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
from mastapy._private._internal.implicit import (
    enum_with_selected_value,
    list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.nodal_analysis.fe_export_utility import _173, _174
from mastapy._private.utility.units_and_measurements import _1662

_SYSTEM_DEFLECTION_FE_EXPORT_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "SystemDeflectionFEExportOptions"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.fe import _2462, _2463

    Self = TypeVar("Self", bound="SystemDeflectionFEExportOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SystemDeflectionFEExportOptions._Cast_SystemDeflectionFEExportOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SystemDeflectionFEExportOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SystemDeflectionFEExportOptions:
    """Special nested class for casting SystemDeflectionFEExportOptions to subclasses."""

    __parent__: "SystemDeflectionFEExportOptions"

    @property
    def system_deflection_fe_export_options(
        self: "CastSelf",
    ) -> "SystemDeflectionFEExportOptions":
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
class SystemDeflectionFEExportOptions(_0.APIBase):
    """SystemDeflectionFEExportOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SYSTEM_DEFLECTION_FE_EXPORT_OPTIONS

    class ExportType(Enum):
        """ExportType is a nested enum."""

        @classmethod
        def type_(cls) -> "Type":
            return _SYSTEM_DEFLECTION_FE_EXPORT_OPTIONS.ExportType

        BOUNDARY_CONDITIONS_FOR_FE_SOLVER = 0
        FULL_MESH_RESULTS_AS_OP2_FILE = 1

    def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
        raise AttributeError("Cannot set the attributes of an Enum.") from None

    def __enum_delattr(self: "Self", attr: str) -> None:
        raise AttributeError("Cannot delete the attributes of an Enum.") from None

    ExportType.__setattr__ = __enum_setattr
    ExportType.__delattr__ = __enum_delattr

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def alternative_fe_mesh_file(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AlternativeFEMeshFile")

        if temp is None:
            return ""

        return temp

    @property
    def base_couplings_on_alternative_fe_mesh(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "BaseCouplingsOnAlternativeFEMesh")

        if temp is None:
            return False

        return temp

    @base_couplings_on_alternative_fe_mesh.setter
    @enforce_parameter_types
    def base_couplings_on_alternative_fe_mesh(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BaseCouplingsOnAlternativeFEMesh",
            bool(value) if value is not None else False,
        )

    @property
    def default_type_of_result_to_export(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_BoundaryConditionType":
        """EnumWithSelectedValue[mastapy.nodal_analysis.fe_export_utility.BoundaryConditionType]"""
        temp = pythonnet_property_get(self.wrapped, "DefaultTypeOfResultToExport")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_BoundaryConditionType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @default_type_of_result_to_export.setter
    @enforce_parameter_types
    def default_type_of_result_to_export(
        self: "Self", value: "_173.BoundaryConditionType"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_BoundaryConditionType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "DefaultTypeOfResultToExport", value)

    @property
    def fe_export_format(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_FEExportFormat":
        """EnumWithSelectedValue[mastapy.nodal_analysis.fe_export_utility.FEExportFormat]"""
        temp = pythonnet_property_get(self.wrapped, "FEExportFormat")

        if temp is None:
            return None

        value = (
            enum_with_selected_value.EnumWithSelectedValue_FEExportFormat.wrapped_type()
        )
        return enum_with_selected_value_runtime.create(temp, value)

    @fe_export_format.setter
    @enforce_parameter_types
    def fe_export_format(self: "Self", value: "_174.FEExportFormat") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FEExportFormat.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "FEExportFormat", value)

    @property
    def file_type(self: "Self") -> "SystemDeflectionFEExportOptions.ExportType":
        """mastapy.system_model.fe.SystemDeflectionFEExportOptions.ExportType"""
        temp = pythonnet_property_get(self.wrapped, "FileType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.FE.SystemDeflectionFEExportOptions+ExportType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.fe.SystemDeflectionFEExportOptions.SystemDeflectionFEExportOptions",
            "ExportType",
        )(value)

    @file_type.setter
    @enforce_parameter_types
    def file_type(
        self: "Self", value: "SystemDeflectionFEExportOptions.ExportType"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.FE.SystemDeflectionFEExportOptions+ExportType",
        )
        pythonnet_property_set(self.wrapped, "FileType", value)

    @property
    def force_unit(self: "Self") -> "list_with_selected_item.ListWithSelectedItem_Unit":
        """ListWithSelectedItem[mastapy.utility.units_and_measurements.Unit]"""
        temp = pythonnet_property_get(self.wrapped, "ForceUnit")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Unit",
        )(temp)

    @force_unit.setter
    @enforce_parameter_types
    def force_unit(self: "Self", value: "_1662.Unit") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.wrapper_type()
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "ForceUnit", value)

    @property
    def include_rigid_coupling_nodes_and_constraints_added_by_masta(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "IncludeRigidCouplingNodesAndConstraintsAddedByMASTA"
        )

        if temp is None:
            return False

        return temp

    @include_rigid_coupling_nodes_and_constraints_added_by_masta.setter
    @enforce_parameter_types
    def include_rigid_coupling_nodes_and_constraints_added_by_masta(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeRigidCouplingNodesAndConstraintsAddedByMASTA",
            bool(value) if value is not None else False,
        )

    @property
    def include_an_fe_mesh(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeAnFEMesh")

        if temp is None:
            return False

        return temp

    @include_an_fe_mesh.setter
    @enforce_parameter_types
    def include_an_fe_mesh(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IncludeAnFEMesh", bool(value) if value is not None else False
        )

    @property
    def length_unit(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_Unit":
        """ListWithSelectedItem[mastapy.utility.units_and_measurements.Unit]"""
        temp = pythonnet_property_get(self.wrapped, "LengthUnit")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Unit",
        )(temp)

    @length_unit.setter
    @enforce_parameter_types
    def length_unit(self: "Self", value: "_1662.Unit") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.wrapper_type()
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "LengthUnit", value)

    @property
    def path_of_fe_mesh_file_to_be_included(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PathOfFEMeshFileToBeIncluded")

        if temp is None:
            return ""

        return temp

    @property
    def use_rigid_coupling_types_from_fe_substructure_for_exported_couplings(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseRigidCouplingTypesFromFESubstructureForExportedCouplings"
        )

        if temp is None:
            return False

        return temp

    @use_rigid_coupling_types_from_fe_substructure_for_exported_couplings.setter
    @enforce_parameter_types
    def use_rigid_coupling_types_from_fe_substructure_for_exported_couplings(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseRigidCouplingTypesFromFESubstructureForExportedCouplings",
            bool(value) if value is not None else False,
        )

    @property
    def links(self: "Self") -> "List[_2462.PerLinkExportOptions]":
        """List[mastapy.system_model.fe.PerLinkExportOptions]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Links")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def nodes(self: "Self") -> "List[_2463.PerNodeExportOptions]":
        """List[mastapy.system_model.fe.PerNodeExportOptions]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Nodes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

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
    def export_to_file(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "ExportToFile", file_path if file_path else ""
        )

    @enforce_parameter_types
    def export_to_op2_file(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "ExportToOP2File", file_path if file_path else ""
        )

    @enforce_parameter_types
    def set_alternative_fe_mesh_file(
        self: "Self",
        file_path: "str",
        format_: "_174.FEExportFormat",
        length_scale: "float" = 1.0,
        force_scale: "float" = 1.0,
    ) -> None:
        """Method does not return.

        Args:
            file_path (str)
            format_ (mastapy.nodal_analysis.fe_export_utility.FEExportFormat)
            length_scale (float, optional)
            force_scale (float, optional)
        """
        file_path = str(file_path)
        format_ = conversion.mp_to_pn_enum(
            format_, "SMT.MastaAPI.NodalAnalysis.FeExportUtility.FEExportFormat"
        )
        length_scale = float(length_scale)
        force_scale = float(force_scale)
        pythonnet_method_call(
            self.wrapped,
            "SetAlternativeFEMeshFile",
            file_path if file_path else "",
            format_,
            length_scale if length_scale else 0.0,
            force_scale if force_scale else 0.0,
        )

    @enforce_parameter_types
    def set_fe_mesh_file_to_include(
        self: "Self",
        file_path: "str",
        format_: "_174.FEExportFormat",
        length_scale: "float" = 1.0,
        force_scale: "float" = 1.0,
    ) -> None:
        """Method does not return.

        Args:
            file_path (str)
            format_ (mastapy.nodal_analysis.fe_export_utility.FEExportFormat)
            length_scale (float, optional)
            force_scale (float, optional)
        """
        file_path = str(file_path)
        format_ = conversion.mp_to_pn_enum(
            format_, "SMT.MastaAPI.NodalAnalysis.FeExportUtility.FEExportFormat"
        )
        length_scale = float(length_scale)
        force_scale = float(force_scale)
        pythonnet_method_call(
            self.wrapped,
            "SetFEMeshFileToInclude",
            file_path if file_path else "",
            format_,
            length_scale if length_scale else 0.0,
            force_scale if force_scale else 0.0,
        )

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
    def cast_to(self: "Self") -> "_Cast_SystemDeflectionFEExportOptions":
        """Cast to another type.

        Returns:
            _Cast_SystemDeflectionFEExportOptions
        """
        return _Cast_SystemDeflectionFEExportOptions(self)
