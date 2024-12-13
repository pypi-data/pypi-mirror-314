"""MASTASettings"""

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

_MASTA_SETTINGS = python_net_import("SMT.MastaAPI.SystemModel", "MASTASettings")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _1934, _1935, _1948, _1954
    from mastapy._private.bearings.bearing_results.rolling import _2031
    from mastapy._private.bolts import _1519, _1521, _1526
    from mastapy._private.cycloidal import _1507, _1514
    from mastapy._private.electric_machines import _1331, _1349, _1364
    from mastapy._private.gears import _328, _329, _355
    from mastapy._private.gears.gear_designs import _966, _968, _971, _977
    from mastapy._private.gears.gear_designs.cylindrical import (
        _1043,
        _1047,
        _1048,
        _1053,
        _1064,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser import (
        _946,
        _947,
        _950,
        _951,
        _953,
        _954,
        _956,
        _957,
        _959,
        _960,
        _961,
        _962,
    )
    from mastapy._private.gears.ltca.cylindrical import _880
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
        _612,
        _621,
        _622,
        _631,
    )
    from mastapy._private.gears.rating.cylindrical import _465, _466, _481, _482
    from mastapy._private.materials import _259, _262, _281, _284, _285
    from mastapy._private.nodal_analysis import _48, _49, _68
    from mastapy._private.nodal_analysis.geometry_modeller_link import _168
    from mastapy._private.shafts import _25, _38, _39
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6732,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5898,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5590
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4775
    from mastapy._private.system_model.analyses_and_results.power_flows import _4234
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3978,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3185,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2917,
    )
    from mastapy._private.system_model.drawing import _2309
    from mastapy._private.system_model.optimization import _2285, _2293
    from mastapy._private.system_model.part_model import _2530
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
        _2625,
    )
    from mastapy._private.utility import _1647, _1648
    from mastapy._private.utility.cad_export import _1887
    from mastapy._private.utility.databases import _1882
    from mastapy._private.utility.scripting import _1792
    from mastapy._private.utility.units_and_measurements import _1658

    Self = TypeVar("Self", bound="MASTASettings")
    CastSelf = TypeVar("CastSelf", bound="MASTASettings._Cast_MASTASettings")


