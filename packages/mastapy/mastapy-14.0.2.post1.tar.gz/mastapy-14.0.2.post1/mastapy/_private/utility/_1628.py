"""Command"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _7727
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)

_COMMAND = python_net_import("SMT.MastaAPI.Utility", "Command")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Command")
    CastSelf = TypeVar("CastSelf", bound="Command._Cast_Command")


__docformat__ = "restructuredtext en"
__all__ = ("Command",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Command:
    """Special nested class for casting Command to subclasses."""

    __parent__: "Command"

    @property
    def marshal_by_ref_object_permanent(
        self: "CastSelf",
    ) -> "_7727.MarshalByRefObjectPermanent":
        return self.__parent__._cast(_7727.MarshalByRefObjectPermanent)

    @property
    def command(self: "CastSelf") -> "Command":
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
class Command(_7727.MarshalByRefObjectPermanent):
    """Command

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMMAND

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    def run(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Run")

    @property
    def cast_to(self: "Self") -> "_Cast_Command":
        """Cast to another type.

        Returns:
            _Cast_Command
        """
        return _Cast_Command(self)
