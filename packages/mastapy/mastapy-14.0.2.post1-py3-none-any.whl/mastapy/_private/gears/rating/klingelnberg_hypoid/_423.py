"""KlingelnbergCycloPalloidHypoidGearSetRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.klingelnberg_conical import _426

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.KlingelnbergHypoid",
    "KlingelnbergCycloPalloidHypoidGearSetRating",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1257
    from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1005
    from mastapy._private.gears.rating import _367, _376
    from mastapy._private.gears.rating.conical import _555
    from mastapy._private.gears.rating.klingelnberg_hypoid import _421, _422

    Self = TypeVar("Self", bound="KlingelnbergCycloPalloidHypoidGearSetRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidHypoidGearSetRating._Cast_KlingelnbergCycloPalloidHypoidGearSetRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidHypoidGearSetRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidHypoidGearSetRating:
    """Special nested class for casting KlingelnbergCycloPalloidHypoidGearSetRating to subclasses."""

    __parent__: "KlingelnbergCycloPalloidHypoidGearSetRating"

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_rating(
        self: "CastSelf",
    ) -> "_426.KlingelnbergCycloPalloidConicalGearSetRating":
        return self.__parent__._cast(_426.KlingelnbergCycloPalloidConicalGearSetRating)

    @property
    def conical_gear_set_rating(self: "CastSelf") -> "_555.ConicalGearSetRating":
        from mastapy._private.gears.rating.conical import _555

        return self.__parent__._cast(_555.ConicalGearSetRating)

    @property
    def gear_set_rating(self: "CastSelf") -> "_376.GearSetRating":
        from mastapy._private.gears.rating import _376

        return self.__parent__._cast(_376.GearSetRating)

    @property
    def abstract_gear_set_rating(self: "CastSelf") -> "_367.AbstractGearSetRating":
        from mastapy._private.gears.rating import _367

        return self.__parent__._cast(_367.AbstractGearSetRating)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1257.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1257

        return self.__parent__._cast(_1257.AbstractGearSetAnalysis)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_rating(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidHypoidGearSetRating":
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
class KlingelnbergCycloPalloidHypoidGearSetRating(
    _426.KlingelnbergCycloPalloidConicalGearSetRating
):
    """KlingelnbergCycloPalloidHypoidGearSetRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "Self",
    ) -> "_1005.KlingelnbergCycloPalloidHypoidGearSetDesign":
        """mastapy.gears.gear_designs.klingelnberg_hypoid.KlingelnbergCycloPalloidHypoidGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidHypoidGearSet"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_ratings(
        self: "Self",
    ) -> "List[_422.KlingelnbergCycloPalloidHypoidGearRating]":
        """List[mastapy.gears.rating.klingelnberg_hypoid.KlingelnbergCycloPalloidHypoidGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidHypoidGearRatings"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_mesh_ratings(
        self: "Self",
    ) -> "List[_421.KlingelnbergCycloPalloidHypoidGearMeshRating]":
        """List[mastapy.gears.rating.klingelnberg_hypoid.KlingelnbergCycloPalloidHypoidGearMeshRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidHypoidMeshRatings"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_KlingelnbergCycloPalloidHypoidGearSetRating":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidHypoidGearSetRating
        """
        return _Cast_KlingelnbergCycloPalloidHypoidGearSetRating(self)
