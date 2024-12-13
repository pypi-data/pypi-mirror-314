"""ConicalSetMicroGeometryConfigBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.analysis import _1271
from mastapy._private.gears.ltca import _852

_CONICAL_SET_MICRO_GEOMETRY_CONFIG_BASE = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "ConicalSetMicroGeometryConfigBase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears import _337
    from mastapy._private.gears.analysis import _1257, _1266
    from mastapy._private.gears.manufacturing.bevel import _816, _817

    Self = TypeVar("Self", bound="ConicalSetMicroGeometryConfigBase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalSetMicroGeometryConfigBase._Cast_ConicalSetMicroGeometryConfigBase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalSetMicroGeometryConfigBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalSetMicroGeometryConfigBase:
    """Special nested class for casting ConicalSetMicroGeometryConfigBase to subclasses."""

    __parent__: "ConicalSetMicroGeometryConfigBase"

    @property
    def gear_set_implementation_detail(
        self: "CastSelf",
    ) -> "_1271.GearSetImplementationDetail":
        return self.__parent__._cast(_1271.GearSetImplementationDetail)

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "_1266.GearSetDesignAnalysis":
        from mastapy._private.gears.analysis import _1266

        return self.__parent__._cast(_1266.GearSetDesignAnalysis)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1257.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1257

        return self.__parent__._cast(_1257.AbstractGearSetAnalysis)

    @property
    def conical_set_manufacturing_config(
        self: "CastSelf",
    ) -> "_816.ConicalSetManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _816

        return self.__parent__._cast(_816.ConicalSetManufacturingConfig)

    @property
    def conical_set_micro_geometry_config(
        self: "CastSelf",
    ) -> "_817.ConicalSetMicroGeometryConfig":
        from mastapy._private.gears.manufacturing.bevel import _817

        return self.__parent__._cast(_817.ConicalSetMicroGeometryConfig)

    @property
    def conical_set_micro_geometry_config_base(
        self: "CastSelf",
    ) -> "ConicalSetMicroGeometryConfigBase":
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
class ConicalSetMicroGeometryConfigBase(_1271.GearSetImplementationDetail):
    """ConicalSetMicroGeometryConfigBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_SET_MICRO_GEOMETRY_CONFIG_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def compound_layer_thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CompoundLayerThickness")

        if temp is None:
            return 0.0

        return temp

    @compound_layer_thickness.setter
    @enforce_parameter_types
    def compound_layer_thickness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CompoundLayerThickness",
            float(value) if value is not None else 0.0,
        )

    @property
    def contact_chart_results_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ContactResultType":
        """EnumWithSelectedValue[mastapy.gears.ltca.ContactResultType]"""
        temp = pythonnet_property_get(self.wrapped, "ContactChartResultsType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ContactResultType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @contact_chart_results_type.setter
    @enforce_parameter_types
    def contact_chart_results_type(
        self: "Self", value: "_852.ContactResultType"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ContactResultType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ContactChartResultsType", value)

    @property
    def deflection_from_bending_option(
        self: "Self",
    ) -> "_337.DeflectionFromBendingOption":
        """mastapy.gears.DeflectionFromBendingOption"""
        temp = pythonnet_property_get(self.wrapped, "DeflectionFromBendingOption")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.DeflectionFromBendingOption"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._337", "DeflectionFromBendingOption"
        )(value)

    @deflection_from_bending_option.setter
    @enforce_parameter_types
    def deflection_from_bending_option(
        self: "Self", value: "_337.DeflectionFromBendingOption"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.DeflectionFromBendingOption"
        )
        pythonnet_property_set(self.wrapped, "DeflectionFromBendingOption", value)

    @property
    def file_location_for_contact_chart(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "FileLocationForContactChart")

        if temp is None:
            return ""

        return temp

    @file_location_for_contact_chart.setter
    @enforce_parameter_types
    def file_location_for_contact_chart(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FileLocationForContactChart",
            str(value) if value is not None else "",
        )

    @property
    def number_of_columns_for_grid(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfColumnsForGrid")

        if temp is None:
            return 0

        return temp

    @number_of_columns_for_grid.setter
    @enforce_parameter_types
    def number_of_columns_for_grid(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfColumnsForGrid",
            int(value) if value is not None else 0,
        )

    @property
    def number_of_points_for_interpolated_surface_u(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfPointsForInterpolatedSurfaceU"
        )

        if temp is None:
            return 0

        return temp

    @number_of_points_for_interpolated_surface_u.setter
    @enforce_parameter_types
    def number_of_points_for_interpolated_surface_u(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfPointsForInterpolatedSurfaceU",
            int(value) if value is not None else 0,
        )

    @property
    def number_of_points_for_interpolated_surface_v(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfPointsForInterpolatedSurfaceV"
        )

        if temp is None:
            return 0

        return temp

    @number_of_points_for_interpolated_surface_v.setter
    @enforce_parameter_types
    def number_of_points_for_interpolated_surface_v(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfPointsForInterpolatedSurfaceV",
            int(value) if value is not None else 0,
        )

    @property
    def number_of_rows_for_fillet_grid(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfRowsForFilletGrid")

        if temp is None:
            return 0

        return temp

    @number_of_rows_for_fillet_grid.setter
    @enforce_parameter_types
    def number_of_rows_for_fillet_grid(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfRowsForFilletGrid",
            int(value) if value is not None else 0,
        )

    @property
    def number_of_rows_for_flank_grid(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfRowsForFlankGrid")

        if temp is None:
            return 0

        return temp

    @number_of_rows_for_flank_grid.setter
    @enforce_parameter_types
    def number_of_rows_for_flank_grid(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfRowsForFlankGrid",
            int(value) if value is not None else 0,
        )

    @property
    def single_tooth_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SingleToothStiffness")

        if temp is None:
            return 0.0

        return temp

    @single_tooth_stiffness.setter
    @enforce_parameter_types
    def single_tooth_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SingleToothStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    def write_contact_chart_to_file_after_solve(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "WriteContactChartToFileAfterSolve")

        if temp is None:
            return False

        return temp

    @write_contact_chart_to_file_after_solve.setter
    @enforce_parameter_types
    def write_contact_chart_to_file_after_solve(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WriteContactChartToFileAfterSolve",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalSetMicroGeometryConfigBase":
        """Cast to another type.

        Returns:
            _Cast_ConicalSetMicroGeometryConfigBase
        """
        return _Cast_ConicalSetMicroGeometryConfigBase(self)
