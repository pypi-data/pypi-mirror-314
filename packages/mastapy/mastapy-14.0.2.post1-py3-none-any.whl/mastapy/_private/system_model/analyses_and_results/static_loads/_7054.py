"""HarmonicLoadDataImportBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

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

_HARMONIC_LOAD_DATA_IMPORT_BASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "HarmonicLoadDataImportBase",
)

if TYPE_CHECKING:
    from typing import Any, List, Type

    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7033,
        _7051,
        _7052,
        _7053,
        _7055,
        _7056,
        _7057,
    )

    Self = TypeVar("Self", bound="HarmonicLoadDataImportBase")
    CastSelf = TypeVar(
        "CastSelf", bound="HarmonicLoadDataImportBase._Cast_HarmonicLoadDataImportBase"
    )

T = TypeVar("T", bound="_7033.ElectricMachineHarmonicLoadImportOptionsBase")

__docformat__ = "restructuredtext en"
__all__ = ("HarmonicLoadDataImportBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicLoadDataImportBase:
    """Special nested class for casting HarmonicLoadDataImportBase to subclasses."""

    __parent__: "HarmonicLoadDataImportBase"

    @property
    def harmonic_load_data_csv_import(
        self: "CastSelf",
    ) -> "_7051.HarmonicLoadDataCSVImport":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7051,
        )

        return self.__parent__._cast(_7051.HarmonicLoadDataCSVImport)

    @property
    def harmonic_load_data_excel_import(
        self: "CastSelf",
    ) -> "_7052.HarmonicLoadDataExcelImport":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7052,
        )

        return self.__parent__._cast(_7052.HarmonicLoadDataExcelImport)

    @property
    def harmonic_load_data_flux_import(
        self: "CastSelf",
    ) -> "_7053.HarmonicLoadDataFluxImport":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7053,
        )

        return self.__parent__._cast(_7053.HarmonicLoadDataFluxImport)

    @property
    def harmonic_load_data_import_from_motor_packages(
        self: "CastSelf",
    ) -> "_7055.HarmonicLoadDataImportFromMotorPackages":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7055,
        )

        return self.__parent__._cast(_7055.HarmonicLoadDataImportFromMotorPackages)

    @property
    def harmonic_load_data_jmag_import(
        self: "CastSelf",
    ) -> "_7056.HarmonicLoadDataJMAGImport":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7056,
        )

        return self.__parent__._cast(_7056.HarmonicLoadDataJMAGImport)

    @property
    def harmonic_load_data_motor_cad_import(
        self: "CastSelf",
    ) -> "_7057.HarmonicLoadDataMotorCADImport":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7057,
        )

        return self.__parent__._cast(_7057.HarmonicLoadDataMotorCADImport)

    @property
    def harmonic_load_data_import_base(
        self: "CastSelf",
    ) -> "HarmonicLoadDataImportBase":
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
class HarmonicLoadDataImportBase(_0.APIBase, Generic[T]):
    """HarmonicLoadDataImportBase

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _HARMONIC_LOAD_DATA_IMPORT_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def file_name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "FileName")

        if temp is None:
            return ""

        return temp

    @file_name.setter
    @enforce_parameter_types
    def file_name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "FileName", str(value) if value is not None else ""
        )

    @property
    def imported_data_has_different_direction_for_tooth_ids_to_masta_model(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "ImportedDataHasDifferentDirectionForToothIdsToMASTAModel"
        )

        if temp is None:
            return False

        return temp

    @imported_data_has_different_direction_for_tooth_ids_to_masta_model.setter
    @enforce_parameter_types
    def imported_data_has_different_direction_for_tooth_ids_to_masta_model(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ImportedDataHasDifferentDirectionForToothIdsToMASTAModel",
            bool(value) if value is not None else False,
        )

    @property
    def negate_speed_data_on_import(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "NegateSpeedDataOnImport")

        if temp is None:
            return False

        return temp

    @negate_speed_data_on_import.setter
    @enforce_parameter_types
    def negate_speed_data_on_import(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NegateSpeedDataOnImport",
            bool(value) if value is not None else False,
        )

    @property
    def negate_stator_axial_load_data_on_import(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "NegateStatorAxialLoadDataOnImport")

        if temp is None:
            return False

        return temp

    @negate_stator_axial_load_data_on_import.setter
    @enforce_parameter_types
    def negate_stator_axial_load_data_on_import(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NegateStatorAxialLoadDataOnImport",
            bool(value) if value is not None else False,
        )

    @property
    def negate_stator_radial_load_data_on_import(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "NegateStatorRadialLoadDataOnImport"
        )

        if temp is None:
            return False

        return temp

    @negate_stator_radial_load_data_on_import.setter
    @enforce_parameter_types
    def negate_stator_radial_load_data_on_import(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NegateStatorRadialLoadDataOnImport",
            bool(value) if value is not None else False,
        )

    @property
    def negate_stator_tangential_load_data_on_import(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "NegateStatorTangentialLoadDataOnImport"
        )

        if temp is None:
            return False

        return temp

    @negate_stator_tangential_load_data_on_import.setter
    @enforce_parameter_types
    def negate_stator_tangential_load_data_on_import(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NegateStatorTangentialLoadDataOnImport",
            bool(value) if value is not None else False,
        )

    @property
    def negate_tooth_axial_moment_data_on_import(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "NegateToothAxialMomentDataOnImport"
        )

        if temp is None:
            return False

        return temp

    @negate_tooth_axial_moment_data_on_import.setter
    @enforce_parameter_types
    def negate_tooth_axial_moment_data_on_import(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NegateToothAxialMomentDataOnImport",
            bool(value) if value is not None else False,
        )

    @property
    def negate_torque_data_on_import(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "NegateTorqueDataOnImport")

        if temp is None:
            return False

        return temp

    @negate_torque_data_on_import.setter
    @enforce_parameter_types
    def negate_torque_data_on_import(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NegateTorqueDataOnImport",
            bool(value) if value is not None else False,
        )

    @property
    def node_id_of_first_tooth(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "NodeIdOfFirstTooth")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @node_id_of_first_tooth.setter
    @enforce_parameter_types
    def node_id_of_first_tooth(self: "Self", value: "str") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else ""
        )
        pythonnet_property_set(self.wrapped, "NodeIdOfFirstTooth", value)

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

    def read_data_from_file(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ReadDataFromFile")

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
    def cast_to(self: "Self") -> "_Cast_HarmonicLoadDataImportBase":
        """Cast to another type.

        Returns:
            _Cast_HarmonicLoadDataImportBase
        """
        return _Cast_HarmonicLoadDataImportBase(self)
