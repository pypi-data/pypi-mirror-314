"""CycloidalDiscPlanetaryBearingSocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.connections_and_sockets import _2346

_CYCLOIDAL_DISC_PLANETARY_BEARING_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal",
    "CycloidalDiscPlanetaryBearingSocket",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import _2333, _2353

    Self = TypeVar("Self", bound="CycloidalDiscPlanetaryBearingSocket")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CycloidalDiscPlanetaryBearingSocket._Cast_CycloidalDiscPlanetaryBearingSocket",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalDiscPlanetaryBearingSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDiscPlanetaryBearingSocket:
    """Special nested class for casting CycloidalDiscPlanetaryBearingSocket to subclasses."""

    __parent__: "CycloidalDiscPlanetaryBearingSocket"

    @property
    def planetary_socket_base(self: "CastSelf") -> "_2346.PlanetarySocketBase":
        return self.__parent__._cast(_2346.PlanetarySocketBase)

    @property
    def cylindrical_socket(self: "CastSelf") -> "_2333.CylindricalSocket":
        from mastapy._private.system_model.connections_and_sockets import _2333

        return self.__parent__._cast(_2333.CylindricalSocket)

    @property
    def socket(self: "CastSelf") -> "_2353.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2353

        return self.__parent__._cast(_2353.Socket)

    @property
    def cycloidal_disc_planetary_bearing_socket(
        self: "CastSelf",
    ) -> "CycloidalDiscPlanetaryBearingSocket":
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
class CycloidalDiscPlanetaryBearingSocket(_2346.PlanetarySocketBase):
    """CycloidalDiscPlanetaryBearingSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYCLOIDAL_DISC_PLANETARY_BEARING_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def is_for_eccentric_bearing(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsForEccentricBearing")

        if temp is None:
            return False

        return temp

    @is_for_eccentric_bearing.setter
    @enforce_parameter_types
    def is_for_eccentric_bearing(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsForEccentricBearing",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CycloidalDiscPlanetaryBearingSocket":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDiscPlanetaryBearingSocket
        """
        return _Cast_CycloidalDiscPlanetaryBearingSocket(self)
