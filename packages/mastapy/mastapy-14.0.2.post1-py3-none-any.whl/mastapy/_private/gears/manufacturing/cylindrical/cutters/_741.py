"""CylindricalGearShaverDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.cylindrical import _635
from mastapy._private.gears.manufacturing.cylindrical.cutters import _740

_CYLINDRICAL_GEAR_SHAVER_DATABASE = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters",
    "CylindricalGearShaverDatabase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.databases import _1879, _1883, _1886

    Self = TypeVar("Self", bound="CylindricalGearShaverDatabase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearShaverDatabase._Cast_CylindricalGearShaverDatabase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearShaverDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearShaverDatabase:
    """Special nested class for casting CylindricalGearShaverDatabase to subclasses."""

    __parent__: "CylindricalGearShaverDatabase"

    @property
    def cylindrical_cutter_database(
        self: "CastSelf",
    ) -> "_635.CylindricalCutterDatabase":
        return self.__parent__._cast(_635.CylindricalCutterDatabase)

    @property
    def named_database(self: "CastSelf") -> "_1883.NamedDatabase":
        from mastapy._private.utility.databases import _1883

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
    def cylindrical_gear_shaver_database(
        self: "CastSelf",
    ) -> "CylindricalGearShaverDatabase":
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
class CylindricalGearShaverDatabase(
    _635.CylindricalCutterDatabase[_740.CylindricalGearShaver]
):
    """CylindricalGearShaverDatabase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SHAVER_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearShaverDatabase":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearShaverDatabase
        """
        return _Cast_CylindricalGearShaverDatabase(self)
