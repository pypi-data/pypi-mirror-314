"""KlingelnbergCycloPalloidConicalGearMeshRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating.conical import _552

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.KlingelnbergConical",
    "KlingelnbergCycloPalloidConicalGearMeshRating",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1256
    from mastapy._private.gears.rating import _365, _373
    from mastapy._private.gears.rating.klingelnberg_hypoid import _421
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _418

    Self = TypeVar("Self", bound="KlingelnbergCycloPalloidConicalGearMeshRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidConicalGearMeshRating._Cast_KlingelnbergCycloPalloidConicalGearMeshRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearMeshRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidConicalGearMeshRating:
    """Special nested class for casting KlingelnbergCycloPalloidConicalGearMeshRating to subclasses."""

    __parent__: "KlingelnbergCycloPalloidConicalGearMeshRating"

    @property
    def conical_gear_mesh_rating(self: "CastSelf") -> "_552.ConicalGearMeshRating":
        return self.__parent__._cast(_552.ConicalGearMeshRating)

    @property
    def gear_mesh_rating(self: "CastSelf") -> "_373.GearMeshRating":
        from mastapy._private.gears.rating import _373

        return self.__parent__._cast(_373.GearMeshRating)

    @property
    def abstract_gear_mesh_rating(self: "CastSelf") -> "_365.AbstractGearMeshRating":
        from mastapy._private.gears.rating import _365

        return self.__parent__._cast(_365.AbstractGearMeshRating)

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1256.AbstractGearMeshAnalysis":
        from mastapy._private.gears.analysis import _1256

        return self.__parent__._cast(_1256.AbstractGearMeshAnalysis)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_418.KlingelnbergCycloPalloidSpiralBevelGearMeshRating":
        from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _418

        return self.__parent__._cast(
            _418.KlingelnbergCycloPalloidSpiralBevelGearMeshRating
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_421.KlingelnbergCycloPalloidHypoidGearMeshRating":
        from mastapy._private.gears.rating.klingelnberg_hypoid import _421

        return self.__parent__._cast(_421.KlingelnbergCycloPalloidHypoidGearMeshRating)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_rating(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidConicalGearMeshRating":
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
class KlingelnbergCycloPalloidConicalGearMeshRating(_552.ConicalGearMeshRating):
    """KlingelnbergCycloPalloidConicalGearMeshRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_KlingelnbergCycloPalloidConicalGearMeshRating":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidConicalGearMeshRating
        """
        return _Cast_KlingelnbergCycloPalloidConicalGearMeshRating(self)
