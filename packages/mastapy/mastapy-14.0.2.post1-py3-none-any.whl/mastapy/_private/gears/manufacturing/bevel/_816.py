"""ConicalSetManufacturingConfig"""

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
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.conical import _1197, _1198
from mastapy._private.gears.manufacturing.bevel import _818

_CONICAL_SET_MANUFACTURING_CONFIG = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "ConicalSetManufacturingConfig"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1257, _1266, _1271
    from mastapy._private.gears.manufacturing.bevel import _801, _810

    Self = TypeVar("Self", bound="ConicalSetManufacturingConfig")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalSetManufacturingConfig._Cast_ConicalSetManufacturingConfig",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalSetManufacturingConfig",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalSetManufacturingConfig:
    """Special nested class for casting ConicalSetManufacturingConfig to subclasses."""

    __parent__: "ConicalSetManufacturingConfig"

    @property
    def conical_set_micro_geometry_config_base(
        self: "CastSelf",
    ) -> "_818.ConicalSetMicroGeometryConfigBase":
        return self.__parent__._cast(_818.ConicalSetMicroGeometryConfigBase)

    @property
    def gear_set_implementation_detail(
        self: "CastSelf",
    ) -> "_1271.GearSetImplementationDetail":
        from mastapy._private.gears.analysis import _1271

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
    ) -> "ConicalSetManufacturingConfig":
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
class ConicalSetManufacturingConfig(_818.ConicalSetMicroGeometryConfigBase):
    """ConicalSetManufacturingConfig

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_SET_MANUFACTURING_CONFIG

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def machine_setting_calculation_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ConicalMachineSettingCalculationMethods":
        """EnumWithSelectedValue[mastapy.gears.gear_designs.conical.ConicalMachineSettingCalculationMethods]"""
        temp = pythonnet_property_get(self.wrapped, "MachineSettingCalculationMethod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ConicalMachineSettingCalculationMethods.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @machine_setting_calculation_method.setter
    @enforce_parameter_types
    def machine_setting_calculation_method(
        self: "Self", value: "_1197.ConicalMachineSettingCalculationMethods"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ConicalMachineSettingCalculationMethods.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "MachineSettingCalculationMethod", value)

    @property
    def manufacture_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ConicalManufactureMethods":
        """EnumWithSelectedValue[mastapy.gears.gear_designs.conical.ConicalManufactureMethods]"""
        temp = pythonnet_property_get(self.wrapped, "ManufactureMethod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ConicalManufactureMethods.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @manufacture_method.setter
    @enforce_parameter_types
    def manufacture_method(
        self: "Self", value: "_1198.ConicalManufactureMethods"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ConicalManufactureMethods.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ManufactureMethod", value)

    @property
    def gear_manufacturing_configurations(
        self: "Self",
    ) -> "List[_801.ConicalGearManufacturingConfig]":
        """List[mastapy.gears.manufacturing.bevel.ConicalGearManufacturingConfig]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearManufacturingConfigurations")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def meshes(self: "Self") -> "List[_810.ConicalMeshManufacturingConfig]":
        """List[mastapy.gears.manufacturing.bevel.ConicalMeshManufacturingConfig]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Meshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    def duplicate(self: "Self") -> "ConicalSetManufacturingConfig":
        """mastapy.gears.manufacturing.bevel.ConicalSetManufacturingConfig"""
        method_result = pythonnet_method_call(self.wrapped, "Duplicate")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalSetManufacturingConfig":
        """Cast to another type.

        Returns:
            _Cast_ConicalSetManufacturingConfig
        """
        return _Cast_ConicalSetManufacturingConfig(self)
