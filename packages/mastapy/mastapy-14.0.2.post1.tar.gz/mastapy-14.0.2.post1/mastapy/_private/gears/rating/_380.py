"""RateableMesh"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import

_RATEABLE_MESH = python_net_import("SMT.MastaAPI.Gears.Rating", "RateableMesh")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating.agma_gleason_conical import _581
    from mastapy._private.gears.rating.bevel.standards import _577
    from mastapy._private.gears.rating.conical import _560
    from mastapy._private.gears.rating.cylindrical import _484
    from mastapy._private.gears.rating.cylindrical.agma import _549
    from mastapy._private.gears.rating.cylindrical.iso6336 import _535, _536
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import (
        _506,
        _511,
        _512,
        _513,
    )
    from mastapy._private.gears.rating.hypoid.standards import _457
    from mastapy._private.gears.rating.iso_10300 import _440
    from mastapy._private.gears.rating.klingelnberg_conical.kn3030 import _428

    Self = TypeVar("Self", bound="RateableMesh")
    CastSelf = TypeVar("CastSelf", bound="RateableMesh._Cast_RateableMesh")


__docformat__ = "restructuredtext en"
__all__ = ("RateableMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RateableMesh:
    """Special nested class for casting RateableMesh to subclasses."""

    __parent__: "RateableMesh"

    @property
    def klingelnberg_conical_rateable_mesh(
        self: "CastSelf",
    ) -> "_428.KlingelnbergConicalRateableMesh":
        from mastapy._private.gears.rating.klingelnberg_conical.kn3030 import _428

        return self.__parent__._cast(_428.KlingelnbergConicalRateableMesh)

    @property
    def iso10300_rateable_mesh(self: "CastSelf") -> "_440.ISO10300RateableMesh":
        from mastapy._private.gears.rating.iso_10300 import _440

        return self.__parent__._cast(_440.ISO10300RateableMesh)

    @property
    def hypoid_rateable_mesh(self: "CastSelf") -> "_457.HypoidRateableMesh":
        from mastapy._private.gears.rating.hypoid.standards import _457

        return self.__parent__._cast(_457.HypoidRateableMesh)

    @property
    def cylindrical_rateable_mesh(self: "CastSelf") -> "_484.CylindricalRateableMesh":
        from mastapy._private.gears.rating.cylindrical import _484

        return self.__parent__._cast(_484.CylindricalRateableMesh)

    @property
    def plastic_gear_vdi2736_abstract_rateable_mesh(
        self: "CastSelf",
    ) -> "_506.PlasticGearVDI2736AbstractRateableMesh":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _506

        return self.__parent__._cast(_506.PlasticGearVDI2736AbstractRateableMesh)

    @property
    def vdi2736_metal_plastic_rateable_mesh(
        self: "CastSelf",
    ) -> "_511.VDI2736MetalPlasticRateableMesh":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _511

        return self.__parent__._cast(_511.VDI2736MetalPlasticRateableMesh)

    @property
    def vdi2736_plastic_metal_rateable_mesh(
        self: "CastSelf",
    ) -> "_512.VDI2736PlasticMetalRateableMesh":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _512

        return self.__parent__._cast(_512.VDI2736PlasticMetalRateableMesh)

    @property
    def vdi2736_plastic_plastic_rateable_mesh(
        self: "CastSelf",
    ) -> "_513.VDI2736PlasticPlasticRateableMesh":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _513

        return self.__parent__._cast(_513.VDI2736PlasticPlasticRateableMesh)

    @property
    def iso6336_metal_rateable_mesh(
        self: "CastSelf",
    ) -> "_535.ISO6336MetalRateableMesh":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _535

        return self.__parent__._cast(_535.ISO6336MetalRateableMesh)

    @property
    def iso6336_rateable_mesh(self: "CastSelf") -> "_536.ISO6336RateableMesh":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _536

        return self.__parent__._cast(_536.ISO6336RateableMesh)

    @property
    def agma2101_rateable_mesh(self: "CastSelf") -> "_549.AGMA2101RateableMesh":
        from mastapy._private.gears.rating.cylindrical.agma import _549

        return self.__parent__._cast(_549.AGMA2101RateableMesh)

    @property
    def conical_rateable_mesh(self: "CastSelf") -> "_560.ConicalRateableMesh":
        from mastapy._private.gears.rating.conical import _560

        return self.__parent__._cast(_560.ConicalRateableMesh)

    @property
    def spiral_bevel_rateable_mesh(self: "CastSelf") -> "_577.SpiralBevelRateableMesh":
        from mastapy._private.gears.rating.bevel.standards import _577

        return self.__parent__._cast(_577.SpiralBevelRateableMesh)

    @property
    def agma_gleason_conical_rateable_mesh(
        self: "CastSelf",
    ) -> "_581.AGMAGleasonConicalRateableMesh":
        from mastapy._private.gears.rating.agma_gleason_conical import _581

        return self.__parent__._cast(_581.AGMAGleasonConicalRateableMesh)

    @property
    def rateable_mesh(self: "CastSelf") -> "RateableMesh":
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
class RateableMesh(_0.APIBase):
    """RateableMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RATEABLE_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_RateableMesh":
        """Cast to another type.

        Returns:
            _Cast_RateableMesh
        """
        return _Cast_RateableMesh(self)
