"""ElectricMachineHarmonicLoadDataBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import (
    enum_with_selected_value,
    list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines import _1342
from mastapy._private.electric_machines.harmonic_load_data import _1429, _1432, _1433

_ELECTRIC_MACHINE_HARMONIC_LOAD_DATA_BASE = python_net_import(
    "SMT.MastaAPI.ElectricMachines.HarmonicLoadData",
    "ElectricMachineHarmonicLoadDataBase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines.harmonic_load_data import (
        _1430,
        _1435,
        _1436,
    )
    from mastapy._private.electric_machines.results import _1371
    from mastapy._private.math_utility import _1571
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7024,
        _7025,
        _7026,
        _7027,
        _7028,
        _7029,
        _7030,
    )
    from mastapy._private.utility_gui.charts import _1917, _1921

    Self = TypeVar("Self", bound="ElectricMachineHarmonicLoadDataBase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineHarmonicLoadDataBase._Cast_ElectricMachineHarmonicLoadDataBase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineHarmonicLoadDataBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineHarmonicLoadDataBase:
    """Special nested class for casting ElectricMachineHarmonicLoadDataBase to subclasses."""

    __parent__: "ElectricMachineHarmonicLoadDataBase"

    @property
    def speed_dependent_harmonic_load_data(
        self: "CastSelf",
    ) -> "_1433.SpeedDependentHarmonicLoadData":
        return self.__parent__._cast(_1433.SpeedDependentHarmonicLoadData)

    @property
    def harmonic_load_data_base(self: "CastSelf") -> "_1430.HarmonicLoadDataBase":
        from mastapy._private.electric_machines.harmonic_load_data import _1430

        return self.__parent__._cast(_1430.HarmonicLoadDataBase)

    @property
    def dynamic_force_results(self: "CastSelf") -> "_1371.DynamicForceResults":
        from mastapy._private.electric_machines.results import _1371

        return self.__parent__._cast(_1371.DynamicForceResults)

    @property
    def electric_machine_harmonic_load_data(
        self: "CastSelf",
    ) -> "_7024.ElectricMachineHarmonicLoadData":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7024,
        )

        return self.__parent__._cast(_7024.ElectricMachineHarmonicLoadData)

    @property
    def electric_machine_harmonic_load_data_from_excel(
        self: "CastSelf",
    ) -> "_7025.ElectricMachineHarmonicLoadDataFromExcel":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7025,
        )

        return self.__parent__._cast(_7025.ElectricMachineHarmonicLoadDataFromExcel)

    @property
    def electric_machine_harmonic_load_data_from_flux(
        self: "CastSelf",
    ) -> "_7026.ElectricMachineHarmonicLoadDataFromFlux":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7026,
        )

        return self.__parent__._cast(_7026.ElectricMachineHarmonicLoadDataFromFlux)

    @property
    def electric_machine_harmonic_load_data_from_jmag(
        self: "CastSelf",
    ) -> "_7027.ElectricMachineHarmonicLoadDataFromJMAG":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7027,
        )

        return self.__parent__._cast(_7027.ElectricMachineHarmonicLoadDataFromJMAG)

    @property
    def electric_machine_harmonic_load_data_from_masta(
        self: "CastSelf",
    ) -> "_7028.ElectricMachineHarmonicLoadDataFromMASTA":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7028,
        )

        return self.__parent__._cast(_7028.ElectricMachineHarmonicLoadDataFromMASTA)

    @property
    def electric_machine_harmonic_load_data_from_motor_cad(
        self: "CastSelf",
    ) -> "_7029.ElectricMachineHarmonicLoadDataFromMotorCAD":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7029,
        )

        return self.__parent__._cast(_7029.ElectricMachineHarmonicLoadDataFromMotorCAD)

    @property
    def electric_machine_harmonic_load_data_from_motor_packages(
        self: "CastSelf",
    ) -> "_7030.ElectricMachineHarmonicLoadDataFromMotorPackages":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7030,
        )

        return self.__parent__._cast(
            _7030.ElectricMachineHarmonicLoadDataFromMotorPackages
        )

    @property
    def electric_machine_harmonic_load_data_base(
        self: "CastSelf",
    ) -> "ElectricMachineHarmonicLoadDataBase":
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
class ElectricMachineHarmonicLoadDataBase(_1433.SpeedDependentHarmonicLoadData):
    """ElectricMachineHarmonicLoadDataBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_HARMONIC_LOAD_DATA_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def compare_torque_ripple_and_stator_torque_reaction_derived_from_stator_tangential_loads(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "CompareTorqueRippleAndStatorTorqueReactionDerivedFromStatorTangentialLoads",
        )

        if temp is None:
            return False

        return temp

    @compare_torque_ripple_and_stator_torque_reaction_derived_from_stator_tangential_loads.setter
    @enforce_parameter_types
    def compare_torque_ripple_and_stator_torque_reaction_derived_from_stator_tangential_loads(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "CompareTorqueRippleAndStatorTorqueReactionDerivedFromStatorTangentialLoads",
            bool(value) if value is not None else False,
        )

    @property
    def data_type_for_force_moment_distribution_and_temporal_spatial_harmonics_charts(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType":
        """EnumWithSelectedValue[mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType]"""
        temp = pythonnet_property_get(
            self.wrapped,
            "DataTypeForForceMomentDistributionAndTemporalSpatialHarmonicsCharts",
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @data_type_for_force_moment_distribution_and_temporal_spatial_harmonics_charts.setter
    @enforce_parameter_types
    def data_type_for_force_moment_distribution_and_temporal_spatial_harmonics_charts(
        self: "Self", value: "_1432.HarmonicLoadDataType"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped,
            "DataTypeForForceMomentDistributionAndTemporalSpatialHarmonicsCharts",
            value,
        )

    @property
    def display_interpolated_data(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "DisplayInterpolatedData")

        if temp is None:
            return False

        return temp

    @display_interpolated_data.setter
    @enforce_parameter_types
    def display_interpolated_data(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DisplayInterpolatedData",
            bool(value) if value is not None else False,
        )

    @property
    def display_option_for_slice_data(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ForceDisplayOption":
        """EnumWithSelectedValue[mastapy.electric_machines.harmonic_load_data.ForceDisplayOption]"""
        temp = pythonnet_property_get(self.wrapped, "DisplayOptionForSliceData")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ForceDisplayOption.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @display_option_for_slice_data.setter
    @enforce_parameter_types
    def display_option_for_slice_data(
        self: "Self", value: "_1429.ForceDisplayOption"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ForceDisplayOption.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "DisplayOptionForSliceData", value)

    @property
    def force_distribution_3d(self: "Self") -> "_1921.ThreeDVectorChartDefinition":
        """mastapy.utility_gui.charts.ThreeDVectorChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceDistribution3D")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def force_moment_distribution(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceMomentDistribution")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def invert_axis(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "InvertAxis")

        if temp is None:
            return False

        return temp

    @invert_axis.setter
    @enforce_parameter_types
    def invert_axis(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "InvertAxis", bool(value) if value is not None else False
        )

    @property
    def plot_as_vectors(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "PlotAsVectors")

        if temp is None:
            return False

        return temp

    @plot_as_vectors.setter
    @enforce_parameter_types
    def plot_as_vectors(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "PlotAsVectors", bool(value) if value is not None else False
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
    def show_all_forces(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowAllForces")

        if temp is None:
            return False

        return temp

    @show_all_forces.setter
    @enforce_parameter_types
    def show_all_forces(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowAllForces", bool(value) if value is not None else False
        )

    @property
    def show_all_teeth(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowAllTeeth")

        if temp is None:
            return False

        return temp

    @show_all_teeth.setter
    @enforce_parameter_types
    def show_all_teeth(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowAllTeeth", bool(value) if value is not None else False
        )

    @property
    def slice(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_RotorSkewSlice":
        """ListWithSelectedItem[mastapy.electric_machines.RotorSkewSlice]"""
        temp = pythonnet_property_get(self.wrapped, "Slice")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_RotorSkewSlice",
        )(temp)

    @slice.setter
    @enforce_parameter_types
    def slice(self: "Self", value: "_1342.RotorSkewSlice") -> None:
        wrapper_type = (
            list_with_selected_item.ListWithSelectedItem_RotorSkewSlice.wrapper_type()
        )
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_RotorSkewSlice.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "Slice", value)

    @property
    def speed_to_view(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpeedToView")

        if temp is None:
            return 0.0

        return temp

    @speed_to_view.setter
    @enforce_parameter_types
    def speed_to_view(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SpeedToView", float(value) if value is not None else 0.0
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
    def sum_over_all_nodes(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SumOverAllNodes")

        if temp is None:
            return False

        return temp

    @sum_over_all_nodes.setter
    @enforce_parameter_types
    def sum_over_all_nodes(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "SumOverAllNodes", bool(value) if value is not None else False
        )

    @property
    def temporal_spatial_harmonics_chart(
        self: "Self",
    ) -> "_1917.ScatterChartDefinition":
        """mastapy.utility_gui.charts.ScatterChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TemporalSpatialHarmonicsChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

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
    def use_log_scale_for_temporal_spatial_harmonics_chart(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseLogScaleForTemporalSpatialHarmonicsChart"
        )

        if temp is None:
            return False

        return temp

    @use_log_scale_for_temporal_spatial_harmonics_chart.setter
    @enforce_parameter_types
    def use_log_scale_for_temporal_spatial_harmonics_chart(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseLogScaleForTemporalSpatialHarmonicsChart",
            bool(value) if value is not None else False,
        )

    @property
    def rotor_x_force(self: "Self") -> "_1571.MultipleFourierSeriesInterpolator":
        """mastapy.math_utility.MultipleFourierSeriesInterpolator

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RotorXForce")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def rotor_y_force(self: "Self") -> "_1571.MultipleFourierSeriesInterpolator":
        """mastapy.math_utility.MultipleFourierSeriesInterpolator

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RotorYForce")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def stator_axial_loads(self: "Self") -> "_1435.StatorToothLoadInterpolator":
        """mastapy.electric_machines.harmonic_load_data.StatorToothLoadInterpolator

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StatorAxialLoads")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def stator_radial_loads(self: "Self") -> "_1435.StatorToothLoadInterpolator":
        """mastapy.electric_machines.harmonic_load_data.StatorToothLoadInterpolator

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StatorRadialLoads")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def stator_tangential_loads(self: "Self") -> "_1435.StatorToothLoadInterpolator":
        """mastapy.electric_machines.harmonic_load_data.StatorToothLoadInterpolator

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StatorTangentialLoads")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def stator_tooth_moments(self: "Self") -> "_1436.StatorToothMomentInterpolator":
        """mastapy.electric_machines.harmonic_load_data.StatorToothMomentInterpolator

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StatorToothMoments")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @enforce_parameter_types
    def multiple_fourier_series_interpolator_for(
        self: "Self",
        harmonic_load_data_type: "_1432.HarmonicLoadDataType",
        slice_index: "int",
    ) -> "_1571.MultipleFourierSeriesInterpolator":
        """mastapy.math_utility.MultipleFourierSeriesInterpolator

        Args:
            harmonic_load_data_type (mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType)
            slice_index (int)
        """
        harmonic_load_data_type = conversion.mp_to_pn_enum(
            harmonic_load_data_type,
            "SMT.MastaAPI.ElectricMachines.HarmonicLoadData.HarmonicLoadDataType",
        )
        slice_index = int(slice_index)
        method_result = pythonnet_method_call(
            self.wrapped,
            "MultipleFourierSeriesInterpolatorFor",
            harmonic_load_data_type,
            slice_index if slice_index else 0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def stator_tooth_load_interpolator_for(
        self: "Self",
        harmonic_load_data_type: "_1432.HarmonicLoadDataType",
        slice_index: "int",
    ) -> "_1435.StatorToothLoadInterpolator":
        """mastapy.electric_machines.harmonic_load_data.StatorToothLoadInterpolator

        Args:
            harmonic_load_data_type (mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType)
            slice_index (int)
        """
        harmonic_load_data_type = conversion.mp_to_pn_enum(
            harmonic_load_data_type,
            "SMT.MastaAPI.ElectricMachines.HarmonicLoadData.HarmonicLoadDataType",
        )
        slice_index = int(slice_index)
        method_result = pythonnet_method_call(
            self.wrapped,
            "StatorToothLoadInterpolatorFor",
            harmonic_load_data_type,
            slice_index if slice_index else 0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def stator_tooth_moment_interpolator_for(
        self: "Self",
        harmonic_load_data_type: "_1432.HarmonicLoadDataType",
        slice_index: "int",
    ) -> "_1436.StatorToothMomentInterpolator":
        """mastapy.electric_machines.harmonic_load_data.StatorToothMomentInterpolator

        Args:
            harmonic_load_data_type (mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType)
            slice_index (int)
        """
        harmonic_load_data_type = conversion.mp_to_pn_enum(
            harmonic_load_data_type,
            "SMT.MastaAPI.ElectricMachines.HarmonicLoadData.HarmonicLoadDataType",
        )
        slice_index = int(slice_index)
        method_result = pythonnet_method_call(
            self.wrapped,
            "StatorToothMomentInterpolatorFor",
            harmonic_load_data_type,
            slice_index if slice_index else 0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ElectricMachineHarmonicLoadDataBase":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineHarmonicLoadDataBase
        """
        return _Cast_ElectricMachineHarmonicLoadDataBase(self)
