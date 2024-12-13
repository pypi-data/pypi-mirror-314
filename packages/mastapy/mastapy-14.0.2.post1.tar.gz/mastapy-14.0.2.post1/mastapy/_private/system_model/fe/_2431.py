"""ElectricMachineDataSet"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.fe import _2443

_ARRAY = python_net_import("System", "Array")
_DOUBLE = python_net_import("System", "Double")
_STRING = python_net_import("System", "String")
_HARMONIC_LOAD_DATA_TYPE = python_net_import(
    "SMT.MastaAPI.ElectricMachines.HarmonicLoadData", "HarmonicLoadDataType"
)
_FE_SUBSTRUCTURE_NODE = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "FESubstructureNode"
)
_ELECTRIC_MACHINE_DATA_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "ElectricMachineDataSet"
)
_LIST = python_net_import("System.Collections.Generic", "List")
_MEASUREMENT_TYPE = python_net_import(
    "SMT.MastaAPIUtility.UnitsAndMeasurements", "MeasurementType"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.electric_machines.harmonic_load_data import _1432
    from mastapy._private.math_utility import _1571
    from mastapy._private.system_model.analyses_and_results.static_loads import _7131
    from mastapy._private.units_and_measurements import _7734

    Self = TypeVar("Self", bound="ElectricMachineDataSet")
    CastSelf = TypeVar(
        "CastSelf", bound="ElectricMachineDataSet._Cast_ElectricMachineDataSet"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineDataSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineDataSet:
    """Special nested class for casting ElectricMachineDataSet to subclasses."""

    __parent__: "ElectricMachineDataSet"

    @property
    def electric_machine_data_set(self: "CastSelf") -> "ElectricMachineDataSet":
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
class ElectricMachineDataSet(_0.APIBase):
    """ElectricMachineDataSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_DATA_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def data_set_name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "DataSetName")

        if temp is None:
            return ""

        return temp

    @data_set_name.setter
    @enforce_parameter_types
    def data_set_name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "DataSetName", str(value) if value is not None else ""
        )

    @property
    def node_for_first_tooth(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_FESubstructureNode":
        """ListWithSelectedItem[mastapy.system_model.fe.FESubstructureNode]"""
        temp = pythonnet_property_get(self.wrapped, "NodeForFirstTooth")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_FESubstructureNode",
        )(temp)

    @node_for_first_tooth.setter
    @enforce_parameter_types
    def node_for_first_tooth(self: "Self", value: "_2443.FESubstructureNode") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_FESubstructureNode.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_FESubstructureNode.implicit_type()
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "NodeForFirstTooth", value)

    @property
    def rotor_moment_from_stator_teeth_axial_loads_amplitude_cut_off(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "RotorMomentFromStatorTeethAxialLoadsAmplitudeCutOff"
        )

        if temp is None:
            return 0.0

        return temp

    @rotor_moment_from_stator_teeth_axial_loads_amplitude_cut_off.setter
    @enforce_parameter_types
    def rotor_moment_from_stator_teeth_axial_loads_amplitude_cut_off(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "RotorMomentFromStatorTeethAxialLoadsAmplitudeCutOff",
            float(value) if value is not None else 0.0,
        )

    @property
    def rotor_x_force_amplitude_cut_off(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotorXForceAmplitudeCutOff")

        if temp is None:
            return 0.0

        return temp

    @rotor_x_force_amplitude_cut_off.setter
    @enforce_parameter_types
    def rotor_x_force_amplitude_cut_off(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RotorXForceAmplitudeCutOff",
            float(value) if value is not None else 0.0,
        )

    @property
    def rotor_y_force_amplitude_cut_off(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotorYForceAmplitudeCutOff")

        if temp is None:
            return 0.0

        return temp

    @rotor_y_force_amplitude_cut_off.setter
    @enforce_parameter_types
    def rotor_y_force_amplitude_cut_off(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RotorYForceAmplitudeCutOff",
            float(value) if value is not None else 0.0,
        )

    @property
    def rotor_z_force_amplitude_cut_off(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotorZForceAmplitudeCutOff")

        if temp is None:
            return 0.0

        return temp

    @rotor_z_force_amplitude_cut_off.setter
    @enforce_parameter_types
    def rotor_z_force_amplitude_cut_off(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RotorZForceAmplitudeCutOff",
            float(value) if value is not None else 0.0,
        )

    @property
    def stator_axial_loads_amplitude_cut_off(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StatorAxialLoadsAmplitudeCutOff")

        if temp is None:
            return 0.0

        return temp

    @stator_axial_loads_amplitude_cut_off.setter
    @enforce_parameter_types
    def stator_axial_loads_amplitude_cut_off(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StatorAxialLoadsAmplitudeCutOff",
            float(value) if value is not None else 0.0,
        )

    @property
    def stator_radial_loads_amplitude_cut_off(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StatorRadialLoadsAmplitudeCutOff")

        if temp is None:
            return 0.0

        return temp

    @stator_radial_loads_amplitude_cut_off.setter
    @enforce_parameter_types
    def stator_radial_loads_amplitude_cut_off(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StatorRadialLoadsAmplitudeCutOff",
            float(value) if value is not None else 0.0,
        )

    @property
    def stator_tangential_loads_amplitude_cut_off(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "StatorTangentialLoadsAmplitudeCutOff"
        )

        if temp is None:
            return 0.0

        return temp

    @stator_tangential_loads_amplitude_cut_off.setter
    @enforce_parameter_types
    def stator_tangential_loads_amplitude_cut_off(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StatorTangentialLoadsAmplitudeCutOff",
            float(value) if value is not None else 0.0,
        )

    @property
    def stator_tooth_moments_amplitude_cut_off(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StatorToothMomentsAmplitudeCutOff")

        if temp is None:
            return 0.0

        return temp

    @stator_tooth_moments_amplitude_cut_off.setter
    @enforce_parameter_types
    def stator_tooth_moments_amplitude_cut_off(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StatorToothMomentsAmplitudeCutOff",
            float(value) if value is not None else 0.0,
        )

    @property
    def torque_ripple_amplitude_cut_off(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TorqueRippleAmplitudeCutOff")

        if temp is None:
            return 0.0

        return temp

    @torque_ripple_amplitude_cut_off.setter
    @enforce_parameter_types
    def torque_ripple_amplitude_cut_off(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TorqueRippleAmplitudeCutOff",
            float(value) if value is not None else 0.0,
        )

    @property
    def torque_ripple_input_type(self: "Self") -> "_7131.TorqueRippleInputType":
        """mastapy.system_model.analyses_and_results.static_loads.TorqueRippleInputType"""
        temp = pythonnet_property_get(self.wrapped, "TorqueRippleInputType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.TorqueRippleInputType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.static_loads._7131",
            "TorqueRippleInputType",
        )(value)

    @torque_ripple_input_type.setter
    @enforce_parameter_types
    def torque_ripple_input_type(
        self: "Self", value: "_7131.TorqueRippleInputType"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.TorqueRippleInputType",
        )
        pythonnet_property_set(self.wrapped, "TorqueRippleInputType", value)

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
    def add_or_replace_excitation_data_with_amplitudes_phases_and_fe_node(
        self: "Self",
        harmonic_load_data_type: "_1432.HarmonicLoadDataType",
        node: "_2443.FESubstructureNode",
        speed: "float",
        fourier_series_amplitudes: "List[float]",
        fourier_series_phases: "List[float]",
        fourier_series_mean_value: "float",
        fourier_series_name: "str",
        fourier_series_measurement_type: "_7734.MeasurementType",
    ) -> None:
        """Method does not return.

        Args:
            harmonic_load_data_type (mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType)
            node (mastapy.system_model.fe.FESubstructureNode)
            speed (float)
            fourier_series_amplitudes (List[float])
            fourier_series_phases (List[float])
            fourier_series_mean_value (float)
            fourier_series_name (str)
            fourier_series_measurement_type (mastapy.units_and_measurements.MeasurementType)
        """
        harmonic_load_data_type = conversion.mp_to_pn_enum(
            harmonic_load_data_type,
            "SMT.MastaAPI.ElectricMachines.HarmonicLoadData.HarmonicLoadDataType",
        )
        speed = float(speed)
        fourier_series_amplitudes = conversion.mp_to_pn_list_float(
            fourier_series_amplitudes
        )
        fourier_series_phases = conversion.mp_to_pn_list_float(fourier_series_phases)
        fourier_series_mean_value = float(fourier_series_mean_value)
        fourier_series_name = str(fourier_series_name)
        fourier_series_measurement_type = conversion.mp_to_pn_enum(
            fourier_series_measurement_type,
            "SMT.MastaAPIUtility.UnitsAndMeasurements.MeasurementType",
        )
        pythonnet_method_call_overload(
            self.wrapped,
            "AddOrReplaceExcitationData",
            [
                _HARMONIC_LOAD_DATA_TYPE,
                _FE_SUBSTRUCTURE_NODE,
                _DOUBLE,
                _LIST[_DOUBLE],
                _LIST[_DOUBLE],
                _DOUBLE,
                _STRING,
                _MEASUREMENT_TYPE,
            ],
            harmonic_load_data_type,
            node.wrapped if node else None,
            speed if speed else 0.0,
            fourier_series_amplitudes,
            fourier_series_phases,
            fourier_series_mean_value if fourier_series_mean_value else 0.0,
            fourier_series_name if fourier_series_name else "",
            fourier_series_measurement_type,
        )

    @enforce_parameter_types
    def add_or_replace_excitation_data_with_fe_node(
        self: "Self",
        harmonic_load_data_type: "_1432.HarmonicLoadDataType",
        node: "_2443.FESubstructureNode",
        speed: "float",
        fourier_series_values: "List[float]",
        fourier_series_name: "str",
        fourier_series_measurement_type: "_7734.MeasurementType",
    ) -> None:
        """Method does not return.

        Args:
            harmonic_load_data_type (mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType)
            node (mastapy.system_model.fe.FESubstructureNode)
            speed (float)
            fourier_series_values (List[float])
            fourier_series_name (str)
            fourier_series_measurement_type (mastapy.units_and_measurements.MeasurementType)
        """
        harmonic_load_data_type = conversion.mp_to_pn_enum(
            harmonic_load_data_type,
            "SMT.MastaAPI.ElectricMachines.HarmonicLoadData.HarmonicLoadDataType",
        )
        speed = float(speed)
        fourier_series_values = conversion.mp_to_pn_array_float(fourier_series_values)
        fourier_series_name = str(fourier_series_name)
        fourier_series_measurement_type = conversion.mp_to_pn_enum(
            fourier_series_measurement_type,
            "SMT.MastaAPIUtility.UnitsAndMeasurements.MeasurementType",
        )
        pythonnet_method_call_overload(
            self.wrapped,
            "AddOrReplaceExcitationData",
            [
                _HARMONIC_LOAD_DATA_TYPE,
                _FE_SUBSTRUCTURE_NODE,
                _DOUBLE,
                _ARRAY[_DOUBLE],
                _STRING,
                _MEASUREMENT_TYPE,
            ],
            harmonic_load_data_type,
            node.wrapped if node else None,
            speed if speed else 0.0,
            fourier_series_values,
            fourier_series_name if fourier_series_name else "",
            fourier_series_measurement_type,
        )

    @enforce_parameter_types
    def add_or_replace_excitation_data_with_amplitudes_and_phases(
        self: "Self",
        harmonic_load_data_type: "_1432.HarmonicLoadDataType",
        speed: "float",
        fourier_series_amplitudes: "List[float]",
        fourier_series_phases: "List[float]",
        fourier_series_mean_value: "float",
        fourier_series_name: "str",
        fourier_series_measurement_type: "_7734.MeasurementType",
    ) -> None:
        """Method does not return.

        Args:
            harmonic_load_data_type (mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType)
            speed (float)
            fourier_series_amplitudes (List[float])
            fourier_series_phases (List[float])
            fourier_series_mean_value (float)
            fourier_series_name (str)
            fourier_series_measurement_type (mastapy.units_and_measurements.MeasurementType)
        """
        harmonic_load_data_type = conversion.mp_to_pn_enum(
            harmonic_load_data_type,
            "SMT.MastaAPI.ElectricMachines.HarmonicLoadData.HarmonicLoadDataType",
        )
        speed = float(speed)
        fourier_series_amplitudes = conversion.mp_to_pn_list_float(
            fourier_series_amplitudes
        )
        fourier_series_phases = conversion.mp_to_pn_list_float(fourier_series_phases)
        fourier_series_mean_value = float(fourier_series_mean_value)
        fourier_series_name = str(fourier_series_name)
        fourier_series_measurement_type = conversion.mp_to_pn_enum(
            fourier_series_measurement_type,
            "SMT.MastaAPIUtility.UnitsAndMeasurements.MeasurementType",
        )
        pythonnet_method_call_overload(
            self.wrapped,
            "AddOrReplaceExcitationData",
            [
                _HARMONIC_LOAD_DATA_TYPE,
                _DOUBLE,
                _LIST[_DOUBLE],
                _LIST[_DOUBLE],
                _DOUBLE,
                _STRING,
                _MEASUREMENT_TYPE,
            ],
            harmonic_load_data_type,
            speed if speed else 0.0,
            fourier_series_amplitudes,
            fourier_series_phases,
            fourier_series_mean_value if fourier_series_mean_value else 0.0,
            fourier_series_name if fourier_series_name else "",
            fourier_series_measurement_type,
        )

    @enforce_parameter_types
    def add_or_replace_excitation_data(
        self: "Self",
        harmonic_load_data_type: "_1432.HarmonicLoadDataType",
        speed: "float",
        fourier_series_values: "List[float]",
        fourier_series_name: "str",
        fourier_series_measurement_type: "_7734.MeasurementType",
    ) -> None:
        """Method does not return.

        Args:
            harmonic_load_data_type (mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType)
            speed (float)
            fourier_series_values (List[float])
            fourier_series_name (str)
            fourier_series_measurement_type (mastapy.units_and_measurements.MeasurementType)
        """
        harmonic_load_data_type = conversion.mp_to_pn_enum(
            harmonic_load_data_type,
            "SMT.MastaAPI.ElectricMachines.HarmonicLoadData.HarmonicLoadDataType",
        )
        speed = float(speed)
        fourier_series_values = conversion.mp_to_pn_array_float(fourier_series_values)
        fourier_series_name = str(fourier_series_name)
        fourier_series_measurement_type = conversion.mp_to_pn_enum(
            fourier_series_measurement_type,
            "SMT.MastaAPIUtility.UnitsAndMeasurements.MeasurementType",
        )
        pythonnet_method_call_overload(
            self.wrapped,
            "AddOrReplaceExcitationData",
            [
                _HARMONIC_LOAD_DATA_TYPE,
                _DOUBLE,
                _ARRAY[_DOUBLE],
                _STRING,
                _MEASUREMENT_TYPE,
            ],
            harmonic_load_data_type,
            speed if speed else 0.0,
            fourier_series_values,
            fourier_series_name if fourier_series_name else "",
            fourier_series_measurement_type,
        )

    def clear_all_data(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ClearAllData")

    def delete(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Delete")

    def derive_rotor_forces_from_stator_loads(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "DeriveRotorForcesFromStatorLoads")

    def derive_rotor_moments_interpolators_from_stator_axial_loads_interpolators(
        self: "Self",
    ) -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped,
            "DeriveRotorMomentsInterpolatorsFromStatorAxialLoadsInterpolators",
        )

    def derive_rotor_z_force_interpolator_from_stator_axial_load_interpolators(
        self: "Self",
    ) -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped,
            "DeriveRotorZForceInterpolatorFromStatorAxialLoadInterpolators",
        )

    def derive_stator_tangential_load_interpolators_from_torque_ripple_interpolators(
        self: "Self",
    ) -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped,
            "DeriveStatorTangentialLoadInterpolatorsFromTorqueRippleInterpolators",
        )

    def derive_torque_ripple_interpolator_from_stator_tangential_load_interpolators(
        self: "Self",
    ) -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped,
            "DeriveTorqueRippleInterpolatorFromStatorTangentialLoadInterpolators",
        )

    @enforce_parameter_types
    def multiple_fourier_series_interpolator_for(
        self: "Self", harmonic_load_data_type: "_1432.HarmonicLoadDataType"
    ) -> "_1571.MultipleFourierSeriesInterpolator":
        """mastapy.math_utility.MultipleFourierSeriesInterpolator

        Args:
            harmonic_load_data_type (mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType)
        """
        harmonic_load_data_type = conversion.mp_to_pn_enum(
            harmonic_load_data_type,
            "SMT.MastaAPI.ElectricMachines.HarmonicLoadData.HarmonicLoadDataType",
        )
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "MultipleFourierSeriesInterpolatorFor",
            [_HARMONIC_LOAD_DATA_TYPE],
            harmonic_load_data_type,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def multiple_fourier_series_interpolator_for_with_fe_node(
        self: "Self",
        harmonic_load_data_type: "_1432.HarmonicLoadDataType",
        node: "_2443.FESubstructureNode",
    ) -> "_1571.MultipleFourierSeriesInterpolator":
        """mastapy.math_utility.MultipleFourierSeriesInterpolator

        Args:
            harmonic_load_data_type (mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType)
            node (mastapy.system_model.fe.FESubstructureNode)
        """
        harmonic_load_data_type = conversion.mp_to_pn_enum(
            harmonic_load_data_type,
            "SMT.MastaAPI.ElectricMachines.HarmonicLoadData.HarmonicLoadDataType",
        )
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "MultipleFourierSeriesInterpolatorFor",
            [_HARMONIC_LOAD_DATA_TYPE, _FE_SUBSTRUCTURE_NODE],
            harmonic_load_data_type,
            node.wrapped if node else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
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
    def cast_to(self: "Self") -> "_Cast_ElectricMachineDataSet":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineDataSet
        """
        return _Cast_ElectricMachineDataSet(self)
