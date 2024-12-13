"""PulleySocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2333

_PULLEY_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "PulleySocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import _2331, _2353

    Self = TypeVar("Self", bound="PulleySocket")
    CastSelf = TypeVar("CastSelf", bound="PulleySocket._Cast_PulleySocket")


__docformat__ = "restructuredtext en"
__all__ = ("PulleySocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PulleySocket:
    """Special nested class for casting PulleySocket to subclasses."""

    __parent__: "PulleySocket"

    @property
    def cylindrical_socket(self: "CastSelf") -> "_2333.CylindricalSocket":
        return self.__parent__._cast(_2333.CylindricalSocket)

    @property
    def socket(self: "CastSelf") -> "_2353.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2353

        return self.__parent__._cast(_2353.Socket)

    @property
    def cvt_pulley_socket(self: "CastSelf") -> "_2331.CVTPulleySocket":
        from mastapy._private.system_model.connections_and_sockets import _2331

        return self.__parent__._cast(_2331.CVTPulleySocket)

    @property
    def pulley_socket(self: "CastSelf") -> "PulleySocket":
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
class PulleySocket(_2333.CylindricalSocket):
    """PulleySocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PULLEY_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_PulleySocket":
        """Cast to another type.

        Returns:
            _Cast_PulleySocket
        """
        return _Cast_PulleySocket(self)
