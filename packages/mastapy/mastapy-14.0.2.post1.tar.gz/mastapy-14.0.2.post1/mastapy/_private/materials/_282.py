"""Material"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.databases import _1884

_MATERIAL = python_net_import("SMT.MastaAPI.Materials", "Material")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bolts import _1516, _1520
    from mastapy._private.cycloidal import _1506, _1513
    from mastapy._private.detailed_rigid_connectors.splines import _1466
    from mastapy._private.electric_machines import _1330, _1348, _1363
    from mastapy._private.gears.materials import (
        _596,
        _599,
        _601,
        _606,
        _610,
        _618,
        _623,
        _627,
    )
    from mastapy._private.materials import _258, _271, _287
    from mastapy._private.shafts import _24

    Self = TypeVar("Self", bound="Material")
    CastSelf = TypeVar("CastSelf", bound="Material._Cast_Material")


__docformat__ = "restructuredtext en"
__all__ = ("Material",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Material:
    """Special nested class for casting Material to subclasses."""

    __parent__: "Material"

    @property
    def named_database_item(self: "CastSelf") -> "_1884.NamedDatabaseItem":
        return self.__parent__._cast(_1884.NamedDatabaseItem)

    @property
    def shaft_material(self: "CastSelf") -> "_24.ShaftMaterial":
        from mastapy._private.shafts import _24

        return self.__parent__._cast(_24.ShaftMaterial)

    @property
    def bearing_material(self: "CastSelf") -> "_258.BearingMaterial":
        from mastapy._private.materials import _258

        return self.__parent__._cast(_258.BearingMaterial)

    @property
    def agma_cylindrical_gear_material(
        self: "CastSelf",
    ) -> "_596.AGMACylindricalGearMaterial":
        from mastapy._private.gears.materials import _596

        return self.__parent__._cast(_596.AGMACylindricalGearMaterial)

    @property
    def bevel_gear_iso_material(self: "CastSelf") -> "_599.BevelGearISOMaterial":
        from mastapy._private.gears.materials import _599

        return self.__parent__._cast(_599.BevelGearISOMaterial)

    @property
    def bevel_gear_material(self: "CastSelf") -> "_601.BevelGearMaterial":
        from mastapy._private.gears.materials import _601

        return self.__parent__._cast(_601.BevelGearMaterial)

    @property
    def cylindrical_gear_material(self: "CastSelf") -> "_606.CylindricalGearMaterial":
        from mastapy._private.gears.materials import _606

        return self.__parent__._cast(_606.CylindricalGearMaterial)

    @property
    def gear_material(self: "CastSelf") -> "_610.GearMaterial":
        from mastapy._private.gears.materials import _610

        return self.__parent__._cast(_610.GearMaterial)

    @property
    def iso_cylindrical_gear_material(
        self: "CastSelf",
    ) -> "_618.ISOCylindricalGearMaterial":
        from mastapy._private.gears.materials import _618

        return self.__parent__._cast(_618.ISOCylindricalGearMaterial)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_material(
        self: "CastSelf",
    ) -> "_623.KlingelnbergCycloPalloidConicalGearMaterial":
        from mastapy._private.gears.materials import _623

        return self.__parent__._cast(_623.KlingelnbergCycloPalloidConicalGearMaterial)

    @property
    def plastic_cylindrical_gear_material(
        self: "CastSelf",
    ) -> "_627.PlasticCylindricalGearMaterial":
        from mastapy._private.gears.materials import _627

        return self.__parent__._cast(_627.PlasticCylindricalGearMaterial)

    @property
    def magnet_material(self: "CastSelf") -> "_1330.MagnetMaterial":
        from mastapy._private.electric_machines import _1330

        return self.__parent__._cast(_1330.MagnetMaterial)

    @property
    def stator_rotor_material(self: "CastSelf") -> "_1348.StatorRotorMaterial":
        from mastapy._private.electric_machines import _1348

        return self.__parent__._cast(_1348.StatorRotorMaterial)

    @property
    def winding_material(self: "CastSelf") -> "_1363.WindingMaterial":
        from mastapy._private.electric_machines import _1363

        return self.__parent__._cast(_1363.WindingMaterial)

    @property
    def spline_material(self: "CastSelf") -> "_1466.SplineMaterial":
        from mastapy._private.detailed_rigid_connectors.splines import _1466

        return self.__parent__._cast(_1466.SplineMaterial)

    @property
    def cycloidal_disc_material(self: "CastSelf") -> "_1506.CycloidalDiscMaterial":
        from mastapy._private.cycloidal import _1506

        return self.__parent__._cast(_1506.CycloidalDiscMaterial)

    @property
    def ring_pins_material(self: "CastSelf") -> "_1513.RingPinsMaterial":
        from mastapy._private.cycloidal import _1513

        return self.__parent__._cast(_1513.RingPinsMaterial)

    @property
    def bolted_joint_material(self: "CastSelf") -> "_1516.BoltedJointMaterial":
        from mastapy._private.bolts import _1516

        return self.__parent__._cast(_1516.BoltedJointMaterial)

    @property
    def bolt_material(self: "CastSelf") -> "_1520.BoltMaterial":
        from mastapy._private.bolts import _1520

        return self.__parent__._cast(_1520.BoltMaterial)

    @property
    def material(self: "CastSelf") -> "Material":
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
class Material(_1884.NamedDatabaseItem):
    """Material

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MATERIAL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def coefficient_of_thermal_expansion(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CoefficientOfThermalExpansion")

        if temp is None:
            return 0.0

        return temp

    @coefficient_of_thermal_expansion.setter
    @enforce_parameter_types
    def coefficient_of_thermal_expansion(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CoefficientOfThermalExpansion",
            float(value) if value is not None else 0.0,
        )

    @property
    def cost_per_unit_mass(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CostPerUnitMass")

        if temp is None:
            return 0.0

        return temp

    @cost_per_unit_mass.setter
    @enforce_parameter_types
    def cost_per_unit_mass(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CostPerUnitMass", float(value) if value is not None else 0.0
        )

    @property
    def density(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Density")

        if temp is None:
            return 0.0

        return temp

    @density.setter
    @enforce_parameter_types
    def density(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Density", float(value) if value is not None else 0.0
        )

    @property
    def hardness_type(self: "Self") -> "_271.HardnessType":
        """mastapy.materials.HardnessType"""
        temp = pythonnet_property_get(self.wrapped, "HardnessType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Materials.HardnessType")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._271", "HardnessType"
        )(value)

    @hardness_type.setter
    @enforce_parameter_types
    def hardness_type(self: "Self", value: "_271.HardnessType") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Materials.HardnessType")
        pythonnet_property_set(self.wrapped, "HardnessType", value)

    @property
    def heat_conductivity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HeatConductivity")

        if temp is None:
            return 0.0

        return temp

    @heat_conductivity.setter
    @enforce_parameter_types
    def heat_conductivity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "HeatConductivity", float(value) if value is not None else 0.0
        )

    @property
    def material_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaterialName")

        if temp is None:
            return ""

        return temp

    @property
    def maximum_allowable_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumAllowableTemperature")

        if temp is None:
            return 0.0

        return temp

    @maximum_allowable_temperature.setter
    @enforce_parameter_types
    def maximum_allowable_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumAllowableTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    def modulus_of_elasticity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ModulusOfElasticity")

        if temp is None:
            return 0.0

        return temp

    @modulus_of_elasticity.setter
    @enforce_parameter_types
    def modulus_of_elasticity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ModulusOfElasticity",
            float(value) if value is not None else 0.0,
        )

    @property
    def plane_strain_modulus(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlaneStrainModulus")

        if temp is None:
            return 0.0

        return temp

    @property
    def poissons_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PoissonsRatio")

        if temp is None:
            return 0.0

        return temp

    @poissons_ratio.setter
    @enforce_parameter_types
    def poissons_ratio(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PoissonsRatio", float(value) if value is not None else 0.0
        )

    @property
    def shear_fatigue_strength(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShearFatigueStrength")

        if temp is None:
            return 0.0

        return temp

    @property
    def shear_modulus(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShearModulus")

        if temp is None:
            return 0.0

        return temp

    @property
    def shear_yield_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShearYieldStress")

        if temp is None:
            return 0.0

        return temp

    @property
    def specific_heat(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpecificHeat")

        if temp is None:
            return 0.0

        return temp

    @specific_heat.setter
    @enforce_parameter_types
    def specific_heat(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SpecificHeat", float(value) if value is not None else 0.0
        )

    @property
    def standard(self: "Self") -> "_287.MaterialStandards":
        """mastapy.materials.MaterialStandards

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Standard")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.MaterialStandards"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._287", "MaterialStandards"
        )(value)

    @property
    def surface_hardness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SurfaceHardness")

        if temp is None:
            return 0.0

        return temp

    @surface_hardness.setter
    @enforce_parameter_types
    def surface_hardness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SurfaceHardness", float(value) if value is not None else 0.0
        )

    @property
    def surface_hardness_range_max_in_hb(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceHardnessRangeMaxInHB")

        if temp is None:
            return 0.0

        return temp

    @property
    def surface_hardness_range_max_in_hrc(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceHardnessRangeMaxInHRC")

        if temp is None:
            return 0.0

        return temp

    @property
    def surface_hardness_range_max_in_hv(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceHardnessRangeMaxInHV")

        if temp is None:
            return 0.0

        return temp

    @property
    def surface_hardness_range_min_in_hb(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceHardnessRangeMinInHB")

        if temp is None:
            return 0.0

        return temp

    @property
    def surface_hardness_range_min_in_hrc(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceHardnessRangeMinInHRC")

        if temp is None:
            return 0.0

        return temp

    @property
    def surface_hardness_range_min_in_hv(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceHardnessRangeMinInHV")

        if temp is None:
            return 0.0

        return temp

    @property
    def tensile_yield_strength(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TensileYieldStrength")

        if temp is None:
            return 0.0

        return temp

    @tensile_yield_strength.setter
    @enforce_parameter_types
    def tensile_yield_strength(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TensileYieldStrength",
            float(value) if value is not None else 0.0,
        )

    @property
    def ultimate_tensile_strength(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "UltimateTensileStrength")

        if temp is None:
            return 0.0

        return temp

    @ultimate_tensile_strength.setter
    @enforce_parameter_types
    def ultimate_tensile_strength(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UltimateTensileStrength",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_Material":
        """Cast to another type.

        Returns:
            _Cast_Material
        """
        return _Cast_Material(self)
