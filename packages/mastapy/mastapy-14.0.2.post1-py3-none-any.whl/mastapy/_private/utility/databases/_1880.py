"""DatabaseConnectionSettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_DATABASE_CONNECTION_SETTINGS = python_net_import(
    "SMT.MastaAPI.Utility.Databases", "DatabaseConnectionSettings"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DatabaseConnectionSettings")
    CastSelf = TypeVar(
        "CastSelf", bound="DatabaseConnectionSettings._Cast_DatabaseConnectionSettings"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DatabaseConnectionSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DatabaseConnectionSettings:
    """Special nested class for casting DatabaseConnectionSettings to subclasses."""

    __parent__: "DatabaseConnectionSettings"

    @property
    def database_connection_settings(self: "CastSelf") -> "DatabaseConnectionSettings":
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
class DatabaseConnectionSettings(_0.APIBase):
    """DatabaseConnectionSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DATABASE_CONNECTION_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def can_use_local_db(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CanUseLocalDB")

        if temp is None:
            return False

        return temp

    @property
    def display_sql_connection_integrated_security(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DisplaySQLConnectionIntegratedSecurity"
        )

        if temp is None:
            return False

        return temp

    @property
    def force_use_of_local_db2012(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceUseOfLocalDB2012")

        if temp is None:
            return False

        return temp

    @property
    def is_local_db_path_specified(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsLocalDBPathSpecified")

        if temp is None:
            return False

        return temp

    @property
    def local_db_file_path(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LocalDBFilePath")

        if temp is None:
            return ""

        return temp

    @property
    def network_connection_string(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NetworkConnectionString")

        if temp is None:
            return ""

        return temp

    @property
    def sql_connection_db_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SQLConnectionDbName")

        if temp is None:
            return ""

        return temp

    @property
    def sql_connection_integrated_security(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SQLConnectionIntegratedSecurity")

        if temp is None:
            return False

        return temp

    @property
    def sql_connection_server_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SQLConnectionServerName")

        if temp is None:
            return ""

        return temp

    @property
    def sql_connection_user_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SQLConnectionUserName")

        if temp is None:
            return ""

        return temp

    @property
    def specified_local_db_file_path(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpecifiedLocalDBFilePath")

        if temp is None:
            return ""

        return temp

    @property
    def use_file_db(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UseFileDB")

        if temp is None:
            return False

        return temp

    @property
    def use_local_database(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UseLocalDatabase")

        if temp is None:
            return False

        return temp

    @property
    def use_network_database(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UseNetworkDatabase")

        if temp is None:
            return False

        return temp

    @property
    def uses_network_database_or_local_database_is_on_network_path(
        self: "Self",
    ) -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "UsesNetworkDatabaseOrLocalDatabaseIsOnNetworkPath"
        )

        if temp is None:
            return False

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_DatabaseConnectionSettings":
        """Cast to another type.

        Returns:
            _Cast_DatabaseConnectionSettings
        """
        return _Cast_DatabaseConnectionSettings(self)
