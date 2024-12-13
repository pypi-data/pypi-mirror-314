"""SystemOptimiserDetails"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_SYSTEM_OPTIMISER_DETAILS = python_net_import(
    "SMT.MastaAPI.SystemModel.Optimization.SystemOptimiser", "SystemOptimiserDetails"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.system_model.analyses_and_results.load_case_groups import (
        _5805,
        _5806,
    )
    from mastapy._private.system_model.optimization.system_optimiser import _2294, _2295

    Self = TypeVar("Self", bound="SystemOptimiserDetails")
    CastSelf = TypeVar(
        "CastSelf", bound="SystemOptimiserDetails._Cast_SystemOptimiserDetails"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SystemOptimiserDetails",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SystemOptimiserDetails:
    """Special nested class for casting SystemOptimiserDetails to subclasses."""

    __parent__: "SystemOptimiserDetails"

    @property
    def system_optimiser_details(self: "CastSelf") -> "SystemOptimiserDetails":
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
class SystemOptimiserDetails(_0.APIBase):
    """SystemOptimiserDetails

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SYSTEM_OPTIMISER_DETAILS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def avoid_specific_orders(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "AvoidSpecificOrders")

        if temp is None:
            return False

        return temp

    @avoid_specific_orders.setter
    @enforce_parameter_types
    def avoid_specific_orders(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AvoidSpecificOrders",
            bool(value) if value is not None else False,
        )

    @property
    def check_passing_order_separation(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CheckPassingOrderSeparation")

        if temp is None:
            return False

        return temp

    @check_passing_order_separation.setter
    @enforce_parameter_types
    def check_passing_order_separation(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CheckPassingOrderSeparation",
            bool(value) if value is not None else False,
        )

    @property
    def criteria_for_selecting_configurations_to_keep(
        self: "Self",
    ) -> "_5806.SystemOptimiserTargets":
        """mastapy.system_model.analyses_and_results.load_case_groups.SystemOptimiserTargets"""
        temp = pythonnet_property_get(
            self.wrapped, "CriteriaForSelectingConfigurationsToKeep"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups.SystemOptimiserTargets",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.load_case_groups._5806",
            "SystemOptimiserTargets",
        )(value)

    @criteria_for_selecting_configurations_to_keep.setter
    @enforce_parameter_types
    def criteria_for_selecting_configurations_to_keep(
        self: "Self", value: "_5806.SystemOptimiserTargets"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups.SystemOptimiserTargets",
        )
        pythonnet_property_set(
            self.wrapped, "CriteriaForSelectingConfigurationsToKeep", value
        )

    @property
    def filter_designs_on_estimated_maximum_achievable_transverse_contact_ratio(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "FilterDesignsOnEstimatedMaximumAchievableTransverseContactRatio",
        )

        if temp is None:
            return False

        return temp

    @filter_designs_on_estimated_maximum_achievable_transverse_contact_ratio.setter
    @enforce_parameter_types
    def filter_designs_on_estimated_maximum_achievable_transverse_contact_ratio(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "FilterDesignsOnEstimatedMaximumAchievableTransverseContactRatio",
            bool(value) if value is not None else False,
        )

    @property
    def gear_set_optimisation(
        self: "Self",
    ) -> "_5805.SystemOptimiserGearSetOptimisation":
        """mastapy.system_model.analyses_and_results.load_case_groups.SystemOptimiserGearSetOptimisation"""
        temp = pythonnet_property_get(self.wrapped, "GearSetOptimisation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups.SystemOptimiserGearSetOptimisation",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.load_case_groups._5805",
            "SystemOptimiserGearSetOptimisation",
        )(value)

    @gear_set_optimisation.setter
    @enforce_parameter_types
    def gear_set_optimisation(
        self: "Self", value: "_5805.SystemOptimiserGearSetOptimisation"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups.SystemOptimiserGearSetOptimisation",
        )
        pythonnet_property_set(self.wrapped, "GearSetOptimisation", value)

    @property
    def maximum_number_of_configurations_to_create(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumNumberOfConfigurationsToCreate"
        )

        if temp is None:
            return 0

        return temp

    @maximum_number_of_configurations_to_create.setter
    @enforce_parameter_types
    def maximum_number_of_configurations_to_create(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumNumberOfConfigurationsToCreate",
            int(value) if value is not None else 0,
        )

    @property
    def maximum_number_of_solutions(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "MaximumNumberOfSolutions")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @maximum_number_of_solutions.setter
    @enforce_parameter_types
    def maximum_number_of_solutions(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaximumNumberOfSolutions", value)

    @property
    def minimum_number_of_solutions(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "MinimumNumberOfSolutions")

        if temp is None:
            return 0

        return temp

    @minimum_number_of_solutions.setter
    @enforce_parameter_types
    def minimum_number_of_solutions(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumNumberOfSolutions",
            int(value) if value is not None else 0,
        )

    @property
    def modify_face_widths(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ModifyFaceWidths")

        if temp is None:
            return False

        return temp

    @modify_face_widths.setter
    @enforce_parameter_types
    def modify_face_widths(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ModifyFaceWidths",
            bool(value) if value is not None else False,
        )

    @property
    def number_of_orders_to_avoid(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfOrdersToAvoid")

        if temp is None:
            return 0

        return temp

    @number_of_orders_to_avoid.setter
    @enforce_parameter_types
    def number_of_orders_to_avoid(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfOrdersToAvoid",
            int(value) if value is not None else 0,
        )

    @property
    def number_of_harmonics_for_passing_order_separation_test(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfHarmonicsForPassingOrderSeparationTest"
        )

        if temp is None:
            return 0

        return temp

    @number_of_harmonics_for_passing_order_separation_test.setter
    @enforce_parameter_types
    def number_of_harmonics_for_passing_order_separation_test(
        self: "Self", value: "int"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfHarmonicsForPassingOrderSeparationTest",
            int(value) if value is not None else 0,
        )

    @property
    def number_of_solutions(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfSolutions")

        if temp is None:
            return 0

        return temp

    @property
    def required_normalised_safety_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RequiredNormalisedSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @required_normalised_safety_factor.setter
    @enforce_parameter_types
    def required_normalised_safety_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RequiredNormalisedSafetyFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def required_passing_order_separation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RequiredPassingOrderSeparation")

        if temp is None:
            return 0.0

        return temp

    @required_passing_order_separation.setter
    @enforce_parameter_types
    def required_passing_order_separation(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RequiredPassingOrderSeparation",
            float(value) if value is not None else 0.0,
        )

    @property
    def show_ratio_as_speed_increasing(self: "Self") -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(self.wrapped, "ShowRatioAsSpeedIncreasing")

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @show_ratio_as_speed_increasing.setter
    @enforce_parameter_types
    def show_ratio_as_speed_increasing(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ShowRatioAsSpeedIncreasing", value)

    @property
    def target_maximum_absolute_cylindrical_gear_profile_shift_coefficient(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "TargetMaximumAbsoluteCylindricalGearProfileShiftCoefficient"
        )

        if temp is None:
            return 0.0

        return temp

    @target_maximum_absolute_cylindrical_gear_profile_shift_coefficient.setter
    @enforce_parameter_types
    def target_maximum_absolute_cylindrical_gear_profile_shift_coefficient(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "TargetMaximumAbsoluteCylindricalGearProfileShiftCoefficient",
            float(value) if value is not None else 0.0,
        )

    @property
    def tolerance_for_combining_duty_cycles(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ToleranceForCombiningDutyCycles")

        if temp is None:
            return 0.0

        return temp

    @tolerance_for_combining_duty_cycles.setter
    @enforce_parameter_types
    def tolerance_for_combining_duty_cycles(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ToleranceForCombiningDutyCycles",
            float(value) if value is not None else 0.0,
        )

    @property
    def planet_gear_options(self: "Self") -> "List[_2295.PlanetGearOptions]":
        """List[mastapy.system_model.optimization.system_optimiser.PlanetGearOptions]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlanetGearOptions")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def target_ratios(self: "Self") -> "List[_2294.DesignStateTargetRatio]":
        """List[mastapy.system_model.optimization.system_optimiser.DesignStateTargetRatio]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TargetRatios")

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

    def create_designs(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CreateDesigns")

    def determine_ratio_tolerances(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "DetermineRatioTolerances")

    def find_solutions_from_current_ratio_tolerances(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "FindSolutionsFromCurrentRatioTolerances")

    def perform_system_optimisation(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "PerformSystemOptimisation")

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
    def cast_to(self: "Self") -> "_Cast_SystemOptimiserDetails":
        """Cast to another type.

        Returns:
            _Cast_SystemOptimiserDetails
        """
        return _Cast_SystemOptimiserDetails(self)
