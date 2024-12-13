"""SurfacePermanentMagnetRotor"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.electric_machines import _1337

_SURFACE_PERMANENT_MAGNET_ROTOR = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "SurfacePermanentMagnetRotor"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines import _1340

    Self = TypeVar("Self", bound="SurfacePermanentMagnetRotor")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SurfacePermanentMagnetRotor._Cast_SurfacePermanentMagnetRotor",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SurfacePermanentMagnetRotor",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SurfacePermanentMagnetRotor:
    """Special nested class for casting SurfacePermanentMagnetRotor to subclasses."""

    __parent__: "SurfacePermanentMagnetRotor"

    @property
    def permanent_magnet_rotor(self: "CastSelf") -> "_1337.PermanentMagnetRotor":
        return self.__parent__._cast(_1337.PermanentMagnetRotor)

    @property
    def rotor(self: "CastSelf") -> "_1340.Rotor":
        from mastapy._private.electric_machines import _1340

        return self.__parent__._cast(_1340.Rotor)

    @property
    def surface_permanent_magnet_rotor(
        self: "CastSelf",
    ) -> "SurfacePermanentMagnetRotor":
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
class SurfacePermanentMagnetRotor(_1337.PermanentMagnetRotor):
    """SurfacePermanentMagnetRotor

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SURFACE_PERMANENT_MAGNET_ROTOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_SurfacePermanentMagnetRotor":
        """Cast to another type.

        Returns:
            _Cast_SurfacePermanentMagnetRotor
        """
        return _Cast_SurfacePermanentMagnetRotor(self)
