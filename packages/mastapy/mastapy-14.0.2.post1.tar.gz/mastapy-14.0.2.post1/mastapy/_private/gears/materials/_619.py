"""ISOTC60CoefficientOfFrictionCalculator"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.materials import _613

_ISOTC60_COEFFICIENT_OF_FRICTION_CALCULATOR = python_net_import(
    "SMT.MastaAPI.Gears.Materials", "ISOTC60CoefficientOfFrictionCalculator"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.materials import _603

    Self = TypeVar("Self", bound="ISOTC60CoefficientOfFrictionCalculator")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISOTC60CoefficientOfFrictionCalculator._Cast_ISOTC60CoefficientOfFrictionCalculator",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISOTC60CoefficientOfFrictionCalculator",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISOTC60CoefficientOfFrictionCalculator:
    """Special nested class for casting ISOTC60CoefficientOfFrictionCalculator to subclasses."""

    __parent__: "ISOTC60CoefficientOfFrictionCalculator"

    @property
    def instantaneous_coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "_613.InstantaneousCoefficientOfFrictionCalculator":
        return self.__parent__._cast(_613.InstantaneousCoefficientOfFrictionCalculator)

    @property
    def coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "_603.CoefficientOfFrictionCalculator":
        from mastapy._private.gears.materials import _603

        return self.__parent__._cast(_603.CoefficientOfFrictionCalculator)

    @property
    def isotc60_coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "ISOTC60CoefficientOfFrictionCalculator":
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
class ISOTC60CoefficientOfFrictionCalculator(
    _613.InstantaneousCoefficientOfFrictionCalculator
):
    """ISOTC60CoefficientOfFrictionCalculator

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISOTC60_COEFFICIENT_OF_FRICTION_CALCULATOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ISOTC60CoefficientOfFrictionCalculator":
        """Cast to another type.

        Returns:
            _Cast_ISOTC60CoefficientOfFrictionCalculator
        """
        return _Cast_ISOTC60CoefficientOfFrictionCalculator(self)
