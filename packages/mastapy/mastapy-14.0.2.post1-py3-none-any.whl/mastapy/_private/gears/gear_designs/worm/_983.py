"""WormGearDesign"""

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
from mastapy._private.gears.gear_designs import _973

_WORM_GEAR_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Worm", "WormGearDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears import _345
    from mastapy._private.gears.gear_designs import _974
    from mastapy._private.gears.gear_designs.worm import _982, _986

    Self = TypeVar("Self", bound="WormGearDesign")
    CastSelf = TypeVar("CastSelf", bound="WormGearDesign._Cast_WormGearDesign")


__docformat__ = "restructuredtext en"
__all__ = ("WormGearDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormGearDesign:
    """Special nested class for casting WormGearDesign to subclasses."""

    __parent__: "WormGearDesign"

    @property
    def gear_design(self: "CastSelf") -> "_973.GearDesign":
        return self.__parent__._cast(_973.GearDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_974.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _974

        return self.__parent__._cast(_974.GearDesignComponent)

    @property
    def worm_design(self: "CastSelf") -> "_982.WormDesign":
        from mastapy._private.gears.gear_designs.worm import _982

        return self.__parent__._cast(_982.WormDesign)

    @property
    def worm_wheel_design(self: "CastSelf") -> "_986.WormWheelDesign":
        from mastapy._private.gears.gear_designs.worm import _986

        return self.__parent__._cast(_986.WormWheelDesign)

    @property
    def worm_gear_design(self: "CastSelf") -> "WormGearDesign":
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
class WormGearDesign(_973.GearDesign):
    """WormGearDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_GEAR_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def hand(self: "Self") -> "_345.Hand":
        """mastapy.gears.Hand"""
        temp = pythonnet_property_get(self.wrapped, "Hand")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Gears.Hand")

        if value is None:
            return None

        return constructor.new_from_mastapy("mastapy._private.gears._345", "Hand")(
            value
        )

    @hand.setter
    @enforce_parameter_types
    def hand(self: "Self", value: "_345.Hand") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Gears.Hand")
        pythonnet_property_set(self.wrapped, "Hand", value)

    @property
    def root_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def whole_depth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WholeDepth")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_WormGearDesign":
        """Cast to another type.

        Returns:
            _Cast_WormGearDesign
        """
        return _Cast_WormGearDesign(self)
