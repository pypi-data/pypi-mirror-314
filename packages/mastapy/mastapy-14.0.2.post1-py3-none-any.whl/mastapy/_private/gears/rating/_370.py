"""GearDutyCycleRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating import _366

_GEAR_DUTY_CYCLE_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating", "GearDutyCycleRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1255
    from mastapy._private.gears.rating import _371, _374, _375
    from mastapy._private.gears.rating.concept import _561
    from mastapy._private.gears.rating.conical import _551
    from mastapy._private.gears.rating.cylindrical import _468
    from mastapy._private.gears.rating.face import _458
    from mastapy._private.gears.rating.worm import _385

    Self = TypeVar("Self", bound="GearDutyCycleRating")
    CastSelf = TypeVar(
        "CastSelf", bound="GearDutyCycleRating._Cast_GearDutyCycleRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearDutyCycleRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearDutyCycleRating:
    """Special nested class for casting GearDutyCycleRating to subclasses."""

    __parent__: "GearDutyCycleRating"

    @property
    def abstract_gear_rating(self: "CastSelf") -> "_366.AbstractGearRating":
        return self.__parent__._cast(_366.AbstractGearRating)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1255.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1255

        return self.__parent__._cast(_1255.AbstractGearAnalysis)

    @property
    def worm_gear_duty_cycle_rating(self: "CastSelf") -> "_385.WormGearDutyCycleRating":
        from mastapy._private.gears.rating.worm import _385

        return self.__parent__._cast(_385.WormGearDutyCycleRating)

    @property
    def face_gear_duty_cycle_rating(self: "CastSelf") -> "_458.FaceGearDutyCycleRating":
        from mastapy._private.gears.rating.face import _458

        return self.__parent__._cast(_458.FaceGearDutyCycleRating)

    @property
    def cylindrical_gear_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_468.CylindricalGearDutyCycleRating":
        from mastapy._private.gears.rating.cylindrical import _468

        return self.__parent__._cast(_468.CylindricalGearDutyCycleRating)

    @property
    def conical_gear_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_551.ConicalGearDutyCycleRating":
        from mastapy._private.gears.rating.conical import _551

        return self.__parent__._cast(_551.ConicalGearDutyCycleRating)

    @property
    def concept_gear_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_561.ConceptGearDutyCycleRating":
        from mastapy._private.gears.rating.concept import _561

        return self.__parent__._cast(_561.ConceptGearDutyCycleRating)

    @property
    def gear_duty_cycle_rating(self: "CastSelf") -> "GearDutyCycleRating":
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
class GearDutyCycleRating(_366.AbstractGearRating):
    """GearDutyCycleRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_DUTY_CYCLE_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def maximum_bending_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumBendingStress")

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumContactStress")

        if temp is None:
            return 0.0

        return temp

    @property
    def gear_set_design_duty_cycle(self: "Self") -> "_375.GearSetDutyCycleRating":
        """mastapy.gears.rating.GearSetDutyCycleRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSetDesignDutyCycle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def left_flank_rating(self: "Self") -> "_371.GearFlankRating":
        """mastapy.gears.rating.GearFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftFlankRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def right_flank_rating(self: "Self") -> "_371.GearFlankRating":
        """mastapy.gears.rating.GearFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightFlankRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gear_ratings(self: "Self") -> "List[_374.GearRating]":
        """List[mastapy.gears.rating.GearRating]

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
    def cast_to(self: "Self") -> "_Cast_GearDutyCycleRating":
        """Cast to another type.

        Returns:
            _Cast_GearDutyCycleRating
        """
        return _Cast_GearDutyCycleRating(self)
