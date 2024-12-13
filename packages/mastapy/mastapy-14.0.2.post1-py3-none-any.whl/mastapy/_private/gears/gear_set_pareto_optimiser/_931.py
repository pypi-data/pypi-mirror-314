"""DesignSpaceSearchBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private import _0
from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_set_pareto_optimiser import _928

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_DESIGN_SPACE_SEARCH_BASE = python_net_import(
    "SMT.MastaAPI.Gears.GearSetParetoOptimiser", "DesignSpaceSearchBase"
)

if TYPE_CHECKING:
    from typing import Any, List, Type

    from mastapy._private.gears.analysis import _1257
    from mastapy._private.gears.gear_set_pareto_optimiser import (
        _929,
        _930,
        _933,
        _937,
        _938,
        _940,
        _941,
        _945,
        _948,
        _963,
        _964,
        _965,
    )
    from mastapy._private.math_utility.optimisation import _1591, _1596, _1599

    Self = TypeVar("Self", bound="DesignSpaceSearchBase")
    CastSelf = TypeVar(
        "CastSelf", bound="DesignSpaceSearchBase._Cast_DesignSpaceSearchBase"
    )

TAnalysis = TypeVar("TAnalysis", bound="_1257.AbstractGearSetAnalysis")
TCandidate = TypeVar("TCandidate")

__docformat__ = "restructuredtext en"
__all__ = ("DesignSpaceSearchBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DesignSpaceSearchBase:
    """Special nested class for casting DesignSpaceSearchBase to subclasses."""

    __parent__: "DesignSpaceSearchBase"

    @property
    def cylindrical_gear_set_pareto_optimiser(
        self: "CastSelf",
    ) -> "_930.CylindricalGearSetParetoOptimiser":
        from mastapy._private.gears.gear_set_pareto_optimiser import _930

        return self.__parent__._cast(_930.CylindricalGearSetParetoOptimiser)

    @property
    def face_gear_set_pareto_optimiser(
        self: "CastSelf",
    ) -> "_933.FaceGearSetParetoOptimiser":
        from mastapy._private.gears.gear_set_pareto_optimiser import _933

        return self.__parent__._cast(_933.FaceGearSetParetoOptimiser)

    @property
    def gear_set_pareto_optimiser(self: "CastSelf") -> "_937.GearSetParetoOptimiser":
        from mastapy._private.gears.gear_set_pareto_optimiser import _937

        return self.__parent__._cast(_937.GearSetParetoOptimiser)

    @property
    def hypoid_gear_set_pareto_optimiser(
        self: "CastSelf",
    ) -> "_938.HypoidGearSetParetoOptimiser":
        from mastapy._private.gears.gear_set_pareto_optimiser import _938

        return self.__parent__._cast(_938.HypoidGearSetParetoOptimiser)

    @property
    def micro_geometry_design_space_search(
        self: "CastSelf",
    ) -> "_941.MicroGeometryDesignSpaceSearch":
        from mastapy._private.gears.gear_set_pareto_optimiser import _941

        return self.__parent__._cast(_941.MicroGeometryDesignSpaceSearch)

    @property
    def micro_geometry_gear_set_design_space_search(
        self: "CastSelf",
    ) -> "_945.MicroGeometryGearSetDesignSpaceSearch":
        from mastapy._private.gears.gear_set_pareto_optimiser import _945

        return self.__parent__._cast(_945.MicroGeometryGearSetDesignSpaceSearch)

    @property
    def spiral_bevel_gear_set_pareto_optimiser(
        self: "CastSelf",
    ) -> "_964.SpiralBevelGearSetParetoOptimiser":
        from mastapy._private.gears.gear_set_pareto_optimiser import _964

        return self.__parent__._cast(_964.SpiralBevelGearSetParetoOptimiser)

    @property
    def straight_bevel_gear_set_pareto_optimiser(
        self: "CastSelf",
    ) -> "_965.StraightBevelGearSetParetoOptimiser":
        from mastapy._private.gears.gear_set_pareto_optimiser import _965

        return self.__parent__._cast(_965.StraightBevelGearSetParetoOptimiser)

    @property
    def design_space_search_base(self: "CastSelf") -> "DesignSpaceSearchBase":
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
class DesignSpaceSearchBase(_0.APIBase, Generic[TAnalysis, TCandidate]):
    """DesignSpaceSearchBase

    This is a mastapy class.

    Generic Types:
        TAnalysis
        TCandidate
    """

    TYPE: ClassVar["Type"] = _DESIGN_SPACE_SEARCH_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def design_space_search_strategy_database(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "DesignSpaceSearchStrategyDatabase", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @design_space_search_strategy_database.setter
    @enforce_parameter_types
    def design_space_search_strategy_database(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "DesignSpaceSearchStrategyDatabase",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    def design_space_search_strategy_database_duty_cycle(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped,
            "DesignSpaceSearchStrategyDatabaseDutyCycle",
            "SelectedItemName",
        )

        if temp is None:
            return ""

        return temp

    @design_space_search_strategy_database_duty_cycle.setter
    @enforce_parameter_types
    def design_space_search_strategy_database_duty_cycle(
        self: "Self", value: "str"
    ) -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "DesignSpaceSearchStrategyDatabaseDutyCycle",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    def display_candidates(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_CandidateDisplayChoice":
        """EnumWithSelectedValue[mastapy.gears.gear_set_pareto_optimiser.CandidateDisplayChoice]"""
        temp = pythonnet_property_get(self.wrapped, "DisplayCandidates")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_CandidateDisplayChoice.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @display_candidates.setter
    @enforce_parameter_types
    def display_candidates(self: "Self", value: "_928.CandidateDisplayChoice") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_CandidateDisplayChoice.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "DisplayCandidates", value)

    @property
    def maximum_number_of_candidates_to_display(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumNumberOfCandidatesToDisplay"
        )

        if temp is None:
            return 0

        return temp

    @maximum_number_of_candidates_to_display.setter
    @enforce_parameter_types
    def maximum_number_of_candidates_to_display(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumNumberOfCandidatesToDisplay",
            int(value) if value is not None else 0,
        )

    @property
    def number_of_candidates_after_filtering(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfCandidatesAfterFiltering")

        if temp is None:
            return 0

        return temp

    @property
    def number_of_dominant_candidates(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfDominantCandidates")

        if temp is None:
            return 0

        return temp

    @property
    def number_of_feasible_candidates(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfFeasibleCandidates")

        if temp is None:
            return 0

        return temp

    @property
    def number_of_unfiltered_candidates(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfUnfilteredCandidates")

        if temp is None:
            return 0

        return temp

    @property
    def number_of_unrateable_designs(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfUnrateableDesigns")

        if temp is None:
            return 0

        return temp

    @property
    def remove_candidates_with(self: "Self") -> "_940.LargerOrSmaller":
        """mastapy.gears.gear_set_pareto_optimiser.LargerOrSmaller"""
        temp = pythonnet_property_get(self.wrapped, "RemoveCandidatesWith")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearSetParetoOptimiser.LargerOrSmaller"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_set_pareto_optimiser._940", "LargerOrSmaller"
        )(value)

    @remove_candidates_with.setter
    @enforce_parameter_types
    def remove_candidates_with(self: "Self", value: "_940.LargerOrSmaller") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.GearSetParetoOptimiser.LargerOrSmaller"
        )
        pythonnet_property_set(self.wrapped, "RemoveCandidatesWith", value)

    @property
    def reporting_string_for_too_many_candidates_to_be_evaluated(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ReportingStringForTooManyCandidatesToBeEvaluated"
        )

        if temp is None:
            return ""

        return temp

    @property
    def selected_points(self: "Self") -> "List[int]":
        """List[int]"""
        temp = pythonnet_property_get(self.wrapped, "SelectedPoints")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, int)

        if value is None:
            return None

        return value

    @selected_points.setter
    @enforce_parameter_types
    def selected_points(self: "Self", value: "List[int]") -> None:
        value = conversion.mp_to_pn_objects_in_list(value)
        pythonnet_property_set(self.wrapped, "SelectedPoints", value)

    @property
    def total_number_of_candidates_to_be_evaluated(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalNumberOfCandidatesToBeEvaluated"
        )

        if temp is None:
            return 0

        return temp

    @property
    def viewing_candidates_selected_in_chart(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ViewingCandidatesSelectedInChart")

        if temp is None:
            return False

        return temp

    @property
    def load_case_duty_cycle(self: "Self") -> "TAnalysis":
        """TAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCaseDutyCycle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def selected_candidate(self: "Self") -> "TAnalysis":
        """TAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SelectedCandidate")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def selected_design_space_search_strategy(
        self: "Self",
    ) -> "_1599.ParetoOptimisationStrategy":
        """mastapy.math_utility.optimisation.ParetoOptimisationStrategy

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SelectedDesignSpaceSearchStrategy")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def all_candidate_designs_including_original_design(
        self: "Self",
    ) -> "List[TCandidate]":
        """List[TCandidate]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AllCandidateDesignsIncludingOriginalDesign"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def all_candidate_designs_to_display(self: "Self") -> "List[TCandidate]":
        """List[TCandidate]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllCandidateDesignsToDisplay")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def all_candidate_designs_to_display_without_original_design(
        self: "Self",
    ) -> "List[TCandidate]":
        """List[TCandidate]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AllCandidateDesignsToDisplayWithoutOriginalDesign"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def candidate_designs_to_display(self: "Self") -> "List[TCandidate]":
        """List[TCandidate]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CandidateDesignsToDisplay")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def chart_details(
        self: "Self",
    ) -> "List[_929.ChartInfoBase[TAnalysis, TCandidate]]":
        """List[mastapy.gears.gear_set_pareto_optimiser.ChartInfoBase[TAnalysis, TCandidate]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ChartDetails")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def filters(self: "Self") -> "List[_1596.ParetoOptimisationFilter]":
        """List[mastapy.math_utility.optimisation.ParetoOptimisationFilter]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Filters")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def input_setters(self: "Self") -> "List[_1591.InputSetter[TAnalysis]]":
        """List[mastapy.math_utility.optimisation.InputSetter[TAnalysis]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InputSetters")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def optimisation_targets(
        self: "Self",
    ) -> "List[_948.OptimisationTarget[TAnalysis]]":
        """List[mastapy.gears.gear_set_pareto_optimiser.OptimisationTarget[TAnalysis]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OptimisationTargets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def reasons_for_invalid_candidates(
        self: "Self",
    ) -> "List[_963.ReasonsForInvalidDesigns]":
        """List[mastapy.gears.gear_set_pareto_optimiser.ReasonsForInvalidDesigns]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReasonsForInvalidCandidates")

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

    def add_table_filter(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddTableFilter")

    def find_dominant_candidates(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "FindDominantCandidates")

    def load_strategy(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "LoadStrategy")

    def save_results(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SaveResults")

    def save_strategy(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SaveStrategy")

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
    def cast_to(self: "Self") -> "_Cast_DesignSpaceSearchBase":
        """Cast to another type.

        Returns:
            _Cast_DesignSpaceSearchBase
        """
        return _Cast_DesignSpaceSearchBase(self)
