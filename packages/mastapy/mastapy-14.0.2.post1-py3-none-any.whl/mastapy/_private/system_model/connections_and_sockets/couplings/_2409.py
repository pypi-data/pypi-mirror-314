"""TorqueConverterConnection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets.couplings import _2403

_TORQUE_CONVERTER_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings",
    "TorqueConverterConnection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2260
    from mastapy._private.system_model.connections_and_sockets import _2329, _2338

    Self = TypeVar("Self", bound="TorqueConverterConnection")
    CastSelf = TypeVar(
        "CastSelf", bound="TorqueConverterConnection._Cast_TorqueConverterConnection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TorqueConverterConnection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TorqueConverterConnection:
    """Special nested class for casting TorqueConverterConnection to subclasses."""

    __parent__: "TorqueConverterConnection"

    @property
    def coupling_connection(self: "CastSelf") -> "_2403.CouplingConnection":
        return self.__parent__._cast(_2403.CouplingConnection)

    @property
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2338.InterMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2338

        return self.__parent__._cast(_2338.InterMountableComponentConnection)

    @property
    def connection(self: "CastSelf") -> "_2329.Connection":
        from mastapy._private.system_model.connections_and_sockets import _2329

        return self.__parent__._cast(_2329.Connection)

    @property
    def design_entity(self: "CastSelf") -> "_2260.DesignEntity":
        from mastapy._private.system_model import _2260

        return self.__parent__._cast(_2260.DesignEntity)

    @property
    def torque_converter_connection(self: "CastSelf") -> "TorqueConverterConnection":
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
class TorqueConverterConnection(_2403.CouplingConnection):
    """TorqueConverterConnection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TORQUE_CONVERTER_CONNECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_TorqueConverterConnection":
        """Cast to another type.

        Returns:
            _Cast_TorqueConverterConnection
        """
        return _Cast_TorqueConverterConnection(self)
