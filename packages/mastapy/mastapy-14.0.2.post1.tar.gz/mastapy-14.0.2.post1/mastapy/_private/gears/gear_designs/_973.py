"""GearDesign"""

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

_GEAR_DESIGN = python_net_import("SMT.MastaAPI.Gears.GearDesigns", "GearDesign")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.fe_model import _1237
    from mastapy._private.gears.gear_designs.agma_gleason_conical import _1233
    from mastapy._private.gears.gear_designs.bevel import _1220
    from mastapy._private.gears.gear_designs.concept import _1216
    from mastapy._private.gears.gear_designs.conical import _1194
    from mastapy._private.gears.gear_designs.cylindrical import _1044, _1074
    from mastapy._private.gears.gear_designs.face import _1015, _1020, _1023
    from mastapy._private.gears.gear_designs.hypoid import _1011
    from mastapy._private.gears.gear_designs.klingelnberg_conical import _1007
    from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1003
    from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _999
    from mastapy._private.gears.gear_designs.spiral_bevel import _995
    from mastapy._private.gears.gear_designs.straight_bevel import _987
    from mastapy._private.gears.gear_designs.straight_bevel_diff import _991
    from mastapy._private.gears.gear_designs.worm import _982, _983, _986
    from mastapy._private.gears.gear_designs.zerol_bevel import _978

    Self = TypeVar("Self", bound="GearDesign")
    CastSelf = TypeVar("CastSelf", bound="GearDesign._Cast_GearDesign")


