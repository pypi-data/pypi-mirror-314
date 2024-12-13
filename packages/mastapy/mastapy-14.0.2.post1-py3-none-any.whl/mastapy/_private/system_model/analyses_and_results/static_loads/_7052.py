"""HarmonicLoadDataExcelImport"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
from mastapy._private.system_model.analyses_and_results.static_loads import _7031, _7054
from mastapy._private.utility.units_and_measurements import _1662

_HARMONIC_LOAD_DATA_EXCEL_IMPORT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "HarmonicLoadDataExcelImport",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.static_loads import _7080

    Self = TypeVar("Self", bound="HarmonicLoadDataExcelImport")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HarmonicLoadDataExcelImport._Cast_HarmonicLoadDataExcelImport",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicLoadDataExcelImport",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicLoadDataExcelImport:
    """Special nested class for casting HarmonicLoadDataExcelImport to subclasses."""

    __parent__: "HarmonicLoadDataExcelImport"

    @property
    def harmonic_load_data_import_base(
        self: "CastSelf",
    ) -> "_7054.HarmonicLoadDataImportBase":
        return self.__parent__._cast(_7054.HarmonicLoadDataImportBase)

    @property
    def harmonic_load_data_excel_import(
        self: "CastSelf",
    ) -> "HarmonicLoadDataExcelImport":
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
class HarmonicLoadDataExcelImport(
    _7054.HarmonicLoadDataImportBase[
        _7031.ElectricMachineHarmonicLoadExcelImportOptions
    ]
):
    """HarmonicLoadDataExcelImport

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HARMONIC_LOAD_DATA_EXCEL_IMPORT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def column_index_of_first_data_point(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "ColumnIndexOfFirstDataPoint")

        if temp is None:
            return 0

        return temp

    @column_index_of_first_data_point.setter
    @enforce_parameter_types
    def column_index_of_first_data_point(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ColumnIndexOfFirstDataPoint",
            int(value) if value is not None else 0,
        )

    @property
    def column_index_of_first_speed_point(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "ColumnIndexOfFirstSpeedPoint")

        if temp is None:
            return 0

        return temp

    @column_index_of_first_speed_point.setter
    @enforce_parameter_types
    def column_index_of_first_speed_point(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ColumnIndexOfFirstSpeedPoint",
            int(value) if value is not None else 0,
        )

    @property
    def excitation_order_as_rotational_order_of_shaft(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ExcitationOrderAsRotationalOrderOfShaft"
        )

        if temp is None:
            return 0.0

        return temp

    @excitation_order_as_rotational_order_of_shaft.setter
    @enforce_parameter_types
    def excitation_order_as_rotational_order_of_shaft(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ExcitationOrderAsRotationalOrderOfShaft",
            float(value) if value is not None else 0.0,
        )

    @property
    def number_of_speeds(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfSpeeds")

        if temp is None:
            return 0

        return temp

    @number_of_speeds.setter
    @enforce_parameter_types
    def number_of_speeds(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfSpeeds", int(value) if value is not None else 0
        )

    @property
    def read_speeds_from_excel_sheet(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ReadSpeedsFromExcelSheet")

        if temp is None:
            return False

        return temp

    @read_speeds_from_excel_sheet.setter
    @enforce_parameter_types
    def read_speeds_from_excel_sheet(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReadSpeedsFromExcelSheet",
            bool(value) if value is not None else False,
        )

    @property
    def row_index_of_first_data_point(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "RowIndexOfFirstDataPoint")

        if temp is None:
            return 0

        return temp

    @row_index_of_first_data_point.setter
    @enforce_parameter_types
    def row_index_of_first_data_point(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RowIndexOfFirstDataPoint",
            int(value) if value is not None else 0,
        )

    @property
    def row_index_of_first_speed_point(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "RowIndexOfFirstSpeedPoint")

        if temp is None:
            return 0

        return temp

    @row_index_of_first_speed_point.setter
    @enforce_parameter_types
    def row_index_of_first_speed_point(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RowIndexOfFirstSpeedPoint",
            int(value) if value is not None else 0,
        )

    @property
    def row_index_of_last_data_point(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "RowIndexOfLastDataPoint")

        if temp is None:
            return 0

        return temp

    @row_index_of_last_data_point.setter
    @enforce_parameter_types
    def row_index_of_last_data_point(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RowIndexOfLastDataPoint",
            int(value) if value is not None else 0,
        )

    @property
    def sheet_for_first_set_of_data(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "SheetForFirstSetOfData")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @sheet_for_first_set_of_data.setter
    @enforce_parameter_types
    def sheet_for_first_set_of_data(self: "Self", value: "str") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else ""
        )
        pythonnet_property_set(self.wrapped, "SheetForFirstSetOfData", value)

    @property
    def sheet_with_speed_data(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "SheetWithSpeedData")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @sheet_with_speed_data.setter
    @enforce_parameter_types
    def sheet_with_speed_data(self: "Self", value: "str") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else ""
        )
        pythonnet_property_set(self.wrapped, "SheetWithSpeedData", value)

    @property
    def speed_units(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_Unit":
        """ListWithSelectedItem[mastapy.utility.units_and_measurements.Unit]"""
        temp = pythonnet_property_get(self.wrapped, "SpeedUnits")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Unit",
        )(temp)

    @speed_units.setter
    @enforce_parameter_types
    def speed_units(self: "Self", value: "_1662.Unit") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.wrapper_type()
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "SpeedUnits", value)

    @property
    def units_for_data_being_imported(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_Unit":
        """ListWithSelectedItem[mastapy.utility.units_and_measurements.Unit]"""
        temp = pythonnet_property_get(self.wrapped, "UnitsForDataBeingImported")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Unit",
        )(temp)

    @units_for_data_being_imported.setter
    @enforce_parameter_types
    def units_for_data_being_imported(self: "Self", value: "_1662.Unit") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.wrapper_type()
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "UnitsForDataBeingImported", value)

    @property
    def speeds(self: "Self") -> "List[_7080.NamedSpeed]":
        """List[mastapy.system_model.analyses_and_results.static_loads.NamedSpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Speeds")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    def select_excel_file(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SelectExcelFile")

    @property
    def cast_to(self: "Self") -> "_Cast_HarmonicLoadDataExcelImport":
        """Cast to another type.

        Returns:
            _Cast_HarmonicLoadDataExcelImport
        """
        return _Cast_HarmonicLoadDataExcelImport(self)
