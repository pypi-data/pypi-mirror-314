"""GearStiffness"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis import _66

_GEAR_STIFFNESS = python_net_import("SMT.MastaAPI.Gears.LTCA", "GearStiffness")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.ltca import _858, _860
    from mastapy._private.gears.ltca.conical import _888, _890
    from mastapy._private.gears.ltca.cylindrical import _876, _878

    Self = TypeVar("Self", bound="GearStiffness")
    CastSelf = TypeVar("CastSelf", bound="GearStiffness._Cast_GearStiffness")


__docformat__ = "restructuredtext en"
__all__ = ("GearStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearStiffness:
    """Special nested class for casting GearStiffness to subclasses."""

    __parent__: "GearStiffness"

    @property
    def fe_stiffness(self: "CastSelf") -> "_66.FEStiffness":
        return self.__parent__._cast(_66.FEStiffness)

    @property
    def gear_bending_stiffness(self: "CastSelf") -> "_858.GearBendingStiffness":
        from mastapy._private.gears.ltca import _858

        return self.__parent__._cast(_858.GearBendingStiffness)

    @property
    def gear_contact_stiffness(self: "CastSelf") -> "_860.GearContactStiffness":
        from mastapy._private.gears.ltca import _860

        return self.__parent__._cast(_860.GearContactStiffness)

    @property
    def cylindrical_gear_bending_stiffness(
        self: "CastSelf",
    ) -> "_876.CylindricalGearBendingStiffness":
        from mastapy._private.gears.ltca.cylindrical import _876

        return self.__parent__._cast(_876.CylindricalGearBendingStiffness)

    @property
    def cylindrical_gear_contact_stiffness(
        self: "CastSelf",
    ) -> "_878.CylindricalGearContactStiffness":
        from mastapy._private.gears.ltca.cylindrical import _878

        return self.__parent__._cast(_878.CylindricalGearContactStiffness)

    @property
    def conical_gear_bending_stiffness(
        self: "CastSelf",
    ) -> "_888.ConicalGearBendingStiffness":
        from mastapy._private.gears.ltca.conical import _888

        return self.__parent__._cast(_888.ConicalGearBendingStiffness)

    @property
    def conical_gear_contact_stiffness(
        self: "CastSelf",
    ) -> "_890.ConicalGearContactStiffness":
        from mastapy._private.gears.ltca.conical import _890

        return self.__parent__._cast(_890.ConicalGearContactStiffness)

    @property
    def gear_stiffness(self: "CastSelf") -> "GearStiffness":
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
class GearStiffness(_66.FEStiffness):
    """GearStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_STIFFNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearStiffness":
        """Cast to another type.

        Returns:
            _Cast_GearStiffness
        """
        return _Cast_GearStiffness(self)
