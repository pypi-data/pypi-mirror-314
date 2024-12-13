"""KlingelnbergCycloPalloidSpiralBevelGearSetDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.klingelnberg_conical import _1009

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.KlingelnbergSpiralBevel",
    "KlingelnbergCycloPalloidSpiralBevelGearSetDesign",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs import _974, _976
    from mastapy._private.gears.gear_designs.conical import _1196
    from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import (
        _999,
        _1000,
    )

    Self = TypeVar("Self", bound="KlingelnbergCycloPalloidSpiralBevelGearSetDesign")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidSpiralBevelGearSetDesign._Cast_KlingelnbergCycloPalloidSpiralBevelGearSetDesign",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidSpiralBevelGearSetDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidSpiralBevelGearSetDesign:
    """Special nested class for casting KlingelnbergCycloPalloidSpiralBevelGearSetDesign to subclasses."""

    __parent__: "KlingelnbergCycloPalloidSpiralBevelGearSetDesign"

    @property
    def klingelnberg_conical_gear_set_design(
        self: "CastSelf",
    ) -> "_1009.KlingelnbergConicalGearSetDesign":
        return self.__parent__._cast(_1009.KlingelnbergConicalGearSetDesign)

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
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidSpiralBevelGearSetDesign":
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
class KlingelnbergCycloPalloidSpiralBevelGearSetDesign(
    _1009.KlingelnbergConicalGearSetDesign
):
    """KlingelnbergCycloPalloidSpiralBevelGearSetDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def circular_pitch(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CircularPitch")

        if temp is None:
            return 0.0

        return temp

    @property
    def cutter_blade_tip_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CutterBladeTipWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    def cutter_tooth_fillet_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CutterToothFilletRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    def face_contact_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceContactAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def face_width_normal_module(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceWidthNormalModule")

        if temp is None:
            return 0.0

        return temp

    @property
    def hw(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HW")

        if temp is None:
            return 0.0

        return temp

    @property
    def helix_angle_at_base_circle_of_virtual_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HelixAngleAtBaseCircleOfVirtualGear"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def mean_normal_module(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MeanNormalModule")

        if temp is None:
            return 0.0

        return temp

    @mean_normal_module.setter
    @enforce_parameter_types
    def mean_normal_module(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MeanNormalModule", float(value) if value is not None else 0.0
        )

    @property
    def mean_transverse_module(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanTransverseModule")

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_addendum_modification_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumAddendumModificationFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def normal_pressure_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NormalPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @normal_pressure_angle.setter
    @enforce_parameter_types
    def normal_pressure_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalPressureAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    def number_of_teeth_of_crown_wheel(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeethOfCrownWheel")

        if temp is None:
            return 0.0

        return temp

    @property
    def outer_cone_distance_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterConeDistanceFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    def partial_contact_ratio_of_virtual_pinion_teeth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PartialContactRatioOfVirtualPinionTeeth"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def partial_contact_ratio_of_virtual_wheel_teeth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PartialContactRatioOfVirtualWheelTeeth"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def profile_contact_ratio_in_transverse_section(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ProfileContactRatioInTransverseSection"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def settling_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SettlingAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def tooth_tip_width_for_reduction(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothTipWidthForReduction")

        if temp is None:
            return 0.0

        return temp

    @property
    def transverse_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransversePressureAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def virtual_number_of_pinion_teeth_at_mean_cone_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "VirtualNumberOfPinionTeethAtMeanConeDistance"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def virtual_number_of_wheel_teeth_at_mean_cone_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "VirtualNumberOfWheelTeethAtMeanConeDistance"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def virtual_number_of_teeth_on_inside_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "VirtualNumberOfTeethOnInsideDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def wheel_inner_cone_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelInnerConeDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    def width_of_tooth_tip_chamfer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WidthOfToothTipChamfer")

        if temp is None:
            return 0.0

        return temp

    @property
    def gears(
        self: "Self",
    ) -> "List[_999.KlingelnbergCycloPalloidSpiralBevelGearDesign]":
        """List[mastapy.gears.gear_designs.klingelnberg_spiral_bevel.KlingelnbergCycloPalloidSpiralBevelGearDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Gears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears(
        self: "Self",
    ) -> "List[_999.KlingelnbergCycloPalloidSpiralBevelGearDesign]":
        """List[mastapy.gears.gear_designs.klingelnberg_spiral_bevel.KlingelnbergCycloPalloidSpiralBevelGearDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidSpiralBevelGears"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_conical_meshes(
        self: "Self",
    ) -> "List[_1000.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign]":
        """List[mastapy.gears.gear_designs.klingelnberg_spiral_bevel.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KlingelnbergConicalMeshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes(
        self: "Self",
    ) -> "List[_1000.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign]":
        """List[mastapy.gears.gear_designs.klingelnberg_spiral_bevel.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidSpiralBevelMeshes"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_KlingelnbergCycloPalloidSpiralBevelGearSetDesign":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidSpiralBevelGearSetDesign
        """
        return _Cast_KlingelnbergCycloPalloidSpiralBevelGearSetDesign(self)
