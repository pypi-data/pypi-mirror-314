"""GearSetRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.rating import _367

_GEAR_SET_RATING = python_net_import("SMT.MastaAPI.Gears.Rating", "GearSetRating")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1257
    from mastapy._private.gears.rating import _373, _374
    from mastapy._private.gears.rating.agma_gleason_conical import _580
    from mastapy._private.gears.rating.bevel import _569
    from mastapy._private.gears.rating.concept import _566
    from mastapy._private.gears.rating.conical import _555
    from mastapy._private.gears.rating.cylindrical import _477
    from mastapy._private.gears.rating.face import _463
    from mastapy._private.gears.rating.hypoid import _453
    from mastapy._private.gears.rating.klingelnberg_conical import _426
    from mastapy._private.gears.rating.klingelnberg_hypoid import _423
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _420
    from mastapy._private.gears.rating.spiral_bevel import _417
    from mastapy._private.gears.rating.straight_bevel import _410
    from mastapy._private.gears.rating.straight_bevel_diff import _413
    from mastapy._private.gears.rating.worm import _389
    from mastapy._private.gears.rating.zerol_bevel import _384
    from mastapy._private.materials import _280

    Self = TypeVar("Self", bound="GearSetRating")
    CastSelf = TypeVar("CastSelf", bound="GearSetRating._Cast_GearSetRating")


__docformat__ = "restructuredtext en"
__all__ = ("GearSetRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetRating:
    """Special nested class for casting GearSetRating to subclasses."""

    __parent__: "GearSetRating"

    @property
    def abstract_gear_set_rating(self: "CastSelf") -> "_367.AbstractGearSetRating":
        return self.__parent__._cast(_367.AbstractGearSetRating)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1257.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1257

        return self.__parent__._cast(_1257.AbstractGearSetAnalysis)

    @property
    def zerol_bevel_gear_set_rating(self: "CastSelf") -> "_384.ZerolBevelGearSetRating":
        from mastapy._private.gears.rating.zerol_bevel import _384

        return self.__parent__._cast(_384.ZerolBevelGearSetRating)

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
    def face_gear_set_rating(self: "CastSelf") -> "_463.FaceGearSetRating":
        from mastapy._private.gears.rating.face import _463

        return self.__parent__._cast(_463.FaceGearSetRating)

    @property
    def cylindrical_gear_set_rating(
        self: "CastSelf",
    ) -> "_477.CylindricalGearSetRating":
        from mastapy._private.gears.rating.cylindrical import _477

        return self.__parent__._cast(_477.CylindricalGearSetRating)

    @property
    def conical_gear_set_rating(self: "CastSelf") -> "_555.ConicalGearSetRating":
        from mastapy._private.gears.rating.conical import _555

        return self.__parent__._cast(_555.ConicalGearSetRating)

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
    def gear_set_rating(self: "CastSelf") -> "GearSetRating":
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
class GearSetRating(_367.AbstractGearSetRating):
    """GearSetRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def rating(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rating")

        if temp is None:
            return ""

        return temp

    @property
    def total_gear_set_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalGearSetReliability")

        if temp is None:
            return 0.0

        return temp

    @property
    def lubrication_detail(self: "Self") -> "_280.LubricationDetail":
        """mastapy.materials.LubricationDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricationDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gear_mesh_ratings(self: "Self") -> "List[_373.GearMeshRating]":
        """List[mastapy.gears.rating.GearMeshRating]

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
    def cast_to(self: "Self") -> "_Cast_GearSetRating":
        """Cast to another type.

        Returns:
            _Cast_GearSetRating
        """
        return _Cast_GearSetRating(self)
