"""AnalysisSettingsItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.databases import _1884

_ANALYSIS_SETTINGS_ITEM = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "AnalysisSettingsItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis import _84, _85

    Self = TypeVar("Self", bound="AnalysisSettingsItem")
    CastSelf = TypeVar(
        "CastSelf", bound="AnalysisSettingsItem._Cast_AnalysisSettingsItem"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AnalysisSettingsItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AnalysisSettingsItem:
    """Special nested class for casting AnalysisSettingsItem to subclasses."""

    __parent__: "AnalysisSettingsItem"

    @property
    def named_database_item(self: "CastSelf") -> "_1884.NamedDatabaseItem":
        return self.__parent__._cast(_1884.NamedDatabaseItem)

    @property
    def analysis_settings_item(self: "CastSelf") -> "AnalysisSettingsItem":
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
class AnalysisSettingsItem(_1884.NamedDatabaseItem):
    """AnalysisSettingsItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ANALYSIS_SETTINGS_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def gear_mesh_nodes_per_unit_length_to_diameter_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "GearMeshNodesPerUnitLengthToDiameterRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @gear_mesh_nodes_per_unit_length_to_diameter_ratio.setter
    @enforce_parameter_types
    def gear_mesh_nodes_per_unit_length_to_diameter_ratio(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "GearMeshNodesPerUnitLengthToDiameterRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    def maximum_nodes_for_nvh_analysis(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "MaximumNodesForNVHAnalysis")

        if temp is None:
            return 0

        return temp

    @maximum_nodes_for_nvh_analysis.setter
    @enforce_parameter_types
    def maximum_nodes_for_nvh_analysis(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumNodesForNVHAnalysis",
            int(value) if value is not None else 0,
        )

    @property
    def maximum_section_length_to_diameter_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumSectionLengthToDiameterRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @maximum_section_length_to_diameter_ratio.setter
    @enforce_parameter_types
    def maximum_section_length_to_diameter_ratio(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumSectionLengthToDiameterRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    def minimum_number_of_gear_mesh_nodes(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "MinimumNumberOfGearMeshNodes")

        if temp is None:
            return 0

        return temp

    @minimum_number_of_gear_mesh_nodes.setter
    @enforce_parameter_types
    def minimum_number_of_gear_mesh_nodes(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumNumberOfGearMeshNodes",
            int(value) if value is not None else 0,
        )

    @property
    def overwrite_advanced_system_deflection_load_cases_created_for_harmonic_excitations(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "OverwriteAdvancedSystemDeflectionLoadCasesCreatedForHarmonicExcitations",
        )

        if temp is None:
            return False

        return temp

    @overwrite_advanced_system_deflection_load_cases_created_for_harmonic_excitations.setter
    @enforce_parameter_types
    def overwrite_advanced_system_deflection_load_cases_created_for_harmonic_excitations(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverwriteAdvancedSystemDeflectionLoadCasesCreatedForHarmonicExcitations",
            bool(value) if value is not None else False,
        )

    @property
    def rating_type_for_bearing_reliability(
        self: "Self",
    ) -> "_84.RatingTypeForBearingReliability":
        """mastapy.nodal_analysis.RatingTypeForBearingReliability"""
        temp = pythonnet_property_get(self.wrapped, "RatingTypeForBearingReliability")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.RatingTypeForBearingReliability"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis._84", "RatingTypeForBearingReliability"
        )(value)

    @rating_type_for_bearing_reliability.setter
    @enforce_parameter_types
    def rating_type_for_bearing_reliability(
        self: "Self", value: "_84.RatingTypeForBearingReliability"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.RatingTypeForBearingReliability"
        )
        pythonnet_property_set(self.wrapped, "RatingTypeForBearingReliability", value)

    @property
    def rating_type_for_shaft_reliability(
        self: "Self",
    ) -> "_85.RatingTypeForShaftReliability":
        """mastapy.nodal_analysis.RatingTypeForShaftReliability"""
        temp = pythonnet_property_get(self.wrapped, "RatingTypeForShaftReliability")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.RatingTypeForShaftReliability"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis._85", "RatingTypeForShaftReliability"
        )(value)

    @rating_type_for_shaft_reliability.setter
    @enforce_parameter_types
    def rating_type_for_shaft_reliability(
        self: "Self", value: "_85.RatingTypeForShaftReliability"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.RatingTypeForShaftReliability"
        )
        pythonnet_property_set(self.wrapped, "RatingTypeForShaftReliability", value)

    @property
    def remove_rigid_body_rotation_theta_z_twist_from_shaft_reporting(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "RemoveRigidBodyRotationThetaZTwistFromShaftReporting"
        )

        if temp is None:
            return False

        return temp

    @remove_rigid_body_rotation_theta_z_twist_from_shaft_reporting.setter
    @enforce_parameter_types
    def remove_rigid_body_rotation_theta_z_twist_from_shaft_reporting(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "RemoveRigidBodyRotationThetaZTwistFromShaftReporting",
            bool(value) if value is not None else False,
        )

    @property
    def spline_nodes_per_unit_length_to_diameter_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "SplineNodesPerUnitLengthToDiameterRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @spline_nodes_per_unit_length_to_diameter_ratio.setter
    @enforce_parameter_types
    def spline_nodes_per_unit_length_to_diameter_ratio(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "SplineNodesPerUnitLengthToDiameterRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    def system_deflection_maximum_iterations(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionMaximumIterations")

        if temp is None:
            return 0

        return temp

    @system_deflection_maximum_iterations.setter
    @enforce_parameter_types
    def system_deflection_maximum_iterations(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SystemDeflectionMaximumIterations",
            int(value) if value is not None else 0,
        )

    @property
    def use_mean_load_and_load_sharing_factor_for_planet_bearing_reliability(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseMeanLoadAndLoadSharingFactorForPlanetBearingReliability"
        )

        if temp is None:
            return False

        return temp

    @use_mean_load_and_load_sharing_factor_for_planet_bearing_reliability.setter
    @enforce_parameter_types
    def use_mean_load_and_load_sharing_factor_for_planet_bearing_reliability(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseMeanLoadAndLoadSharingFactorForPlanetBearingReliability",
            bool(value) if value is not None else False,
        )

    @property
    def use_single_node_for_cylindrical_gear_meshes(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseSingleNodeForCylindricalGearMeshes"
        )

        if temp is None:
            return False

        return temp

    @use_single_node_for_cylindrical_gear_meshes.setter
    @enforce_parameter_types
    def use_single_node_for_cylindrical_gear_meshes(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseSingleNodeForCylindricalGearMeshes",
            bool(value) if value is not None else False,
        )

    @property
    def use_single_node_for_spline_connections(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseSingleNodeForSplineConnections")

        if temp is None:
            return False

        return temp

    @use_single_node_for_spline_connections.setter
    @enforce_parameter_types
    def use_single_node_for_spline_connections(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseSingleNodeForSplineConnections",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_AnalysisSettingsItem":
        """Cast to another type.

        Returns:
            _Cast_AnalysisSettingsItem
        """
        return _Cast_AnalysisSettingsItem(self)
