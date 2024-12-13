"""ConicalPinionManufacturingConfig"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.manufacturing.bevel import _801

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_CONICAL_PINION_MANUFACTURING_CONFIG = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "ConicalPinionManufacturingConfig"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1255, _1258, _1261
    from mastapy._private.gears.manufacturing.bevel import _803, _806, _810, _831, _835
    from mastapy._private.gears.manufacturing.bevel.cutters import _838, _839

    Self = TypeVar("Self", bound="ConicalPinionManufacturingConfig")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalPinionManufacturingConfig._Cast_ConicalPinionManufacturingConfig",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalPinionManufacturingConfig",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalPinionManufacturingConfig:
    """Special nested class for casting ConicalPinionManufacturingConfig to subclasses."""

    __parent__: "ConicalPinionManufacturingConfig"

    @property
    def conical_gear_manufacturing_config(
        self: "CastSelf",
    ) -> "_801.ConicalGearManufacturingConfig":
        return self.__parent__._cast(_801.ConicalGearManufacturingConfig)

    @property
    def conical_gear_micro_geometry_config_base(
        self: "CastSelf",
    ) -> "_803.ConicalGearMicroGeometryConfigBase":
        from mastapy._private.gears.manufacturing.bevel import _803

        return self.__parent__._cast(_803.ConicalGearMicroGeometryConfigBase)

    @property
    def gear_implementation_detail(
        self: "CastSelf",
    ) -> "_1261.GearImplementationDetail":
        from mastapy._private.gears.analysis import _1261

        return self.__parent__._cast(_1261.GearImplementationDetail)

    @property
    def gear_design_analysis(self: "CastSelf") -> "_1258.GearDesignAnalysis":
        from mastapy._private.gears.analysis import _1258

        return self.__parent__._cast(_1258.GearDesignAnalysis)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1255.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1255

        return self.__parent__._cast(_1255.AbstractGearAnalysis)

    @property
    def conical_pinion_manufacturing_config(
        self: "CastSelf",
    ) -> "ConicalPinionManufacturingConfig":
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
class ConicalPinionManufacturingConfig(_801.ConicalGearManufacturingConfig):
    """ConicalPinionManufacturingConfig

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_PINION_MANUFACTURING_CONFIG

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def pinion_finish_manufacturing_machine(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "PinionFinishManufacturingMachine", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @pinion_finish_manufacturing_machine.setter
    @enforce_parameter_types
    def pinion_finish_manufacturing_machine(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "PinionFinishManufacturingMachine",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    def pinion_rough_manufacturing_machine(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "PinionRoughManufacturingMachine", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @pinion_rough_manufacturing_machine.setter
    @enforce_parameter_types
    def pinion_rough_manufacturing_machine(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "PinionRoughManufacturingMachine",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    def mesh_config(self: "Self") -> "_810.ConicalMeshManufacturingConfig":
        """mastapy.gears.manufacturing.bevel.ConicalMeshManufacturingConfig

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshConfig")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def pinion_concave_ob_configuration(
        self: "Self",
    ) -> "_806.ConicalMeshFlankManufacturingConfig":
        """mastapy.gears.manufacturing.bevel.ConicalMeshFlankManufacturingConfig

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionConcaveOBConfiguration")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def pinion_convex_ib_configuration(
        self: "Self",
    ) -> "_806.ConicalMeshFlankManufacturingConfig":
        """mastapy.gears.manufacturing.bevel.ConicalMeshFlankManufacturingConfig

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionConvexIBConfiguration")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def pinion_cutter_parameters_concave(
        self: "Self",
    ) -> "_831.PinionFinishMachineSettings":
        """mastapy.gears.manufacturing.bevel.PinionFinishMachineSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionCutterParametersConcave")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def pinion_cutter_parameters_convex(
        self: "Self",
    ) -> "_831.PinionFinishMachineSettings":
        """mastapy.gears.manufacturing.bevel.PinionFinishMachineSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionCutterParametersConvex")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def pinion_finish_cutter(self: "Self") -> "_838.PinionFinishCutter":
        """mastapy.gears.manufacturing.bevel.cutters.PinionFinishCutter

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionFinishCutter")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def pinion_rough_cutter(self: "Self") -> "_839.PinionRoughCutter":
        """mastapy.gears.manufacturing.bevel.cutters.PinionRoughCutter

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionRoughCutter")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def pinion_rough_machine_setting(self: "Self") -> "_835.PinionRoughMachineSetting":
        """mastapy.gears.manufacturing.bevel.PinionRoughMachineSetting

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionRoughMachineSetting")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalPinionManufacturingConfig":
        """Cast to another type.

        Returns:
            _Cast_ConicalPinionManufacturingConfig
        """
        return _Cast_ConicalPinionManufacturingConfig(self)
