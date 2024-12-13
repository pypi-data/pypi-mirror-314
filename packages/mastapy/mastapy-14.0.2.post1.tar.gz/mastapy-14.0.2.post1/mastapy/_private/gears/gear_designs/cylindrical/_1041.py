"""CylindricalGearBasicRackFlank"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.gear_designs.cylindrical import _1039

_CYLINDRICAL_GEAR_BASIC_RACK_FLANK = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CylindricalGearBasicRackFlank"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1111

    Self = TypeVar("Self", bound="CylindricalGearBasicRackFlank")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearBasicRackFlank._Cast_CylindricalGearBasicRackFlank",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearBasicRackFlank",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearBasicRackFlank:
    """Special nested class for casting CylindricalGearBasicRackFlank to subclasses."""

    __parent__: "CylindricalGearBasicRackFlank"

    @property
    def cylindrical_gear_abstract_rack_flank(
        self: "CastSelf",
    ) -> "_1039.CylindricalGearAbstractRackFlank":
        return self.__parent__._cast(_1039.CylindricalGearAbstractRackFlank)

    @property
    def standard_rack_flank(self: "CastSelf") -> "_1111.StandardRackFlank":
        from mastapy._private.gears.gear_designs.cylindrical import _1111

        return self.__parent__._cast(_1111.StandardRackFlank)

    @property
    def cylindrical_gear_basic_rack_flank(
        self: "CastSelf",
    ) -> "CylindricalGearBasicRackFlank":
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
class CylindricalGearBasicRackFlank(_1039.CylindricalGearAbstractRackFlank):
    """CylindricalGearBasicRackFlank

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_BASIC_RACK_FLANK

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearBasicRackFlank":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearBasicRackFlank
        """
        return _Cast_CylindricalGearBasicRackFlank(self)
