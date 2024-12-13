"""PermanentMagnetRotor"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.electric_machines import _1340

_PERMANENT_MAGNET_ROTOR = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "PermanentMagnetRotor"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines import _1321, _1351, _1370

    Self = TypeVar("Self", bound="PermanentMagnetRotor")
    CastSelf = TypeVar(
        "CastSelf", bound="PermanentMagnetRotor._Cast_PermanentMagnetRotor"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PermanentMagnetRotor",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PermanentMagnetRotor:
    """Special nested class for casting PermanentMagnetRotor to subclasses."""

    __parent__: "PermanentMagnetRotor"

    @property
    def rotor(self: "CastSelf") -> "_1340.Rotor":
        return self.__parent__._cast(_1340.Rotor)

    @property
    def interior_permanent_magnet_and_synchronous_reluctance_rotor(
        self: "CastSelf",
    ) -> "_1321.InteriorPermanentMagnetAndSynchronousReluctanceRotor":
        from mastapy._private.electric_machines import _1321

        return self.__parent__._cast(
            _1321.InteriorPermanentMagnetAndSynchronousReluctanceRotor
        )

    @property
    def surface_permanent_magnet_rotor(
        self: "CastSelf",
    ) -> "_1351.SurfacePermanentMagnetRotor":
        from mastapy._private.electric_machines import _1351

        return self.__parent__._cast(_1351.SurfacePermanentMagnetRotor)

    @property
    def wound_field_synchronous_rotor(
        self: "CastSelf",
    ) -> "_1370.WoundFieldSynchronousRotor":
        from mastapy._private.electric_machines import _1370

        return self.__parent__._cast(_1370.WoundFieldSynchronousRotor)

    @property
    def permanent_magnet_rotor(self: "CastSelf") -> "PermanentMagnetRotor":
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
class PermanentMagnetRotor(_1340.Rotor):
    """PermanentMagnetRotor

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PERMANENT_MAGNET_ROTOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_PermanentMagnetRotor":
        """Cast to another type.

        Returns:
            _Cast_PermanentMagnetRotor
        """
        return _Cast_PermanentMagnetRotor(self)
