"""BevelGearSetDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import enum_with_selected_value, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.agma_gleason_conical import _1235
from mastapy._private.gears.gear_designs.bevel import _1230

_BEVEL_GEAR_SET_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Bevel", "BevelGearSetDesign"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.gears import _359
    from mastapy._private.gears.gear_designs import _974, _976
    from mastapy._private.gears.gear_designs.bevel import _1229, _1231
    from mastapy._private.gears.gear_designs.conical import _1191, _1196
    from mastapy._private.gears.gear_designs.spiral_bevel import _997
    from mastapy._private.gears.gear_designs.straight_bevel import _989
    from mastapy._private.gears.gear_designs.straight_bevel_diff import _993
    from mastapy._private.gears.gear_designs.zerol_bevel import _980
    from mastapy._private.math_utility import _1569

    Self = TypeVar("Self", bound="BevelGearSetDesign")
    CastSelf = TypeVar("CastSelf", bound="BevelGearSetDesign._Cast_BevelGearSetDesign")


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearSetDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearSetDesign:
    """Special nested class for casting BevelGearSetDesign to subclasses."""

    __parent__: "BevelGearSetDesign"

    @property
    def agma_gleason_conical_gear_set_design(
        self: "CastSelf",
    ) -> "_1235.AGMAGleasonConicalGearSetDesign":
        return self.__parent__._cast(_1235.AGMAGleasonConicalGearSetDesign)

    @property
    def conical_gear_set_design(self: "CastSelf") -> "_1196.ConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.conical import _1196

        return self.__parent__._cast(_1196.ConicalGearSetDesign)

    @property
    def gear_set_design(self: "CastSelf") -> "_976.GearSetDesign":
        from mastapy._private.gears.gear_designs import _976

        return self.__parent__._cast(_976.GearSetDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_974.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _974

        return self.__parent__._cast(_974.GearDesignComponent)

    @property
    def zerol_bevel_gear_set_design(self: "CastSelf") -> "_980.ZerolBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _980

        return self.__parent__._cast(_980.ZerolBevelGearSetDesign)

    @property
    def straight_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_989.StraightBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _989

        return self.__parent__._cast(_989.StraightBevelGearSetDesign)

    @property
    def straight_bevel_diff_gear_set_design(
        self: "CastSelf",
    ) -> "_993.StraightBevelDiffGearSetDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _993

        return self.__parent__._cast(_993.StraightBevelDiffGearSetDesign)

    @property
    def spiral_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_997.SpiralBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _997

        return self.__parent__._cast(_997.SpiralBevelGearSetDesign)

    @property
    def bevel_gear_set_design(self: "CastSelf") -> "BevelGearSetDesign":
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
class BevelGearSetDesign(_1235.AGMAGleasonConicalGearSetDesign):
    """BevelGearSetDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_SET_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def allowable_scoring_index(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AllowableScoringIndex")

        if temp is None:
            return 0.0

        return temp

    @allowable_scoring_index.setter
    @enforce_parameter_types
    def allowable_scoring_index(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AllowableScoringIndex",
            float(value) if value is not None else 0.0,
        )

    @property
    def backlash_distribution_rule(self: "Self") -> "_1191.BacklashDistributionRule":
        """mastapy.gears.gear_designs.conical.BacklashDistributionRule"""
        temp = pythonnet_property_get(self.wrapped, "BacklashDistributionRule")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Conical.BacklashDistributionRule"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.conical._1191",
            "BacklashDistributionRule",
        )(value)

    @backlash_distribution_rule.setter
    @enforce_parameter_types
    def backlash_distribution_rule(
        self: "Self", value: "_1191.BacklashDistributionRule"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.GearDesigns.Conical.BacklashDistributionRule"
        )
        pythonnet_property_set(self.wrapped, "BacklashDistributionRule", value)

    @property
    def backlash_used_for_tooth_thickness_calculation(
        self: "Self",
    ) -> "_1569.MaxMinMean":
        """mastapy.math_utility.MaxMinMean"""
        temp = pythonnet_property_get(
            self.wrapped, "BacklashUsedForToothThicknessCalculation"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.MathUtility.MaxMinMean")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility._1569", "MaxMinMean"
        )(value)

    @backlash_used_for_tooth_thickness_calculation.setter
    @enforce_parameter_types
    def backlash_used_for_tooth_thickness_calculation(
        self: "Self", value: "_1569.MaxMinMean"
    ) -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.MathUtility.MaxMinMean")
        pythonnet_property_set(
            self.wrapped, "BacklashUsedForToothThicknessCalculation", value
        )

    @property
    def basic_crown_gear_addendum_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicCrownGearAddendumFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def basic_crown_gear_dedendum_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicCrownGearDedendumFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def circular_thickness_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CircularThicknessFactor")

        if temp is None:
            return 0.0

        return temp

    @circular_thickness_factor.setter
    @enforce_parameter_types
    def circular_thickness_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CircularThicknessFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def clearance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Clearance")

        if temp is None:
            return 0.0

        return temp

    @property
    def diametral_pitch(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DiametralPitch")

        if temp is None:
            return 0.0

        return temp

    @property
    def factor_of_safety_for_scoring(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FactorOfSafetyForScoring")

        if temp is None:
            return 0.0

        return temp

    @factor_of_safety_for_scoring.setter
    @enforce_parameter_types
    def factor_of_safety_for_scoring(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FactorOfSafetyForScoring",
            float(value) if value is not None else 0.0,
        )

    @property
    def ideal_circular_thickness_factor(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "IdealCircularThicknessFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @ideal_circular_thickness_factor.setter
    @enforce_parameter_types
    def ideal_circular_thickness_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "IdealCircularThicknessFactor", value)

    @property
    def ideal_pinion_mean_transverse_circular_thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "IdealPinionMeanTransverseCircularThickness"
        )

        if temp is None:
            return 0.0

        return temp

    @ideal_pinion_mean_transverse_circular_thickness.setter
    @enforce_parameter_types
    def ideal_pinion_mean_transverse_circular_thickness(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "IdealPinionMeanTransverseCircularThickness",
            float(value) if value is not None else 0.0,
        )

    @property
    def ideal_pinion_outer_transverse_circular_thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "IdealPinionOuterTransverseCircularThickness"
        )

        if temp is None:
            return 0.0

        return temp

    @ideal_pinion_outer_transverse_circular_thickness.setter
    @enforce_parameter_types
    def ideal_pinion_outer_transverse_circular_thickness(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "IdealPinionOuterTransverseCircularThickness",
            float(value) if value is not None else 0.0,
        )

    @property
    def ideal_wheel_finish_cutter_point_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "IdealWheelFinishCutterPointWidth")

        if temp is None:
            return 0.0

        return temp

    @ideal_wheel_finish_cutter_point_width.setter
    @enforce_parameter_types
    def ideal_wheel_finish_cutter_point_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IdealWheelFinishCutterPointWidth",
            float(value) if value is not None else 0.0,
        )

    @property
    def ideal_wheel_mean_slot_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "IdealWheelMeanSlotWidth")

        if temp is None:
            return 0.0

        return temp

    @ideal_wheel_mean_slot_width.setter
    @enforce_parameter_types
    def ideal_wheel_mean_slot_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IdealWheelMeanSlotWidth",
            float(value) if value is not None else 0.0,
        )

    @property
    def mean_addendum_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MeanAddendumFactor")

        if temp is None:
            return 0.0

        return temp

    @mean_addendum_factor.setter
    @enforce_parameter_types
    def mean_addendum_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MeanAddendumFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def mean_circular_pitch(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanCircularPitch")

        if temp is None:
            return 0.0

        return temp

    @property
    def mean_clearance_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MeanClearanceFactor")

        if temp is None:
            return 0.0

        return temp

    @mean_clearance_factor.setter
    @enforce_parameter_types
    def mean_clearance_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MeanClearanceFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def mean_depth_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MeanDepthFactor")

        if temp is None:
            return 0.0

        return temp

    @mean_depth_factor.setter
    @enforce_parameter_types
    def mean_depth_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MeanDepthFactor", float(value) if value is not None else 0.0
        )

    @property
    def mean_diametral_pitch(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanDiametralPitch")

        if temp is None:
            return 0.0

        return temp

    @property
    def mean_whole_depth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanWholeDepth")

        if temp is None:
            return 0.0

        return temp

    @property
    def mean_working_depth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanWorkingDepth")

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_number_of_teeth_for_recommended_tooth_proportions(
        self: "Self",
    ) -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumNumberOfTeethForRecommendedToothProportions"
        )

        if temp is None:
            return 0

        return temp

    @property
    def outer_wheel_addendum(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterWheelAddendum")

        if temp is None:
            return 0.0

        return temp

    @outer_wheel_addendum.setter
    @enforce_parameter_types
    def outer_wheel_addendum(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OuterWheelAddendum",
            float(value) if value is not None else 0.0,
        )

    @property
    def outer_whole_depth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterWholeDepth")

        if temp is None:
            return 0.0

        return temp

    @outer_whole_depth.setter
    @enforce_parameter_types
    def outer_whole_depth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "OuterWholeDepth", float(value) if value is not None else 0.0
        )

    @property
    def outer_working_depth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterWorkingDepth")

        if temp is None:
            return 0.0

        return temp

    @outer_working_depth.setter
    @enforce_parameter_types
    def outer_working_depth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OuterWorkingDepth",
            float(value) if value is not None else 0.0,
        )

    @property
    def pressure_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PressureAngle")

        if temp is None:
            return 0.0

        return temp

    @pressure_angle.setter
    @enforce_parameter_types
    def pressure_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PressureAngle", float(value) if value is not None else 0.0
        )

    @property
    def profile_shift_coefficient(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileShiftCoefficient")

        if temp is None:
            return 0.0

        return temp

    @property
    def round_cutter_specifications(
        self: "Self",
    ) -> "_1231.WheelFinishCutterPointWidthRestrictionMethod":
        """mastapy.gears.gear_designs.bevel.WheelFinishCutterPointWidthRestrictionMethod"""
        temp = pythonnet_property_get(self.wrapped, "RoundCutterSpecifications")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Bevel.WheelFinishCutterPointWidthRestrictionMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.bevel._1231",
            "WheelFinishCutterPointWidthRestrictionMethod",
        )(value)

    @round_cutter_specifications.setter
    @enforce_parameter_types
    def round_cutter_specifications(
        self: "Self", value: "_1231.WheelFinishCutterPointWidthRestrictionMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Bevel.WheelFinishCutterPointWidthRestrictionMethod",
        )
        pythonnet_property_set(self.wrapped, "RoundCutterSpecifications", value)

    @property
    def specified_pinion_dedendum_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedPinionDedendumAngle")

        if temp is None:
            return 0.0

        return temp

    @specified_pinion_dedendum_angle.setter
    @enforce_parameter_types
    def specified_pinion_dedendum_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifiedPinionDedendumAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    def specified_wheel_dedendum_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedWheelDedendumAngle")

        if temp is None:
            return 0.0

        return temp

    @specified_wheel_dedendum_angle.setter
    @enforce_parameter_types
    def specified_wheel_dedendum_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifiedWheelDedendumAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    def strength_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StrengthFactor")

        if temp is None:
            return 0.0

        return temp

    @strength_factor.setter
    @enforce_parameter_types
    def strength_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "StrengthFactor", float(value) if value is not None else 0.0
        )

    @property
    def thickness_modification_coefficient_theoretical(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThicknessModificationCoefficientTheoretical"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def tooth_proportions_input_method(
        self: "Self",
    ) -> "_1229.ToothProportionsInputMethod":
        """mastapy.gears.gear_designs.bevel.ToothProportionsInputMethod"""
        temp = pythonnet_property_get(self.wrapped, "ToothProportionsInputMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Bevel.ToothProportionsInputMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.bevel._1229",
            "ToothProportionsInputMethod",
        )(value)

    @tooth_proportions_input_method.setter
    @enforce_parameter_types
    def tooth_proportions_input_method(
        self: "Self", value: "_1229.ToothProportionsInputMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.GearDesigns.Bevel.ToothProportionsInputMethod"
        )
        pythonnet_property_set(self.wrapped, "ToothProportionsInputMethod", value)

    @property
    def tooth_taper_root_line_tilt_method(
        self: "Self",
    ) -> "_359.SpiralBevelRootLineTilt":
        """mastapy.gears.SpiralBevelRootLineTilt"""
        temp = pythonnet_property_get(self.wrapped, "ToothTaperRootLineTiltMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.SpiralBevelRootLineTilt"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._359", "SpiralBevelRootLineTilt"
        )(value)

    @tooth_taper_root_line_tilt_method.setter
    @enforce_parameter_types
    def tooth_taper_root_line_tilt_method(
        self: "Self", value: "_359.SpiralBevelRootLineTilt"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.SpiralBevelRootLineTilt"
        )
        pythonnet_property_set(self.wrapped, "ToothTaperRootLineTiltMethod", value)

    @property
    def tooth_thickness_specification_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ToothThicknessSpecificationMethod":
        """EnumWithSelectedValue[mastapy.gears.gear_designs.bevel.ToothThicknessSpecificationMethod]"""
        temp = pythonnet_property_get(self.wrapped, "ToothThicknessSpecificationMethod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ToothThicknessSpecificationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @tooth_thickness_specification_method.setter
    @enforce_parameter_types
    def tooth_thickness_specification_method(
        self: "Self", value: "_1230.ToothThicknessSpecificationMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ToothThicknessSpecificationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ToothThicknessSpecificationMethod", value)

    @property
    def use_recommended_tooth_proportions(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseRecommendedToothProportions")

        if temp is None:
            return False

        return temp

    @use_recommended_tooth_proportions.setter
    @enforce_parameter_types
    def use_recommended_tooth_proportions(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseRecommendedToothProportions",
            bool(value) if value is not None else False,
        )

    @property
    def wheel_addendum_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelAddendumFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def wheel_addendum_multiplier(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WheelAddendumMultiplier")

        if temp is None:
            return 0.0

        return temp

    @wheel_addendum_multiplier.setter
    @enforce_parameter_types
    def wheel_addendum_multiplier(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WheelAddendumMultiplier",
            float(value) if value is not None else 0.0,
        )

    @property
    def wheel_finish_cutter_point_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WheelFinishCutterPointWidth")

        if temp is None:
            return 0.0

        return temp

    @wheel_finish_cutter_point_width.setter
    @enforce_parameter_types
    def wheel_finish_cutter_point_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WheelFinishCutterPointWidth",
            float(value) if value is not None else 0.0,
        )

    @property
    def wheel_inner_spiral_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelInnerSpiralAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def whole_depth_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WholeDepthFactor")

        if temp is None:
            return 0.0

        return temp

    @whole_depth_factor.setter
    @enforce_parameter_types
    def whole_depth_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "WholeDepthFactor", float(value) if value is not None else 0.0
        )

    @property
    def working_depth_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WorkingDepthFactor")

        if temp is None:
            return 0.0

        return temp

    @working_depth_factor.setter
    @enforce_parameter_types
    def working_depth_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WorkingDepthFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def mean_spiral_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MeanSpiralAngle")

        if temp is None:
            return 0.0

        return temp

    @mean_spiral_angle.setter
    @enforce_parameter_types
    def mean_spiral_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MeanSpiralAngle", float(value) if value is not None else 0.0
        )

    @property
    def transverse_circular_thickness_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TransverseCircularThicknessFactor")

        if temp is None:
            return 0.0

        return temp

    @transverse_circular_thickness_factor.setter
    @enforce_parameter_types
    def transverse_circular_thickness_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TransverseCircularThicknessFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_BevelGearSetDesign":
        """Cast to another type.

        Returns:
            _Cast_BevelGearSetDesign
        """
        return _Cast_BevelGearSetDesign(self)
