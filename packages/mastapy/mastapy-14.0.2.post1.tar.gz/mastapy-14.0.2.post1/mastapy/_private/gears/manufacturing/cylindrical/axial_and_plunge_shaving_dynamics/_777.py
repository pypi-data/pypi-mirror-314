"""ConventionalShavingDynamicsCalculationForDesignedGears"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
    _776,
    _792,
)

_CONVENTIONAL_SHAVING_DYNAMICS_CALCULATION_FOR_DESIGNED_GEARS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics",
    "ConventionalShavingDynamicsCalculationForDesignedGears",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
        _791,
    )

    Self = TypeVar(
        "Self", bound="ConventionalShavingDynamicsCalculationForDesignedGears"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConventionalShavingDynamicsCalculationForDesignedGears._Cast_ConventionalShavingDynamicsCalculationForDesignedGears",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConventionalShavingDynamicsCalculationForDesignedGears",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConventionalShavingDynamicsCalculationForDesignedGears:
    """Special nested class for casting ConventionalShavingDynamicsCalculationForDesignedGears to subclasses."""

    __parent__: "ConventionalShavingDynamicsCalculationForDesignedGears"

    @property
    def shaving_dynamics_calculation_for_designed_gears(
        self: "CastSelf",
    ) -> "_792.ShavingDynamicsCalculationForDesignedGears":
        return self.__parent__._cast(_792.ShavingDynamicsCalculationForDesignedGears)

    @property
    def shaving_dynamics_calculation(
        self: "CastSelf",
    ) -> "_791.ShavingDynamicsCalculation":
        from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
            _791,
        )

        return self.__parent__._cast(_791.ShavingDynamicsCalculation)

    @property
    def conventional_shaving_dynamics_calculation_for_designed_gears(
        self: "CastSelf",
    ) -> "ConventionalShavingDynamicsCalculationForDesignedGears":
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
class ConventionalShavingDynamicsCalculationForDesignedGears(
    _792.ShavingDynamicsCalculationForDesignedGears[_776.ConventionalShavingDynamics]
):
    """ConventionalShavingDynamicsCalculationForDesignedGears

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _CONVENTIONAL_SHAVING_DYNAMICS_CALCULATION_FOR_DESIGNED_GEARS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ConventionalShavingDynamicsCalculationForDesignedGears":
        """Cast to another type.

        Returns:
            _Cast_ConventionalShavingDynamicsCalculationForDesignedGears
        """
        return _Cast_ConventionalShavingDynamicsCalculationForDesignedGears(self)
