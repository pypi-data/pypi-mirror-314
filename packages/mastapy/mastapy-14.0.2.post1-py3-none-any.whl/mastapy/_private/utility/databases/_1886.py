"""SQLDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.databases import _1879

_SQL_DATABASE = python_net_import("SMT.MastaAPI.Utility.Databases", "SQLDatabase")

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.bearings import _1935, _1948
    from mastapy._private.bearings.bearing_results.rolling import _2031
    from mastapy._private.bolts import _1517, _1519, _1521, _1526
    from mastapy._private.cycloidal import _1507, _1514
    from mastapy._private.electric_machines import _1331, _1349, _1364
    from mastapy._private.gears import _355
    from mastapy._private.gears.gear_designs import _966, _968, _971
    from mastapy._private.gears.gear_designs.cylindrical import _1047, _1053
    from mastapy._private.gears.gear_set_pareto_optimiser import (
        _944,
        _946,
        _947,
        _949,
        _950,
        _951,
        _952,
        _953,
        _954,
        _955,
        _956,
        _957,
        _959,
        _960,
        _961,
        _962,
    )
    from mastapy._private.gears.manufacturing.bevel import _825
    from mastapy._private.gears.manufacturing.cylindrical import _635, _640, _651
    from mastapy._private.gears.manufacturing.cylindrical.cutters import (
        _730,
        _736,
        _741,
        _742,
    )
    from mastapy._private.gears.materials import (
        _598,
        _600,
        _602,
        _604,
        _605,
        _607,
        _608,
        _611,
        _621,
        _622,
        _631,
    )
    from mastapy._private.gears.rating.cylindrical import _466, _482
    from mastapy._private.materials import _259, _262, _281, _283, _285
    from mastapy._private.math_utility.optimisation import _1590, _1602
    from mastapy._private.nodal_analysis import _49
    from mastapy._private.shafts import _25, _39
    from mastapy._private.system_model.optimization import _2285, _2293
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
        _2625,
    )
    from mastapy._private.utility.databases import _1881, _1883

    Self = TypeVar("Self", bound="SQLDatabase")
    CastSelf = TypeVar("CastSelf", bound="SQLDatabase._Cast_SQLDatabase")

TKey = TypeVar("TKey", bound="_1881.DatabaseKey")
TValue = TypeVar("TValue", bound="_0.APIBase")

__docformat__ = "restructuredtext en"
__all__ = ("SQLDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SQLDatabase:
    """Special nested class for casting SQLDatabase to subclasses."""

    __parent__: "SQLDatabase"

    @property
    def database(self: "CastSelf") -> "_1879.Database":
        return self.__parent__._cast(_1879.Database)

    @property
    def shaft_material_database(self: "CastSelf") -> "_25.ShaftMaterialDatabase":
        from mastapy._private.shafts import _25

        return self.__parent__._cast(_25.ShaftMaterialDatabase)

    @property
    def shaft_settings_database(self: "CastSelf") -> "_39.ShaftSettingsDatabase":
        from mastapy._private.shafts import _39

        return self.__parent__._cast(_39.ShaftSettingsDatabase)

    @property
    def analysis_settings_database(self: "CastSelf") -> "_49.AnalysisSettingsDatabase":
        from mastapy._private.nodal_analysis import _49

        return self.__parent__._cast(_49.AnalysisSettingsDatabase)

    @property
    def bearing_material_database(self: "CastSelf") -> "_259.BearingMaterialDatabase":
        from mastapy._private.materials import _259

        return self.__parent__._cast(_259.BearingMaterialDatabase)

    @property
    def component_material_database(
        self: "CastSelf",
    ) -> "_262.ComponentMaterialDatabase":
        from mastapy._private.materials import _262

        return self.__parent__._cast(_262.ComponentMaterialDatabase)

    @property
    def lubrication_detail_database(
        self: "CastSelf",
    ) -> "_281.LubricationDetailDatabase":
        from mastapy._private.materials import _281

        return self.__parent__._cast(_281.LubricationDetailDatabase)

    @property
    def material_database(self: "CastSelf") -> "_283.MaterialDatabase":
        from mastapy._private.materials import _283

        return self.__parent__._cast(_283.MaterialDatabase)

    @property
    def materials_settings_database(
        self: "CastSelf",
    ) -> "_285.MaterialsSettingsDatabase":
        from mastapy._private.materials import _285

        return self.__parent__._cast(_285.MaterialsSettingsDatabase)

    @property
    def pocketing_power_loss_coefficients_database(
        self: "CastSelf",
    ) -> "_355.PocketingPowerLossCoefficientsDatabase":
        from mastapy._private.gears import _355

        return self.__parent__._cast(_355.PocketingPowerLossCoefficientsDatabase)

    @property
    def cylindrical_gear_design_and_rating_settings_database(
        self: "CastSelf",
    ) -> "_466.CylindricalGearDesignAndRatingSettingsDatabase":
        from mastapy._private.gears.rating.cylindrical import _466

        return self.__parent__._cast(
            _466.CylindricalGearDesignAndRatingSettingsDatabase
        )

    @property
    def cylindrical_plastic_gear_rating_settings_database(
        self: "CastSelf",
    ) -> "_482.CylindricalPlasticGearRatingSettingsDatabase":
        from mastapy._private.gears.rating.cylindrical import _482

        return self.__parent__._cast(_482.CylindricalPlasticGearRatingSettingsDatabase)

    @property
    def bevel_gear_abstract_material_database(
        self: "CastSelf",
    ) -> "_598.BevelGearAbstractMaterialDatabase":
        from mastapy._private.gears.materials import _598

        return self.__parent__._cast(_598.BevelGearAbstractMaterialDatabase)

    @property
    def bevel_gear_iso_material_database(
        self: "CastSelf",
    ) -> "_600.BevelGearISOMaterialDatabase":
        from mastapy._private.gears.materials import _600

        return self.__parent__._cast(_600.BevelGearISOMaterialDatabase)

    @property
    def bevel_gear_material_database(
        self: "CastSelf",
    ) -> "_602.BevelGearMaterialDatabase":
        from mastapy._private.gears.materials import _602

        return self.__parent__._cast(_602.BevelGearMaterialDatabase)

    @property
    def cylindrical_gear_agma_material_database(
        self: "CastSelf",
    ) -> "_604.CylindricalGearAGMAMaterialDatabase":
        from mastapy._private.gears.materials import _604

        return self.__parent__._cast(_604.CylindricalGearAGMAMaterialDatabase)

    @property
    def cylindrical_gear_iso_material_database(
        self: "CastSelf",
    ) -> "_605.CylindricalGearISOMaterialDatabase":
        from mastapy._private.gears.materials import _605

        return self.__parent__._cast(_605.CylindricalGearISOMaterialDatabase)

    @property
    def cylindrical_gear_material_database(
        self: "CastSelf",
    ) -> "_607.CylindricalGearMaterialDatabase":
        from mastapy._private.gears.materials import _607

        return self.__parent__._cast(_607.CylindricalGearMaterialDatabase)

    @property
    def cylindrical_gear_plastic_material_database(
        self: "CastSelf",
    ) -> "_608.CylindricalGearPlasticMaterialDatabase":
        from mastapy._private.gears.materials import _608

        return self.__parent__._cast(_608.CylindricalGearPlasticMaterialDatabase)

    @property
    def gear_material_database(self: "CastSelf") -> "_611.GearMaterialDatabase":
        from mastapy._private.gears.materials import _611

        return self.__parent__._cast(_611.GearMaterialDatabase)

    @property
    def isotr1417912001_coefficient_of_friction_constants_database(
        self: "CastSelf",
    ) -> "_621.ISOTR1417912001CoefficientOfFrictionConstantsDatabase":
        from mastapy._private.gears.materials import _621

        return self.__parent__._cast(
            _621.ISOTR1417912001CoefficientOfFrictionConstantsDatabase
        )

    @property
    def klingelnberg_conical_gear_material_database(
        self: "CastSelf",
    ) -> "_622.KlingelnbergConicalGearMaterialDatabase":
        from mastapy._private.gears.materials import _622

        return self.__parent__._cast(_622.KlingelnbergConicalGearMaterialDatabase)

    @property
    def raw_material_database(self: "CastSelf") -> "_631.RawMaterialDatabase":
        from mastapy._private.gears.materials import _631

        return self.__parent__._cast(_631.RawMaterialDatabase)

    @property
    def cylindrical_cutter_database(
        self: "CastSelf",
    ) -> "_635.CylindricalCutterDatabase":
        from mastapy._private.gears.manufacturing.cylindrical import _635

        return self.__parent__._cast(_635.CylindricalCutterDatabase)

    @property
    def cylindrical_hob_database(self: "CastSelf") -> "_640.CylindricalHobDatabase":
        from mastapy._private.gears.manufacturing.cylindrical import _640

        return self.__parent__._cast(_640.CylindricalHobDatabase)

    @property
    def cylindrical_shaper_database(
        self: "CastSelf",
    ) -> "_651.CylindricalShaperDatabase":
        from mastapy._private.gears.manufacturing.cylindrical import _651

        return self.__parent__._cast(_651.CylindricalShaperDatabase)

    @property
    def cylindrical_formed_wheel_grinder_database(
        self: "CastSelf",
    ) -> "_730.CylindricalFormedWheelGrinderDatabase":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _730

        return self.__parent__._cast(_730.CylindricalFormedWheelGrinderDatabase)

    @property
    def cylindrical_gear_plunge_shaver_database(
        self: "CastSelf",
    ) -> "_736.CylindricalGearPlungeShaverDatabase":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _736

        return self.__parent__._cast(_736.CylindricalGearPlungeShaverDatabase)

    @property
    def cylindrical_gear_shaver_database(
        self: "CastSelf",
    ) -> "_741.CylindricalGearShaverDatabase":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _741

        return self.__parent__._cast(_741.CylindricalGearShaverDatabase)

    @property
    def cylindrical_worm_grinder_database(
        self: "CastSelf",
    ) -> "_742.CylindricalWormGrinderDatabase":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _742

        return self.__parent__._cast(_742.CylindricalWormGrinderDatabase)

    @property
    def manufacturing_machine_database(
        self: "CastSelf",
    ) -> "_825.ManufacturingMachineDatabase":
        from mastapy._private.gears.manufacturing.bevel import _825

        return self.__parent__._cast(_825.ManufacturingMachineDatabase)

    @property
    def micro_geometry_design_space_search_strategy_database(
        self: "CastSelf",
    ) -> "_944.MicroGeometryDesignSpaceSearchStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _944

        return self.__parent__._cast(
            _944.MicroGeometryDesignSpaceSearchStrategyDatabase
        )

    @property
    def micro_geometry_gear_set_design_space_search_strategy_database(
        self: "CastSelf",
    ) -> "_946.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _946

        return self.__parent__._cast(
            _946.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase
        )

    @property
    def micro_geometry_gear_set_duty_cycle_design_space_search_strategy_database(
        self: "CastSelf",
    ) -> "_947.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _947

        return self.__parent__._cast(
            _947.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase
        )

    @property
    def pareto_conical_rating_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_949.ParetoConicalRatingOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _949

        return self.__parent__._cast(
            _949.ParetoConicalRatingOptimisationStrategyDatabase
        )

    @property
    def pareto_cylindrical_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_950.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _950

        return self.__parent__._cast(
            _950.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_cylindrical_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_951.ParetoCylindricalGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _951

        return self.__parent__._cast(
            _951.ParetoCylindricalGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_cylindrical_rating_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_952.ParetoCylindricalRatingOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _952

        return self.__parent__._cast(
            _952.ParetoCylindricalRatingOptimisationStrategyDatabase
        )

    @property
    def pareto_face_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_953.ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _953

        return self.__parent__._cast(
            _953.ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_face_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_954.ParetoFaceGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _954

        return self.__parent__._cast(_954.ParetoFaceGearSetOptimisationStrategyDatabase)

    @property
    def pareto_face_rating_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_955.ParetoFaceRatingOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _955

        return self.__parent__._cast(_955.ParetoFaceRatingOptimisationStrategyDatabase)

    @property
    def pareto_hypoid_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_956.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _956

        return self.__parent__._cast(
            _956.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_hypoid_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_957.ParetoHypoidGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _957

        return self.__parent__._cast(
            _957.ParetoHypoidGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_spiral_bevel_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_959.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _959

        return self.__parent__._cast(
            _959.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_spiral_bevel_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_960.ParetoSpiralBevelGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _960

        return self.__parent__._cast(
            _960.ParetoSpiralBevelGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_straight_bevel_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_961.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _961

        return self.__parent__._cast(
            _961.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_straight_bevel_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_962.ParetoStraightBevelGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _962

        return self.__parent__._cast(
            _962.ParetoStraightBevelGearSetOptimisationStrategyDatabase
        )

    @property
    def bevel_hypoid_gear_design_settings_database(
        self: "CastSelf",
    ) -> "_966.BevelHypoidGearDesignSettingsDatabase":
        from mastapy._private.gears.gear_designs import _966

        return self.__parent__._cast(_966.BevelHypoidGearDesignSettingsDatabase)

    @property
    def bevel_hypoid_gear_rating_settings_database(
        self: "CastSelf",
    ) -> "_968.BevelHypoidGearRatingSettingsDatabase":
        from mastapy._private.gears.gear_designs import _968

        return self.__parent__._cast(_968.BevelHypoidGearRatingSettingsDatabase)

    @property
    def design_constraint_collection_database(
        self: "CastSelf",
    ) -> "_971.DesignConstraintCollectionDatabase":
        from mastapy._private.gears.gear_designs import _971

        return self.__parent__._cast(_971.DesignConstraintCollectionDatabase)

    @property
    def cylindrical_gear_design_constraints_database(
        self: "CastSelf",
    ) -> "_1047.CylindricalGearDesignConstraintsDatabase":
        from mastapy._private.gears.gear_designs.cylindrical import _1047

        return self.__parent__._cast(_1047.CylindricalGearDesignConstraintsDatabase)

    @property
    def cylindrical_gear_micro_geometry_settings_database(
        self: "CastSelf",
    ) -> "_1053.CylindricalGearMicroGeometrySettingsDatabase":
        from mastapy._private.gears.gear_designs.cylindrical import _1053

        return self.__parent__._cast(_1053.CylindricalGearMicroGeometrySettingsDatabase)

    @property
    def magnet_material_database(self: "CastSelf") -> "_1331.MagnetMaterialDatabase":
        from mastapy._private.electric_machines import _1331

        return self.__parent__._cast(_1331.MagnetMaterialDatabase)

    @property
    def stator_rotor_material_database(
        self: "CastSelf",
    ) -> "_1349.StatorRotorMaterialDatabase":
        from mastapy._private.electric_machines import _1349

        return self.__parent__._cast(_1349.StatorRotorMaterialDatabase)

    @property
    def winding_material_database(self: "CastSelf") -> "_1364.WindingMaterialDatabase":
        from mastapy._private.electric_machines import _1364

        return self.__parent__._cast(_1364.WindingMaterialDatabase)

    @property
    def cycloidal_disc_material_database(
        self: "CastSelf",
    ) -> "_1507.CycloidalDiscMaterialDatabase":
        from mastapy._private.cycloidal import _1507

        return self.__parent__._cast(_1507.CycloidalDiscMaterialDatabase)

    @property
    def ring_pins_material_database(
        self: "CastSelf",
    ) -> "_1514.RingPinsMaterialDatabase":
        from mastapy._private.cycloidal import _1514

        return self.__parent__._cast(_1514.RingPinsMaterialDatabase)

    @property
    def bolted_joint_material_database(
        self: "CastSelf",
    ) -> "_1517.BoltedJointMaterialDatabase":
        from mastapy._private.bolts import _1517

        return self.__parent__._cast(_1517.BoltedJointMaterialDatabase)

    @property
    def bolt_geometry_database(self: "CastSelf") -> "_1519.BoltGeometryDatabase":
        from mastapy._private.bolts import _1519

        return self.__parent__._cast(_1519.BoltGeometryDatabase)

    @property
    def bolt_material_database(self: "CastSelf") -> "_1521.BoltMaterialDatabase":
        from mastapy._private.bolts import _1521

        return self.__parent__._cast(_1521.BoltMaterialDatabase)

    @property
    def clamped_section_material_database(
        self: "CastSelf",
    ) -> "_1526.ClampedSectionMaterialDatabase":
        from mastapy._private.bolts import _1526

        return self.__parent__._cast(_1526.ClampedSectionMaterialDatabase)

    @property
    def design_space_search_strategy_database(
        self: "CastSelf",
    ) -> "_1590.DesignSpaceSearchStrategyDatabase":
        from mastapy._private.math_utility.optimisation import _1590

        return self.__parent__._cast(_1590.DesignSpaceSearchStrategyDatabase)

    @property
    def pareto_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1602.ParetoOptimisationStrategyDatabase":
        from mastapy._private.math_utility.optimisation import _1602

        return self.__parent__._cast(_1602.ParetoOptimisationStrategyDatabase)

    @property
    def named_database(self: "CastSelf") -> "_1883.NamedDatabase":
        from mastapy._private.utility.databases import _1883

        return self.__parent__._cast(_1883.NamedDatabase)

    @property
    def bearing_settings_database(self: "CastSelf") -> "_1935.BearingSettingsDatabase":
        from mastapy._private.bearings import _1935

        return self.__parent__._cast(_1935.BearingSettingsDatabase)

    @property
    def rolling_bearing_database(self: "CastSelf") -> "_1948.RollingBearingDatabase":
        from mastapy._private.bearings import _1948

        return self.__parent__._cast(_1948.RollingBearingDatabase)

    @property
    def iso14179_settings_database(
        self: "CastSelf",
    ) -> "_2031.ISO14179SettingsDatabase":
        from mastapy._private.bearings.bearing_results.rolling import _2031

        return self.__parent__._cast(_2031.ISO14179SettingsDatabase)

    @property
    def conical_gear_optimization_strategy_database(
        self: "CastSelf",
    ) -> "_2285.ConicalGearOptimizationStrategyDatabase":
        from mastapy._private.system_model.optimization import _2285

        return self.__parent__._cast(_2285.ConicalGearOptimizationStrategyDatabase)

    @property
    def optimization_strategy_database(
        self: "CastSelf",
    ) -> "_2293.OptimizationStrategyDatabase":
        from mastapy._private.system_model.optimization import _2293

        return self.__parent__._cast(_2293.OptimizationStrategyDatabase)

    @property
    def supercharger_rotor_set_database(
        self: "CastSelf",
    ) -> "_2625.SuperchargerRotorSetDatabase":
        from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
            _2625,
        )

        return self.__parent__._cast(_2625.SuperchargerRotorSetDatabase)

    @property
    def sql_database(self: "CastSelf") -> "SQLDatabase":
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
class SQLDatabase(_1879.Database[TKey, TValue]):
    """SQLDatabase

    This is a mastapy class.

    Generic Types:
        TKey
        TValue
    """

    TYPE: ClassVar["Type"] = _SQL_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def allow_network_database(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowNetworkDatabase")

        if temp is None:
            return False

        return temp

    @property
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def uses_database(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UsesDatabase")

        if temp is None:
            return False

        return temp

    @enforce_parameter_types
    def delete(self: "Self", key: "TKey") -> None:
        """Method does not return.

        Args:
            key (TKey)
        """
        pythonnet_method_call(self.wrapped, "Delete", key)

    def reload(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Reload")

    @enforce_parameter_types
    def save(self: "Self", item: "TValue") -> None:
        """Method does not return.

        Args:
            item (TValue)
        """
        pythonnet_method_call(self.wrapped, "Save", item)

    @property
    def cast_to(self: "Self") -> "_Cast_SQLDatabase":
        """Cast to another type.

        Returns:
            _Cast_SQLDatabase
        """
        return _Cast_SQLDatabase(self)