__docformat__ = "restructuredtext en"
__all__ = ("GearDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearDesign:
    """Special nested class for casting GearDesign to subclasses."""

    __parent__: "GearDesign"

    @property
    def gear_design_component(self: "CastSelf") -> "_974.GearDesignComponent":
        return self.__parent__._cast(_974.GearDesignComponent)

    @property
    def zerol_bevel_gear_design(self: "CastSelf") -> "_978.ZerolBevelGearDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _978

        return self.__parent__._cast(_978.ZerolBevelGearDesign)

    @property
    def worm_design(self: "CastSelf") -> "_982.WormDesign":
        from mastapy._private.gears.gear_designs.worm import _982

        return self.__parent__._cast(_982.WormDesign)

    @property
    def worm_gear_design(self: "CastSelf") -> "_983.WormGearDesign":
        from mastapy._private.gears.gear_designs.worm import _983

        return self.__parent__._cast(_983.WormGearDesign)

    @property
    def worm_wheel_design(self: "CastSelf") -> "_986.WormWheelDesign":
        from mastapy._private.gears.gear_designs.worm import _986

        return self.__parent__._cast(_986.WormWheelDesign)

    @property
    def straight_bevel_gear_design(self: "CastSelf") -> "_987.StraightBevelGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _987

        return self.__parent__._cast(_987.StraightBevelGearDesign)

    @property
    def straight_bevel_diff_gear_design(
        self: "CastSelf",
    ) -> "_991.StraightBevelDiffGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _991

        return self.__parent__._cast(_991.StraightBevelDiffGearDesign)

    @property
    def spiral_bevel_gear_design(self: "CastSelf") -> "_995.SpiralBevelGearDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _995

        return self.__parent__._cast(_995.SpiralBevelGearDesign)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_design(
        self: "CastSelf",
    ) -> "_999.KlingelnbergCycloPalloidSpiralBevelGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _999

        return self.__parent__._cast(_999.KlingelnbergCycloPalloidSpiralBevelGearDesign)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_design(
        self: "CastSelf",
    ) -> "_1003.KlingelnbergCycloPalloidHypoidGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1003

        return self.__parent__._cast(_1003.KlingelnbergCycloPalloidHypoidGearDesign)

    @property
    def klingelnberg_conical_gear_design(
        self: "CastSelf",
    ) -> "_1007.KlingelnbergConicalGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_conical import _1007

        return self.__parent__._cast(_1007.KlingelnbergConicalGearDesign)

    @property
    def hypoid_gear_design(self: "CastSelf") -> "_1011.HypoidGearDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1011

        return self.__parent__._cast(_1011.HypoidGearDesign)

    @property
    def face_gear_design(self: "CastSelf") -> "_1015.FaceGearDesign":
        from mastapy._private.gears.gear_designs.face import _1015

        return self.__parent__._cast(_1015.FaceGearDesign)

    @property
    def face_gear_pinion_design(self: "CastSelf") -> "_1020.FaceGearPinionDesign":
        from mastapy._private.gears.gear_designs.face import _1020

        return self.__parent__._cast(_1020.FaceGearPinionDesign)

    @property
    def face_gear_wheel_design(self: "CastSelf") -> "_1023.FaceGearWheelDesign":
        from mastapy._private.gears.gear_designs.face import _1023

        return self.__parent__._cast(_1023.FaceGearWheelDesign)

    @property
    def cylindrical_gear_design(self: "CastSelf") -> "_1044.CylindricalGearDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1044

        return self.__parent__._cast(_1044.CylindricalGearDesign)

    @property
    def cylindrical_planet_gear_design(
        self: "CastSelf",
    ) -> "_1074.CylindricalPlanetGearDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1074

        return self.__parent__._cast(_1074.CylindricalPlanetGearDesign)

    @property
    def conical_gear_design(self: "CastSelf") -> "_1194.ConicalGearDesign":
        from mastapy._private.gears.gear_designs.conical import _1194

        return self.__parent__._cast(_1194.ConicalGearDesign)

    @property
    def concept_gear_design(self: "CastSelf") -> "_1216.ConceptGearDesign":
        from mastapy._private.gears.gear_designs.concept import _1216

        return self.__parent__._cast(_1216.ConceptGearDesign)

    @property
    def bevel_gear_design(self: "CastSelf") -> "_1220.BevelGearDesign":
        from mastapy._private.gears.gear_designs.bevel import _1220

        return self.__parent__._cast(_1220.BevelGearDesign)

    @property
    def agma_gleason_conical_gear_design(
        self: "CastSelf",
    ) -> "_1233.AGMAGleasonConicalGearDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1233

        return self.__parent__._cast(_1233.AGMAGleasonConicalGearDesign)

    @property
    def gear_design(self: "CastSelf") -> "GearDesign":
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
class GearDesign(_974.GearDesignComponent):
    """GearDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def absolute_shaft_inner_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AbsoluteShaftInnerDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def face_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FaceWidth")

        if temp is None:
            return 0.0

        return temp

    @face_width.setter
    @enforce_parameter_types
    def face_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FaceWidth", float(value) if value is not None else 0.0
        )

    @property
    def mass(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Mass")

        if temp is None:
            return 0.0

        return temp

    @property
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def names_of_meshing_gears(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NamesOfMeshingGears")

        if temp is None:
            return ""

        return temp

    @property
    def number_of_teeth(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @number_of_teeth.setter
    @enforce_parameter_types
    def number_of_teeth(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfTeeth", int(value) if value is not None else 0
        )

    @property
    def number_of_teeth_maintaining_ratio(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeethMaintainingRatio")

        if temp is None:
            return 0

        return temp

    @number_of_teeth_maintaining_ratio.setter
    @enforce_parameter_types
    def number_of_teeth_maintaining_ratio(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfTeethMaintainingRatio",
            int(value) if value is not None else 0,
        )

    @property
    def shaft_inner_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftInnerDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def shaft_outer_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftOuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def tifffe_model(self: "Self") -> "_1237.GearFEModel":
        """mastapy.gears.fe_model.GearFEModel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TIFFFEModel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearDesign":
        """Cast to another type.

        Returns:
            _Cast_GearDesign
        """
        return _Cast_GearDesign(self)
