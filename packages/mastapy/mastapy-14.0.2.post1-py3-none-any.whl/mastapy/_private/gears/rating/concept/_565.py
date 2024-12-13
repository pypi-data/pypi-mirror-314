"""ConceptGearSetDutyCycleRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating import _375

_CONCEPT_GEAR_SET_DUTY_CYCLE_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Concept", "ConceptGearSetDutyCycleRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1257
    from mastapy._private.gears.rating import _367

    Self = TypeVar("Self", bound="ConceptGearSetDutyCycleRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConceptGearSetDutyCycleRating._Cast_ConceptGearSetDutyCycleRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConceptGearSetDutyCycleRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConceptGearSetDutyCycleRating:
    """Special nested class for casting ConceptGearSetDutyCycleRating to subclasses."""

    __parent__: "ConceptGearSetDutyCycleRating"

    @property
    def gear_set_duty_cycle_rating(self: "CastSelf") -> "_375.GearSetDutyCycleRating":
        return self.__parent__._cast(_375.GearSetDutyCycleRating)

    @property
    def abstract_gear_set_rating(self: "CastSelf") -> "_367.AbstractGearSetRating":
        from mastapy._private.gears.rating import _367

        return self.__parent__._cast(_367.AbstractGearSetRating)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1257.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1257

        return self.__parent__._cast(_1257.AbstractGearSetAnalysis)

    @property
    def concept_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "ConceptGearSetDutyCycleRating":
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
class ConceptGearSetDutyCycleRating(_375.GearSetDutyCycleRating):
    """ConceptGearSetDutyCycleRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCEPT_GEAR_SET_DUTY_CYCLE_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConceptGearSetDutyCycleRating":
        """Cast to another type.

        Returns:
            _Cast_ConceptGearSetDutyCycleRating
        """
        return _Cast_ConceptGearSetDutyCycleRating(self)
