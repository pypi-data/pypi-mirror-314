"""CylindricalGearSetRatingOptimisationHelper"""

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
from mastapy._private.gears.rating.cylindrical.optimisation import _518, _519, _520

_CYLINDRICAL_GEAR_SET_RATING_OPTIMISATION_HELPER = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.Optimisation",
    "CylindricalGearSetRatingOptimisationHelper",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating.cylindrical.optimisation import _515, _516

    Self = TypeVar("Self", bound="CylindricalGearSetRatingOptimisationHelper")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearSetRatingOptimisationHelper._Cast_CylindricalGearSetRatingOptimisationHelper",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearSetRatingOptimisationHelper",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearSetRatingOptimisationHelper:
    """Special nested class for casting CylindricalGearSetRatingOptimisationHelper to subclasses."""

    __parent__: "CylindricalGearSetRatingOptimisationHelper"

    @property
    def cylindrical_gear_set_rating_optimisation_helper(
        self: "CastSelf",
    ) -> "CylindricalGearSetRatingOptimisationHelper":
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
class CylindricalGearSetRatingOptimisationHelper(_0.APIBase):
    """CylindricalGearSetRatingOptimisationHelper

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SET_RATING_OPTIMISATION_HELPER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def helix_angle_optimisation_results(
        self: "Self",
    ) -> "_515.OptimisationResultsPair[_518.SafetyFactorOptimisationStepResultAngle]":
        """mastapy.gears.rating.cylindrical.optimisation.OptimisationResultsPair[mastapy.gears.rating.cylindrical.optimisation.SafetyFactorOptimisationStepResultAngle]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HelixAngleOptimisationResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _518.SafetyFactorOptimisationStepResultAngle
        ](temp)

    @property
    def maximum_transverse_contact_ratio_optimisation_results(
        self: "Self",
    ) -> "_515.OptimisationResultsPair[_519.SafetyFactorOptimisationStepResultNumber]":
        """mastapy.gears.rating.cylindrical.optimisation.OptimisationResultsPair[mastapy.gears.rating.cylindrical.optimisation.SafetyFactorOptimisationStepResultNumber]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumTransverseContactRatioOptimisationResults"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _519.SafetyFactorOptimisationStepResultNumber
        ](temp)

    @property
    def normal_module_optimisation_results(
        self: "Self",
    ) -> "_515.OptimisationResultsPair[_520.SafetyFactorOptimisationStepResultShortLength]":
        """mastapy.gears.rating.cylindrical.optimisation.OptimisationResultsPair[mastapy.gears.rating.cylindrical.optimisation.SafetyFactorOptimisationStepResultShortLength]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalModuleOptimisationResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _520.SafetyFactorOptimisationStepResultShortLength
        ](temp)

    @property
    def pressure_angle_optimisation_results(
        self: "Self",
    ) -> "_515.OptimisationResultsPair[_518.SafetyFactorOptimisationStepResultAngle]":
        """mastapy.gears.rating.cylindrical.optimisation.OptimisationResultsPair[mastapy.gears.rating.cylindrical.optimisation.SafetyFactorOptimisationStepResultAngle]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PressureAngleOptimisationResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _518.SafetyFactorOptimisationStepResultAngle
        ](temp)

    @property
    def profile_shift_coefficient_optimisation_results(
        self: "Self",
    ) -> "_515.OptimisationResultsPair[_519.SafetyFactorOptimisationStepResultNumber]":
        """mastapy.gears.rating.cylindrical.optimisation.OptimisationResultsPair[mastapy.gears.rating.cylindrical.optimisation.SafetyFactorOptimisationStepResultNumber]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ProfileShiftCoefficientOptimisationResults"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _519.SafetyFactorOptimisationStepResultNumber
        ](temp)

    @property
    def all_helix_angle_optimisation_results(
        self: "Self",
    ) -> "List[_516.SafetyFactorOptimisationResults[_518.SafetyFactorOptimisationStepResultAngle]]":
        """List[mastapy.gears.rating.cylindrical.optimisation.SafetyFactorOptimisationResults[mastapy.gears.rating.cylindrical.optimisation.SafetyFactorOptimisationStepResultAngle]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllHelixAngleOptimisationResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def all_normal_module_optimisation_results(
        self: "Self",
    ) -> "List[_516.SafetyFactorOptimisationResults[_520.SafetyFactorOptimisationStepResultShortLength]]":
        """List[mastapy.gears.rating.cylindrical.optimisation.SafetyFactorOptimisationResults[mastapy.gears.rating.cylindrical.optimisation.SafetyFactorOptimisationStepResultShortLength]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AllNormalModuleOptimisationResults"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def all_normal_pressure_angle_optimisation_results(
        self: "Self",
    ) -> "List[_516.SafetyFactorOptimisationResults[_518.SafetyFactorOptimisationStepResultAngle]]":
        """List[mastapy.gears.rating.cylindrical.optimisation.SafetyFactorOptimisationResults[mastapy.gears.rating.cylindrical.optimisation.SafetyFactorOptimisationStepResultAngle]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AllNormalPressureAngleOptimisationResults"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def all_profile_shift_optimisation_results(
        self: "Self",
    ) -> "List[_516.SafetyFactorOptimisationResults[_519.SafetyFactorOptimisationStepResultNumber]]":
        """List[mastapy.gears.rating.cylindrical.optimisation.SafetyFactorOptimisationResults[mastapy.gears.rating.cylindrical.optimisation.SafetyFactorOptimisationStepResultNumber]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AllProfileShiftOptimisationResults"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def helix_angle_and_normal_pressure_angle_optimisation_results(
        self: "Self",
    ) -> "List[_516.SafetyFactorOptimisationResults[_518.SafetyFactorOptimisationStepResultAngle]]":
        """List[mastapy.gears.rating.cylindrical.optimisation.SafetyFactorOptimisationResults[mastapy.gears.rating.cylindrical.optimisation.SafetyFactorOptimisationStepResultAngle]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HelixAngleAndNormalPressureAngleOptimisationResults"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def results_transverse_contact_ratio_results(
        self: "Self",
    ) -> "List[_516.SafetyFactorOptimisationResults[_519.SafetyFactorOptimisationStepResultNumber]]":
        """List[mastapy.gears.rating.cylindrical.optimisation.SafetyFactorOptimisationResults[mastapy.gears.rating.cylindrical.optimisation.SafetyFactorOptimisationStepResultNumber]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ResultsTransverseContactRatioResults"
        )

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

    def calculate_optimisation_charts(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CalculateOptimisationCharts")

    def create_optimisation_report(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CreateOptimisationReport")

    def set_face_widths_for_required_safety_factor(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SetFaceWidthsForRequiredSafetyFactor")

    def set_helix_angle_for_maximum_safety_factor(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SetHelixAngleForMaximumSafetyFactor")

    def set_normal_module_for_maximum_safety_factor(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SetNormalModuleForMaximumSafetyFactor")

    def set_pressure_angle_for_maximum_safety_factor(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SetPressureAngleForMaximumSafetyFactor")

    def set_profile_shift_coefficient_for_maximum_safety_factor(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "SetProfileShiftCoefficientForMaximumSafetyFactor"
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
    def cast_to(self: "Self") -> "_Cast_CylindricalGearSetRatingOptimisationHelper":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearSetRatingOptimisationHelper
        """
        return _Cast_CylindricalGearSetRatingOptimisationHelper(self)
