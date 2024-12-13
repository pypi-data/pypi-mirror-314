"""NamedDatabaseItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_NAMED_DATABASE_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Databases", "NamedDatabaseItem"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings import _1936
    from mastapy._private.bearings.bearing_results.rolling import _2030
    from mastapy._private.bolts import _1516, _1518, _1520
    from mastapy._private.cycloidal import _1506, _1513
    from mastapy._private.detailed_rigid_connectors.splines import _1466
    from mastapy._private.electric_machines import _1330, _1348, _1363
    from mastapy._private.gears import _354
    from mastapy._private.gears.gear_designs import _967, _969, _972
    from mastapy._private.gears.gear_designs.cylindrical import _1046, _1054
    from mastapy._private.gears.manufacturing.bevel import _824
    from mastapy._private.gears.manufacturing.cylindrical.cutters import (
        _731,
        _732,
        _733,
        _734,
        _735,
        _737,
        _738,
        _739,
        _740,
        _743,
    )
    from mastapy._private.gears.materials import (
        _596,
        _599,
        _601,
        _606,
        _610,
        _618,
        _620,
        _623,
        _627,
        _630,
    )
    from mastapy._private.gears.rating.cylindrical import _467, _483
    from mastapy._private.materials import _258, _280, _282, _286
    from mastapy._private.math_utility.optimisation import _1599
    from mastapy._private.nodal_analysis import _50
    from mastapy._private.shafts import _24, _40, _43
    from mastapy._private.system_model.optimization import _2283, _2286, _2291, _2292
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
        _2624,
    )
    from mastapy._private.utility import _1633
    from mastapy._private.utility.databases import _1885

    Self = TypeVar("Self", bound="NamedDatabaseItem")
    CastSelf = TypeVar("CastSelf", bound="NamedDatabaseItem._Cast_NamedDatabaseItem")


__docformat__ = "restructuredtext en"
__all__ = ("NamedDatabaseItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NamedDatabaseItem:
    """Special nested class for casting NamedDatabaseItem to subclasses."""

    __parent__: "NamedDatabaseItem"

    @property
    def shaft_material(self: "CastSelf") -> "_24.ShaftMaterial":
        from mastapy._private.shafts import _24

        return self.__parent__._cast(_24.ShaftMaterial)

    @property
    def shaft_settings_item(self: "CastSelf") -> "_40.ShaftSettingsItem":
        from mastapy._private.shafts import _40

        return self.__parent__._cast(_40.ShaftSettingsItem)

    @property
    def simple_shaft_definition(self: "CastSelf") -> "_43.SimpleShaftDefinition":
        from mastapy._private.shafts import _43

        return self.__parent__._cast(_43.SimpleShaftDefinition)

    @property
    def analysis_settings_item(self: "CastSelf") -> "_50.AnalysisSettingsItem":
        from mastapy._private.nodal_analysis import _50

        return self.__parent__._cast(_50.AnalysisSettingsItem)

    @property
    def bearing_material(self: "CastSelf") -> "_258.BearingMaterial":
        from mastapy._private.materials import _258

        return self.__parent__._cast(_258.BearingMaterial)

    @property
    def lubrication_detail(self: "CastSelf") -> "_280.LubricationDetail":
        from mastapy._private.materials import _280

        return self.__parent__._cast(_280.LubricationDetail)

    @property
    def material(self: "CastSelf") -> "_282.Material":
        from mastapy._private.materials import _282

        return self.__parent__._cast(_282.Material)

    @property
    def materials_settings_item(self: "CastSelf") -> "_286.MaterialsSettingsItem":
        from mastapy._private.materials import _286

        return self.__parent__._cast(_286.MaterialsSettingsItem)

    @property
    def pocketing_power_loss_coefficients(
        self: "CastSelf",
    ) -> "_354.PocketingPowerLossCoefficients":
        from mastapy._private.gears import _354

        return self.__parent__._cast(_354.PocketingPowerLossCoefficients)

    @property
    def cylindrical_gear_design_and_rating_settings_item(
        self: "CastSelf",
    ) -> "_467.CylindricalGearDesignAndRatingSettingsItem":
        from mastapy._private.gears.rating.cylindrical import _467

        return self.__parent__._cast(_467.CylindricalGearDesignAndRatingSettingsItem)

    @property
    def cylindrical_plastic_gear_rating_settings_item(
        self: "CastSelf",
    ) -> "_483.CylindricalPlasticGearRatingSettingsItem":
        from mastapy._private.gears.rating.cylindrical import _483

        return self.__parent__._cast(_483.CylindricalPlasticGearRatingSettingsItem)

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
    def isotr1417912001_coefficient_of_friction_constants(
        self: "CastSelf",
    ) -> "_620.ISOTR1417912001CoefficientOfFrictionConstants":
        from mastapy._private.gears.materials import _620

        return self.__parent__._cast(_620.ISOTR1417912001CoefficientOfFrictionConstants)

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
    def raw_material(self: "CastSelf") -> "_630.RawMaterial":
        from mastapy._private.gears.materials import _630

        return self.__parent__._cast(_630.RawMaterial)

    @property
    def cylindrical_gear_abstract_cutter_design(
        self: "CastSelf",
    ) -> "_731.CylindricalGearAbstractCutterDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _731

        return self.__parent__._cast(_731.CylindricalGearAbstractCutterDesign)

    @property
    def cylindrical_gear_form_grinding_wheel(
        self: "CastSelf",
    ) -> "_732.CylindricalGearFormGrindingWheel":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _732

        return self.__parent__._cast(_732.CylindricalGearFormGrindingWheel)

    @property
    def cylindrical_gear_grinding_worm(
        self: "CastSelf",
    ) -> "_733.CylindricalGearGrindingWorm":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _733

        return self.__parent__._cast(_733.CylindricalGearGrindingWorm)

    @property
    def cylindrical_gear_hob_design(
        self: "CastSelf",
    ) -> "_734.CylindricalGearHobDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _734

        return self.__parent__._cast(_734.CylindricalGearHobDesign)

    @property
    def cylindrical_gear_plunge_shaver(
        self: "CastSelf",
    ) -> "_735.CylindricalGearPlungeShaver":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _735

        return self.__parent__._cast(_735.CylindricalGearPlungeShaver)

    @property
    def cylindrical_gear_rack_design(
        self: "CastSelf",
    ) -> "_737.CylindricalGearRackDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _737

        return self.__parent__._cast(_737.CylindricalGearRackDesign)

    @property
    def cylindrical_gear_real_cutter_design(
        self: "CastSelf",
    ) -> "_738.CylindricalGearRealCutterDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _738

        return self.__parent__._cast(_738.CylindricalGearRealCutterDesign)

    @property
    def cylindrical_gear_shaper(self: "CastSelf") -> "_739.CylindricalGearShaper":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _739

        return self.__parent__._cast(_739.CylindricalGearShaper)

    @property
    def cylindrical_gear_shaver(self: "CastSelf") -> "_740.CylindricalGearShaver":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _740

        return self.__parent__._cast(_740.CylindricalGearShaver)

    @property
    def involute_cutter_design(self: "CastSelf") -> "_743.InvoluteCutterDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _743

        return self.__parent__._cast(_743.InvoluteCutterDesign)

    @property
    def manufacturing_machine(self: "CastSelf") -> "_824.ManufacturingMachine":
        from mastapy._private.gears.manufacturing.bevel import _824

        return self.__parent__._cast(_824.ManufacturingMachine)

    @property
    def bevel_hypoid_gear_design_settings_item(
        self: "CastSelf",
    ) -> "_967.BevelHypoidGearDesignSettingsItem":
        from mastapy._private.gears.gear_designs import _967

        return self.__parent__._cast(_967.BevelHypoidGearDesignSettingsItem)

    @property
    def bevel_hypoid_gear_rating_settings_item(
        self: "CastSelf",
    ) -> "_969.BevelHypoidGearRatingSettingsItem":
        from mastapy._private.gears.gear_designs import _969

        return self.__parent__._cast(_969.BevelHypoidGearRatingSettingsItem)

    @property
    def design_constraints_collection(
        self: "CastSelf",
    ) -> "_972.DesignConstraintsCollection":
        from mastapy._private.gears.gear_designs import _972

        return self.__parent__._cast(_972.DesignConstraintsCollection)

    @property
    def cylindrical_gear_design_constraints(
        self: "CastSelf",
    ) -> "_1046.CylindricalGearDesignConstraints":
        from mastapy._private.gears.gear_designs.cylindrical import _1046

        return self.__parent__._cast(_1046.CylindricalGearDesignConstraints)

    @property
    def cylindrical_gear_micro_geometry_settings_item(
        self: "CastSelf",
    ) -> "_1054.CylindricalGearMicroGeometrySettingsItem":
        from mastapy._private.gears.gear_designs.cylindrical import _1054

        return self.__parent__._cast(_1054.CylindricalGearMicroGeometrySettingsItem)

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
    def bolt_geometry(self: "CastSelf") -> "_1518.BoltGeometry":
        from mastapy._private.bolts import _1518

        return self.__parent__._cast(_1518.BoltGeometry)

    @property
    def bolt_material(self: "CastSelf") -> "_1520.BoltMaterial":
        from mastapy._private.bolts import _1520

        return self.__parent__._cast(_1520.BoltMaterial)

    @property
    def pareto_optimisation_strategy(
        self: "CastSelf",
    ) -> "_1599.ParetoOptimisationStrategy":
        from mastapy._private.math_utility.optimisation import _1599

        return self.__parent__._cast(_1599.ParetoOptimisationStrategy)

    @property
    def bearing_settings_item(self: "CastSelf") -> "_1936.BearingSettingsItem":
        from mastapy._private.bearings import _1936

        return self.__parent__._cast(_1936.BearingSettingsItem)

    @property
    def iso14179_settings(self: "CastSelf") -> "_2030.ISO14179Settings":
        from mastapy._private.bearings.bearing_results.rolling import _2030

        return self.__parent__._cast(_2030.ISO14179Settings)

    @property
    def conical_gear_optimisation_strategy(
        self: "CastSelf",
    ) -> "_2283.ConicalGearOptimisationStrategy":
        from mastapy._private.system_model.optimization import _2283

        return self.__parent__._cast(_2283.ConicalGearOptimisationStrategy)

    @property
    def cylindrical_gear_optimisation_strategy(
        self: "CastSelf",
    ) -> "_2286.CylindricalGearOptimisationStrategy":
        from mastapy._private.system_model.optimization import _2286

        return self.__parent__._cast(_2286.CylindricalGearOptimisationStrategy)

    @property
    def optimization_strategy(self: "CastSelf") -> "_2291.OptimizationStrategy":
        from mastapy._private.system_model.optimization import _2291

        return self.__parent__._cast(_2291.OptimizationStrategy)

    @property
    def optimization_strategy_base(
        self: "CastSelf",
    ) -> "_2292.OptimizationStrategyBase":
        from mastapy._private.system_model.optimization import _2292

        return self.__parent__._cast(_2292.OptimizationStrategyBase)

    @property
    def supercharger_rotor_set(self: "CastSelf") -> "_2624.SuperchargerRotorSet":
        from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
            _2624,
        )

        return self.__parent__._cast(_2624.SuperchargerRotorSet)

    @property
    def named_database_item(self: "CastSelf") -> "NamedDatabaseItem":
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
class NamedDatabaseItem(_0.APIBase):
    """NamedDatabaseItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NAMED_DATABASE_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def comment(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Comment")

        if temp is None:
            return ""

        return temp

    @comment.setter
    @enforce_parameter_types
    def comment(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Comment", str(value) if value is not None else ""
        )

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
    def no_history(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NoHistory")

        if temp is None:
            return ""

        return temp

    @property
    def history(self: "Self") -> "_1633.FileHistory":
        """mastapy.utility.FileHistory

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "History")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def database_key(self: "Self") -> "_1885.NamedKey":
        """mastapy.utility.databases.NamedKey"""
        temp = pythonnet_property_get(self.wrapped, "DatabaseKey")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @database_key.setter
    @enforce_parameter_types
    def database_key(self: "Self", value: "_1885.NamedKey") -> None:
        pythonnet_property_set(self.wrapped, "DatabaseKey", value.wrapped)

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
    def cast_to(self: "Self") -> "_Cast_NamedDatabaseItem":
        """Cast to another type.

        Returns:
            _Cast_NamedDatabaseItem
        """
        return _Cast_NamedDatabaseItem(self)
