"""ShaftSettingsDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.shafts import _40
from mastapy._private.utility.databases import _1883

_SHAFT_SETTINGS_DATABASE = python_net_import(
    "SMT.MastaAPI.Shafts", "ShaftSettingsDatabase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.databases import _1879, _1886

    Self = TypeVar("Self", bound="ShaftSettingsDatabase")
    CastSelf = TypeVar(
        "CastSelf", bound="ShaftSettingsDatabase._Cast_ShaftSettingsDatabase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftSettingsDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftSettingsDatabase:
    """Special nested class for casting ShaftSettingsDatabase to subclasses."""

    __parent__: "ShaftSettingsDatabase"

    @property
    def named_database(self: "CastSelf") -> "_1883.NamedDatabase":
        return self.__parent__._cast(_1883.NamedDatabase)

    @property
    def sql_database(self: "CastSelf") -> "_1886.SQLDatabase":
        pass

        from mastapy._private.utility.databases import _1886

        return self.__parent__._cast(_1886.SQLDatabase)

    @property
    def database(self: "CastSelf") -> "_1879.Database":
        pass

        from mastapy._private.utility.databases import _1879

        return self.__parent__._cast(_1879.Database)

    @property
    def shaft_settings_database(self: "CastSelf") -> "ShaftSettingsDatabase":
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
class ShaftSettingsDatabase(_1883.NamedDatabase[_40.ShaftSettingsItem]):
    """ShaftSettingsDatabase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_SETTINGS_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftSettingsDatabase":
        """Cast to another type.

        Returns:
            _Cast_ShaftSettingsDatabase
        """
        return _Cast_ShaftSettingsDatabase(self)
