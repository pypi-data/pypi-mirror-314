"""GearSetDutyCycleRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.rating import _367

_GEAR_SET_DUTY_CYCLE_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating", "GearSetDutyCycleRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1257
    from mastapy._private.gears.gear_designs import _976
    from mastapy._private.gears.rating import _370, _378
    from mastapy._private.gears.rating.concept import _565
    from mastapy._private.gears.rating.conical import _554
    from mastapy._private.gears.rating.cylindrical import _476, _493
    from mastapy._private.gears.rating.face import _462
    from mastapy._private.gears.rating.worm import _388

    Self = TypeVar("Self", bound="GearSetDutyCycleRating")
    CastSelf = TypeVar(
        "CastSelf", bound="GearSetDutyCycleRating._Cast_GearSetDutyCycleRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetDutyCycleRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetDutyCycleRating:
    """Special nested class for casting GearSetDutyCycleRating to subclasses."""

    __parent__: "GearSetDutyCycleRating"

    @property
    def abstract_gear_set_rating(self: "CastSelf") -> "_367.AbstractGearSetRating":
        return self.__parent__._cast(_367.AbstractGearSetRating)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1257.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1257

        return self.__parent__._cast(_1257.AbstractGearSetAnalysis)

    @property
    def worm_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_388.WormGearSetDutyCycleRating":
        from mastapy._private.gears.rating.worm import _388

        return self.__parent__._cast(_388.WormGearSetDutyCycleRating)

    @property
    def face_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_462.FaceGearSetDutyCycleRating":
        from mastapy._private.gears.rating.face import _462

        return self.__parent__._cast(_462.FaceGearSetDutyCycleRating)

    @property
    def cylindrical_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_476.CylindricalGearSetDutyCycleRating":
        from mastapy._private.gears.rating.cylindrical import _476

        return self.__parent__._cast(_476.CylindricalGearSetDutyCycleRating)

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
    def concept_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_565.ConceptGearSetDutyCycleRating":
        from mastapy._private.gears.rating.concept import _565

        return self.__parent__._cast(_565.ConceptGearSetDutyCycleRating)

    @property
    def gear_set_duty_cycle_rating(self: "CastSelf") -> "GearSetDutyCycleRating":
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
class GearSetDutyCycleRating(_367.AbstractGearSetRating):
    """GearSetDutyCycleRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_DUTY_CYCLE_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def duty_cycle_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DutyCycleName")

        if temp is None:
            return ""

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
    def total_duty_cycle_gear_set_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalDutyCycleGearSetReliability")

        if temp is None:
            return 0.0

        return temp

    @property
    def gear_set_design(self: "Self") -> "_976.GearSetDesign":
        """mastapy.gears.gear_designs.GearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gear_ratings(self: "Self") -> "List[_370.GearDutyCycleRating]":
        """List[mastapy.gears.rating.GearDutyCycleRating]

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
    def gear_duty_cycle_ratings(self: "Self") -> "List[_370.GearDutyCycleRating]":
        """List[mastapy.gears.rating.GearDutyCycleRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearDutyCycleRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def gear_mesh_ratings(self: "Self") -> "List[_378.MeshDutyCycleRating]":
        """List[mastapy.gears.rating.MeshDutyCycleRating]

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
    def gear_mesh_duty_cycle_ratings(self: "Self") -> "List[_378.MeshDutyCycleRating]":
        """List[mastapy.gears.rating.MeshDutyCycleRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearMeshDutyCycleRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    def set_face_widths_for_specified_safety_factors(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SetFaceWidthsForSpecifiedSafetyFactors")

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetDutyCycleRating":
        """Cast to another type.

        Returns:
            _Cast_GearSetDutyCycleRating
        """
        return _Cast_GearSetDutyCycleRating(self)
