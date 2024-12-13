"""CylindricalMeshSingleFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating import _379

_CYLINDRICAL_MESH_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "CylindricalMeshSingleFlankRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears import _333
    from mastapy._private.gears.gear_designs.cylindrical import _1104, _1105
    from mastapy._private.gears.rating.cylindrical import _467, _475, _478
    from mastapy._private.gears.rating.cylindrical.agma import _548
    from mastapy._private.gears.rating.cylindrical.din3990 import _546
    from mastapy._private.gears.rating.cylindrical.iso6336 import (
        _525,
        _527,
        _529,
        _531,
        _533,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import (
        _503,
        _505,
        _507,
    )
    from mastapy._private.materials import _280

    Self = TypeVar("Self", bound="CylindricalMeshSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalMeshSingleFlankRating._Cast_CylindricalMeshSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalMeshSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalMeshSingleFlankRating:
    """Special nested class for casting CylindricalMeshSingleFlankRating to subclasses."""

    __parent__: "CylindricalMeshSingleFlankRating"

    @property
    def mesh_single_flank_rating(self: "CastSelf") -> "_379.MeshSingleFlankRating":
        return self.__parent__._cast(_379.MeshSingleFlankRating)

    @property
    def metal_plastic_or_plastic_metal_vdi2736_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_503.MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _503

        return self.__parent__._cast(
            _503.MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating
        )

    @property
    def plastic_gear_vdi2736_abstract_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_505.PlasticGearVDI2736AbstractMeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _505

        return self.__parent__._cast(
            _505.PlasticGearVDI2736AbstractMeshSingleFlankRating
        )

    @property
    def plastic_plastic_vdi2736_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_507.PlasticPlasticVDI2736MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _507

        return self.__parent__._cast(_507.PlasticPlasticVDI2736MeshSingleFlankRating)

    @property
    def iso63361996_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_525.ISO63361996MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _525

        return self.__parent__._cast(_525.ISO63361996MeshSingleFlankRating)

    @property
    def iso63362006_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_527.ISO63362006MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _527

        return self.__parent__._cast(_527.ISO63362006MeshSingleFlankRating)

    @property
    def iso63362019_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_529.ISO63362019MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _529

        return self.__parent__._cast(_529.ISO63362019MeshSingleFlankRating)

    @property
    def iso6336_abstract_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_531.ISO6336AbstractMeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _531

        return self.__parent__._cast(_531.ISO6336AbstractMeshSingleFlankRating)

    @property
    def iso6336_abstract_metal_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_533.ISO6336AbstractMetalMeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _533

        return self.__parent__._cast(_533.ISO6336AbstractMetalMeshSingleFlankRating)

    @property
    def din3990_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_546.DIN3990MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.din3990 import _546

        return self.__parent__._cast(_546.DIN3990MeshSingleFlankRating)

    @property
    def agma2101_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_548.AGMA2101MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.agma import _548

        return self.__parent__._cast(_548.AGMA2101MeshSingleFlankRating)

    @property
    def cylindrical_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "CylindricalMeshSingleFlankRating":
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
class CylindricalMeshSingleFlankRating(_379.MeshSingleFlankRating):
    """CylindricalMeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_MESH_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def active_length_of_the_line_of_action(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveLengthOfTheLineOfAction")

        if temp is None:
            return 0.0

        return temp

    @property
    def axial_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    def axial_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialForce")

        if temp is None:
            return 0.0

        return temp

    @property
    def centre_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CentreDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    def coefficient_of_friction_method_flash_temperature_method(
        self: "Self",
    ) -> "_1105.ScuffingCoefficientOfFrictionMethods":
        """mastapy.gears.gear_designs.cylindrical.ScuffingCoefficientOfFrictionMethods

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CoefficientOfFrictionMethodFlashTemperatureMethod"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.ScuffingCoefficientOfFrictionMethods",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1105",
            "ScuffingCoefficientOfFrictionMethods",
        )(value)

    @property
    def contact_ratio_source(self: "Self") -> "_333.ContactRatioDataSource":
        """mastapy.gears.ContactRatioDataSource

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactRatioSource")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.ContactRatioDataSource"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._333", "ContactRatioDataSource"
        )(value)

    @property
    def duration(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Duration")

        if temp is None:
            return 0.0

        return temp

    @property
    def dynamic_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def effective_arithmetic_mean_roughness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectiveArithmeticMeanRoughness")

        if temp is None:
            return 0.0

        return temp

    @property
    def effective_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectiveFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    def elasticity_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElasticityFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def equivalent_misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EquivalentMisalignment")

        if temp is None:
            return 0.0

        return temp

    @property
    def face_load_factor_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceLoadFactorContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def face_load_factor_contact_source(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceLoadFactorContactSource")

        if temp is None:
            return ""

        return temp

    @property
    def gear_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    def line_of_action_parameter_of_maximum_flash_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LineOfActionParameterOfMaximumFlashTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def load_case(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCase")

        if temp is None:
            return ""

        return temp

    @property
    def load_sharing_factor_of_maximum_flash_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LoadSharingFactorOfMaximumFlashTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def lubricant_dynamic_viscosity_at_tooth_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LubricantDynamicViscosityAtToothTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_contact_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumContactTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_flash_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumFlashTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    def mean_coefficient_of_friction_calculated_constant_flash_temperature_method(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "MeanCoefficientOfFrictionCalculatedConstantFlashTemperatureMethod",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def mean_coefficient_of_friction_of_maximum_flash_temperature(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeanCoefficientOfFrictionOfMaximumFlashTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_dynamic_factor_for_wind_turbine_applications(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumDynamicFactorForWindTurbineApplications"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_face_load_factor_for_contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumFaceLoadFactorForContactStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def misalignment_source(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MisalignmentSource")

        if temp is None:
            return ""

        return temp

    @property
    def nominal_axial_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalAxialForce")

        if temp is None:
            return 0.0

        return temp

    @property
    def nominal_radial_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalRadialLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    def nominal_tangential_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalTangentialLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    def nominal_transverse_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalTransverseLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    def operating_normal_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OperatingNormalPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def pinion_roll_angle_at_highest_point_of_single_tooth_contact(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PinionRollAngleAtHighestPointOfSingleToothContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def pitch_line_velocity_at_operating_pitch_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PitchLineVelocityAtOperatingPitchDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def radial_separating_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadialSeparatingLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    def reduced_modulus_of_elasticity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReducedModulusOfElasticity")

        if temp is None:
            return 0.0

        return temp

    @property
    def roll_angle_of_maximum_flash_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RollAngleOfMaximumFlashTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def scuffing_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ScuffingTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    def signed_gear_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SignedGearRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    def slideto_roll_ratio_at_end_of_active_profile(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SlidetoRollRatioAtEndOfActiveProfile"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def slideto_roll_ratio_at_pitch_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlidetoRollRatioAtPitchPoint")

        if temp is None:
            return 0.0

        return temp

    @property
    def slideto_roll_ratio_at_start_of_active_profile(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SlidetoRollRatioAtStartOfActiveProfile"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def sump_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SumpTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    def tangential_velocity_at_reference_cylinder(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TangentialVelocityAtReferenceCylinder"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def transmitted_tangential_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransmittedTangentialLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    def transverse_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    def transverse_load_factor_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseLoadFactorContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def user_specified_coefficient_of_friction_flash_temperature_method(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "UserSpecifiedCoefficientOfFrictionFlashTemperatureMethod"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def virtual_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VirtualContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    def welding_structural_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WeldingStructuralFactor")

        if temp is None:
            return 0.0

        return temp

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
    def rating_settings(
        self: "Self",
    ) -> "_467.CylindricalGearDesignAndRatingSettingsItem":
        """mastapy.gears.rating.cylindrical.CylindricalGearDesignAndRatingSettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatingSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def scuffing(self: "Self") -> "_1104.Scuffing":
        """mastapy.gears.gear_designs.cylindrical.Scuffing

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Scuffing")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def sorted_scuffing_results(self: "Self") -> "_475.CylindricalGearScuffingResults":
        """mastapy.gears.rating.cylindrical.CylindricalGearScuffingResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SortedScuffingResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def sorted_scuffing_results_without_special_values(
        self: "Self",
    ) -> "_475.CylindricalGearScuffingResults":
        """mastapy.gears.rating.cylindrical.CylindricalGearScuffingResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SortedScuffingResultsWithoutSpecialValues"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gear_single_flank_ratings(
        self: "Self",
    ) -> "List[_478.CylindricalGearSingleFlankRating]":
        """List[mastapy.gears.rating.cylindrical.CylindricalGearSingleFlankRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSingleFlankRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalMeshSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_CylindricalMeshSingleFlankRating
        """
        return _Cast_CylindricalMeshSingleFlankRating(self)
