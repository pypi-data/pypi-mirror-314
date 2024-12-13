"""KlingelnbergHypoidGearTeethSocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets.gears import _2374

_KLINGELNBERG_HYPOID_GEAR_TEETH_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears",
    "KlingelnbergHypoidGearTeethSocket",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import _2353
    from mastapy._private.system_model.connections_and_sockets.gears import _2365, _2371

    Self = TypeVar("Self", bound="KlingelnbergHypoidGearTeethSocket")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergHypoidGearTeethSocket._Cast_KlingelnbergHypoidGearTeethSocket",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergHypoidGearTeethSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergHypoidGearTeethSocket:
    """Special nested class for casting KlingelnbergHypoidGearTeethSocket to subclasses."""

    __parent__: "KlingelnbergHypoidGearTeethSocket"

    @property
    def klingelnberg_conical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2374.KlingelnbergConicalGearTeethSocket":
        return self.__parent__._cast(_2374.KlingelnbergConicalGearTeethSocket)

    @property
    def conical_gear_teeth_socket(self: "CastSelf") -> "_2365.ConicalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2365

        return self.__parent__._cast(_2365.ConicalGearTeethSocket)

    @property
    def gear_teeth_socket(self: "CastSelf") -> "_2371.GearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2371

        return self.__parent__._cast(_2371.GearTeethSocket)

    @property
    def socket(self: "CastSelf") -> "_2353.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2353

        return self.__parent__._cast(_2353.Socket)

    @property
    def klingelnberg_hypoid_gear_teeth_socket(
        self: "CastSelf",
    ) -> "KlingelnbergHypoidGearTeethSocket":
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
class KlingelnbergHypoidGearTeethSocket(_2374.KlingelnbergConicalGearTeethSocket):
    """KlingelnbergHypoidGearTeethSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_HYPOID_GEAR_TEETH_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_KlingelnbergHypoidGearTeethSocket":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergHypoidGearTeethSocket
        """
        return _Cast_KlingelnbergHypoidGearTeethSocket(self)
