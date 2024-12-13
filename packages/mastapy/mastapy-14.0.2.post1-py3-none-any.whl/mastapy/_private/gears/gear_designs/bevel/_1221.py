"""BevelGearMeshDesign"""

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
from mastapy._private.gears.gear_designs.agma_gleason_conical import _1234

_BEVEL_GEAR_MESH_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Bevel", "BevelGearMeshDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs import _974, _975
    from mastapy._private.gears.gear_designs.conical import _1195
    from mastapy._private.gears.gear_designs.spiral_bevel import _996
    from mastapy._private.gears.gear_designs.straight_bevel import _988
    from mastapy._private.gears.gear_designs.straight_bevel_diff import _992
    from mastapy._private.gears.gear_designs.zerol_bevel import _979

    Self = TypeVar("Self", bound="BevelGearMeshDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="BevelGearMeshDesign._Cast_BevelGearMeshDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearMeshDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearMeshDesign:
    """Special nested class for casting BevelGearMeshDesign to subclasses."""

    __parent__: "BevelGearMeshDesign"

    @property
    def agma_gleason_conical_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1234.AGMAGleasonConicalGearMeshDesign":
        return self.__parent__._cast(_1234.AGMAGleasonConicalGearMeshDesign)

    @property
    def conical_gear_mesh_design(self: "CastSelf") -> "_1195.ConicalGearMeshDesign":
        from mastapy._private.gears.gear_designs.conical import _1195

        return self.__parent__._cast(_1195.ConicalGearMeshDesign)

    @property
    def gear_mesh_design(self: "CastSelf") -> "_975.GearMeshDesign":
        from mastapy._private.gears.gear_designs import _975

        return self.__parent__._cast(_975.GearMeshDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_974.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _974

        return self.__parent__._cast(_974.GearDesignComponent)

    @property
    def zerol_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_979.ZerolBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _979

        return self.__parent__._cast(_979.ZerolBevelGearMeshDesign)

    @property
    def straight_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_988.StraightBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _988

        return self.__parent__._cast(_988.StraightBevelGearMeshDesign)

    @property
    def straight_bevel_diff_gear_mesh_design(
        self: "CastSelf",
    ) -> "_992.StraightBevelDiffGearMeshDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _992

        return self.__parent__._cast(_992.StraightBevelDiffGearMeshDesign)

    @property
    def spiral_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_996.SpiralBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _996

        return self.__parent__._cast(_996.SpiralBevelGearMeshDesign)

    @property
    def bevel_gear_mesh_design(self: "CastSelf") -> "BevelGearMeshDesign":
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
class BevelGearMeshDesign(_1234.AGMAGleasonConicalGearMeshDesign):
    """BevelGearMeshDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_MESH_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def contact_effective_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactEffectiveFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    def contact_wheel_inner_cone_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactWheelInnerConeDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    def contact_wheel_mean_cone_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactWheelMeanConeDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    def contact_wheel_outer_cone_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactWheelOuterConeDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    def face_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    def geometry_factor_g(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeometryFactorG")

        if temp is None:
            return 0.0

        return temp

    @property
    def geometry_factor_i(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeometryFactorI")

        if temp is None:
            return 0.0

        return temp

    @property
    def ideal_pinion_pitch_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IdealPinionPitchAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def ideal_wheel_pitch_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IdealWheelPitchAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def inertia_factor_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InertiaFactorBending")

        if temp is None:
            return 0.0

        return temp

    @property
    def inertia_factor_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InertiaFactorContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def is_topland_balanced(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsToplandBalanced")

        if temp is None:
            return False

        return temp

    @property
    def length_of_line_of_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LengthOfLineOfContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def load_sharing_ratio_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadSharingRatioContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def load_sharing_ratio_scoring(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadSharingRatioScoring")

        if temp is None:
            return 0.0

        return temp

    @property
    def modified_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModifiedContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    def pinion_face_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionFaceAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def pinion_inner_dedendum(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionInnerDedendum")

        if temp is None:
            return 0.0

        return temp

    @property
    def pinion_inner_dedendum_limit(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionInnerDedendumLimit")

        if temp is None:
            return 0.0

        return temp

    @property
    def pinion_passed_undercut_check(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionPassedUndercutCheck")

        if temp is None:
            return False

        return temp

    @property
    def pinion_pitch_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionPitchAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def pinion_pitch_angle_modification(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PinionPitchAngleModification")

        if temp is None:
            return 0.0

        return temp

    @pinion_pitch_angle_modification.setter
    @enforce_parameter_types
    def pinion_pitch_angle_modification(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PinionPitchAngleModification",
            float(value) if value is not None else 0.0,
        )

    @property
    def pinion_root_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionRootAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def pinion_thickness_modification_coefficient_backlash_included(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PinionThicknessModificationCoefficientBacklashIncluded"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def pitting_resistance_geometry_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PittingResistanceGeometryFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def strength_balance_agma_coast(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StrengthBalanceAGMACoast")

        if temp is None:
            return 0.0

        return temp

    @property
    def strength_balance_agma_drive(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StrengthBalanceAGMADrive")

        if temp is None:
            return 0.0

        return temp

    @property
    def strength_balance_gleason_coast(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StrengthBalanceGleasonCoast")

        if temp is None:
            return 0.0

        return temp

    @property
    def strength_balance_gleason_drive(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StrengthBalanceGleasonDrive")

        if temp is None:
            return 0.0

        return temp

    @property
    def strength_balance_obtained_coast(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StrengthBalanceObtainedCoast")

        if temp is None:
            return 0.0

        return temp

    @property
    def strength_balance_obtained_drive(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StrengthBalanceObtainedDrive")

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
    def wheel_face_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelFaceAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def wheel_pitch_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelPitchAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def wheel_pitch_angle_modification(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WheelPitchAngleModification")

        if temp is None:
            return 0.0

        return temp

    @wheel_pitch_angle_modification.setter
    @enforce_parameter_types
    def wheel_pitch_angle_modification(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WheelPitchAngleModification",
            float(value) if value is not None else 0.0,
        )

    @property
    def wheel_root_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelRootAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def wheel_spiral_angle_at_contact_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelSpiralAngleAtContactOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    def wheel_thickness_modification_coefficient_backlash_included(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WheelThicknessModificationCoefficientBacklashIncluded"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_BevelGearMeshDesign":
        """Cast to another type.

        Returns:
            _Cast_BevelGearMeshDesign
        """
        return _Cast_BevelGearMeshDesign(self)
