"""ZerolBevelGearDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.gear_designs.bevel import _1220

_ZEROL_BEVEL_GEAR_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.ZerolBevel", "ZerolBevelGearDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs import _973, _974
    from mastapy._private.gears.gear_designs.agma_gleason_conical import _1233
    from mastapy._private.gears.gear_designs.conical import _1194

    Self = TypeVar("Self", bound="ZerolBevelGearDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="ZerolBevelGearDesign._Cast_ZerolBevelGearDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ZerolBevelGearDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ZerolBevelGearDesign:
    """Special nested class for casting ZerolBevelGearDesign to subclasses."""

    __parent__: "ZerolBevelGearDesign"

    @property
    def bevel_gear_design(self: "CastSelf") -> "_1220.BevelGearDesign":
        return self.__parent__._cast(_1220.BevelGearDesign)

    @property
    def agma_gleason_conical_gear_design(
        self: "CastSelf",
    ) -> "_1233.AGMAGleasonConicalGearDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1233

        return self.__parent__._cast(_1233.AGMAGleasonConicalGearDesign)

    @property
    def conical_gear_design(self: "CastSelf") -> "_1194.ConicalGearDesign":
        from mastapy._private.gears.gear_designs.conical import _1194

        return self.__parent__._cast(_1194.ConicalGearDesign)

    @property
    def gear_design(self: "CastSelf") -> "_973.GearDesign":
        from mastapy._private.gears.gear_designs import _973

        return self.__parent__._cast(_973.GearDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_974.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _974

        return self.__parent__._cast(_974.GearDesignComponent)

    @property
    def zerol_bevel_gear_design(self: "CastSelf") -> "ZerolBevelGearDesign":
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
class ZerolBevelGearDesign(_1220.BevelGearDesign):
    """ZerolBevelGearDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ZEROL_BEVEL_GEAR_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def mean_spiral_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanSpiralAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ZerolBevelGearDesign":
        """Cast to another type.

        Returns:
            _Cast_ZerolBevelGearDesign
        """
        return _Cast_ZerolBevelGearDesign(self)
