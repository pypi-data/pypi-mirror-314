"""GeneralTransmissionProperties"""

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
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_GENERAL_TRANSMISSION_PROPERTIES = python_net_import(
    "SMT.MastaAPI.Materials", "GeneralTransmissionProperties"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.materials import (
        _256,
        _268,
        _272,
        _280,
        _300,
        _302,
        _303,
        _304,
    )

    Self = TypeVar("Self", bound="GeneralTransmissionProperties")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GeneralTransmissionProperties._Cast_GeneralTransmissionProperties",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GeneralTransmissionProperties",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GeneralTransmissionProperties:
    """Special nested class for casting GeneralTransmissionProperties to subclasses."""

    __parent__: "GeneralTransmissionProperties"

    @property
    def general_transmission_properties(
        self: "CastSelf",
    ) -> "GeneralTransmissionProperties":
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
class GeneralTransmissionProperties(_0.APIBase):
    """GeneralTransmissionProperties

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GENERAL_TRANSMISSION_PROPERTIES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def agma_over_load_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "AGMAOverLoadFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @agma_over_load_factor.setter
    @enforce_parameter_types
    def agma_over_load_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AGMAOverLoadFactor", value)

    @property
    def application_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ApplicationFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @application_factor.setter
    @enforce_parameter_types
    def application_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ApplicationFactor", value)

    @property
    def bearing_iso762006_static_safety_factor_limit(
        self: "Self",
    ) -> "_272.ISO76StaticSafetyFactorLimits":
        """mastapy.materials.ISO76StaticSafetyFactorLimits"""
        temp = pythonnet_property_get(
            self.wrapped, "BearingISO762006StaticSafetyFactorLimit"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.ISO76StaticSafetyFactorLimits"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._272", "ISO76StaticSafetyFactorLimits"
        )(value)

    @bearing_iso762006_static_safety_factor_limit.setter
    @enforce_parameter_types
    def bearing_iso762006_static_safety_factor_limit(
        self: "Self", value: "_272.ISO76StaticSafetyFactorLimits"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.ISO76StaticSafetyFactorLimits"
        )
        pythonnet_property_set(
            self.wrapped, "BearingISO762006StaticSafetyFactorLimit", value
        )

    @property
    def drawn_cup_needle_roller_bearings_iso762006_static_safety_factor_limit(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "DrawnCupNeedleRollerBearingsISO762006StaticSafetyFactorLimit"
        )

        if temp is None:
            return 0.0

        return temp

    @drawn_cup_needle_roller_bearings_iso762006_static_safety_factor_limit.setter
    @enforce_parameter_types
    def drawn_cup_needle_roller_bearings_iso762006_static_safety_factor_limit(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "DrawnCupNeedleRollerBearingsISO762006StaticSafetyFactorLimit",
            float(value) if value is not None else 0.0,
        )

    @property
    def driven_machine_characteristics(self: "Self") -> "_304.WorkingCharacteristics":
        """mastapy.materials.WorkingCharacteristics"""
        temp = pythonnet_property_get(self.wrapped, "DrivenMachineCharacteristics")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.WorkingCharacteristics"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._304", "WorkingCharacteristics"
        )(value)

    @driven_machine_characteristics.setter
    @enforce_parameter_types
    def driven_machine_characteristics(
        self: "Self", value: "_304.WorkingCharacteristics"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.WorkingCharacteristics"
        )
        pythonnet_property_set(self.wrapped, "DrivenMachineCharacteristics", value)

    @property
    def driving_machine_characteristics(self: "Self") -> "_304.WorkingCharacteristics":
        """mastapy.materials.WorkingCharacteristics"""
        temp = pythonnet_property_get(self.wrapped, "DrivingMachineCharacteristics")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.WorkingCharacteristics"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._304", "WorkingCharacteristics"
        )(value)

    @driving_machine_characteristics.setter
    @enforce_parameter_types
    def driving_machine_characteristics(
        self: "Self", value: "_304.WorkingCharacteristics"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.WorkingCharacteristics"
        )
        pythonnet_property_set(self.wrapped, "DrivingMachineCharacteristics", value)

    @property
    def energy_convergence_absolute_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EnergyConvergenceAbsoluteTolerance"
        )

        if temp is None:
            return 0.0

        return temp

    @energy_convergence_absolute_tolerance.setter
    @enforce_parameter_types
    def energy_convergence_absolute_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EnergyConvergenceAbsoluteTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    def feed_flow_rate(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FeedFlowRate")

        if temp is None:
            return 0.0

        return temp

    @feed_flow_rate.setter
    @enforce_parameter_types
    def feed_flow_rate(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FeedFlowRate", float(value) if value is not None else 0.0
        )

    @property
    def feed_pressure(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FeedPressure")

        if temp is None:
            return 0.0

        return temp

    @feed_pressure.setter
    @enforce_parameter_types
    def feed_pressure(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FeedPressure", float(value) if value is not None else 0.0
        )

    @property
    def gearing_type(self: "Self") -> "_268.GearingTypes":
        """mastapy.materials.GearingTypes"""
        temp = pythonnet_property_get(self.wrapped, "GearingType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Materials.GearingTypes")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._268", "GearingTypes"
        )(value)

    @gearing_type.setter
    @enforce_parameter_types
    def gearing_type(self: "Self", value: "_268.GearingTypes") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Materials.GearingTypes")
        pythonnet_property_set(self.wrapped, "GearingType", value)

    @property
    def iso2812007_safety_factor_requirement(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ISO2812007SafetyFactorRequirement")

        if temp is None:
            return 0.0

        return temp

    @iso2812007_safety_factor_requirement.setter
    @enforce_parameter_types
    def iso2812007_safety_factor_requirement(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ISO2812007SafetyFactorRequirement",
            float(value) if value is not None else 0.0,
        )

    @property
    def isots162812008_safety_factor_requirement(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ISOTS162812008SafetyFactorRequirement"
        )

        if temp is None:
            return 0.0

        return temp

    @isots162812008_safety_factor_requirement.setter
    @enforce_parameter_types
    def isots162812008_safety_factor_requirement(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ISOTS162812008SafetyFactorRequirement",
            float(value) if value is not None else 0.0,
        )

    @property
    def include_ansiabma_ratings(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeANSIABMARatings")

        if temp is None:
            return False

        return temp

    @include_ansiabma_ratings.setter
    @enforce_parameter_types
    def include_ansiabma_ratings(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeANSIABMARatings",
            bool(value) if value is not None else False,
        )

    @property
    def linear_bearings_minimum_axial_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "LinearBearingsMinimumAxialStiffness"
        )

        if temp is None:
            return 0.0

        return temp

    @linear_bearings_minimum_axial_stiffness.setter
    @enforce_parameter_types
    def linear_bearings_minimum_axial_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LinearBearingsMinimumAxialStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    def linear_bearings_minimum_radial_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "LinearBearingsMinimumRadialStiffness"
        )

        if temp is None:
            return 0.0

        return temp

    @linear_bearings_minimum_radial_stiffness.setter
    @enforce_parameter_types
    def linear_bearings_minimum_radial_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LinearBearingsMinimumRadialStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    def linear_bearings_minimum_tilt_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "LinearBearingsMinimumTiltStiffness"
        )

        if temp is None:
            return 0.0

        return temp

    @linear_bearings_minimum_tilt_stiffness.setter
    @enforce_parameter_types
    def linear_bearings_minimum_tilt_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LinearBearingsMinimumTiltStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    def lubrication_detail_database(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "LubricationDetailDatabase", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @lubrication_detail_database.setter
    @enforce_parameter_types
    def lubrication_detail_database(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "LubricationDetailDatabase",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    def mass(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Mass")

        if temp is None:
            return 0.0

        return temp

    @mass.setter
    @enforce_parameter_types
    def mass(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Mass", float(value) if value is not None else 0.0
        )

    @property
    def maximum_bearing_life_modification_factor(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumBearingLifeModificationFactor"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_bearing_life_modification_factor.setter
    @enforce_parameter_types
    def maximum_bearing_life_modification_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MaximumBearingLifeModificationFactor", value
        )

    @property
    def maximum_iso762006_static_safety_factor_for_a_loaded_bearing(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumISO762006StaticSafetyFactorForALoadedBearing"
        )

        if temp is None:
            return 0.0

        return temp

    @maximum_iso762006_static_safety_factor_for_a_loaded_bearing.setter
    @enforce_parameter_types
    def maximum_iso762006_static_safety_factor_for_a_loaded_bearing(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumISO762006StaticSafetyFactorForALoadedBearing",
            float(value) if value is not None else 0.0,
        )

    @property
    def maximum_static_contact_safety_factor_for_loaded_gears_in_a_mesh(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumStaticContactSafetyFactorForLoadedGearsInAMesh"
        )

        if temp is None:
            return 0.0

        return temp

    @maximum_static_contact_safety_factor_for_loaded_gears_in_a_mesh.setter
    @enforce_parameter_types
    def maximum_static_contact_safety_factor_for_loaded_gears_in_a_mesh(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumStaticContactSafetyFactorForLoadedGearsInAMesh",
            float(value) if value is not None else 0.0,
        )

    @property
    def minimum_force_for_bearing_to_be_considered_loaded(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumForceForBearingToBeConsideredLoaded"
        )

        if temp is None:
            return 0.0

        return temp

    @minimum_force_for_bearing_to_be_considered_loaded.setter
    @enforce_parameter_types
    def minimum_force_for_bearing_to_be_considered_loaded(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumForceForBearingToBeConsideredLoaded",
            float(value) if value is not None else 0.0,
        )

    @property
    def minimum_moment_for_bearing_to_be_considered_loaded(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumMomentForBearingToBeConsideredLoaded"
        )

        if temp is None:
            return 0.0

        return temp

    @minimum_moment_for_bearing_to_be_considered_loaded.setter
    @enforce_parameter_types
    def minimum_moment_for_bearing_to_be_considered_loaded(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumMomentForBearingToBeConsideredLoaded",
            float(value) if value is not None else 0.0,
        )

    @property
    def minimum_static_safety_factor_for_maximum_contact_stress(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumStaticSafetyFactorForMaximumContactStress"
        )

        if temp is None:
            return 0.0

        return temp

    @minimum_static_safety_factor_for_maximum_contact_stress.setter
    @enforce_parameter_types
    def minimum_static_safety_factor_for_maximum_contact_stress(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumStaticSafetyFactorForMaximumContactStress",
            float(value) if value is not None else 0.0,
        )

    @property
    def non_linear_bearings_minimum_axial_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "NonLinearBearingsMinimumAxialStiffness"
        )

        if temp is None:
            return 0.0

        return temp

    @non_linear_bearings_minimum_axial_stiffness.setter
    @enforce_parameter_types
    def non_linear_bearings_minimum_axial_stiffness(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NonLinearBearingsMinimumAxialStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    def non_linear_bearings_minimum_radial_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "NonLinearBearingsMinimumRadialStiffness"
        )

        if temp is None:
            return 0.0

        return temp

    @non_linear_bearings_minimum_radial_stiffness.setter
    @enforce_parameter_types
    def non_linear_bearings_minimum_radial_stiffness(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NonLinearBearingsMinimumRadialStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    def non_linear_bearings_minimum_tilt_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "NonLinearBearingsMinimumTiltStiffness"
        )

        if temp is None:
            return 0.0

        return temp

    @non_linear_bearings_minimum_tilt_stiffness.setter
    @enforce_parameter_types
    def non_linear_bearings_minimum_tilt_stiffness(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NonLinearBearingsMinimumTiltStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    def permissible_track_truncation_ball_bearings(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleTrackTruncationBallBearings"
        )

        if temp is None:
            return 0.0

        return temp

    @permissible_track_truncation_ball_bearings.setter
    @enforce_parameter_types
    def permissible_track_truncation_ball_bearings(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "PermissibleTrackTruncationBallBearings",
            float(value) if value is not None else 0.0,
        )

    @property
    def power_convergence_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PowerConvergenceTolerance")

        if temp is None:
            return 0.0

        return temp

    @power_convergence_tolerance.setter
    @enforce_parameter_types
    def power_convergence_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PowerConvergenceTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    def required_safety_factor_for_cvt_belt_clamping_force(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "RequiredSafetyFactorForCVTBeltClampingForce"
        )

        if temp is None:
            return 0.0

        return temp

    @required_safety_factor_for_cvt_belt_clamping_force.setter
    @enforce_parameter_types
    def required_safety_factor_for_cvt_belt_clamping_force(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "RequiredSafetyFactorForCVTBeltClampingForce",
            float(value) if value is not None else 0.0,
        )

    @property
    def safety_factor_against_plastic_strain(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorAgainstPlasticStrain")

        if temp is None:
            return 0.0

        return temp

    @safety_factor_against_plastic_strain.setter
    @enforce_parameter_types
    def safety_factor_against_plastic_strain(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SafetyFactorAgainstPlasticStrain",
            float(value) if value is not None else 0.0,
        )

    @property
    def safety_factor_against_sliding(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorAgainstSliding")

        if temp is None:
            return 0.0

        return temp

    @safety_factor_against_sliding.setter
    @enforce_parameter_types
    def safety_factor_against_sliding(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SafetyFactorAgainstSliding",
            float(value) if value is not None else 0.0,
        )

    @property
    def thrust_spherical_roller_bearings_iso762006_static_safety_factor_limit(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped,
            "ThrustSphericalRollerBearingsISO762006StaticSafetyFactorLimit",
        )

        if temp is None:
            return 0.0

        return temp

    @thrust_spherical_roller_bearings_iso762006_static_safety_factor_limit.setter
    @enforce_parameter_types
    def thrust_spherical_roller_bearings_iso762006_static_safety_factor_limit(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ThrustSphericalRollerBearingsISO762006StaticSafetyFactorLimit",
            float(value) if value is not None else 0.0,
        )

    @property
    def transmission_application(self: "Self") -> "_300.TransmissionApplications":
        """mastapy.materials.TransmissionApplications"""
        temp = pythonnet_property_get(self.wrapped, "TransmissionApplication")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.TransmissionApplications"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._300", "TransmissionApplications"
        )(value)

    @transmission_application.setter
    @enforce_parameter_types
    def transmission_application(
        self: "Self", value: "_300.TransmissionApplications"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.TransmissionApplications"
        )
        pythonnet_property_set(self.wrapped, "TransmissionApplication", value)

    @property
    def volume(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Volume")

        if temp is None:
            return 0.0

        return temp

    @volume.setter
    @enforce_parameter_types
    def volume(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Volume", float(value) if value is not None else 0.0
        )

    @property
    def wind_turbine_standard(self: "Self") -> "_303.WindTurbineStandards":
        """mastapy.materials.WindTurbineStandards"""
        temp = pythonnet_property_get(self.wrapped, "WindTurbineStandard")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.WindTurbineStandards"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._303", "WindTurbineStandards"
        )(value)

    @wind_turbine_standard.setter
    @enforce_parameter_types
    def wind_turbine_standard(self: "Self", value: "_303.WindTurbineStandards") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.WindTurbineStandards"
        )
        pythonnet_property_set(self.wrapped, "WindTurbineStandard", value)

    @property
    def zero_speed_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ZeroSpeedTolerance")

        if temp is None:
            return 0.0

        return temp

    @zero_speed_tolerance.setter
    @enforce_parameter_types
    def zero_speed_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ZeroSpeedTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    def air_properties(self: "Self") -> "_256.AirProperties":
        """mastapy.materials.AirProperties

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AirProperties")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def lubrication_detail(self: "Self") -> "_280.LubricationDetail":
        """mastapy.materials.LubricationDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricationDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def vehicle_dynamics(self: "Self") -> "_302.VehicleDynamicsProperties":
        """mastapy.materials.VehicleDynamicsProperties

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VehicleDynamics")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GeneralTransmissionProperties":
        """Cast to another type.

        Returns:
            _Cast_GeneralTransmissionProperties
        """
        return _Cast_GeneralTransmissionProperties(self)
