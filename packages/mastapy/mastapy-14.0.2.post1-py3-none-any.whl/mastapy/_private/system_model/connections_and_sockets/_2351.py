"""ShaftSocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2333

_SHAFT_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "ShaftSocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2336,
        _2337,
        _2342,
        _2343,
        _2353,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2390,
        _2391,
        _2393,
    )

    Self = TypeVar("Self", bound="ShaftSocket")
    CastSelf = TypeVar("CastSelf", bound="ShaftSocket._Cast_ShaftSocket")


__docformat__ = "restructuredtext en"
__all__ = ("ShaftSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftSocket:
    """Special nested class for casting ShaftSocket to subclasses."""

    __parent__: "ShaftSocket"

    @property
    def cylindrical_socket(self: "CastSelf") -> "_2333.CylindricalSocket":
        return self.__parent__._cast(_2333.CylindricalSocket)

    @property
    def socket(self: "CastSelf") -> "_2353.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2353

        return self.__parent__._cast(_2353.Socket)

    @property
    def inner_shaft_socket(self: "CastSelf") -> "_2336.InnerShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2336

        return self.__parent__._cast(_2336.InnerShaftSocket)

    @property
    def inner_shaft_socket_base(self: "CastSelf") -> "_2337.InnerShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2337

        return self.__parent__._cast(_2337.InnerShaftSocketBase)

    @property
    def outer_shaft_socket(self: "CastSelf") -> "_2342.OuterShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2342

        return self.__parent__._cast(_2342.OuterShaftSocket)

    @property
    def outer_shaft_socket_base(self: "CastSelf") -> "_2343.OuterShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2343

        return self.__parent__._cast(_2343.OuterShaftSocketBase)

    @property
    def cycloidal_disc_axial_left_socket(
        self: "CastSelf",
    ) -> "_2390.CycloidalDiscAxialLeftSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2390,
        )

        return self.__parent__._cast(_2390.CycloidalDiscAxialLeftSocket)

    @property
    def cycloidal_disc_axial_right_socket(
        self: "CastSelf",
    ) -> "_2391.CycloidalDiscAxialRightSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2391,
        )

        return self.__parent__._cast(_2391.CycloidalDiscAxialRightSocket)

    @property
    def cycloidal_disc_inner_socket(
        self: "CastSelf",
    ) -> "_2393.CycloidalDiscInnerSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2393,
        )

        return self.__parent__._cast(_2393.CycloidalDiscInnerSocket)

    @property
    def shaft_socket(self: "CastSelf") -> "ShaftSocket":
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
class ShaftSocket(_2333.CylindricalSocket):
    """ShaftSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftSocket":
        """Cast to another type.

        Returns:
            _Cast_ShaftSocket
        """
        return _Cast_ShaftSocket(self)
