"""AbstractGearSetRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.analysis import _1257

_ABSTRACT_GEAR_SET_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating", "AbstractGearSetRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears import _340
    from mastapy._private.gears.rating import _365, _366, _375, _376
    from mastapy._private.gears.rating.agma_gleason_conical import _580
    from mastapy._private.gears.rating.bevel import _569
    from mastapy._private.gears.rating.concept import _565, _566
    from mastapy._private.gears.rating.conical import _554, _555
    from mastapy._private.gears.rating.cylindrical import _476, _477, _493
    from mastapy._private.gears.rating.face import _462, _463
    from mastapy._private.gears.rating.hypoid import _453
    from mastapy._private.gears.rating.klingelnberg_conical import _426
    from mastapy._private.gears.rating.klingelnberg_hypoid import _423
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _420
    from mastapy._private.gears.rating.spiral_bevel import _417
    from mastapy._private.gears.rating.straight_bevel import _410
    from mastapy._private.gears.rating.straight_bevel_diff import _413
    from mastapy._private.gears.rating.worm import _388, _389
    from mastapy._private.gears.rating.zerol_bevel import _384

    Self = TypeVar("Self", bound="AbstractGearSetRating")
    CastSelf = TypeVar(
        "CastSelf", bound="AbstractGearSetRating._Cast_AbstractGearSetRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractGearSetRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractGearSetRating:
    """Special nested class for casting AbstractGearSetRating to subclasses."""

    __parent__: "AbstractGearSetRating"

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1257.AbstractGearSetAnalysis":
        return self.__parent__._cast(_1257.AbstractGearSetAnalysis)

    @property
    def gear_set_duty_cycle_rating(self: "CastSelf") -> "_375.GearSetDutyCycleRating":
        from mastapy._private.gears.rating import _375

        return self.__parent__._cast(_375.GearSetDutyCycleRating)

    @property
    def gear_set_rating(self: "CastSelf") -> "_376.GearSetRating":
        from mastapy._private.gears.rating import _376

        return self.__parent__._cast(_376.GearSetRating)

    @property
    def zerol_bevel_gear_set_rating(self: "CastSelf") -> "_384.ZerolBevelGearSetRating":
        from mastapy._private.gears.rating.zerol_bevel import _384

        return self.__parent__._cast(_384.ZerolBevelGearSetRating)

    @property
    def worm_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_388.WormGearSetDutyCycleRating":
        from mastapy._private.gears.rating.worm import _388

        return self.__parent__._cast(_388.WormGearSetDutyCycleRating)

    @property
    def worm_gear_set_rating(self: "CastSelf") -> "_389.WormGearSetRating":
        from mastapy._private.gears.rating.worm import _389

        return self.__parent__._cast(_389.WormGearSetRating)

    @property
    def straight_bevel_gear_set_rating(
        self: "CastSelf",
    ) -> "_410.StraightBevelGearSetRating":
        from mastapy._private.gears.rating.straight_bevel import _410

        return self.__parent__._cast(_410.StraightBevelGearSetRating)

    @property
    def straight_bevel_diff_gear_set_rating(
        self: "CastSelf",
    ) -> "_413.StraightBevelDiffGearSetRating":
        from mastapy._private.gears.rating.straight_bevel_diff import _413

        return self.__parent__._cast(_413.StraightBevelDiffGearSetRating)

    @property
    def spiral_bevel_gear_set_rating(
        self: "CastSelf",
    ) -> "_417.SpiralBevelGearSetRating":
        from mastapy._private.gears.rating.spiral_bevel import _417

        return self.__parent__._cast(_417.SpiralBevelGearSetRating)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_rating(
        self: "CastSelf",
    ) -> "_420.KlingelnbergCycloPalloidSpiralBevelGearSetRating":
        from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _420

        return self.__parent__._cast(
            _420.KlingelnbergCycloPalloidSpiralBevelGearSetRating
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_rating(
        self: "CastSelf",
    ) -> "_423.KlingelnbergCycloPalloidHypoidGearSetRating":
        from mastapy._private.gears.rating.klingelnberg_hypoid import _423

        return self.__parent__._cast(_423.KlingelnbergCycloPalloidHypoidGearSetRating)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_rating(
        self: "CastSelf",
    ) -> "_426.KlingelnbergCycloPalloidConicalGearSetRating":
        from mastapy._private.gears.rating.klingelnberg_conical import _426

        return self.__parent__._cast(_426.KlingelnbergCycloPalloidConicalGearSetRating)

    @property
    def hypoid_gear_set_rating(self: "CastSelf") -> "_453.HypoidGearSetRating":
        from mastapy._private.gears.rating.hypoid import _453

        return self.__parent__._cast(_453.HypoidGearSetRating)

    @property
    def face_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_462.FaceGearSetDutyCycleRating":
        from mastapy._private.gears.rating.face import _462

        return self.__parent__._cast(_462.FaceGearSetDutyCycleRating)

    @property
    def face_gear_set_rating(self: "CastSelf") -> "_463.FaceGearSetRating":
        from mastapy._private.gears.rating.face import _463

        return self.__parent__._cast(_463.FaceGearSetRating)

    @property
    def cylindrical_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_476.CylindricalGearSetDutyCycleRating":
        from mastapy._private.gears.rating.cylindrical import _476

        return self.__parent__._cast(_476.CylindricalGearSetDutyCycleRating)

    @property
    def cylindrical_gear_set_rating(
        self: "CastSelf",
    ) -> "_477.CylindricalGearSetRating":
        from mastapy._private.gears.rating.cylindrical import _477

        return self.__parent__._cast(_477.CylindricalGearSetRating)

    @property
    def reduced_cylindrical_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_493.ReducedCylindricalGearSetDutyCycleRating":
        from mastapy._private.gears.rating.cylindrical import _493

        return self.__parent__._cast(_493.ReducedCylindricalGearSetDutyCycleRating)

    @property
    def conical_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_554.ConicalGearSetDutyCycleRating":
        from mastapy._private.gears.rating.conical import _554

        return self.__parent__._cast(_554.ConicalGearSetDutyCycleRating)

    @property
    def conical_gear_set_rating(self: "CastSelf") -> "_555.ConicalGearSetRating":
        from mastapy._private.gears.rating.conical import _555

        return self.__parent__._cast(_555.ConicalGearSetRating)

    @property
    def concept_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_565.ConceptGearSetDutyCycleRating":
        from mastapy._private.gears.rating.concept import _565

        return self.__parent__._cast(_565.ConceptGearSetDutyCycleRating)

    @property
    def concept_gear_set_rating(self: "CastSelf") -> "_566.ConceptGearSetRating":
        from mastapy._private.gears.rating.concept import _566

        return self.__parent__._cast(_566.ConceptGearSetRating)

    @property
    def bevel_gear_set_rating(self: "CastSelf") -> "_569.BevelGearSetRating":
        from mastapy._private.gears.rating.bevel import _569

        return self.__parent__._cast(_569.BevelGearSetRating)

    @property
    def agma_gleason_conical_gear_set_rating(
        self: "CastSelf",
    ) -> "_580.AGMAGleasonConicalGearSetRating":
        from mastapy._private.gears.rating.agma_gleason_conical import _580

        return self.__parent__._cast(_580.AGMAGleasonConicalGearSetRating)

    @property
    def abstract_gear_set_rating(self: "CastSelf") -> "AbstractGearSetRating":
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
class AbstractGearSetRating(_1257.AbstractGearSetAnalysis):
    """AbstractGearSetRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_GEAR_SET_RATING

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
    def normalised_safety_factor_for_fatigue_and_static(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NormalisedSafetyFactorForFatigueAndStatic"
        )

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
    def transmission_properties_gears(self: "Self") -> "_340.GearSetDesignGroup":
        """mastapy.gears.GearSetDesignGroup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransmissionPropertiesGears")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gear_mesh_ratings(self: "Self") -> "List[_365.AbstractGearMeshRating]":
        """List[mastapy.gears.rating.AbstractGearMeshRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearMeshRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def gear_ratings(self: "Self") -> "List[_366.AbstractGearRating]":
        """List[mastapy.gears.rating.AbstractGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractGearSetRating":
        """Cast to another type.

        Returns:
            _Cast_AbstractGearSetRating
        """
        return _Cast_AbstractGearSetRating(self)
