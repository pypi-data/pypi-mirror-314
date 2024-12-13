"""AGMAGleasonConicalMeshedGearDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.gear_designs.conical import _1199

_AGMA_GLEASON_CONICAL_MESHED_GEAR_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.AGMAGleasonConical",
    "AGMAGleasonConicalMeshedGearDesign",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs import _974
    from mastapy._private.gears.gear_designs.bevel import _1223
    from mastapy._private.gears.gear_designs.hypoid import _1014
    from mastapy._private.gears.gear_designs.spiral_bevel import _998
    from mastapy._private.gears.gear_designs.straight_bevel import _990
    from mastapy._private.gears.gear_designs.straight_bevel_diff import _994
    from mastapy._private.gears.gear_designs.zerol_bevel import _981

    Self = TypeVar("Self", bound="AGMAGleasonConicalMeshedGearDesign")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalMeshedGearDesign._Cast_AGMAGleasonConicalMeshedGearDesign",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalMeshedGearDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalMeshedGearDesign:
    """Special nested class for casting AGMAGleasonConicalMeshedGearDesign to subclasses."""

    __parent__: "AGMAGleasonConicalMeshedGearDesign"

    @property
    def conical_meshed_gear_design(self: "CastSelf") -> "_1199.ConicalMeshedGearDesign":
        return self.__parent__._cast(_1199.ConicalMeshedGearDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_974.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _974

        return self.__parent__._cast(_974.GearDesignComponent)

    @property
    def zerol_bevel_meshed_gear_design(
        self: "CastSelf",
    ) -> "_981.ZerolBevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _981

        return self.__parent__._cast(_981.ZerolBevelMeshedGearDesign)

    @property
    def straight_bevel_meshed_gear_design(
        self: "CastSelf",
    ) -> "_990.StraightBevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _990

        return self.__parent__._cast(_990.StraightBevelMeshedGearDesign)

    @property
    def straight_bevel_diff_meshed_gear_design(
        self: "CastSelf",
    ) -> "_994.StraightBevelDiffMeshedGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _994

        return self.__parent__._cast(_994.StraightBevelDiffMeshedGearDesign)

    @property
    def spiral_bevel_meshed_gear_design(
        self: "CastSelf",
    ) -> "_998.SpiralBevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _998

        return self.__parent__._cast(_998.SpiralBevelMeshedGearDesign)

    @property
    def hypoid_meshed_gear_design(self: "CastSelf") -> "_1014.HypoidMeshedGearDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1014

        return self.__parent__._cast(_1014.HypoidMeshedGearDesign)

    @property
    def bevel_meshed_gear_design(self: "CastSelf") -> "_1223.BevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.bevel import _1223

        return self.__parent__._cast(_1223.BevelMeshedGearDesign)

    @property
    def agma_gleason_conical_meshed_gear_design(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalMeshedGearDesign":
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
class AGMAGleasonConicalMeshedGearDesign(_1199.ConicalMeshedGearDesign):
    """AGMAGleasonConicalMeshedGearDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_MESHED_GEAR_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def mean_normal_topland(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanNormalTopland")

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_topland_to_module_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumToplandToModuleFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def required_mean_normal_topland(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RequiredMeanNormalTopland")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalMeshedGearDesign":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalMeshedGearDesign
        """
        return _Cast_AGMAGleasonConicalMeshedGearDesign(self)
