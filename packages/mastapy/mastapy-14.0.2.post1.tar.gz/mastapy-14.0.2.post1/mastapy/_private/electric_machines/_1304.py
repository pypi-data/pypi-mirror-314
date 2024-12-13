"""ElectricMachineDetail"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import list_with_selected_item, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines import _1310

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_ELECTRIC_MACHINE_DETAIL = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "ElectricMachineDetail"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private import _7733
    from mastapy._private.electric_machines import (
        _1284,
        _1287,
        _1299,
        _1311,
        _1322,
        _1333,
        _1336,
        _1340,
        _1350,
        _1352,
        _1369,
    )
    from mastapy._private.electric_machines.results import _1392, _1393
    from mastapy._private.math_utility import _1572
    from mastapy._private.utility import _1642

    Self = TypeVar("Self", bound="ElectricMachineDetail")
    CastSelf = TypeVar(
        "CastSelf", bound="ElectricMachineDetail._Cast_ElectricMachineDetail"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineDetail:
    """Special nested class for casting ElectricMachineDetail to subclasses."""

    __parent__: "ElectricMachineDetail"

    @property
    def cad_electric_machine_detail(
        self: "CastSelf",
    ) -> "_1287.CADElectricMachineDetail":
        from mastapy._private.electric_machines import _1287

        return self.__parent__._cast(_1287.CADElectricMachineDetail)

    @property
    def interior_permanent_magnet_machine(
        self: "CastSelf",
    ) -> "_1322.InteriorPermanentMagnetMachine":
        from mastapy._private.electric_machines import _1322

        return self.__parent__._cast(_1322.InteriorPermanentMagnetMachine)

    @property
    def non_cad_electric_machine_detail(
        self: "CastSelf",
    ) -> "_1333.NonCADElectricMachineDetail":
        from mastapy._private.electric_machines import _1333

        return self.__parent__._cast(_1333.NonCADElectricMachineDetail)

    @property
    def permanent_magnet_assisted_synchronous_reluctance_machine(
        self: "CastSelf",
    ) -> "_1336.PermanentMagnetAssistedSynchronousReluctanceMachine":
        from mastapy._private.electric_machines import _1336

        return self.__parent__._cast(
            _1336.PermanentMagnetAssistedSynchronousReluctanceMachine
        )

    @property
    def surface_permanent_magnet_machine(
        self: "CastSelf",
    ) -> "_1350.SurfacePermanentMagnetMachine":
        from mastapy._private.electric_machines import _1350

        return self.__parent__._cast(_1350.SurfacePermanentMagnetMachine)

    @property
    def synchronous_reluctance_machine(
        self: "CastSelf",
    ) -> "_1352.SynchronousReluctanceMachine":
        from mastapy._private.electric_machines import _1352

        return self.__parent__._cast(_1352.SynchronousReluctanceMachine)

    @property
    def wound_field_synchronous_machine(
        self: "CastSelf",
    ) -> "_1369.WoundFieldSynchronousMachine":
        from mastapy._private.electric_machines import _1369

        return self.__parent__._cast(_1369.WoundFieldSynchronousMachine)

    @property
    def electric_machine_detail(self: "CastSelf") -> "ElectricMachineDetail":
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
class ElectricMachineDetail(_0.APIBase):
    """ElectricMachineDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_DETAIL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def core_loss_build_factor_specification_method(
        self: "Self",
    ) -> "_1299.CoreLossBuildFactorSpecificationMethod":
        """mastapy.electric_machines.CoreLossBuildFactorSpecificationMethod"""
        temp = pythonnet_property_get(
            self.wrapped, "CoreLossBuildFactorSpecificationMethod"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.CoreLossBuildFactorSpecificationMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines._1299",
            "CoreLossBuildFactorSpecificationMethod",
        )(value)

    @core_loss_build_factor_specification_method.setter
    @enforce_parameter_types
    def core_loss_build_factor_specification_method(
        self: "Self", value: "_1299.CoreLossBuildFactorSpecificationMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.ElectricMachines.CoreLossBuildFactorSpecificationMethod",
        )
        pythonnet_property_set(
            self.wrapped, "CoreLossBuildFactorSpecificationMethod", value
        )

    @property
    def dc_bus_voltage(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DCBusVoltage")

        if temp is None:
            return 0.0

        return temp

    @dc_bus_voltage.setter
    @enforce_parameter_types
    def dc_bus_voltage(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DCBusVoltage", float(value) if value is not None else 0.0
        )

    @property
    def eddy_current_core_loss_build_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EddyCurrentCoreLossBuildFactor")

        if temp is None:
            return 0.0

        return temp

    @eddy_current_core_loss_build_factor.setter
    @enforce_parameter_types
    def eddy_current_core_loss_build_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EddyCurrentCoreLossBuildFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def effective_machine_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectiveMachineLength")

        if temp is None:
            return 0.0

        return temp

    @property
    def electric_machine_type(self: "Self") -> "_1311.ElectricMachineType":
        """mastapy.electric_machines.ElectricMachineType

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElectricMachineType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.ElectricMachineType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines._1311", "ElectricMachineType"
        )(value)

    @property
    def enclosing_volume(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EnclosingVolume")

        if temp is None:
            return 0.0

        return temp

    @property
    def excess_core_loss_build_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ExcessCoreLossBuildFactor")

        if temp is None:
            return 0.0

        return temp

    @excess_core_loss_build_factor.setter
    @enforce_parameter_types
    def excess_core_loss_build_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ExcessCoreLossBuildFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def has_non_linear_dq_model(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HasNonLinearDQModel")

        if temp is None:
            return False

        return temp

    @property
    def hysteresis_core_loss_build_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HysteresisCoreLossBuildFactor")

        if temp is None:
            return 0.0

        return temp

    @hysteresis_core_loss_build_factor.setter
    @enforce_parameter_types
    def hysteresis_core_loss_build_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HysteresisCoreLossBuildFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def include_default_results_locations(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeDefaultResultsLocations")

        if temp is None:
            return False

        return temp

    @include_default_results_locations.setter
    @enforce_parameter_types
    def include_default_results_locations(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeDefaultResultsLocations",
            bool(value) if value is not None else False,
        )

    @property
    def include_shaft(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeShaft")

        if temp is None:
            return False

        return temp

    @include_shaft.setter
    @enforce_parameter_types
    def include_shaft(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IncludeShaft", bool(value) if value is not None else False
        )

    @property
    def line_line_supply_voltage_rms(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LineLineSupplyVoltageRMS")

        if temp is None:
            return 0.0

        return temp

    @property
    def machine_drawing(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MachineDrawing")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def machine_periodicity_factor(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "MachinePeriodicityFactor")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @machine_periodicity_factor.setter
    @enforce_parameter_types
    def machine_periodicity_factor(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MachinePeriodicityFactor", value)

    @property
    def magnet_loss_build_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MagnetLossBuildFactor")

        if temp is None:
            return 0.0

        return temp

    @magnet_loss_build_factor.setter
    @enforce_parameter_types
    def magnet_loss_build_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MagnetLossBuildFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    def number_of_phases(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfPhases")

        if temp is None:
            return 0

        return temp

    @property
    def number_of_slots_per_phase(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfSlotsPerPhase")

        if temp is None:
            return 0

        return temp

    @property
    def number_of_slots_per_pole(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfSlotsPerPole")

        if temp is None:
            return 0.0

        return temp

    @property
    def number_of_slots_per_pole_per_phase(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfSlotsPerPolePerPhase")

        if temp is None:
            return 0.0

        return temp

    @property
    def phase_supply_voltage_peak(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PhaseSupplyVoltagePeak")

        if temp is None:
            return 0.0

        return temp

    @property
    def phase_supply_voltage_rms(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PhaseSupplyVoltageRMS")

        if temp is None:
            return 0.0

        return temp

    @property
    def radial_air_gap(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialAirGap")

        if temp is None:
            return 0.0

        return temp

    @radial_air_gap.setter
    @enforce_parameter_types
    def radial_air_gap(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RadialAirGap", float(value) if value is not None else 0.0
        )

    @property
    def rated_inverter_current_peak(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RatedInverterCurrentPeak")

        if temp is None:
            return 0.0

        return temp

    @rated_inverter_current_peak.setter
    @enforce_parameter_types
    def rated_inverter_current_peak(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RatedInverterCurrentPeak",
            float(value) if value is not None else 0.0,
        )

    @property
    def rated_inverter_phase_current_peak(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatedInverterPhaseCurrentPeak")

        if temp is None:
            return 0.0

        return temp

    @property
    def rotor_core_loss_build_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotorCoreLossBuildFactor")

        if temp is None:
            return 0.0

        return temp

    @rotor_core_loss_build_factor.setter
    @enforce_parameter_types
    def rotor_core_loss_build_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RotorCoreLossBuildFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def select_setup(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_ElectricMachineSetup":
        """ListWithSelectedItem[mastapy.electric_machines.ElectricMachineSetup]"""
        temp = pythonnet_property_get(self.wrapped, "SelectSetup")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_ElectricMachineSetup",
        )(temp)

    @select_setup.setter
    @enforce_parameter_types
    def select_setup(self: "Self", value: "_1310.ElectricMachineSetup") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_ElectricMachineSetup.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_ElectricMachineSetup.implicit_type()
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "SelectSetup", value)

    @property
    def shaft_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShaftDiameter")

        if temp is None:
            return 0.0

        return temp

    @shaft_diameter.setter
    @enforce_parameter_types
    def shaft_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ShaftDiameter", float(value) if value is not None else 0.0
        )

    @property
    def shaft_material_database(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "ShaftMaterialDatabase", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @shaft_material_database.setter
    @enforce_parameter_types
    def shaft_material_database(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "ShaftMaterialDatabase",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    def stator_core_loss_build_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StatorCoreLossBuildFactor")

        if temp is None:
            return 0.0

        return temp

    @stator_core_loss_build_factor.setter
    @enforce_parameter_types
    def stator_core_loss_build_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StatorCoreLossBuildFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def non_linear_dq_model(self: "Self") -> "_1392.NonLinearDQModel":
        """mastapy.electric_machines.results.NonLinearDQModel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NonLinearDQModel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def non_linear_dq_model_generator_settings(
        self: "Self",
    ) -> "_1393.NonLinearDQModelGeneratorSettings":
        """mastapy.electric_machines.results.NonLinearDQModelGeneratorSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NonLinearDQModelGeneratorSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def rotor(self: "Self") -> "_1340.Rotor":
        """mastapy.electric_machines.Rotor

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rotor")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def selected_setup(self: "Self") -> "_1310.ElectricMachineSetup":
        """mastapy.electric_machines.ElectricMachineSetup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SelectedSetup")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def stator(self: "Self") -> "_1284.AbstractStator":
        """mastapy.electric_machines.AbstractStator

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Stator")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def results_locations(self: "Self") -> "List[_1572.Named2DLocation]":
        """List[mastapy.math_utility.Named2DLocation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsLocations")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def setups(self: "Self") -> "List[_1310.ElectricMachineSetup]":
        """List[mastapy.electric_machines.ElectricMachineSetup]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Setups")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

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

    def generate_cad_geometry_model(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "GenerateCADGeometryModel")

    @enforce_parameter_types
    def add_results_location(self: "Self", name: "str") -> None:
        """Method does not return.

        Args:
            name (str)
        """
        name = str(name)
        pythonnet_method_call(self.wrapped, "AddResultsLocation", name if name else "")

    def add_setup(self: "Self") -> "_1310.ElectricMachineSetup":
        """mastapy.electric_machines.ElectricMachineSetup"""
        method_result = pythonnet_method_call(self.wrapped, "AddSetup")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def duplicate_setup(
        self: "Self", setup: "_1310.ElectricMachineSetup"
    ) -> "_1310.ElectricMachineSetup":
        """mastapy.electric_machines.ElectricMachineSetup

        Args:
            setup (mastapy.electric_machines.ElectricMachineSetup)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "DuplicateSetup", setup.wrapped if setup else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def export_to_smt_format(self: "Self", file_name: "str") -> None:
        """Method does not return.

        Args:
            file_name (str)
        """
        file_name = str(file_name)
        pythonnet_method_call(
            self.wrapped, "ExportToSMTFormat", file_name if file_name else ""
        )

    def generate_design_without_non_linear_dq_model(
        self: "Self",
    ) -> "_1642.MethodOutcomeWithResult[ElectricMachineDetail]":
        """mastapy.utility.MethodOutcomeWithResult[mastapy.electric_machines.ElectricMachineDetail]"""
        method_result = pythonnet_method_call(
            self.wrapped, "GenerateDesignWithoutNonLinearDQModel"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def remove_results_location(self: "Self", name: "str") -> None:
        """Method does not return.

        Args:
            name (str)
        """
        name = str(name)
        pythonnet_method_call(
            self.wrapped, "RemoveResultsLocation", name if name else ""
        )

    @enforce_parameter_types
    def remove_setup(self: "Self", setup: "_1310.ElectricMachineSetup") -> None:
        """Method does not return.

        Args:
            setup (mastapy.electric_machines.ElectricMachineSetup)
        """
        pythonnet_method_call(
            self.wrapped, "RemoveSetup", setup.wrapped if setup else None
        )

    @enforce_parameter_types
    def setup_named(self: "Self", name: "str") -> "_1310.ElectricMachineSetup":
        """mastapy.electric_machines.ElectricMachineSetup

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "SetupNamed", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    def try_generate_non_linear_dq_model(
        self: "Self",
    ) -> "_1642.MethodOutcomeWithResult[ElectricMachineDetail]":
        """mastapy.utility.MethodOutcomeWithResult[mastapy.electric_machines.ElectricMachineDetail]"""
        method_result = pythonnet_method_call(
            self.wrapped, "TryGenerateNonLinearDQModel"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def try_generate_non_linear_dq_model_with_task_progress(
        self: "Self", progress: "_7733.TaskProgress"
    ) -> "_1642.MethodOutcomeWithResult[ElectricMachineDetail]":
        """mastapy.utility.MethodOutcomeWithResult[mastapy.electric_machines.ElectricMachineDetail]

        Args:
            progress (mastapy.TaskProgress)
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "TryGenerateNonLinearDQModelWithTaskProgress",
            progress.wrapped if progress else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def write_dxf_to(self: "Self", file_name: "str") -> None:
        """Method does not return.

        Args:
            file_name (str)
        """
        file_name = str(file_name)
        pythonnet_method_call(
            self.wrapped, "WriteDxfTo", file_name if file_name else ""
        )

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
    def cast_to(self: "Self") -> "_Cast_ElectricMachineDetail":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineDetail
        """
        return _Cast_ElectricMachineDetail(self)
