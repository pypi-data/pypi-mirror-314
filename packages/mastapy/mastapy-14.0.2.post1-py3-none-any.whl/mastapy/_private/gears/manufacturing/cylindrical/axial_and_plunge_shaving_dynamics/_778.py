"""ConventionalShavingDynamicsCalculationForHobbedGears"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
    _776,
    _793,
)

_CONVENTIONAL_SHAVING_DYNAMICS_CALCULATION_FOR_HOBBED_GEARS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics",
    "ConventionalShavingDynamicsCalculationForHobbedGears",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
        _791,
    )

    Self = TypeVar("Self", bound="ConventionalShavingDynamicsCalculationForHobbedGears")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConventionalShavingDynamicsCalculationForHobbedGears._Cast_ConventionalShavingDynamicsCalculationForHobbedGears",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConventionalShavingDynamicsCalculationForHobbedGears",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConventionalShavingDynamicsCalculationForHobbedGears:
    """Special nested class for casting ConventionalShavingDynamicsCalculationForHobbedGears to subclasses."""

    __parent__: "ConventionalShavingDynamicsCalculationForHobbedGears"

    @property
    def shaving_dynamics_calculation_for_hobbed_gears(
        self: "CastSelf",
    ) -> "_793.ShavingDynamicsCalculationForHobbedGears":
        return self.__parent__._cast(_793.ShavingDynamicsCalculationForHobbedGears)

    @property
    def shaving_dynamics_calculation(
        self: "CastSelf",
    ) -> "_791.ShavingDynamicsCalculation":
        from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
            _791,
        )

        return self.__parent__._cast(_791.ShavingDynamicsCalculation)

    @property
    def conventional_shaving_dynamics_calculation_for_hobbed_gears(
        self: "CastSelf",
    ) -> "ConventionalShavingDynamicsCalculationForHobbedGears":
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
class ConventionalShavingDynamicsCalculationForHobbedGears(
    _793.ShavingDynamicsCalculationForHobbedGears[_776.ConventionalShavingDynamics]
):
    """ConventionalShavingDynamicsCalculationForHobbedGears

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONVENTIONAL_SHAVING_DYNAMICS_CALCULATION_FOR_HOBBED_GEARS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ConventionalShavingDynamicsCalculationForHobbedGears":
        """Cast to another type.

        Returns:
            _Cast_ConventionalShavingDynamicsCalculationForHobbedGears
        """
        return _Cast_ConventionalShavingDynamicsCalculationForHobbedGears(self)
