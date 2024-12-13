"""BoltedJointMaterialDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.databases import _1883

_BOLTED_JOINT_MATERIAL_DATABASE = python_net_import(
    "SMT.MastaAPI.Bolts", "BoltedJointMaterialDatabase"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.bolts import _1516, _1521, _1526
    from mastapy._private.utility.databases import _1879, _1886

    Self = TypeVar("Self", bound="BoltedJointMaterialDatabase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BoltedJointMaterialDatabase._Cast_BoltedJointMaterialDatabase",
    )

T = TypeVar("T", bound="_1516.BoltedJointMaterial")

__docformat__ = "restructuredtext en"
__all__ = ("BoltedJointMaterialDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BoltedJointMaterialDatabase:
    """Special nested class for casting BoltedJointMaterialDatabase to subclasses."""

    __parent__: "BoltedJointMaterialDatabase"

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
    def bolt_material_database(self: "CastSelf") -> "_1521.BoltMaterialDatabase":
        from mastapy._private.bolts import _1521

        return self.__parent__._cast(_1521.BoltMaterialDatabase)

    @property
    def clamped_section_material_database(
        self: "CastSelf",
    ) -> "_1526.ClampedSectionMaterialDatabase":
        from mastapy._private.bolts import _1526

        return self.__parent__._cast(_1526.ClampedSectionMaterialDatabase)

    @property
    def bolted_joint_material_database(
        self: "CastSelf",
    ) -> "BoltedJointMaterialDatabase":
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
class BoltedJointMaterialDatabase(_1883.NamedDatabase[T]):
    """BoltedJointMaterialDatabase

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _BOLTED_JOINT_MATERIAL_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_BoltedJointMaterialDatabase":
        """Cast to another type.

        Returns:
            _Cast_BoltedJointMaterialDatabase
        """
        return _Cast_BoltedJointMaterialDatabase(self)
