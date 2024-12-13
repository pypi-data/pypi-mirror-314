"""DatabaseSettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.utility import _1645

_DATABASE_SETTINGS = python_net_import(
    "SMT.MastaAPI.Utility.Databases", "DatabaseSettings"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility import _1646
    from mastapy._private.utility.databases import _1880

    Self = TypeVar("Self", bound="DatabaseSettings")
    CastSelf = TypeVar("CastSelf", bound="DatabaseSettings._Cast_DatabaseSettings")


__docformat__ = "restructuredtext en"
__all__ = ("DatabaseSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DatabaseSettings:
    """Special nested class for casting DatabaseSettings to subclasses."""

    __parent__: "DatabaseSettings"

    @property
    def per_machine_settings(self: "CastSelf") -> "_1645.PerMachineSettings":
        return self.__parent__._cast(_1645.PerMachineSettings)

    @property
    def persistent_singleton(self: "CastSelf") -> "_1646.PersistentSingleton":
        from mastapy._private.utility import _1646

        return self.__parent__._cast(_1646.PersistentSingleton)

    @property
    def database_settings(self: "CastSelf") -> "DatabaseSettings":
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
class DatabaseSettings(_1645.PerMachineSettings):
    """DatabaseSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DATABASE_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_settings(self: "Self") -> "_1880.DatabaseConnectionSettings":
        """mastapy.utility.databases.DatabaseConnectionSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_DatabaseSettings":
        """Cast to another type.

        Returns:
            _Cast_DatabaseSettings
        """
        return _Cast_DatabaseSettings(self)
