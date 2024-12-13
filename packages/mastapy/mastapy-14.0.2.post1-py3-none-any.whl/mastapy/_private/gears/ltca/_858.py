"""GearBendingStiffness"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.ltca import _872

_GEAR_BENDING_STIFFNESS = python_net_import(
    "SMT.MastaAPI.Gears.LTCA", "GearBendingStiffness"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.ltca.conical import _888
    from mastapy._private.gears.ltca.cylindrical import _876
    from mastapy._private.nodal_analysis import _66

    Self = TypeVar("Self", bound="GearBendingStiffness")
    CastSelf = TypeVar(
        "CastSelf", bound="GearBendingStiffness._Cast_GearBendingStiffness"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearBendingStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearBendingStiffness:
    """Special nested class for casting GearBendingStiffness to subclasses."""

    __parent__: "GearBendingStiffness"

    @property
    def gear_stiffness(self: "CastSelf") -> "_872.GearStiffness":
        return self.__parent__._cast(_872.GearStiffness)

    @property
    def fe_stiffness(self: "CastSelf") -> "_66.FEStiffness":
        from mastapy._private.nodal_analysis import _66

        return self.__parent__._cast(_66.FEStiffness)

    @property
    def cylindrical_gear_bending_stiffness(
        self: "CastSelf",
    ) -> "_876.CylindricalGearBendingStiffness":
        from mastapy._private.gears.ltca.cylindrical import _876

        return self.__parent__._cast(_876.CylindricalGearBendingStiffness)

    @property
    def conical_gear_bending_stiffness(
        self: "CastSelf",
    ) -> "_888.ConicalGearBendingStiffness":
        from mastapy._private.gears.ltca.conical import _888

        return self.__parent__._cast(_888.ConicalGearBendingStiffness)

    @property
    def gear_bending_stiffness(self: "CastSelf") -> "GearBendingStiffness":
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
class GearBendingStiffness(_872.GearStiffness):
    """GearBendingStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_BENDING_STIFFNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearBendingStiffness":
        """Cast to another type.

        Returns:
            _Cast_GearBendingStiffness
        """
        return _Cast_GearBendingStiffness(self)
