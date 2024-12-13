"""AbstractGearRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.analysis import _1255

_ABSTRACT_GEAR_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating", "AbstractGearRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _370, _374
    from mastapy._private.gears.rating.agma_gleason_conical import _579
    from mastapy._private.gears.rating.bevel import _568
    from mastapy._private.gears.rating.concept import _561, _564
    from mastapy._private.gears.rating.conical import _551, _553
    from mastapy._private.gears.rating.cylindrical import _468, _473
    from mastapy._private.gears.rating.face import _458, _461
    from mastapy._private.gears.rating.hypoid import _452
    from mastapy._private.gears.rating.klingelnberg_conical import _425
    from mastapy._private.gears.rating.klingelnberg_hypoid import _422
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _419
    from mastapy._private.gears.rating.spiral_bevel import _416
    from mastapy._private.gears.rating.straight_bevel import _409
    from mastapy._private.gears.rating.straight_bevel_diff import _412
    from mastapy._private.gears.rating.worm import _385, _387
    from mastapy._private.gears.rating.zerol_bevel import _383

    Self = TypeVar("Self", bound="AbstractGearRating")
    CastSelf = TypeVar("CastSelf", bound="AbstractGearRating._Cast_AbstractGearRating")


__docformat__ = "restructuredtext en"
__all__ = ("AbstractGearRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractGearRating:
    """Special nested class for casting AbstractGearRating to subclasses."""

    __parent__: "AbstractGearRating"

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1255.AbstractGearAnalysis":
        return self.__parent__._cast(_1255.AbstractGearAnalysis)

    @property
    def gear_duty_cycle_rating(self: "CastSelf") -> "_370.GearDutyCycleRating":
        from mastapy._private.gears.rating import _370

        return self.__parent__._cast(_370.GearDutyCycleRating)

    @property
    def gear_rating(self: "CastSelf") -> "_374.GearRating":
        from mastapy._private.gears.rating import _374

        return self.__parent__._cast(_374.GearRating)

    @property
    def zerol_bevel_gear_rating(self: "CastSelf") -> "_383.ZerolBevelGearRating":
        from mastapy._private.gears.rating.zerol_bevel import _383

        return self.__parent__._cast(_383.ZerolBevelGearRating)

    @property
    def worm_gear_duty_cycle_rating(self: "CastSelf") -> "_385.WormGearDutyCycleRating":
        from mastapy._private.gears.rating.worm import _385

        return self.__parent__._cast(_385.WormGearDutyCycleRating)

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
    def face_gear_duty_cycle_rating(self: "CastSelf") -> "_458.FaceGearDutyCycleRating":
        from mastapy._private.gears.rating.face import _458

        return self.__parent__._cast(_458.FaceGearDutyCycleRating)

    @property
    def face_gear_rating(self: "CastSelf") -> "_461.FaceGearRating":
        from mastapy._private.gears.rating.face import _461

        return self.__parent__._cast(_461.FaceGearRating)

    @property
    def cylindrical_gear_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_468.CylindricalGearDutyCycleRating":
        from mastapy._private.gears.rating.cylindrical import _468

        return self.__parent__._cast(_468.CylindricalGearDutyCycleRating)

    @property
    def cylindrical_gear_rating(self: "CastSelf") -> "_473.CylindricalGearRating":
        from mastapy._private.gears.rating.cylindrical import _473

        return self.__parent__._cast(_473.CylindricalGearRating)

    @property
    def conical_gear_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_551.ConicalGearDutyCycleRating":
        from mastapy._private.gears.rating.conical import _551

        return self.__parent__._cast(_551.ConicalGearDutyCycleRating)

    @property
    def conical_gear_rating(self: "CastSelf") -> "_553.ConicalGearRating":
        from mastapy._private.gears.rating.conical import _553

        return self.__parent__._cast(_553.ConicalGearRating)

    @property
    def concept_gear_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_561.ConceptGearDutyCycleRating":
        from mastapy._private.gears.rating.concept import _561

        return self.__parent__._cast(_561.ConceptGearDutyCycleRating)

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
    def abstract_gear_rating(self: "CastSelf") -> "AbstractGearRating":
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
class AbstractGearRating(_1255.AbstractGearAnalysis):
    """AbstractGearRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_GEAR_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def bending_safety_factor_for_fatigue(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BendingSafetyFactorForFatigue")

        if temp is None:
            return 0.0

        return temp

    @property
    def bending_safety_factor_for_static(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BendingSafetyFactorForStatic")

        if temp is None:
            return 0.0

        return temp

    @property
    def contact_safety_factor_for_fatigue(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactSafetyFactorForFatigue")

        if temp is None:
            return 0.0

        return temp

    @property
    def contact_safety_factor_for_static(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactSafetyFactorForStatic")

        if temp is None:
            return 0.0

        return temp

    @property
    def cycles_to_fail(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CyclesToFail")

        if temp is None:
            return 0.0

        return temp

    @property
    def cycles_to_fail_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CyclesToFailBending")

        if temp is None:
            return 0.0

        return temp

    @property
    def cycles_to_fail_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CyclesToFailContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def damage_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DamageBending")

        if temp is None:
            return 0.0

        return temp

    @property
    def damage_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DamageContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def gear_reliability_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearReliabilityBending")

        if temp is None:
            return 0.0

        return temp

    @property
    def gear_reliability_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearReliabilityContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def normalised_bending_safety_factor_for_fatigue(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NormalisedBendingSafetyFactorForFatigue"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def normalised_bending_safety_factor_for_static(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NormalisedBendingSafetyFactorForStatic"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def normalised_contact_safety_factor_for_fatigue(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NormalisedContactSafetyFactorForFatigue"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def normalised_contact_safety_factor_for_static(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NormalisedContactSafetyFactorForStatic"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def normalised_safety_factor_for_fatigue(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalisedSafetyFactorForFatigue")

        if temp is None:
            return 0.0

        return temp

    @property
    def normalised_safety_factor_for_static(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalisedSafetyFactorForStatic")

        if temp is None:
            return 0.0

        return temp

    @property
    def time_to_fail(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeToFail")

        if temp is None:
            return 0.0

        return temp

    @property
    def time_to_fail_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeToFailBending")

        if temp is None:
            return 0.0

        return temp

    @property
    def time_to_fail_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeToFailContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def total_gear_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalGearReliability")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractGearRating":
        """Cast to another type.

        Returns:
            _Cast_AbstractGearRating
        """
        return _Cast_AbstractGearRating(self)
