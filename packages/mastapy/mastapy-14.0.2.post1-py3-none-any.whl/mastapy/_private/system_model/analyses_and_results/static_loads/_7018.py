"""CylindricalGearSetLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    overridable_enum_runtime,
    utility,
)
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import enum_with_selected_value, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears import _331
from mastapy._private.gears.rating import _372
from mastapy._private.system_model.analyses_and_results.static_loads import _7048

_CYLINDRICAL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CylindricalGearSetLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.gear_designs.cylindrical import _1091
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1141
    from mastapy._private.system_model.analyses_and_results import _2740, _2742, _2746
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6959,
        _7014,
        _7016,
        _7017,
        _7083,
        _7088,
        _7096,
        _7107,
    )
    from mastapy._private.system_model.part_model.gears import _2587

    Self = TypeVar("Self", bound="CylindricalGearSetLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalGearSetLoadCase._Cast_CylindricalGearSetLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearSetLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearSetLoadCase:
    """Special nested class for casting CylindricalGearSetLoadCase to subclasses."""

    __parent__: "CylindricalGearSetLoadCase"

    @property
    def gear_set_load_case(self: "CastSelf") -> "_7048.GearSetLoadCase":
        return self.__parent__._cast(_7048.GearSetLoadCase)

    @property
    def specialised_assembly_load_case(
        self: "CastSelf",
    ) -> "_7107.SpecialisedAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7107,
        )

        return self.__parent__._cast(_7107.SpecialisedAssemblyLoadCase)

    @property
    def abstract_assembly_load_case(
        self: "CastSelf",
    ) -> "_6959.AbstractAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6959,
        )

        return self.__parent__._cast(_6959.AbstractAssemblyLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7083.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7083,
        )

        return self.__parent__._cast(_7083.PartLoadCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2746.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2746

        return self.__parent__._cast(_2746.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2742.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2742

        return self.__parent__._cast(_2742.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2740.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2740

        return self.__parent__._cast(_2740.DesignEntityAnalysis)

    @property
    def planetary_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7088.PlanetaryGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7088,
        )

        return self.__parent__._cast(_7088.PlanetaryGearSetLoadCase)

    @property
    def cylindrical_gear_set_load_case(
        self: "CastSelf",
    ) -> "CylindricalGearSetLoadCase":
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
class CylindricalGearSetLoadCase(_7048.GearSetLoadCase):
    """CylindricalGearSetLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SET_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def boost_pressure(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BoostPressure")

        if temp is None:
            return 0.0

        return temp

    @boost_pressure.setter
    @enforce_parameter_types
    def boost_pressure(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "BoostPressure", float(value) if value is not None else 0.0
        )

    @property
    def coefficient_of_friction_calculation_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_CoefficientOfFrictionCalculationMethod":
        """EnumWithSelectedValue[mastapy.gears.CoefficientOfFrictionCalculationMethod]"""
        temp = pythonnet_property_get(
            self.wrapped, "CoefficientOfFrictionCalculationMethod"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_CoefficientOfFrictionCalculationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @coefficient_of_friction_calculation_method.setter
    @enforce_parameter_types
    def coefficient_of_friction_calculation_method(
        self: "Self", value: "_331.CoefficientOfFrictionCalculationMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_CoefficientOfFrictionCalculationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped, "CoefficientOfFrictionCalculationMethod", value
        )

    @property
    def dynamic_load_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "DynamicLoadFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @dynamic_load_factor.setter
    @enforce_parameter_types
    def dynamic_load_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DynamicLoadFactor", value)

    @property
    def efficiency_rating_method(
        self: "Self",
    ) -> "overridable.Overridable_GearMeshEfficiencyRatingMethod":
        """Overridable[mastapy.gears.rating.GearMeshEfficiencyRatingMethod]"""
        temp = pythonnet_property_get(self.wrapped, "EfficiencyRatingMethod")

        if temp is None:
            return None

        value = overridable.Overridable_GearMeshEfficiencyRatingMethod.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @efficiency_rating_method.setter
    @enforce_parameter_types
    def efficiency_rating_method(
        self: "Self",
        value: "Union[_372.GearMeshEfficiencyRatingMethod, Tuple[_372.GearMeshEfficiencyRatingMethod, bool]]",
    ) -> None:
        wrapper_type = (
            overridable.Overridable_GearMeshEfficiencyRatingMethod.wrapper_type()
        )
        enclosed_type = (
            overridable.Overridable_GearMeshEfficiencyRatingMethod.implicit_type()
        )
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "EfficiencyRatingMethod", value)

    @property
    def override_efficiency_rating_method_script(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "OverrideEfficiencyRatingMethodScript"
        )

        if temp is None:
            return False

        return temp

    @override_efficiency_rating_method_script.setter
    @enforce_parameter_types
    def override_efficiency_rating_method_script(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverrideEfficiencyRatingMethodScript",
            bool(value) if value is not None else False,
        )

    @property
    def override_micro_geometry(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "OverrideMicroGeometry")

        if temp is None:
            return False

        return temp

    @override_micro_geometry.setter
    @enforce_parameter_types
    def override_micro_geometry(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverrideMicroGeometry",
            bool(value) if value is not None else False,
        )

    @property
    def reset_micro_geometry(self: "Self") -> "_7096.ResetMicroGeometryOptions":
        """mastapy.system_model.analyses_and_results.static_loads.ResetMicroGeometryOptions"""
        temp = pythonnet_property_get(self.wrapped, "ResetMicroGeometry")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.ResetMicroGeometryOptions",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.static_loads._7096",
            "ResetMicroGeometryOptions",
        )(value)

    @reset_micro_geometry.setter
    @enforce_parameter_types
    def reset_micro_geometry(
        self: "Self", value: "_7096.ResetMicroGeometryOptions"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.ResetMicroGeometryOptions",
        )
        pythonnet_property_set(self.wrapped, "ResetMicroGeometry", value)

    @property
    def use_design_coefficient_of_friction_calculation_method(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseDesignCoefficientOfFrictionCalculationMethod"
        )

        if temp is None:
            return False

        return temp

    @use_design_coefficient_of_friction_calculation_method.setter
    @enforce_parameter_types
    def use_design_coefficient_of_friction_calculation_method(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseDesignCoefficientOfFrictionCalculationMethod",
            bool(value) if value is not None else False,
        )

    @property
    def use_design_default_ltca_settings(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseDesignDefaultLTCASettings")

        if temp is None:
            return False

        return temp

    @use_design_default_ltca_settings.setter
    @enforce_parameter_types
    def use_design_default_ltca_settings(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseDesignDefaultLTCASettings",
            bool(value) if value is not None else False,
        )

    @property
    def assembly_design(self: "Self") -> "_2587.CylindricalGearSet":
        """mastapy.system_model.part_model.gears.CylindricalGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def ltca(self: "Self") -> "_1091.LTCALoadCaseModifiableSettings":
        """mastapy.gears.gear_designs.cylindrical.LTCALoadCaseModifiableSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LTCA")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def overridden_micro_geometry(
        self: "Self",
    ) -> "_1141.CylindricalGearSetMicroGeometry":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverriddenMicroGeometry")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gears_load_case(self: "Self") -> "List[_7014.CylindricalGearLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearsLoadCase")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cylindrical_gears_load_case(
        self: "Self",
    ) -> "List[_7014.CylindricalGearLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearsLoadCase")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def meshes_load_case(self: "Self") -> "List[_7016.CylindricalGearMeshLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshesLoadCase")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cylindrical_meshes_load_case(
        self: "Self",
    ) -> "List[_7016.CylindricalGearMeshLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalMeshesLoadCase")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    def get_harmonic_load_data_for_import(
        self: "Self",
    ) -> "_7017.CylindricalGearSetHarmonicLoadData":
        """mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetHarmonicLoadData"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetHarmonicLoadDataForImport"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearSetLoadCase":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearSetLoadCase
        """
        return _Cast_CylindricalGearSetLoadCase(self)
