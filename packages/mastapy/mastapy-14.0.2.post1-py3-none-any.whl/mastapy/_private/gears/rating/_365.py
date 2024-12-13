"""AbstractGearMeshRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.analysis import _1256

_ABSTRACT_GEAR_MESH_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating", "AbstractGearMeshRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _373, _378
    from mastapy._private.gears.rating.agma_gleason_conical import _578
    from mastapy._private.gears.rating.bevel import _567
    from mastapy._private.gears.rating.concept import _562, _563
    from mastapy._private.gears.rating.conical import _552, _557
    from mastapy._private.gears.rating.cylindrical import _471, _479
    from mastapy._private.gears.rating.face import _459, _460
    from mastapy._private.gears.rating.hypoid import _451
    from mastapy._private.gears.rating.klingelnberg_conical import _424
    from mastapy._private.gears.rating.klingelnberg_hypoid import _421
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _418
    from mastapy._private.gears.rating.spiral_bevel import _415
    from mastapy._private.gears.rating.straight_bevel import _408
    from mastapy._private.gears.rating.straight_bevel_diff import _411
    from mastapy._private.gears.rating.worm import _386, _390
    from mastapy._private.gears.rating.zerol_bevel import _382

    Self = TypeVar("Self", bound="AbstractGearMeshRating")
    CastSelf = TypeVar(
        "CastSelf", bound="AbstractGearMeshRating._Cast_AbstractGearMeshRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractGearMeshRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractGearMeshRating:
    """Special nested class for casting AbstractGearMeshRating to subclasses."""

    __parent__: "AbstractGearMeshRating"

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1256.AbstractGearMeshAnalysis":
        return self.__parent__._cast(_1256.AbstractGearMeshAnalysis)

    @property
    def gear_mesh_rating(self: "CastSelf") -> "_373.GearMeshRating":
        from mastapy._private.gears.rating import _373

        return self.__parent__._cast(_373.GearMeshRating)

    @property
    def mesh_duty_cycle_rating(self: "CastSelf") -> "_378.MeshDutyCycleRating":
        from mastapy._private.gears.rating import _378

        return self.__parent__._cast(_378.MeshDutyCycleRating)

    @property
    def zerol_bevel_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_382.ZerolBevelGearMeshRating":
        from mastapy._private.gears.rating.zerol_bevel import _382

        return self.__parent__._cast(_382.ZerolBevelGearMeshRating)

    @property
    def worm_gear_mesh_rating(self: "CastSelf") -> "_386.WormGearMeshRating":
        from mastapy._private.gears.rating.worm import _386

        return self.__parent__._cast(_386.WormGearMeshRating)

    @property
    def worm_mesh_duty_cycle_rating(self: "CastSelf") -> "_390.WormMeshDutyCycleRating":
        from mastapy._private.gears.rating.worm import _390

        return self.__parent__._cast(_390.WormMeshDutyCycleRating)

    @property
    def straight_bevel_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_408.StraightBevelGearMeshRating":
        from mastapy._private.gears.rating.straight_bevel import _408

        return self.__parent__._cast(_408.StraightBevelGearMeshRating)

    @property
    def straight_bevel_diff_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_411.StraightBevelDiffGearMeshRating":
        from mastapy._private.gears.rating.straight_bevel_diff import _411

        return self.__parent__._cast(_411.StraightBevelDiffGearMeshRating)

    @property
    def spiral_bevel_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_415.SpiralBevelGearMeshRating":
        from mastapy._private.gears.rating.spiral_bevel import _415

        return self.__parent__._cast(_415.SpiralBevelGearMeshRating)

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
    ) -> "_424.KlingelnbergCycloPalloidConicalGearMeshRating":
        from mastapy._private.gears.rating.klingelnberg_conical import _424

        return self.__parent__._cast(_424.KlingelnbergCycloPalloidConicalGearMeshRating)

    @property
    def hypoid_gear_mesh_rating(self: "CastSelf") -> "_451.HypoidGearMeshRating":
        from mastapy._private.gears.rating.hypoid import _451

        return self.__parent__._cast(_451.HypoidGearMeshRating)

    @property
    def face_gear_mesh_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_459.FaceGearMeshDutyCycleRating":
        from mastapy._private.gears.rating.face import _459

        return self.__parent__._cast(_459.FaceGearMeshDutyCycleRating)

    @property
    def face_gear_mesh_rating(self: "CastSelf") -> "_460.FaceGearMeshRating":
        from mastapy._private.gears.rating.face import _460

        return self.__parent__._cast(_460.FaceGearMeshRating)

    @property
    def cylindrical_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_471.CylindricalGearMeshRating":
        from mastapy._private.gears.rating.cylindrical import _471

        return self.__parent__._cast(_471.CylindricalGearMeshRating)

    @property
    def cylindrical_mesh_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_479.CylindricalMeshDutyCycleRating":
        from mastapy._private.gears.rating.cylindrical import _479

        return self.__parent__._cast(_479.CylindricalMeshDutyCycleRating)

    @property
    def conical_gear_mesh_rating(self: "CastSelf") -> "_552.ConicalGearMeshRating":
        from mastapy._private.gears.rating.conical import _552

        return self.__parent__._cast(_552.ConicalGearMeshRating)

    @property
    def conical_mesh_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_557.ConicalMeshDutyCycleRating":
        from mastapy._private.gears.rating.conical import _557

        return self.__parent__._cast(_557.ConicalMeshDutyCycleRating)

    @property
    def concept_gear_mesh_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_562.ConceptGearMeshDutyCycleRating":
        from mastapy._private.gears.rating.concept import _562

        return self.__parent__._cast(_562.ConceptGearMeshDutyCycleRating)

    @property
    def concept_gear_mesh_rating(self: "CastSelf") -> "_563.ConceptGearMeshRating":
        from mastapy._private.gears.rating.concept import _563

        return self.__parent__._cast(_563.ConceptGearMeshRating)

    @property
    def bevel_gear_mesh_rating(self: "CastSelf") -> "_567.BevelGearMeshRating":
        from mastapy._private.gears.rating.bevel import _567

        return self.__parent__._cast(_567.BevelGearMeshRating)

    @property
    def agma_gleason_conical_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_578.AGMAGleasonConicalGearMeshRating":
        from mastapy._private.gears.rating.agma_gleason_conical import _578

        return self.__parent__._cast(_578.AGMAGleasonConicalGearMeshRating)

    @property
    def abstract_gear_mesh_rating(self: "CastSelf") -> "AbstractGearMeshRating":
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
class AbstractGearMeshRating(_1256.AbstractGearMeshAnalysis):
    """AbstractGearMeshRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_GEAR_MESH_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def calculated_mesh_efficiency(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CalculatedMeshEfficiency")

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
    def cast_to(self: "Self") -> "_Cast_AbstractGearMeshRating":
        """Cast to another type.

        Returns:
            _Cast_AbstractGearMeshRating
        """
        return _Cast_AbstractGearMeshRating(self)
