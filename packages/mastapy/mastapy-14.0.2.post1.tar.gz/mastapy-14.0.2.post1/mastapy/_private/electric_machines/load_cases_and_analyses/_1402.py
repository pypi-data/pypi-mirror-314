"""ElectricMachineAnalysis"""

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
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ELECTRIC_MACHINE_ANALYSIS = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses", "ElectricMachineAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private import _7733
    from mastapy._private.electric_machines import _1304, _1310
    from mastapy._private.electric_machines.load_cases_and_analyses import (
        _1397,
        _1400,
        _1406,
        _1407,
        _1409,
        _1420,
        _1424,
    )

    Self = TypeVar("Self", bound="ElectricMachineAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="ElectricMachineAnalysis._Cast_ElectricMachineAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineAnalysis:
    """Special nested class for casting ElectricMachineAnalysis to subclasses."""

    __parent__: "ElectricMachineAnalysis"

    @property
    def dynamic_force_analysis(self: "CastSelf") -> "_1397.DynamicForceAnalysis":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1397

        return self.__parent__._cast(_1397.DynamicForceAnalysis)

    @property
    def efficiency_map_analysis(self: "CastSelf") -> "_1400.EfficiencyMapAnalysis":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1400

        return self.__parent__._cast(_1400.EfficiencyMapAnalysis)

    @property
    def electric_machine_fe_analysis(
        self: "CastSelf",
    ) -> "_1406.ElectricMachineFEAnalysis":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1406

        return self.__parent__._cast(_1406.ElectricMachineFEAnalysis)

    @property
    def electric_machine_fe_mechanical_analysis(
        self: "CastSelf",
    ) -> "_1407.ElectricMachineFEMechanicalAnalysis":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1407

        return self.__parent__._cast(_1407.ElectricMachineFEMechanicalAnalysis)

    @property
    def single_operating_point_analysis(
        self: "CastSelf",
    ) -> "_1420.SingleOperatingPointAnalysis":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1420

        return self.__parent__._cast(_1420.SingleOperatingPointAnalysis)

    @property
    def speed_torque_curve_analysis(
        self: "CastSelf",
    ) -> "_1424.SpeedTorqueCurveAnalysis":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1424

        return self.__parent__._cast(_1424.SpeedTorqueCurveAnalysis)

    @property
    def electric_machine_analysis(self: "CastSelf") -> "ElectricMachineAnalysis":
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
class ElectricMachineAnalysis(_0.APIBase):
    """ElectricMachineAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def analysis_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AnalysisTime")

        if temp is None:
            return 0.0

        return temp

    @property
    def magnet_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MagnetTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    def windings_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WindingsTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    def electric_machine_detail(self: "Self") -> "_1304.ElectricMachineDetail":
        """mastapy.electric_machines.ElectricMachineDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElectricMachineDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def load_case(self: "Self") -> "_1409.ElectricMachineLoadCaseBase":
        """mastapy.electric_machines.load_cases_and_analyses.ElectricMachineLoadCaseBase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def setup(self: "Self") -> "_1310.ElectricMachineSetup":
        """mastapy.electric_machines.ElectricMachineSetup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Setup")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def results_ready(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsReady")

        if temp is None:
            return False

        return temp

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

    def perform_analysis(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "PerformAnalysis")

    @enforce_parameter_types
    def perform_analysis_with_progress(
        self: "Self", token: "_7733.TaskProgress"
    ) -> None:
        """Method does not return.

        Args:
            token (mastapy.TaskProgress)
        """
        pythonnet_method_call(
            self.wrapped,
            "PerformAnalysisWithProgress",
            token.wrapped if token else None,
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
    def cast_to(self: "Self") -> "_Cast_ElectricMachineAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineAnalysis
        """
        return _Cast_ElectricMachineAnalysis(self)
