"""CylindricalGearMeshLoadDistributionAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._math.vector_2d import Vector2D
from mastapy._private.gears.ltca import _866

_CYLINDRICAL_GEAR_MESH_LOAD_DISTRIBUTION_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.LTCA.Cylindrical", "CylindricalGearMeshLoadDistributionAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1256, _1262, _1263
    from mastapy._private.gears.cylindrical import _1254
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1132
    from mastapy._private.gears.load_case.cylindrical import _909
    from mastapy._private.gears.ltca import _857
    from mastapy._private.gears.ltca.cylindrical import _886
    from mastapy._private.gears.rating.cylindrical import _471

    Self = TypeVar("Self", bound="CylindricalGearMeshLoadDistributionAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearMeshLoadDistributionAnalysis._Cast_CylindricalGearMeshLoadDistributionAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearMeshLoadDistributionAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearMeshLoadDistributionAnalysis:
    """Special nested class for casting CylindricalGearMeshLoadDistributionAnalysis to subclasses."""

    __parent__: "CylindricalGearMeshLoadDistributionAnalysis"

    @property
    def gear_mesh_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_866.GearMeshLoadDistributionAnalysis":
        return self.__parent__._cast(_866.GearMeshLoadDistributionAnalysis)

    @property
    def gear_mesh_implementation_analysis(
        self: "CastSelf",
    ) -> "_1263.GearMeshImplementationAnalysis":
        from mastapy._private.gears.analysis import _1263

        return self.__parent__._cast(_1263.GearMeshImplementationAnalysis)

    @property
    def gear_mesh_design_analysis(self: "CastSelf") -> "_1262.GearMeshDesignAnalysis":
        from mastapy._private.gears.analysis import _1262

        return self.__parent__._cast(_1262.GearMeshDesignAnalysis)

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1256.AbstractGearMeshAnalysis":
        from mastapy._private.gears.analysis import _1256

        return self.__parent__._cast(_1256.AbstractGearMeshAnalysis)

    @property
    def cylindrical_gear_mesh_load_distribution_analysis(
        self: "CastSelf",
    ) -> "CylindricalGearMeshLoadDistributionAnalysis":
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
class CylindricalGearMeshLoadDistributionAnalysis(
    _866.GearMeshLoadDistributionAnalysis
):
    """CylindricalGearMeshLoadDistributionAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MESH_LOAD_DISTRIBUTION_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def average_flash_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageFlashTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    def calculated_face_load_factor_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CalculatedFaceLoadFactorContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def din_scuffing_bulk_tooth_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DINScuffingBulkToothTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    def iso63362006_mesh_stiffness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO63362006MeshStiffness")

        if temp is None:
            return 0.0

        return temp

    @property
    def iso63362006_mesh_stiffness_across_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO63362006MeshStiffnessAcrossFaceWidth"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def iso63362006_single_stiffness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO63362006SingleStiffness")

        if temp is None:
            return 0.0

        return temp

    @property
    def iso63362006_single_stiffness_across_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO63362006SingleStiffnessAcrossFaceWidth"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def iso_scuffing_bulk_tooth_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISOScuffingBulkToothTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_edge_pressure(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumEdgePressure")

        if temp is None:
            return 0.0

        return temp

    @property
    def mean_coefficient_of_friction_from_ltca(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanCoefficientOfFrictionFromLTCA")

        if temp is None:
            return 0.0

        return temp

    @property
    def mean_sliding_power_loss_from_ltca(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanSlidingPowerLossFromLTCA")

        if temp is None:
            return 0.0

        return temp

    @property
    def mean_te(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanTE")

        if temp is None:
            return 0.0

        return temp

    @property
    def mesh_efficiency_from_ltca(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshEfficiencyFromLTCA")

        if temp is None:
            return 0.0

        return temp

    @property
    def misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Misalignment")

        if temp is None:
            return 0.0

        return temp

    @property
    def peak_to_peak_te(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PeakToPeakTE")

        if temp is None:
            return 0.0

        return temp

    @property
    def strip_loads_deviation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StripLoadsDeviation")

        if temp is None:
            return 0.0

        return temp

    @property
    def strip_loads_maximum(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StripLoadsMaximum")

        if temp is None:
            return 0.0

        return temp

    @property
    def strip_loads_minimum(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StripLoadsMinimum")

        if temp is None:
            return 0.0

        return temp

    @property
    def theoretical_total_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TheoreticalTotalContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    def tooth_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    def utilization_force_per_unit_length_cutoff_value(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "UtilizationForcePerUnitLengthCutoffValue"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cylindrical_mesh_load_case(self: "Self") -> "_909.CylindricalMeshLoadCase":
        """mastapy.gears.load_case.cylindrical.CylindricalMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalMeshLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gear_a_in_mesh(
        self: "Self",
    ) -> "_857.CylindricalMeshedGearLoadDistributionAnalysis":
        """mastapy.gears.ltca.CylindricalMeshedGearLoadDistributionAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearAInMesh")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gear_b_in_mesh(
        self: "Self",
    ) -> "_857.CylindricalMeshedGearLoadDistributionAnalysis":
        """mastapy.gears.ltca.CylindricalMeshedGearLoadDistributionAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearBInMesh")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def mesh_micro_geometry(self: "Self") -> "_1132.CylindricalGearMeshMicroGeometry":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearMeshMicroGeometry

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshMicroGeometry")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def points_with_worst_results(self: "Self") -> "_1254.PointsWithWorstResults":
        """mastapy.gears.cylindrical.PointsWithWorstResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PointsWithWorstResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def rating(self: "Self") -> "_471.CylindricalGearMeshRating":
        """mastapy.gears.rating.cylindrical.CylindricalGearMeshRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def load_distribution_analyses_at_single_rotation(
        self: "Self",
    ) -> "List[_886.CylindricalMeshLoadDistributionAtRotation]":
        """List[mastapy.gears.ltca.cylindrical.CylindricalMeshLoadDistributionAtRotation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LoadDistributionAnalysesAtSingleRotation"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def meshed_gears(
        self: "Self",
    ) -> "List[_857.CylindricalMeshedGearLoadDistributionAnalysis]":
        """List[mastapy.gears.ltca.CylindricalMeshedGearLoadDistributionAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshedGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def transmission_error_against_rotation(self: "Self") -> "List[Vector2D]":
        """List[Vector2D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransmissionErrorAgainstRotation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector2D)

        if value is None:
            return None

        return value

    def calculate_mesh_stiffness(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CalculateMeshStiffness")

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearMeshLoadDistributionAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearMeshLoadDistributionAnalysis
        """
        return _Cast_CylindricalGearMeshLoadDistributionAnalysis(self)
