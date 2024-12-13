"""RawMaterialDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.materials import _630
from mastapy._private.utility.databases import _1883

_RAW_MATERIAL_DATABASE = python_net_import(
    "SMT.MastaAPI.Gears.Materials", "RawMaterialDatabase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.databases import _1879, _1886

    Self = TypeVar("Self", bound="RawMaterialDatabase")
    CastSelf = TypeVar(
        "CastSelf", bound="RawMaterialDatabase._Cast_RawMaterialDatabase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RawMaterialDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RawMaterialDatabase:
    """Special nested class for casting RawMaterialDatabase to subclasses."""

    __parent__: "RawMaterialDatabase"

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
    def raw_material_database(self: "CastSelf") -> "RawMaterialDatabase":
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
class RawMaterialDatabase(_1883.NamedDatabase[_630.RawMaterial]):
    """RawMaterialDatabase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RAW_MATERIAL_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_RawMaterialDatabase":
        """Cast to another type.

        Returns:
            _Cast_RawMaterialDatabase
        """
        return _Cast_RawMaterialDatabase(self)
