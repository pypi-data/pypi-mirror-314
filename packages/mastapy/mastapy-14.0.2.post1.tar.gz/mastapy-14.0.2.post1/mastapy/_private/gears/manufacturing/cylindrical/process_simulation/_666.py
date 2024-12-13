"""ShapingProcessSimulation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.manufacturing.cylindrical.process_simulation import _664

_SHAPING_PROCESS_SIMULATION = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.ProcessSimulation",
    "ShapingProcessSimulation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ShapingProcessSimulation")
    CastSelf = TypeVar(
        "CastSelf", bound="ShapingProcessSimulation._Cast_ShapingProcessSimulation"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShapingProcessSimulation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShapingProcessSimulation:
    """Special nested class for casting ShapingProcessSimulation to subclasses."""

    __parent__: "ShapingProcessSimulation"

    @property
    def cutter_process_simulation(self: "CastSelf") -> "_664.CutterProcessSimulation":
        return self.__parent__._cast(_664.CutterProcessSimulation)

    @property
    def shaping_process_simulation(self: "CastSelf") -> "ShapingProcessSimulation":
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
class ShapingProcessSimulation(_664.CutterProcessSimulation):
    """ShapingProcessSimulation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAPING_PROCESS_SIMULATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def circle_blade_flank_angle_error(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CircleBladeFlankAngleError")

        if temp is None:
            return 0.0

        return temp

    @circle_blade_flank_angle_error.setter
    @enforce_parameter_types
    def circle_blade_flank_angle_error(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CircleBladeFlankAngleError",
            float(value) if value is not None else 0.0,
        )

    @property
    def circle_blade_rake_angle_error(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CircleBladeRakeAngleError")

        if temp is None:
            return 0.0

        return temp

    @circle_blade_rake_angle_error.setter
    @enforce_parameter_types
    def circle_blade_rake_angle_error(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CircleBladeRakeAngleError",
            float(value) if value is not None else 0.0,
        )

    @property
    def circumstance_feed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CircumstanceFeed")

        if temp is None:
            return 0.0

        return temp

    @circumstance_feed.setter
    @enforce_parameter_types
    def circumstance_feed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CircumstanceFeed", float(value) if value is not None else 0.0
        )

    @property
    def deviation_in_x_direction(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DeviationInXDirection")

        if temp is None:
            return 0.0

        return temp

    @deviation_in_x_direction.setter
    @enforce_parameter_types
    def deviation_in_x_direction(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DeviationInXDirection",
            float(value) if value is not None else 0.0,
        )

    @property
    def deviation_in_y_direction(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DeviationInYDirection")

        if temp is None:
            return 0.0

        return temp

    @deviation_in_y_direction.setter
    @enforce_parameter_types
    def deviation_in_y_direction(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DeviationInYDirection",
            float(value) if value is not None else 0.0,
        )

    @property
    def distance_between_two_sections(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DistanceBetweenTwoSections")

        if temp is None:
            return 0.0

        return temp

    @distance_between_two_sections.setter
    @enforce_parameter_types
    def distance_between_two_sections(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DistanceBetweenTwoSections",
            float(value) if value is not None else 0.0,
        )

    @property
    def eap_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EAPDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def face_runout(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FaceRunout")

        if temp is None:
            return 0.0

        return temp

    @face_runout.setter
    @enforce_parameter_types
    def face_runout(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FaceRunout", float(value) if value is not None else 0.0
        )

    @property
    def face_runout_check_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FaceRunoutCheckDiameter")

        if temp is None:
            return 0.0

        return temp

    @face_runout_check_diameter.setter
    @enforce_parameter_types
    def face_runout_check_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FaceRunoutCheckDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    def factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Factor")

        if temp is None:
            return 0.0

        return temp

    @factor.setter
    @enforce_parameter_types
    def factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Factor", float(value) if value is not None else 0.0
        )

    @property
    def first_phase_maximum_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FirstPhaseMaximumAngle")

        if temp is None:
            return 0.0

        return temp

    @first_phase_maximum_angle.setter
    @enforce_parameter_types
    def first_phase_maximum_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FirstPhaseMaximumAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    def first_section_runout(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FirstSectionRunout")

        if temp is None:
            return 0.0

        return temp

    @first_section_runout.setter
    @enforce_parameter_types
    def first_section_runout(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FirstSectionRunout",
            float(value) if value is not None else 0.0,
        )

    @property
    def pressure_angle_error_left_flank(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PressureAngleErrorLeftFlank")

        if temp is None:
            return 0.0

        return temp

    @pressure_angle_error_left_flank.setter
    @enforce_parameter_types
    def pressure_angle_error_left_flank(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PressureAngleErrorLeftFlank",
            float(value) if value is not None else 0.0,
        )

    @property
    def pressure_angle_error_right_flank(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PressureAngleErrorRightFlank")

        if temp is None:
            return 0.0

        return temp

    @pressure_angle_error_right_flank.setter
    @enforce_parameter_types
    def pressure_angle_error_right_flank(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PressureAngleErrorRightFlank",
            float(value) if value is not None else 0.0,
        )

    @property
    def profile_evaluation_lower_limit(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProfileEvaluationLowerLimit")

        if temp is None:
            return 0.0

        return temp

    @profile_evaluation_lower_limit.setter
    @enforce_parameter_types
    def profile_evaluation_lower_limit(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileEvaluationLowerLimit",
            float(value) if value is not None else 0.0,
        )

    @property
    def profile_evaluation_upper_limit(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProfileEvaluationUpperLimit")

        if temp is None:
            return 0.0

        return temp

    @profile_evaluation_upper_limit.setter
    @enforce_parameter_types
    def profile_evaluation_upper_limit(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileEvaluationUpperLimit",
            float(value) if value is not None else 0.0,
        )

    @property
    def second_phase_max_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SecondPhaseMaxAngle")

        if temp is None:
            return 0.0

        return temp

    @second_phase_max_angle.setter
    @enforce_parameter_types
    def second_phase_max_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SecondPhaseMaxAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    def second_section_runout(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SecondSectionRunout")

        if temp is None:
            return 0.0

        return temp

    @second_section_runout.setter
    @enforce_parameter_types
    def second_section_runout(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SecondSectionRunout",
            float(value) if value is not None else 0.0,
        )

    @property
    def shaper_cumulative_pitch_error_left_flank(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ShaperCumulativePitchErrorLeftFlank"
        )

        if temp is None:
            return 0.0

        return temp

    @shaper_cumulative_pitch_error_left_flank.setter
    @enforce_parameter_types
    def shaper_cumulative_pitch_error_left_flank(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShaperCumulativePitchErrorLeftFlank",
            float(value) if value is not None else 0.0,
        )

    @property
    def shaper_cumulative_pitch_error_right_flank(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ShaperCumulativePitchErrorRightFlank"
        )

        if temp is None:
            return 0.0

        return temp

    @shaper_cumulative_pitch_error_right_flank.setter
    @enforce_parameter_types
    def shaper_cumulative_pitch_error_right_flank(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShaperCumulativePitchErrorRightFlank",
            float(value) if value is not None else 0.0,
        )

    @property
    def shaper_radial_runout(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShaperRadialRunout")

        if temp is None:
            return 0.0

        return temp

    @shaper_radial_runout.setter
    @enforce_parameter_types
    def shaper_radial_runout(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShaperRadialRunout",
            float(value) if value is not None else 0.0,
        )

    @property
    def shaper_stoke(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShaperStoke")

        if temp is None:
            return 0.0

        return temp

    @shaper_stoke.setter
    @enforce_parameter_types
    def shaper_stoke(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ShaperStoke", float(value) if value is not None else 0.0
        )

    @property
    def shaper_tilt_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaperTiltAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def spindle_angle_at_maximum_face_runout(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpindleAngleAtMaximumFaceRunout")

        if temp is None:
            return 0.0

        return temp

    @spindle_angle_at_maximum_face_runout.setter
    @enforce_parameter_types
    def spindle_angle_at_maximum_face_runout(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpindleAngleAtMaximumFaceRunout",
            float(value) if value is not None else 0.0,
        )

    @property
    def spindle_angle_at_maximum_radial_runout(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpindleAngleAtMaximumRadialRunout")

        if temp is None:
            return 0.0

        return temp

    @spindle_angle_at_maximum_radial_runout.setter
    @enforce_parameter_types
    def spindle_angle_at_maximum_radial_runout(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpindleAngleAtMaximumRadialRunout",
            float(value) if value is not None else 0.0,
        )

    @property
    def test_distance_in_x_direction(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TestDistanceInXDirection")

        if temp is None:
            return 0.0

        return temp

    @test_distance_in_x_direction.setter
    @enforce_parameter_types
    def test_distance_in_x_direction(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TestDistanceInXDirection",
            float(value) if value is not None else 0.0,
        )

    @property
    def test_distance_in_y_direction(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TestDistanceInYDirection")

        if temp is None:
            return 0.0

        return temp

    @test_distance_in_y_direction.setter
    @enforce_parameter_types
    def test_distance_in_y_direction(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TestDistanceInYDirection",
            float(value) if value is not None else 0.0,
        )

    @property
    def use_sin_curve_for_shaper_pitch_error(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseSinCurveForShaperPitchError")

        if temp is None:
            return False

        return temp

    @use_sin_curve_for_shaper_pitch_error.setter
    @enforce_parameter_types
    def use_sin_curve_for_shaper_pitch_error(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseSinCurveForShaperPitchError",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ShapingProcessSimulation":
        """Cast to another type.

        Returns:
            _Cast_ShapingProcessSimulation
        """
        return _Cast_ShapingProcessSimulation(self)
