"""GearMeshDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs import _974

_GEAR_MESH_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns", "GearMeshDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs import _973
    from mastapy._private.gears.gear_designs.agma_gleason_conical import _1234
    from mastapy._private.gears.gear_designs.bevel import _1221
    from mastapy._private.gears.gear_designs.concept import _1217
    from mastapy._private.gears.gear_designs.conical import _1195
    from mastapy._private.gears.gear_designs.cylindrical import _1050
    from mastapy._private.gears.gear_designs.face import _1017
    from mastapy._private.gears.gear_designs.hypoid import _1012
    from mastapy._private.gears.gear_designs.klingelnberg_conical import _1008
    from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1004
    from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1000
    from mastapy._private.gears.gear_designs.spiral_bevel import _996
    from mastapy._private.gears.gear_designs.straight_bevel import _988
    from mastapy._private.gears.gear_designs.straight_bevel_diff import _992
    from mastapy._private.gears.gear_designs.worm import _984
    from mastapy._private.gears.gear_designs.zerol_bevel import _979

    Self = TypeVar("Self", bound="GearMeshDesign")
    CastSelf = TypeVar("CastSelf", bound="GearMeshDesign._Cast_GearMeshDesign")


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshDesign:
    """Special nested class for casting GearMeshDesign to subclasses."""

    __parent__: "GearMeshDesign"

    @property
    def gear_design_component(self: "CastSelf") -> "_974.GearDesignComponent":
        return self.__parent__._cast(_974.GearDesignComponent)

    @property
    def zerol_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_979.ZerolBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _979

        return self.__parent__._cast(_979.ZerolBevelGearMeshDesign)

    @property
    def worm_gear_mesh_design(self: "CastSelf") -> "_984.WormGearMeshDesign":
        from mastapy._private.gears.gear_designs.worm import _984

        return self.__parent__._cast(_984.WormGearMeshDesign)

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
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1000.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1000

        return self.__parent__._cast(
            _1000.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1004.KlingelnbergCycloPalloidHypoidGearMeshDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1004

        return self.__parent__._cast(_1004.KlingelnbergCycloPalloidHypoidGearMeshDesign)

    @property
    def klingelnberg_conical_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1008.KlingelnbergConicalGearMeshDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_conical import _1008

        return self.__parent__._cast(_1008.KlingelnbergConicalGearMeshDesign)

    @property
    def hypoid_gear_mesh_design(self: "CastSelf") -> "_1012.HypoidGearMeshDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1012

        return self.__parent__._cast(_1012.HypoidGearMeshDesign)

    @property
    def face_gear_mesh_design(self: "CastSelf") -> "_1017.FaceGearMeshDesign":
        from mastapy._private.gears.gear_designs.face import _1017

        return self.__parent__._cast(_1017.FaceGearMeshDesign)

    @property
    def cylindrical_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1050.CylindricalGearMeshDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1050

        return self.__parent__._cast(_1050.CylindricalGearMeshDesign)

    @property
    def conical_gear_mesh_design(self: "CastSelf") -> "_1195.ConicalGearMeshDesign":
        from mastapy._private.gears.gear_designs.conical import _1195

        return self.__parent__._cast(_1195.ConicalGearMeshDesign)

    @property
    def concept_gear_mesh_design(self: "CastSelf") -> "_1217.ConceptGearMeshDesign":
        from mastapy._private.gears.gear_designs.concept import _1217

        return self.__parent__._cast(_1217.ConceptGearMeshDesign)

    @property
    def bevel_gear_mesh_design(self: "CastSelf") -> "_1221.BevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.bevel import _1221

        return self.__parent__._cast(_1221.BevelGearMeshDesign)

    @property
    def agma_gleason_conical_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1234.AGMAGleasonConicalGearMeshDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1234

        return self.__parent__._cast(_1234.AGMAGleasonConicalGearMeshDesign)

    @property
    def gear_mesh_design(self: "CastSelf") -> "GearMeshDesign":
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
class GearMeshDesign(_974.GearDesignComponent):
    """GearMeshDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def axial_contact_ratio_rating_for_nvh(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialContactRatioRatingForNVH")

        if temp is None:
            return 0.0

        return temp

    @property
    def has_hunting_ratio(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HasHuntingRatio")

        if temp is None:
            return False

        return temp

    @property
    def highest_common_factor_of_teeth_numbers(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HighestCommonFactorOfTeethNumbers")

        if temp is None:
            return 0

        return temp

    @property
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    def speed_ratio_a_to_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpeedRatioAToB")

        if temp is None:
            return 0.0

        return temp

    @property
    def torque_ratio_a_to_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueRatioAToB")

        if temp is None:
            return 0.0

        return temp

    @property
    def transverse_contact_ratio_rating_for_nvh(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseContactRatioRatingForNVH"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def transverse_and_axial_contact_ratio_rating_for_nvh(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseAndAxialContactRatioRatingForNVH"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def gear_a(self: "Self") -> "_973.GearDesign":
        """mastapy.gears.gear_designs.GearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearA")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gear_b(self: "Self") -> "_973.GearDesign":
        """mastapy.gears.gear_designs.GearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearB")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshDesign":
        """Cast to another type.

        Returns:
            _Cast_GearMeshDesign
        """
        return _Cast_GearMeshDesign(self)