__docformat__ = "restructuredtext en"
__all__ = ("MASTASettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MASTASettings:
    """Special nested class for casting MASTASettings to subclasses."""

    __parent__: "MASTASettings"

    @property
    def masta_settings(self: "CastSelf") -> "MASTASettings":
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
class MASTASettings(_0.APIBase):
    """MASTASettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MASTA_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def iso14179_settings_database(self: "Self") -> "_2031.ISO14179SettingsDatabase":
        """mastapy.bearings.bearing_results.rolling.ISO14179SettingsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO14179SettingsDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def bearing_settings(self: "Self") -> "_1934.BearingSettings":
        """mastapy.bearings.BearingSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BearingSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def bearing_settings_database(self: "Self") -> "_1935.BearingSettingsDatabase":
        """mastapy.bearings.BearingSettingsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BearingSettingsDatabase")

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
    def skf_settings(self: "Self") -> "_1954.SKFSettings":
        """mastapy.bearings.SKFSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SKFSettings")

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
    def cycloidal_disc_material_database(
        self: "Self",
    ) -> "_1507.CycloidalDiscMaterialDatabase":
        """mastapy.cycloidal.CycloidalDiscMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CycloidalDiscMaterialDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def ring_pins_material_database(self: "Self") -> "_1514.RingPinsMaterialDatabase":
        """mastapy.cycloidal.RingPinsMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RingPinsMaterialDatabase")

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
    def stator_rotor_material_database(
        self: "Self",
    ) -> "_1349.StatorRotorMaterialDatabase":
        """mastapy.electric_machines.StatorRotorMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StatorRotorMaterialDatabase")

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
    def bevel_hypoid_gear_design_settings(
        self: "Self",
    ) -> "_328.BevelHypoidGearDesignSettings":
        """mastapy.gears.BevelHypoidGearDesignSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelHypoidGearDesignSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def bevel_hypoid_gear_rating_settings(
        self: "Self",
    ) -> "_329.BevelHypoidGearRatingSettings":
        """mastapy.gears.BevelHypoidGearRatingSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelHypoidGearRatingSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def bevel_hypoid_gear_design_settings_database(
        self: "Self",
    ) -> "_966.BevelHypoidGearDesignSettingsDatabase":
        """mastapy.gears.gear_designs.BevelHypoidGearDesignSettingsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BevelHypoidGearDesignSettingsDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def bevel_hypoid_gear_rating_settings_database(
        self: "Self",
    ) -> "_968.BevelHypoidGearRatingSettingsDatabase":
        """mastapy.gears.gear_designs.BevelHypoidGearRatingSettingsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BevelHypoidGearRatingSettingsDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_gear_defaults(self: "Self") -> "_1043.CylindricalGearDefaults":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearDefaults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearDefaults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_gear_design_constraints_database(
        self: "Self",
    ) -> "_1047.CylindricalGearDesignConstraintsDatabase":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearDesignConstraintsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearDesignConstraintsDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_gear_design_constraint_settings(
        self: "Self",
    ) -> "_1048.CylindricalGearDesignConstraintSettings":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearDesignConstraintSettings

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
    def cylindrical_gear_micro_geometry_settings_database(
        self: "Self",
    ) -> "_1053.CylindricalGearMicroGeometrySettingsDatabase":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearMicroGeometrySettingsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearMicroGeometrySettingsDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_gear_set_micro_geometry_settings(
        self: "Self",
    ) -> "_1064.CylindricalGearSetMicroGeometrySettings":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearSetMicroGeometrySettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearSetMicroGeometrySettings"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def design_constraint_collection_database(
        self: "Self",
    ) -> "_971.DesignConstraintCollectionDatabase":
        """mastapy.gears.gear_designs.DesignConstraintCollectionDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DesignConstraintCollectionDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def selected_design_constraints_collection(
        self: "Self",
    ) -> "_977.SelectedDesignConstraintsCollection":
        """mastapy.gears.gear_designs.SelectedDesignConstraintsCollection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SelectedDesignConstraintsCollection"
        )

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
    def pareto_face_gear_set_duty_cycle_optimisation_strategy_database(
        self: "Self",
    ) -> "_953.ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase":
        """mastapy.gears.gear_set_pareto_optimiser.ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def pareto_face_gear_set_optimisation_strategy_database(
        self: "Self",
    ) -> "_954.ParetoFaceGearSetOptimisationStrategyDatabase":
        """mastapy.gears.gear_set_pareto_optimiser.ParetoFaceGearSetOptimisationStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ParetoFaceGearSetOptimisationStrategyDatabase"
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
    def cylindrical_gear_fe_settings(self: "Self") -> "_880.CylindricalGearFESettings":
        """mastapy.gears.ltca.cylindrical.CylindricalGearFESettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearFESettings")

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
    def bevel_gear_iso_material_database(
        self: "Self",
    ) -> "_600.BevelGearISOMaterialDatabase":
        """mastapy.gears.materials.BevelGearISOMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearISOMaterialDatabase")

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
    def gear_material_expert_system_factor_settings(
        self: "Self",
    ) -> "_612.GearMaterialExpertSystemFactorSettings":
        """mastapy.gears.materials.GearMaterialExpertSystemFactorSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearMaterialExpertSystemFactorSettings"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def isotr1417912001_coefficient_of_friction_constants_database(
        self: "Self",
    ) -> "_621.ISOTR1417912001CoefficientOfFrictionConstantsDatabase":
        """mastapy.gears.materials.ISOTR1417912001CoefficientOfFrictionConstantsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISOTR1417912001CoefficientOfFrictionConstantsDatabase"
        )

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
    def pocketing_power_loss_coefficients_database(
        self: "Self",
    ) -> "_355.PocketingPowerLossCoefficientsDatabase":
        """mastapy.gears.PocketingPowerLossCoefficientsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PocketingPowerLossCoefficientsDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_gear_design_and_rating_settings(
        self: "Self",
    ) -> "_465.CylindricalGearDesignAndRatingSettings":
        """mastapy.gears.rating.cylindrical.CylindricalGearDesignAndRatingSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearDesignAndRatingSettings"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_gear_design_and_rating_settings_database(
        self: "Self",
    ) -> "_466.CylindricalGearDesignAndRatingSettingsDatabase":
        """mastapy.gears.rating.cylindrical.CylindricalGearDesignAndRatingSettingsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearDesignAndRatingSettingsDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_plastic_gear_rating_settings(
        self: "Self",
    ) -> "_481.CylindricalPlasticGearRatingSettings":
        """mastapy.gears.rating.cylindrical.CylindricalPlasticGearRatingSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalPlasticGearRatingSettings"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_plastic_gear_rating_settings_database(
        self: "Self",
    ) -> "_482.CylindricalPlasticGearRatingSettingsDatabase":
        """mastapy.gears.rating.cylindrical.CylindricalPlasticGearRatingSettingsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalPlasticGearRatingSettingsDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def critical_speed_analysis_draw_style(
        self: "Self",
    ) -> "_6732.CriticalSpeedAnalysisDrawStyle":
        """mastapy.system_model.analyses_and_results.critical_speed_analyses.CriticalSpeedAnalysisDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CriticalSpeedAnalysisDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def harmonic_analysis_draw_style(self: "Self") -> "_5898.HarmonicAnalysisDrawStyle":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.HarmonicAnalysisDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HarmonicAnalysisDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def mbd_analysis_draw_style(self: "Self") -> "_5590.MBDAnalysisDrawStyle":
        """mastapy.system_model.analyses_and_results.mbd_analyses.MBDAnalysisDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MBDAnalysisDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def modal_analysis_draw_style(self: "Self") -> "_4775.ModalAnalysisDrawStyle":
        """mastapy.system_model.analyses_and_results.modal_analyses.ModalAnalysisDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModalAnalysisDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def power_flow_draw_style(self: "Self") -> "_4234.PowerFlowDrawStyle":
        """mastapy.system_model.analyses_and_results.power_flows.PowerFlowDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlowDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def stability_analysis_draw_style(
        self: "Self",
    ) -> "_3978.StabilityAnalysisDrawStyle":
        """mastapy.system_model.analyses_and_results.stability_analyses.StabilityAnalysisDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StabilityAnalysisDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def steady_state_synchronous_response_draw_style(
        self: "Self",
    ) -> "_3185.SteadyStateSynchronousResponseDrawStyle":
        """mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.SteadyStateSynchronousResponseDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SteadyStateSynchronousResponseDrawStyle"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_draw_style(self: "Self") -> "_2917.SystemDeflectionDrawStyle":
        """mastapy.system_model.analyses_and_results.system_deflections.SystemDeflectionDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def model_view_options_draw_style(
        self: "Self",
    ) -> "_2309.ModelViewOptionsDrawStyle":
        """mastapy.system_model.drawing.ModelViewOptionsDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModelViewOptionsDrawStyle")

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
    def planet_carrier_settings(self: "Self") -> "_2530.PlanetCarrierSettings":
        """mastapy.system_model.part_model.PlanetCarrierSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlanetCarrierSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

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
    def materials_settings(self: "Self") -> "_284.MaterialsSettings":
        """mastapy.materials.MaterialsSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaterialsSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def materials_settings_database(self: "Self") -> "_285.MaterialsSettingsDatabase":
        """mastapy.materials.MaterialsSettingsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaterialsSettingsDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def analysis_settings(self: "Self") -> "_48.AnalysisSettings":
        """mastapy.nodal_analysis.AnalysisSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AnalysisSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def analysis_settings_database(self: "Self") -> "_49.AnalysisSettingsDatabase":
        """mastapy.nodal_analysis.AnalysisSettingsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AnalysisSettingsDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def fe_user_settings(self: "Self") -> "_68.FEUserSettings":
        """mastapy.nodal_analysis.FEUserSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FEUserSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def geometry_modeller_settings(self: "Self") -> "_168.GeometryModellerSettings":
        """mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeometryModellerSettings")

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
    def shaft_settings(self: "Self") -> "_38.ShaftSettings":
        """mastapy.shafts.ShaftSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def shaft_settings_database(self: "Self") -> "_39.ShaftSettingsDatabase":
        """mastapy.shafts.ShaftSettingsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftSettingsDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cad_export_settings(self: "Self") -> "_1887.CADExportSettings":
        """mastapy.utility.cad_export.CADExportSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CADExportSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def database_settings(self: "Self") -> "_1882.DatabaseSettings":
        """mastapy.utility.databases.DatabaseSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DatabaseSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def program_settings(self: "Self") -> "_1647.ProgramSettings":
        """mastapy.utility.ProgramSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProgramSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def pushbullet_settings(self: "Self") -> "_1648.PushbulletSettings":
        """mastapy.utility.PushbulletSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PushbulletSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def scripting_setup(self: "Self") -> "_1792.ScriptingSetup":
        """mastapy.utility.scripting.ScriptingSetup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ScriptingSetup")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def measurement_settings(self: "Self") -> "_1658.MeasurementSettings":
        """mastapy.utility.units_and_measurements.MeasurementSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeasurementSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_MASTASettings":
        """Cast to another type.

        Returns:
            _Cast_MASTASettings
        """
        return _Cast_MASTASettings(self)
