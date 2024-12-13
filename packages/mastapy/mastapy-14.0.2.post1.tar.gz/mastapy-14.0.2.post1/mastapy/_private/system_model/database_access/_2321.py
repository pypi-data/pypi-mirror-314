"""Databases"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_DATABASES = python_net_import("SMT.MastaAPI.SystemModel.DatabaseAccess", "Databases")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _1948
    from mastapy._private.bolts import _1519, _1521, _1526
    from mastapy._private.electric_machines import _1331, _1349, _1364
    from mastapy._private.gears.gear_set_pareto_optimiser import (
        _946,
        _947,
        _950,
        _951,
        _956,
        _957,
        _959,
        _960,
        _961,
        _962,
    )
    from mastapy._private.gears.manufacturing.bevel import _825
    from mastapy._private.gears.manufacturing.cylindrical import _640, _651
    from mastapy._private.gears.manufacturing.cylindrical.cutters import (
        _730,
        _736,
        _741,
        _742,
    )
    from mastapy._private.gears.materials import (
        _600,
        _602,
        _604,
        _605,
        _608,
        _622,
        _631,
    )
    from mastapy._private.materials import _259, _262, _281
    from mastapy._private.shafts import _25
    from mastapy._private.system_model.optimization import _2285, _2293
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
        _2625,
    )

    Self = TypeVar("Self", bound="Databases")
    CastSelf = TypeVar("CastSelf", bound="Databases._Cast_Databases")


__docformat__ = "restructuredtext en"
__all__ = ("Databases",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Databases:
    """Special nested class for casting Databases to subclasses."""

    __parent__: "Databases"

    @property
    def databases(self: "CastSelf") -> "Databases":
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
class Databases(_0.APIBase):
    """Databases

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DATABASES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def bearing_material_database(self: "Self") -> "_259.BearingMaterialDatabase":
        """mastapy.materials.BearingMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BearingMaterialDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def bevel_gear_iso_material_database(
        self: "Self",
    ) -> "_600.BevelGearISOMaterialDatabase":
        """mastapy.gears.materials.BevelGearISOMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearIsoMaterialDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def bevel_gear_material_database(self: "Self") -> "_602.BevelGearMaterialDatabase":
        """mastapy.gears.materials.BevelGearMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearMaterialDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def bolt_geometry_database(self: "Self") -> "_1519.BoltGeometryDatabase":
        """mastapy.bolts.BoltGeometryDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BoltGeometryDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def bolt_material_database(self: "Self") -> "_1521.BoltMaterialDatabase":
        """mastapy.bolts.BoltMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BoltMaterialDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def clamped_section_material_database(
        self: "Self",
    ) -> "_1526.ClampedSectionMaterialDatabase":
        """mastapy.bolts.ClampedSectionMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ClampedSectionMaterialDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_material_database(self: "Self") -> "_262.ComponentMaterialDatabase":
        """mastapy.materials.ComponentMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentMaterialDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def conical_gear_optimization_strategy_database(
        self: "Self",
    ) -> "_2285.ConicalGearOptimizationStrategyDatabase":
        """mastapy.system_model.optimization.ConicalGearOptimizationStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ConicalGearOptimizationStrategyDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_formed_wheel_grinder_database(
        self: "Self",
    ) -> "_730.CylindricalFormedWheelGrinderDatabase":
        """mastapy.gears.manufacturing.cylindrical.cutters.CylindricalFormedWheelGrinderDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalFormedWheelGrinderDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_gear_agma_material_database(
        self: "Self",
    ) -> "_604.CylindricalGearAGMAMaterialDatabase":
        """mastapy.gears.materials.CylindricalGearAGMAMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearAGMAMaterialDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_gear_iso_material_database(
        self: "Self",
    ) -> "_605.CylindricalGearISOMaterialDatabase":
        """mastapy.gears.materials.CylindricalGearISOMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearISOMaterialDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_gear_plastic_material_database(
        self: "Self",
    ) -> "_608.CylindricalGearPlasticMaterialDatabase":
        """mastapy.gears.materials.CylindricalGearPlasticMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearPlasticMaterialDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_gear_plunge_shaver_database(
        self: "Self",
    ) -> "_736.CylindricalGearPlungeShaverDatabase":
        """mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearPlungeShaverDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearPlungeShaverDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_gear_shaver_database(
        self: "Self",
    ) -> "_741.CylindricalGearShaverDatabase":
        """mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearShaverDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearShaverDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_hob_database(self: "Self") -> "_640.CylindricalHobDatabase":
        """mastapy.gears.manufacturing.cylindrical.CylindricalHobDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalHobDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_shaper_database(self: "Self") -> "_651.CylindricalShaperDatabase":
        """mastapy.gears.manufacturing.cylindrical.CylindricalShaperDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalShaperDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_worm_grinder_database(
        self: "Self",
    ) -> "_742.CylindricalWormGrinderDatabase":
        """mastapy.gears.manufacturing.cylindrical.cutters.CylindricalWormGrinderDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalWormGrinderDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def klingelnberg_conical_gear_material_database(
        self: "Self",
    ) -> "_622.KlingelnbergConicalGearMaterialDatabase":
        """mastapy.gears.materials.KlingelnbergConicalGearMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergConicalGearMaterialDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def lubrication_detail_database(self: "Self") -> "_281.LubricationDetailDatabase":
        """mastapy.materials.LubricationDetailDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricationDetailDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def magnet_material_database(self: "Self") -> "_1331.MagnetMaterialDatabase":
        """mastapy.electric_machines.MagnetMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MagnetMaterialDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def manufacturing_machine_database(
        self: "Self",
    ) -> "_825.ManufacturingMachineDatabase":
        """mastapy.gears.manufacturing.bevel.ManufacturingMachineDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ManufacturingMachineDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def micro_geometry_gear_set_design_space_search_strategy_database(
        self: "Self",
    ) -> "_946.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase":
        """mastapy.gears.gear_set_pareto_optimiser.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MicroGeometryGearSetDesignSpaceSearchStrategyDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def micro_geometry_gear_set_duty_cycle_design_space_search_strategy_database(
        self: "Self",
    ) -> "_947.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase":
        """mastapy.gears.gear_set_pareto_optimiser.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase",
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def optimization_strategy_database(
        self: "Self",
    ) -> "_2293.OptimizationStrategyDatabase":
        """mastapy.system_model.optimization.OptimizationStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OptimizationStrategyDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def pareto_cylindrical_gear_set_duty_cycle_optimisation_strategy_database(
        self: "Self",
    ) -> "_950.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase":
        """mastapy.gears.gear_set_pareto_optimiser.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase",
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def pareto_cylindrical_gear_set_optimisation_strategy_database(
        self: "Self",
    ) -> "_951.ParetoCylindricalGearSetOptimisationStrategyDatabase":
        """mastapy.gears.gear_set_pareto_optimiser.ParetoCylindricalGearSetOptimisationStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ParetoCylindricalGearSetOptimisationStrategyDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def pareto_hypoid_gear_set_duty_cycle_optimisation_strategy_database(
        self: "Self",
    ) -> "_956.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase":
        """mastapy.gears.gear_set_pareto_optimiser.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def pareto_hypoid_gear_set_optimisation_strategy_database(
        self: "Self",
    ) -> "_957.ParetoHypoidGearSetOptimisationStrategyDatabase":
        """mastapy.gears.gear_set_pareto_optimiser.ParetoHypoidGearSetOptimisationStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ParetoHypoidGearSetOptimisationStrategyDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def pareto_spiral_bevel_gear_set_duty_cycle_optimisation_strategy_database(
        self: "Self",
    ) -> "_959.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase":
        """mastapy.gears.gear_set_pareto_optimiser.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase",
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def pareto_spiral_bevel_gear_set_optimisation_strategy_database(
        self: "Self",
    ) -> "_960.ParetoSpiralBevelGearSetOptimisationStrategyDatabase":
        """mastapy.gears.gear_set_pareto_optimiser.ParetoSpiralBevelGearSetOptimisationStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ParetoSpiralBevelGearSetOptimisationStrategyDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def pareto_straight_bevel_gear_set_duty_cycle_optimisation_strategy_database(
        self: "Self",
    ) -> "_961.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase":
        """mastapy.gears.gear_set_pareto_optimiser.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase",
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def pareto_straight_bevel_gear_set_optimisation_strategy_database(
        self: "Self",
    ) -> "_962.ParetoStraightBevelGearSetOptimisationStrategyDatabase":
        """mastapy.gears.gear_set_pareto_optimiser.ParetoStraightBevelGearSetOptimisationStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ParetoStraightBevelGearSetOptimisationStrategyDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def raw_material_database(self: "Self") -> "_631.RawMaterialDatabase":
        """mastapy.gears.materials.RawMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RawMaterialDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def rolling_bearing_database(self: "Self") -> "_1948.RollingBearingDatabase":
        """mastapy.bearings.RollingBearingDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollingBearingDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def shaft_material_database(self: "Self") -> "_25.ShaftMaterialDatabase":
        """mastapy.shafts.ShaftMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftMaterialDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def stator_and_rotor_material_database(
        self: "Self",
    ) -> "_1349.StatorRotorMaterialDatabase":
        """mastapy.electric_machines.StatorRotorMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StatorAndRotorMaterialDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def supercharger_rotor_set_database(
        self: "Self",
    ) -> "_2625.SuperchargerRotorSetDatabase":
        """mastapy.system_model.part_model.gears.supercharger_rotor_set.SuperchargerRotorSetDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SuperchargerRotorSetDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def winding_material_database(self: "Self") -> "_1364.WindingMaterialDatabase":
        """mastapy.electric_machines.WindingMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WindingMaterialDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_Databases":
        """Cast to another type.

        Returns:
            _Cast_Databases
        """
        return _Cast_Databases(self)
