"""LoadedRollingBearingDutyCycle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings import _1930
from mastapy._private.bearings.bearing_results import _2012

_LOADED_ROLLING_BEARING_DUTY_CYCLE = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults", "LoadedRollingBearingDutyCycle"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2004
    from mastapy._private.bearings.bearing_results.rolling import (
        _2048,
        _2055,
        _2063,
        _2079,
        _2102,
        _2117,
    )
    from mastapy._private.nodal_analysis import _50
    from mastapy._private.utility.property import _1893, _1894, _1895, _1896

    Self = TypeVar("Self", bound="LoadedRollingBearingDutyCycle")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedRollingBearingDutyCycle._Cast_LoadedRollingBearingDutyCycle",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedRollingBearingDutyCycle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedRollingBearingDutyCycle:
    """Special nested class for casting LoadedRollingBearingDutyCycle to subclasses."""

    __parent__: "LoadedRollingBearingDutyCycle"

    @property
    def loaded_non_linear_bearing_duty_cycle_results(
        self: "CastSelf",
    ) -> "_2012.LoadedNonLinearBearingDutyCycleResults":
        return self.__parent__._cast(_2012.LoadedNonLinearBearingDutyCycleResults)

    @property
    def loaded_bearing_duty_cycle(self: "CastSelf") -> "_2004.LoadedBearingDutyCycle":
        from mastapy._private.bearings.bearing_results import _2004

        return self.__parent__._cast(_2004.LoadedBearingDutyCycle)

    @property
    def loaded_axial_thrust_cylindrical_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2048.LoadedAxialThrustCylindricalRollerBearingDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2048

        return self.__parent__._cast(
            _2048.LoadedAxialThrustCylindricalRollerBearingDutyCycle
        )

    @property
    def loaded_ball_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2055.LoadedBallBearingDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2055

        return self.__parent__._cast(_2055.LoadedBallBearingDutyCycle)

    @property
    def loaded_cylindrical_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2063.LoadedCylindricalRollerBearingDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2063

        return self.__parent__._cast(_2063.LoadedCylindricalRollerBearingDutyCycle)

    @property
    def loaded_non_barrel_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2079.LoadedNonBarrelRollerBearingDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2079

        return self.__parent__._cast(_2079.LoadedNonBarrelRollerBearingDutyCycle)

    @property
    def loaded_taper_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2102.LoadedTaperRollerBearingDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2102

        return self.__parent__._cast(_2102.LoadedTaperRollerBearingDutyCycle)

    @property
    def loaded_rolling_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "LoadedRollingBearingDutyCycle":
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
class LoadedRollingBearingDutyCycle(_2012.LoadedNonLinearBearingDutyCycleResults):
    """LoadedRollingBearingDutyCycle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_ROLLING_BEARING_DUTY_CYCLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def ansiabma_adjusted_rating_life_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ANSIABMAAdjustedRatingLifeDamage")

        if temp is None:
            return 0.0

        return temp

    @property
    def ansiabma_adjusted_rating_life_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ANSIABMAAdjustedRatingLifeReliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def ansiabma_adjusted_rating_life_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ANSIABMAAdjustedRatingLifeSafetyFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def ansiabma_adjusted_rating_life_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ANSIABMAAdjustedRatingLifeTime")

        if temp is None:
            return 0.0

        return temp

    @property
    def ansiabma_adjusted_rating_life_unreliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ANSIABMAAdjustedRatingLifeUnreliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def ansiabma_basic_rating_life_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ANSIABMABasicRatingLifeDamage")

        if temp is None:
            return 0.0

        return temp

    @property
    def ansiabma_basic_rating_life_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ANSIABMABasicRatingLifeReliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def ansiabma_basic_rating_life_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ANSIABMABasicRatingLifeSafetyFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def ansiabma_basic_rating_life_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ANSIABMABasicRatingLifeTime")

        if temp is None:
            return 0.0

        return temp

    @property
    def ansiabma_basic_rating_life_unreliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ANSIABMABasicRatingLifeUnreliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def ansiabma_dynamic_equivalent_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ANSIABMADynamicEquivalentLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    def iso2812007_basic_rating_life_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO2812007BasicRatingLifeDamage")

        if temp is None:
            return 0.0

        return temp

    @property
    def iso2812007_basic_rating_life_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO2812007BasicRatingLifeReliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def iso2812007_basic_rating_life_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO2812007BasicRatingLifeSafetyFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def iso2812007_basic_rating_life_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO2812007BasicRatingLifeTime")

        if temp is None:
            return 0.0

        return temp

    @property
    def iso2812007_basic_rating_life_unreliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO2812007BasicRatingLifeUnreliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def iso2812007_dynamic_equivalent_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO2812007DynamicEquivalentLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    def iso2812007_modified_rating_life_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO2812007ModifiedRatingLifeDamage"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def iso2812007_modified_rating_life_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO2812007ModifiedRatingLifeReliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def iso2812007_modified_rating_life_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO2812007ModifiedRatingLifeSafetyFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def iso2812007_modified_rating_life_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO2812007ModifiedRatingLifeTime")

        if temp is None:
            return 0.0

        return temp

    @property
    def iso2812007_modified_rating_life_unreliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO2812007ModifiedRatingLifeUnreliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def iso762006_recommended_maximum_element_normal_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO762006RecommendedMaximumElementNormalStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def isots162812008_basic_reference_rating_life_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISOTS162812008BasicReferenceRatingLifeDamage"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def isots162812008_basic_reference_rating_life_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISOTS162812008BasicReferenceRatingLifeReliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def isots162812008_basic_reference_rating_life_safety_factor(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISOTS162812008BasicReferenceRatingLifeSafetyFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def isots162812008_basic_reference_rating_life_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISOTS162812008BasicReferenceRatingLifeTime"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def isots162812008_basic_reference_rating_life_unreliability(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISOTS162812008BasicReferenceRatingLifeUnreliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def isots162812008_dynamic_equivalent_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISOTS162812008DynamicEquivalentLoad"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def isots162812008_modified_reference_rating_life_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISOTS162812008ModifiedReferenceRatingLifeDamage"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def isots162812008_modified_reference_rating_life_reliability(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISOTS162812008ModifiedReferenceRatingLifeReliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def isots162812008_modified_reference_rating_life_safety_factor(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISOTS162812008ModifiedReferenceRatingLifeSafetyFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def isots162812008_modified_reference_rating_life_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISOTS162812008ModifiedReferenceRatingLifeTime"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def isots162812008_modified_reference_rating_life_unreliability(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISOTS162812008ModifiedReferenceRatingLifeUnreliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def lambda_ratio_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LambdaRatioInner")

        if temp is None:
            return 0.0

        return temp

    @property
    def lambda_ratio_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LambdaRatioOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_element_normal_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumElementNormalStress")

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_lambda_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumLambdaRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_lubricating_film_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumLubricatingFilmThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_lubricating_film_thickness_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumLubricatingFilmThicknessInner"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_lubricating_film_thickness_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumLubricatingFilmThicknessOuter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def skf_bearing_rating_life_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SKFBearingRatingLifeDamage")

        if temp is None:
            return 0.0

        return temp

    @property
    def skf_bearing_rating_life_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SKFBearingRatingLifeReliability")

        if temp is None:
            return 0.0

        return temp

    @property
    def skf_bearing_rating_life_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SKFBearingRatingLifeTime")

        if temp is None:
            return 0.0

        return temp

    @property
    def skf_bearing_rating_life_unreliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SKFBearingRatingLifeUnreliability")

        if temp is None:
            return 0.0

        return temp

    @property
    def static_equivalent_load_capacity_ratio_limit(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StaticEquivalentLoadCapacityRatioLimit"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def worst_ansiabma_static_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorstANSIABMAStaticSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def worst_iso762006_safety_factor_static_equivalent_load_capacity_ratio(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WorstISO762006SafetyFactorStaticEquivalentLoadCapacityRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def ansiabma_dynamic_equivalent_load_summary(
        self: "Self",
    ) -> "_1893.DutyCyclePropertySummaryForce[_1930.BearingLoadCaseResultsLightweight]":
        """mastapy.utility.property.DutyCyclePropertySummaryForce[mastapy.bearings.BearingLoadCaseResultsLightweight]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ANSIABMADynamicEquivalentLoadSummary"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _1930.BearingLoadCaseResultsLightweight
        ](temp)

    @property
    def analysis_settings(self: "Self") -> "_50.AnalysisSettingsItem":
        """mastapy.nodal_analysis.AnalysisSettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AnalysisSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def iso2812007_dynamic_equivalent_load_summary(
        self: "Self",
    ) -> "_1893.DutyCyclePropertySummaryForce[_1930.BearingLoadCaseResultsLightweight]":
        """mastapy.utility.property.DutyCyclePropertySummaryForce[mastapy.bearings.BearingLoadCaseResultsLightweight]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO2812007DynamicEquivalentLoadSummary"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _1930.BearingLoadCaseResultsLightweight
        ](temp)

    @property
    def isots162812008_dynamic_equivalent_load_summary(
        self: "Self",
    ) -> "_1893.DutyCyclePropertySummaryForce[_1930.BearingLoadCaseResultsLightweight]":
        """mastapy.utility.property.DutyCyclePropertySummaryForce[mastapy.bearings.BearingLoadCaseResultsLightweight]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISOTS162812008DynamicEquivalentLoadSummary"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _1930.BearingLoadCaseResultsLightweight
        ](temp)

    @property
    def maximum_element_normal_stress_inner_summary(
        self: "Self",
    ) -> (
        "_1896.DutyCyclePropertySummaryStress[_1930.BearingLoadCaseResultsLightweight]"
    ):
        """mastapy.utility.property.DutyCyclePropertySummaryStress[mastapy.bearings.BearingLoadCaseResultsLightweight]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumElementNormalStressInnerSummary"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _1930.BearingLoadCaseResultsLightweight
        ](temp)

    @property
    def maximum_element_normal_stress_outer_summary(
        self: "Self",
    ) -> (
        "_1896.DutyCyclePropertySummaryStress[_1930.BearingLoadCaseResultsLightweight]"
    ):
        """mastapy.utility.property.DutyCyclePropertySummaryStress[mastapy.bearings.BearingLoadCaseResultsLightweight]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumElementNormalStressOuterSummary"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _1930.BearingLoadCaseResultsLightweight
        ](temp)

    @property
    def maximum_element_normal_stress_summary(
        self: "Self",
    ) -> (
        "_1896.DutyCyclePropertySummaryStress[_1930.BearingLoadCaseResultsLightweight]"
    ):
        """mastapy.utility.property.DutyCyclePropertySummaryStress[mastapy.bearings.BearingLoadCaseResultsLightweight]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumElementNormalStressSummary")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _1930.BearingLoadCaseResultsLightweight
        ](temp)

    @property
    def maximum_static_contact_stress_duty_cycle(
        self: "Self",
    ) -> "_2117.MaximumStaticContactStressDutyCycle":
        """mastapy.bearings.bearing_results.rolling.MaximumStaticContactStressDutyCycle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumStaticContactStressDutyCycle"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def maximum_truncation_summary(
        self: "Self",
    ) -> "_1894.DutyCyclePropertySummaryPercentage[_1930.BearingLoadCaseResultsLightweight]":
        """mastapy.utility.property.DutyCyclePropertySummaryPercentage[mastapy.bearings.BearingLoadCaseResultsLightweight]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumTruncationSummary")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _1930.BearingLoadCaseResultsLightweight
        ](temp)

    @property
    def misalignment_summary(
        self: "Self",
    ) -> "_1895.DutyCyclePropertySummarySmallAngle[_1930.BearingLoadCaseResultsLightweight]":
        """mastapy.utility.property.DutyCyclePropertySummarySmallAngle[mastapy.bearings.BearingLoadCaseResultsLightweight]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MisalignmentSummary")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _1930.BearingLoadCaseResultsLightweight
        ](temp)

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedRollingBearingDutyCycle":
        """Cast to another type.

        Returns:
            _Cast_LoadedRollingBearingDutyCycle
        """
        return _Cast_LoadedRollingBearingDutyCycle(self)
