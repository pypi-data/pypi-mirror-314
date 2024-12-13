"""MASTAGUI"""

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
from mastapy._private._math.color import Color
from mastapy._private._math.vector_3d import Vector3D
from mastapy._private.nodal_analysis.geometry_modeller_link import _164

_MASTAGUI = python_net_import("SMT.MastaAPI.SystemModelGUI", "MASTAGUI")

if TYPE_CHECKING:
    from typing import Any, Dict, List, Type, TypeVar

    from mastapy._private.geometry.two_d import _323
    from mastapy._private.math_utility import _1543, _1561
    from mastapy._private.nodal_analysis.geometry_modeller_link import _163, _170, _171
    from mastapy._private.system_model import _2257, _2260
    from mastapy._private.utility.operation_modes import _1843

    Self = TypeVar("Self", bound="MASTAGUI")
    CastSelf = TypeVar("CastSelf", bound="MASTAGUI._Cast_MASTAGUI")


__docformat__ = "restructuredtext en"
__all__ = ("MASTAGUI",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MASTAGUI:
    """Special nested class for casting MASTAGUI to subclasses."""

    __parent__: "MASTAGUI"

    @property
    def mastagui(self: "CastSelf") -> "MASTAGUI":
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
class MASTAGUI(_0.APIBase):
    """MASTAGUI

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MASTAGUI

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def is_initialised(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsInitialised")

        if temp is None:
            return False

        return temp

    @property
    def is_paused(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsPaused")

        if temp is None:
            return False

        return temp

    @is_paused.setter
    @enforce_parameter_types
    def is_paused(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IsPaused", bool(value) if value is not None else False
        )

    @property
    def is_remoting(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsRemoting")

        if temp is None:
            return False

        return temp

    @property
    def active_design(self: "Self") -> "_2257.Design":
        """mastapy.system_model.Design"""
        temp = pythonnet_property_get(self.wrapped, "ActiveDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @active_design.setter
    @enforce_parameter_types
    def active_design(self: "Self", value: "_2257.Design") -> None:
        pythonnet_property_set(self.wrapped, "ActiveDesign", value.wrapped)

    @property
    def color_of_new_problem_node_group(self: "Self") -> "Color":
        """Color"""
        temp = pythonnet_property_get(self.wrapped, "ColorOfNewProblemNodeGroup")

        if temp is None:
            return None

        value = conversion.pn_to_mp_color(temp)

        if value is None:
            return None

        return value

    @color_of_new_problem_node_group.setter
    @enforce_parameter_types
    def color_of_new_problem_node_group(self: "Self", value: "Color") -> None:
        value = conversion.mp_to_pn_color(value)
        pythonnet_property_set(self.wrapped, "ColorOfNewProblemNodeGroup", value)

    @property
    def geometry_modeller_file_path_to_open(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "GeometryModellerFilePathToOpen")

        if temp is None:
            return ""

        return temp

    @geometry_modeller_file_path_to_open.setter
    @enforce_parameter_types
    def geometry_modeller_file_path_to_open(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped,
            "GeometryModellerFilePathToOpen",
            str(value) if value is not None else "",
        )

    @property
    def geometry_modeller_process_id(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "GeometryModellerProcessID")

        if temp is None:
            return 0

        return temp

    @geometry_modeller_process_id.setter
    @enforce_parameter_types
    def geometry_modeller_process_id(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "GeometryModellerProcessID",
            int(value) if value is not None else 0,
        )

    @property
    def is_connected_to_geometry_modeller(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsConnectedToGeometryModeller")

        if temp is None:
            return False

        return temp

    @is_connected_to_geometry_modeller.setter
    @enforce_parameter_types
    def is_connected_to_geometry_modeller(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsConnectedToGeometryModeller",
            bool(value) if value is not None else False,
        )

    @property
    def name_of_new_problem_node_group(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "NameOfNewProblemNodeGroup")

        if temp is None:
            return ""

        return temp

    @name_of_new_problem_node_group.setter
    @enforce_parameter_types
    def name_of_new_problem_node_group(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NameOfNewProblemNodeGroup",
            str(value) if value is not None else "",
        )

    @property
    def open_designs(self: "Self") -> "List[_2257.Design]":
        """List[mastapy.system_model.Design]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OpenDesigns")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def operation_mode(self: "Self") -> "_1843.OperationMode":
        """mastapy.utility.operation_modes.OperationMode"""
        temp = pythonnet_property_get(self.wrapped, "OperationMode")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.OperationModes.OperationMode"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility.operation_modes._1843", "OperationMode"
        )(value)

    @operation_mode.setter
    @enforce_parameter_types
    def operation_mode(self: "Self", value: "_1843.OperationMode") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Utility.OperationModes.OperationMode"
        )
        pythonnet_property_set(self.wrapped, "OperationMode", value)

    @property
    def positions_of_problem_node_group(self: "Self") -> "List[Vector3D]":
        """List[Vector3D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PositionsOfProblemNodeGroup")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector3D)

        if value is None:
            return None

        return value

    @property
    def process_id(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProcessId")

        if temp is None:
            return 0

        return temp

    @property
    def restart_geometry_modeller_flag(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "RestartGeometryModellerFlag")

        if temp is None:
            return False

        return temp

    @restart_geometry_modeller_flag.setter
    @enforce_parameter_types
    def restart_geometry_modeller_flag(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RestartGeometryModellerFlag",
            bool(value) if value is not None else False,
        )

    @property
    def restart_geometry_modeller_save_file(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "RestartGeometryModellerSaveFile")

        if temp is None:
            return ""

        return temp

    @restart_geometry_modeller_save_file.setter
    @enforce_parameter_types
    def restart_geometry_modeller_save_file(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RestartGeometryModellerSaveFile",
            str(value) if value is not None else "",
        )

    @property
    def selected_design_entity(self: "Self") -> "_2260.DesignEntity":
        """mastapy.system_model.DesignEntity"""
        temp = pythonnet_property_get(self.wrapped, "SelectedDesignEntity")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @selected_design_entity.setter
    @enforce_parameter_types
    def selected_design_entity(self: "Self", value: "_2260.DesignEntity") -> None:
        pythonnet_property_set(self.wrapped, "SelectedDesignEntity", value.wrapped)

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

    @staticmethod
    @enforce_parameter_types
    def get_mastagui(process_id: "int") -> "MASTAGUI":
        """mastapy.system_model_gui.MASTAGUI

        Args:
            process_id (int)
        """
        process_id = int(process_id)
        method_result = pythonnet_method_call(
            MASTAGUI.TYPE, "GetMASTAGUI", process_id if process_id else 0
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    def pause(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Pause")

    def resume(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Resume")

    def start_remoting(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "StartRemoting")

    def stop_remoting(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "StopRemoting")

    def aborted(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Aborted")

    @enforce_parameter_types
    def add_electric_machine_from_cad_face_group(
        self: "Self",
        cad_face_group: "_323.CADFaceGroup",
        geometry_modeller_design_information: "_163.GeometryModellerDesignInformation",
        dimensions: "Dict[str, _164.GeometryModellerDimension]",
    ) -> None:
        """Method does not return.

        Args:
            cad_face_group (mastapy.geometry.two_d.CADFaceGroup)
            geometry_modeller_design_information (mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDesignInformation)
            dimensions (Dict[str, mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDimension])
        """
        pythonnet_method_call(
            self.wrapped,
            "AddElectricMachineFromCADFaceGroup",
            cad_face_group.wrapped if cad_face_group else None,
            geometry_modeller_design_information.wrapped
            if geometry_modeller_design_information
            else None,
            dimensions,
        )

    @enforce_parameter_types
    def add_fe_substructure_from_data(
        self: "Self",
        vertices_and_facets: "_1561.FacetedBody",
        geometry_modeller_design_information: "_163.GeometryModellerDesignInformation",
        dimensions: "Dict[str, _164.GeometryModellerDimension]",
        body_moniker: "str",
    ) -> None:
        """Method does not return.

        Args:
            vertices_and_facets (mastapy.math_utility.FacetedBody)
            geometry_modeller_design_information (mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDesignInformation)
            dimensions (Dict[str, mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDimension])
            body_moniker (str)
        """
        body_moniker = str(body_moniker)
        pythonnet_method_call(
            self.wrapped,
            "AddFESubstructureFromData",
            vertices_and_facets.wrapped if vertices_and_facets else None,
            geometry_modeller_design_information.wrapped
            if geometry_modeller_design_information
            else None,
            dimensions,
            body_moniker if body_moniker else "",
        )

    @enforce_parameter_types
    def add_fe_substructure_from_file(
        self: "Self",
        length_scale: "float",
        stl_file_name: "str",
        geometry_modeller_design_information: "_163.GeometryModellerDesignInformation",
        dimensions: "Dict[str, _164.GeometryModellerDimension]",
    ) -> None:
        """Method does not return.

        Args:
            length_scale (float)
            stl_file_name (str)
            geometry_modeller_design_information (mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDesignInformation)
            dimensions (Dict[str, mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDimension])
        """
        length_scale = float(length_scale)
        stl_file_name = str(stl_file_name)
        pythonnet_method_call(
            self.wrapped,
            "AddFESubstructureFromFile",
            length_scale if length_scale else 0.0,
            stl_file_name if stl_file_name else "",
            geometry_modeller_design_information.wrapped
            if geometry_modeller_design_information
            else None,
            dimensions,
        )

    @enforce_parameter_types
    def add_line_from_geometry_modeller(
        self: "Self", circles_on_axis: "_1543.CirclesOnAxis"
    ) -> None:
        """Method does not return.

        Args:
            circles_on_axis (mastapy.math_utility.CirclesOnAxis)
        """
        pythonnet_method_call(
            self.wrapped,
            "AddLineFromGeometryModeller",
            circles_on_axis.wrapped if circles_on_axis else None,
        )

    def are_new_input_available(self: "Self") -> "_170.MeshRequest":
        """mastapy.nodal_analysis.geometry_modeller_link.MeshRequest"""
        method_result = pythonnet_method_call(self.wrapped, "AreNewInputAvailable")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def circle_pairs_from_geometry_modeller(
        self: "Self",
        preselection_circles: "_1543.CirclesOnAxis",
        selected_circles: "List[_1543.CirclesOnAxis]",
    ) -> None:
        """Method does not return.

        Args:
            preselection_circles (mastapy.math_utility.CirclesOnAxis)
            selected_circles (List[mastapy.math_utility.CirclesOnAxis])
        """
        selected_circles = conversion.mp_to_pn_objects_in_list(selected_circles)
        pythonnet_method_call(
            self.wrapped,
            "CirclePairsFromGeometryModeller",
            preselection_circles.wrapped if preselection_circles else None,
            selected_circles,
        )

    @enforce_parameter_types
    def create_geometry_modeller_design_information(
        self: "Self", file_name: "str", main_part_moniker: "str", tab_name: "str"
    ) -> "_163.GeometryModellerDesignInformation":
        """mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDesignInformation

        Args:
            file_name (str)
            main_part_moniker (str)
            tab_name (str)
        """
        file_name = str(file_name)
        main_part_moniker = str(main_part_moniker)
        tab_name = str(tab_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "CreateGeometryModellerDesignInformation",
            file_name if file_name else "",
            main_part_moniker if main_part_moniker else "",
            tab_name if tab_name else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    def create_geometry_modeller_dimension(
        self: "Self",
    ) -> "_164.GeometryModellerDimension":
        """mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDimension"""
        method_result = pythonnet_method_call(
            self.wrapped, "CreateGeometryModellerDimension"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    def create_mesh_request_result(self: "Self") -> "_171.MeshRequestResult":
        """mastapy.nodal_analysis.geometry_modeller_link.MeshRequestResult"""
        method_result = pythonnet_method_call(self.wrapped, "CreateMeshRequestResult")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    def create_new_cad_face_group(self: "Self") -> "_323.CADFaceGroup":
        """mastapy.geometry.two_d.CADFaceGroup"""
        method_result = pythonnet_method_call(self.wrapped, "CreateNewCADFaceGroup")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    def create_new_circles_on_axis(self: "Self") -> "_1543.CirclesOnAxis":
        """mastapy.math_utility.CirclesOnAxis"""
        method_result = pythonnet_method_call(self.wrapped, "CreateNewCirclesOnAxis")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    def create_new_faceted_body(self: "Self") -> "_1561.FacetedBody":
        """mastapy.math_utility.FacetedBody"""
        method_result = pythonnet_method_call(self.wrapped, "CreateNewFacetedBody")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    def flag_message_received(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "FlagMessageReceived")

    def geometry_modeller_document_loaded(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "GeometryModellerDocumentLoaded")

    @enforce_parameter_types
    def move_selected_component(
        self: "Self", origin: "Vector3D", axis: "Vector3D"
    ) -> None:
        """Method does not return.

        Args:
            origin (Vector3D)
            axis (Vector3D)
        """
        origin = conversion.mp_to_pn_vector3d(origin)
        axis = conversion.mp_to_pn_vector3d(axis)
        pythonnet_method_call(self.wrapped, "MoveSelectedComponent", origin, axis)

    @enforce_parameter_types
    def open_design_in_new_tab(self: "Self", design: "_2257.Design") -> None:
        """Method does not return.

        Args:
            design (mastapy.system_model.Design)
        """
        pythonnet_method_call(
            self.wrapped, "OpenDesignInNewTab", design.wrapped if design else None
        )

    @enforce_parameter_types
    def run_command(self: "Self", command: "str") -> None:
        """Method does not return.

        Args:
            command (str)
        """
        command = str(command)
        pythonnet_method_call(self.wrapped, "RunCommand", command if command else "")

    @enforce_parameter_types
    def select_tab(self: "Self", tab_text: "str") -> None:
        """Method does not return.

        Args:
            tab_text (str)
        """
        tab_text = str(tab_text)
        pythonnet_method_call(self.wrapped, "SelectTab", tab_text if tab_text else "")

    @enforce_parameter_types
    def set_error(self: "Self", error: "str") -> None:
        """Method does not return.

        Args:
            error (str)
        """
        error = str(error)
        pythonnet_method_call(self.wrapped, "SetError", error if error else "")

    @enforce_parameter_types
    def set_mesh_request_result(
        self: "Self", mesh_request_result: "_171.MeshRequestResult"
    ) -> None:
        """Method does not return.

        Args:
            mesh_request_result (mastapy.nodal_analysis.geometry_modeller_link.MeshRequestResult)
        """
        pythonnet_method_call(
            self.wrapped,
            "SetMeshRequestResult",
            mesh_request_result.wrapped if mesh_request_result else None,
        )

    @enforce_parameter_types
    def show_boxes(
        self: "Self",
        small_box_corners: "List[Vector3D]",
        big_box_corners: "List[Vector3D]",
    ) -> None:
        """Method does not return.

        Args:
            small_box_corners (List[Vector3D])
            big_box_corners (List[Vector3D])
        """
        small_box_corners = conversion.mp_to_pn_objects_in_list(small_box_corners)
        big_box_corners = conversion.mp_to_pn_objects_in_list(big_box_corners)
        pythonnet_method_call(
            self.wrapped, "ShowBoxes", small_box_corners, big_box_corners
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
    def cast_to(self: "Self") -> "_Cast_MASTAGUI":
        """Cast to another type.

        Returns:
            _Cast_MASTAGUI
        """
        return _Cast_MASTAGUI(self)
