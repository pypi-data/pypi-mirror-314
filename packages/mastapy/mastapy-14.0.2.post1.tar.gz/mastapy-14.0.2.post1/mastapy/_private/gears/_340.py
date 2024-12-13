"""GearSetDesignGroup"""

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
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears import _349

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_GEAR_SET_DESIGN_GROUP = python_net_import("SMT.MastaAPI.Gears", "GearSetDesignGroup")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1046, _1116
    from mastapy._private.gears.rating.cylindrical import _467, _491
    from mastapy._private.materials import _269

    Self = TypeVar("Self", bound="GearSetDesignGroup")
    CastSelf = TypeVar("CastSelf", bound="GearSetDesignGroup._Cast_GearSetDesignGroup")


__docformat__ = "restructuredtext en"
__all__ = ("GearSetDesignGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetDesignGroup:
    """Special nested class for casting GearSetDesignGroup to subclasses."""

    __parent__: "GearSetDesignGroup"

    @property
    def gear_set_design_group(self: "CastSelf") -> "GearSetDesignGroup":
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
class GearSetDesignGroup(_0.APIBase):
    """GearSetDesignGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_DESIGN_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def default_cylindrical_gear_material_agma(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "DefaultCylindricalGearMaterialAGMA", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @default_cylindrical_gear_material_agma.setter
    @enforce_parameter_types
    def default_cylindrical_gear_material_agma(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "DefaultCylindricalGearMaterialAGMA",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    def default_cylindrical_gear_material_iso(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "DefaultCylindricalGearMaterialISO", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @default_cylindrical_gear_material_iso.setter
    @enforce_parameter_types
    def default_cylindrical_gear_material_iso(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "DefaultCylindricalGearMaterialISO",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    def default_rough_toleranced_metal_measurement(
        self: "Self",
    ) -> "_1116.TolerancedMetalMeasurements":
        """mastapy.gears.gear_designs.cylindrical.TolerancedMetalMeasurements"""
        temp = pythonnet_property_get(
            self.wrapped, "DefaultRoughTolerancedMetalMeasurement"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.TolerancedMetalMeasurements",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1116",
            "TolerancedMetalMeasurements",
        )(value)

    @default_rough_toleranced_metal_measurement.setter
    @enforce_parameter_types
    def default_rough_toleranced_metal_measurement(
        self: "Self", value: "_1116.TolerancedMetalMeasurements"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.TolerancedMetalMeasurements",
        )
        pythonnet_property_set(
            self.wrapped, "DefaultRoughTolerancedMetalMeasurement", value
        )

    @property
    def extra_backlash_for_all_gears(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ExtraBacklashForAllGears")

        if temp is None:
            return 0.0

        return temp

    @extra_backlash_for_all_gears.setter
    @enforce_parameter_types
    def extra_backlash_for_all_gears(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ExtraBacklashForAllGears",
            float(value) if value is not None else 0.0,
        )

    @property
    def hunting_ratio_required(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HuntingRatioRequired")

        if temp is None:
            return False

        return temp

    @hunting_ratio_required.setter
    @enforce_parameter_types
    def hunting_ratio_required(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HuntingRatioRequired",
            bool(value) if value is not None else False,
        )

    @property
    def limit_dynamic_factor_if_not_in_main_resonance_range(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "LimitDynamicFactorIfNotInMainResonanceRange"
        )

        if temp is None:
            return False

        return temp

    @limit_dynamic_factor_if_not_in_main_resonance_range.setter
    @enforce_parameter_types
    def limit_dynamic_factor_if_not_in_main_resonance_range(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "LimitDynamicFactorIfNotInMainResonanceRange",
            bool(value) if value is not None else False,
        )

    @property
    def limit_micro_geometry_factor_for_the_dynamic_load(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "LimitMicroGeometryFactorForTheDynamicLoad"
        )

        if temp is None:
            return False

        return temp

    @limit_micro_geometry_factor_for_the_dynamic_load.setter
    @enforce_parameter_types
    def limit_micro_geometry_factor_for_the_dynamic_load(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "LimitMicroGeometryFactorForTheDynamicLoad",
            bool(value) if value is not None else False,
        )

    @property
    def maximum_number_of_planets(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "MaximumNumberOfPlanets")

        if temp is None:
            return 0

        return temp

    @maximum_number_of_planets.setter
    @enforce_parameter_types
    def maximum_number_of_planets(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumNumberOfPlanets",
            int(value) if value is not None else 0,
        )

    @property
    def micro_geometry_model_in_system_deflection(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_MicroGeometryModel":
        """EnumWithSelectedValue[mastapy.gears.MicroGeometryModel]"""
        temp = pythonnet_property_get(
            self.wrapped, "MicroGeometryModelInSystemDeflection"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_MicroGeometryModel.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @micro_geometry_model_in_system_deflection.setter
    @enforce_parameter_types
    def micro_geometry_model_in_system_deflection(
        self: "Self", value: "_349.MicroGeometryModel"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_MicroGeometryModel.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped, "MicroGeometryModelInSystemDeflection", value
        )

    @property
    def minimum_factor_of_safety_for_tooth_fatigue_fracture(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumFactorOfSafetyForToothFatigueFracture"
        )

        if temp is None:
            return 0.0

        return temp

    @minimum_factor_of_safety_for_tooth_fatigue_fracture.setter
    @enforce_parameter_types
    def minimum_factor_of_safety_for_tooth_fatigue_fracture(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumFactorOfSafetyForToothFatigueFracture",
            float(value) if value is not None else 0.0,
        )

    @property
    def minimum_power_for_gear_mesh_to_be_loaded(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumPowerForGearMeshToBeLoaded")

        if temp is None:
            return 0.0

        return temp

    @minimum_power_for_gear_mesh_to_be_loaded.setter
    @enforce_parameter_types
    def minimum_power_for_gear_mesh_to_be_loaded(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumPowerForGearMeshToBeLoaded",
            float(value) if value is not None else 0.0,
        )

    @property
    def minimum_torque_for_gear_mesh_to_be_loaded(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumTorqueForGearMeshToBeLoaded"
        )

        if temp is None:
            return 0.0

        return temp

    @minimum_torque_for_gear_mesh_to_be_loaded.setter
    @enforce_parameter_types
    def minimum_torque_for_gear_mesh_to_be_loaded(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumTorqueForGearMeshToBeLoaded",
            float(value) if value is not None else 0.0,
        )

    @property
    def misalignment_contact_pattern_enhancement(
        self: "Self",
    ) -> "_491.MisalignmentContactPatternEnhancements":
        """mastapy.gears.rating.cylindrical.MisalignmentContactPatternEnhancements"""
        temp = pythonnet_property_get(
            self.wrapped, "MisalignmentContactPatternEnhancement"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.Rating.Cylindrical.MisalignmentContactPatternEnhancements",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating.cylindrical._491",
            "MisalignmentContactPatternEnhancements",
        )(value)

    @misalignment_contact_pattern_enhancement.setter
    @enforce_parameter_types
    def misalignment_contact_pattern_enhancement(
        self: "Self", value: "_491.MisalignmentContactPatternEnhancements"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.Rating.Cylindrical.MisalignmentContactPatternEnhancements",
        )
        pythonnet_property_set(
            self.wrapped, "MisalignmentContactPatternEnhancement", value
        )

    @property
    def planet_carrier_space_required(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PlanetCarrierSpaceRequired")

        if temp is None:
            return 0.0

        return temp

    @planet_carrier_space_required.setter
    @enforce_parameter_types
    def planet_carrier_space_required(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PlanetCarrierSpaceRequired",
            float(value) if value is not None else 0.0,
        )

    @property
    def relative_tolerance_for_convergence(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RelativeToleranceForConvergence")

        if temp is None:
            return 0.0

        return temp

    @relative_tolerance_for_convergence.setter
    @enforce_parameter_types
    def relative_tolerance_for_convergence(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RelativeToleranceForConvergence",
            float(value) if value is not None else 0.0,
        )

    @property
    def required_safety_factor_for_bending(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RequiredSafetyFactorForBending")

        if temp is None:
            return 0.0

        return temp

    @required_safety_factor_for_bending.setter
    @enforce_parameter_types
    def required_safety_factor_for_bending(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RequiredSafetyFactorForBending",
            float(value) if value is not None else 0.0,
        )

    @property
    def required_safety_factor_for_contact(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RequiredSafetyFactorForContact")

        if temp is None:
            return 0.0

        return temp

    @required_safety_factor_for_contact.setter
    @enforce_parameter_types
    def required_safety_factor_for_contact(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RequiredSafetyFactorForContact",
            float(value) if value is not None else 0.0,
        )

    @property
    def required_safety_factor_for_crack_initiation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "RequiredSafetyFactorForCrackInitiation"
        )

        if temp is None:
            return 0.0

        return temp

    @required_safety_factor_for_crack_initiation.setter
    @enforce_parameter_types
    def required_safety_factor_for_crack_initiation(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "RequiredSafetyFactorForCrackInitiation",
            float(value) if value is not None else 0.0,
        )

    @property
    def required_safety_factor_for_micropitting(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "RequiredSafetyFactorForMicropitting"
        )

        if temp is None:
            return 0.0

        return temp

    @required_safety_factor_for_micropitting.setter
    @enforce_parameter_types
    def required_safety_factor_for_micropitting(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RequiredSafetyFactorForMicropitting",
            float(value) if value is not None else 0.0,
        )

    @property
    def required_safety_factor_for_scuffing(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RequiredSafetyFactorForScuffing")

        if temp is None:
            return 0.0

        return temp

    @required_safety_factor_for_scuffing.setter
    @enforce_parameter_types
    def required_safety_factor_for_scuffing(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RequiredSafetyFactorForScuffing",
            float(value) if value is not None else 0.0,
        )

    @property
    def required_safety_factor_for_static_bending(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "RequiredSafetyFactorForStaticBending"
        )

        if temp is None:
            return 0.0

        return temp

    @required_safety_factor_for_static_bending.setter
    @enforce_parameter_types
    def required_safety_factor_for_static_bending(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RequiredSafetyFactorForStaticBending",
            float(value) if value is not None else 0.0,
        )

    @property
    def required_safety_factor_for_static_contact(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "RequiredSafetyFactorForStaticContact"
        )

        if temp is None:
            return 0.0

        return temp

    @required_safety_factor_for_static_contact.setter
    @enforce_parameter_types
    def required_safety_factor_for_static_contact(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RequiredSafetyFactorForStaticContact",
            float(value) if value is not None else 0.0,
        )

    @property
    def cylindrical_gear_design_constraint_settings(
        self: "Self",
    ) -> "_1046.CylindricalGearDesignConstraints":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearDesignConstraints

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearDesignConstraintSettings"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def general_transmission_properties(
        self: "Self",
    ) -> "_269.GeneralTransmissionProperties":
        """mastapy.materials.GeneralTransmissionProperties

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeneralTransmissionProperties")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def settings(self: "Self") -> "_467.CylindricalGearDesignAndRatingSettingsItem":
        """mastapy.gears.rating.cylindrical.CylindricalGearDesignAndRatingSettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Settings")

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
    def cast_to(self: "Self") -> "_Cast_GearSetDesignGroup":
        """Cast to another type.

        Returns:
            _Cast_GearSetDesignGroup
        """
        return _Cast_GearSetDesignGroup(self)
