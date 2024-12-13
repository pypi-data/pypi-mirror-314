"""AccuracyGrades"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import

_ACCURACY_GRADES = python_net_import("SMT.MastaAPI.Gears", "AccuracyGrades")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.agma_gleason_conical import _1232
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
        _1173,
        _1178,
        _1184,
    )

    Self = TypeVar("Self", bound="AccuracyGrades")
    CastSelf = TypeVar("CastSelf", bound="AccuracyGrades._Cast_AccuracyGrades")


__docformat__ = "restructuredtext en"
__all__ = ("AccuracyGrades",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AccuracyGrades:
    """Special nested class for casting AccuracyGrades to subclasses."""

    __parent__: "AccuracyGrades"

    @property
    def agma20151_accuracy_grades(self: "CastSelf") -> "_1173.AGMA20151AccuracyGrades":
        from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
            _1173,
        )

        return self.__parent__._cast(_1173.AGMA20151AccuracyGrades)

    @property
    def cylindrical_accuracy_grades(
        self: "CastSelf",
    ) -> "_1178.CylindricalAccuracyGrades":
        from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
            _1178,
        )

        return self.__parent__._cast(_1178.CylindricalAccuracyGrades)

    @property
    def iso1328_accuracy_grades(self: "CastSelf") -> "_1184.ISO1328AccuracyGrades":
        from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
            _1184,
        )

        return self.__parent__._cast(_1184.ISO1328AccuracyGrades)

    @property
    def agma_gleason_conical_accuracy_grades(
        self: "CastSelf",
    ) -> "_1232.AGMAGleasonConicalAccuracyGrades":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1232

        return self.__parent__._cast(_1232.AGMAGleasonConicalAccuracyGrades)

    @property
    def accuracy_grades(self: "CastSelf") -> "AccuracyGrades":
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
class AccuracyGrades(_0.APIBase):
    """AccuracyGrades

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ACCURACY_GRADES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AccuracyGrades":
        """Cast to another type.

        Returns:
            _Cast_AccuracyGrades
        """
        return _Cast_AccuracyGrades(self)
