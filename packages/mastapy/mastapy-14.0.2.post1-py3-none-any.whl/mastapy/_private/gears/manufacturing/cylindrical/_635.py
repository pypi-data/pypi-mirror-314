"""CylindricalCutterDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.databases import _1883

_CYLINDRICAL_CUTTER_DATABASE = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical", "CylindricalCutterDatabase"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.gears.manufacturing.cylindrical import _640, _651
    from mastapy._private.gears.manufacturing.cylindrical.cutters import (
        _730,
        _736,
        _738,
        _741,
        _742,
    )
    from mastapy._private.utility.databases import _1879, _1886

    Self = TypeVar("Self", bound="CylindricalCutterDatabase")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalCutterDatabase._Cast_CylindricalCutterDatabase"
    )

T = TypeVar("T", bound="_738.CylindricalGearRealCutterDesign")

__docformat__ = "restructuredtext en"
__all__ = ("CylindricalCutterDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalCutterDatabase:
    """Special nested class for casting CylindricalCutterDatabase to subclasses."""

    __parent__: "CylindricalCutterDatabase"

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
    def cylindrical_hob_database(self: "CastSelf") -> "_640.CylindricalHobDatabase":
        from mastapy._private.gears.manufacturing.cylindrical import _640

        return self.__parent__._cast(_640.CylindricalHobDatabase)

    @property
    def cylindrical_shaper_database(
        self: "CastSelf",
    ) -> "_651.CylindricalShaperDatabase":
        from mastapy._private.gears.manufacturing.cylindrical import _651

        return self.__parent__._cast(_651.CylindricalShaperDatabase)

    @property
    def cylindrical_formed_wheel_grinder_database(
        self: "CastSelf",
    ) -> "_730.CylindricalFormedWheelGrinderDatabase":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _730

        return self.__parent__._cast(_730.CylindricalFormedWheelGrinderDatabase)

    @property
    def cylindrical_gear_plunge_shaver_database(
        self: "CastSelf",
    ) -> "_736.CylindricalGearPlungeShaverDatabase":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _736

        return self.__parent__._cast(_736.CylindricalGearPlungeShaverDatabase)

    @property
    def cylindrical_gear_shaver_database(
        self: "CastSelf",
    ) -> "_741.CylindricalGearShaverDatabase":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _741

        return self.__parent__._cast(_741.CylindricalGearShaverDatabase)

    @property
    def cylindrical_worm_grinder_database(
        self: "CastSelf",
    ) -> "_742.CylindricalWormGrinderDatabase":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _742

        return self.__parent__._cast(_742.CylindricalWormGrinderDatabase)

    @property
    def cylindrical_cutter_database(self: "CastSelf") -> "CylindricalCutterDatabase":
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
class CylindricalCutterDatabase(_1883.NamedDatabase[T]):
    """CylindricalCutterDatabase

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_CUTTER_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalCutterDatabase":
        """Cast to another type.

        Returns:
            _Cast_CylindricalCutterDatabase
        """
        return _Cast_CylindricalCutterDatabase(self)
