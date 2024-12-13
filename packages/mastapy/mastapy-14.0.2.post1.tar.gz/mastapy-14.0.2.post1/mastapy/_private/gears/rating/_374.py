"""GearRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating import _366

_GEAR_RATING = python_net_import("SMT.MastaAPI.Gears.Rating", "GearRating")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1255
    from mastapy._private.gears.rating import _368
    from mastapy._private.gears.rating.agma_gleason_conical import _579
    from mastapy._private.gears.rating.bevel import _568
    from mastapy._private.gears.rating.concept import _564
    from mastapy._private.gears.rating.conical import _553
    from mastapy._private.gears.rating.cylindrical import _473
    from mastapy._private.gears.rating.face import _461
    from mastapy._private.gears.rating.hypoid import _452
    from mastapy._private.gears.rating.klingelnberg_conical import _425
    from mastapy._private.gears.rating.klingelnberg_hypoid import _422
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _419
    from mastapy._private.gears.rating.spiral_bevel import _416
    from mastapy._private.gears.rating.straight_bevel import _409
    from mastapy._private.gears.rating.straight_bevel_diff import _412
    from mastapy._private.gears.rating.worm import _387
    from mastapy._private.gears.rating.zerol_bevel import _383
    from mastapy._private.materials import _293

    Self = TypeVar("Self", bound="GearRating")
    CastSelf = TypeVar("CastSelf", bound="GearRating._Cast_GearRating")


__docformat__ = "restructuredtext en"
__all__ = ("GearRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearRating:
    """Special nested class for casting GearRating to subclasses."""

    __parent__: "GearRating"

    @property
    def abstract_gear_rating(self: "CastSelf") -> "_366.AbstractGearRating":
        return self.__parent__._cast(_366.AbstractGearRating)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1255.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1255

        return self.__parent__._cast(_1255.AbstractGearAnalysis)

    @property
    def zerol_bevel_gear_rating(self: "CastSelf") -> "_383.ZerolBevelGearRating":
        from mastapy._private.gears.rating.zerol_bevel import _383

        return self.__parent__._cast(_383.ZerolBevelGearRating)

    @property
    def worm_gear_rating(self: "CastSelf") -> "_387.WormGearRating":
        from mastapy._private.gears.rating.worm import _387

        return self.__parent__._cast(_387.WormGearRating)

    @property
    def straight_bevel_gear_rating(self: "CastSelf") -> "_409.StraightBevelGearRating":
        from mastapy._private.gears.rating.straight_bevel import _409

        return self.__parent__._cast(_409.StraightBevelGearRating)

    @property
    def straight_bevel_diff_gear_rating(
        self: "CastSelf",
    ) -> "_412.StraightBevelDiffGearRating":
        from mastapy._private.gears.rating.straight_bevel_diff import _412

        return self.__parent__._cast(_412.StraightBevelDiffGearRating)

    @property
    def spiral_bevel_gear_rating(self: "CastSelf") -> "_416.SpiralBevelGearRating":
        from mastapy._private.gears.rating.spiral_bevel import _416

        return self.__parent__._cast(_416.SpiralBevelGearRating)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_rating(
        self: "CastSelf",
    ) -> "_419.KlingelnbergCycloPalloidSpiralBevelGearRating":
        from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _419

        return self.__parent__._cast(_419.KlingelnbergCycloPalloidSpiralBevelGearRating)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_rating(
        self: "CastSelf",
    ) -> "_422.KlingelnbergCycloPalloidHypoidGearRating":
        from mastapy._private.gears.rating.klingelnberg_hypoid import _422

        return self.__parent__._cast(_422.KlingelnbergCycloPalloidHypoidGearRating)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_rating(
        self: "CastSelf",
    ) -> "_425.KlingelnbergCycloPalloidConicalGearRating":
        from mastapy._private.gears.rating.klingelnberg_conical import _425

        return self.__parent__._cast(_425.KlingelnbergCycloPalloidConicalGearRating)

    @property
    def hypoid_gear_rating(self: "CastSelf") -> "_452.HypoidGearRating":
        from mastapy._private.gears.rating.hypoid import _452

        return self.__parent__._cast(_452.HypoidGearRating)

    @property
    def face_gear_rating(self: "CastSelf") -> "_461.FaceGearRating":
        from mastapy._private.gears.rating.face import _461

        return self.__parent__._cast(_461.FaceGearRating)

    @property
    def cylindrical_gear_rating(self: "CastSelf") -> "_473.CylindricalGearRating":
        from mastapy._private.gears.rating.cylindrical import _473

        return self.__parent__._cast(_473.CylindricalGearRating)

    @property
    def conical_gear_rating(self: "CastSelf") -> "_553.ConicalGearRating":
        from mastapy._private.gears.rating.conical import _553

        return self.__parent__._cast(_553.ConicalGearRating)

    @property
    def concept_gear_rating(self: "CastSelf") -> "_564.ConceptGearRating":
        from mastapy._private.gears.rating.concept import _564

        return self.__parent__._cast(_564.ConceptGearRating)

    @property
    def bevel_gear_rating(self: "CastSelf") -> "_568.BevelGearRating":
        from mastapy._private.gears.rating.bevel import _568

        return self.__parent__._cast(_568.BevelGearRating)

    @property
    def agma_gleason_conical_gear_rating(
        self: "CastSelf",
    ) -> "_579.AGMAGleasonConicalGearRating":
        from mastapy._private.gears.rating.agma_gleason_conical import _579

        return self.__parent__._cast(_579.AGMAGleasonConicalGearRating)

    @property
    def gear_rating(self: "CastSelf") -> "GearRating":
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
class GearRating(_366.AbstractGearRating):
    """GearRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def bending_safety_factor_results(self: "Self") -> "_293.SafetyFactorItem":
        """mastapy.materials.SafetyFactorItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BendingSafetyFactorResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def contact_safety_factor_results(self: "Self") -> "_293.SafetyFactorItem":
        """mastapy.materials.SafetyFactorItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactSafetyFactorResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def static_safety_factor(self: "Self") -> "_368.BendingAndContactReportingObject":
        """mastapy.gears.rating.BendingAndContactReportingObject

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StaticSafetyFactor")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearRating":
        """Cast to another type.

        Returns:
            _Cast_GearRating
        """
        return _Cast_GearRating(self)
