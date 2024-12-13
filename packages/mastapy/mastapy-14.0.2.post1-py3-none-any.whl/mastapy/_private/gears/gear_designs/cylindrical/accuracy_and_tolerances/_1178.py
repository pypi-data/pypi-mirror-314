"""CylindricalAccuracyGrades"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears import _326

_CYLINDRICAL_ACCURACY_GRADES = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.AccuracyAndTolerances",
    "CylindricalAccuracyGrades",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
        _1173,
        _1184,
    )

    Self = TypeVar("Self", bound="CylindricalAccuracyGrades")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalAccuracyGrades._Cast_CylindricalAccuracyGrades"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalAccuracyGrades",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalAccuracyGrades:
    """Special nested class for casting CylindricalAccuracyGrades to subclasses."""

    __parent__: "CylindricalAccuracyGrades"

    @property
    def accuracy_grades(self: "CastSelf") -> "_326.AccuracyGrades":
        return self.__parent__._cast(_326.AccuracyGrades)

    @property
    def agma20151_accuracy_grades(self: "CastSelf") -> "_1173.AGMA20151AccuracyGrades":
        from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
            _1173,
        )

        return self.__parent__._cast(_1173.AGMA20151AccuracyGrades)

    @property
    def iso1328_accuracy_grades(self: "CastSelf") -> "_1184.ISO1328AccuracyGrades":
        from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
            _1184,
        )

        return self.__parent__._cast(_1184.ISO1328AccuracyGrades)

    @property
    def cylindrical_accuracy_grades(self: "CastSelf") -> "CylindricalAccuracyGrades":
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
class CylindricalAccuracyGrades(_326.AccuracyGrades):
    """CylindricalAccuracyGrades

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_ACCURACY_GRADES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def helix_quality_grade(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "HelixQualityGrade")

        if temp is None:
            return 0

        return temp

    @helix_quality_grade.setter
    @enforce_parameter_types
    def helix_quality_grade(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "HelixQualityGrade", int(value) if value is not None else 0
        )

    @property
    def pitch_quality_grade(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "PitchQualityGrade")

        if temp is None:
            return 0

        return temp

    @pitch_quality_grade.setter
    @enforce_parameter_types
    def pitch_quality_grade(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "PitchQualityGrade", int(value) if value is not None else 0
        )

    @property
    def profile_quality_grade(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "ProfileQualityGrade")

        if temp is None:
            return 0

        return temp

    @profile_quality_grade.setter
    @enforce_parameter_types
    def profile_quality_grade(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "ProfileQualityGrade", int(value) if value is not None else 0
        )

    @property
    def radial_quality_grade(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "RadialQualityGrade")

        if temp is None:
            return 0

        return temp

    @radial_quality_grade.setter
    @enforce_parameter_types
    def radial_quality_grade(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "RadialQualityGrade", int(value) if value is not None else 0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalAccuracyGrades":
        """Cast to another type.

        Returns:
            _Cast_CylindricalAccuracyGrades
        """
        return _Cast_CylindricalAccuracyGrades(self)
