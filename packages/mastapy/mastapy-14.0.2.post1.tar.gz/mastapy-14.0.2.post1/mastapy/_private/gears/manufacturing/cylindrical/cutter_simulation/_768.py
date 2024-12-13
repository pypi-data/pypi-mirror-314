"""RackSimulationCalculator"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import _756

_RACK_SIMULATION_CALCULATOR = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation",
    "RackSimulationCalculator",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import (
        _765,
        _773,
    )

    Self = TypeVar("Self", bound="RackSimulationCalculator")
    CastSelf = TypeVar(
        "CastSelf", bound="RackSimulationCalculator._Cast_RackSimulationCalculator"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RackSimulationCalculator",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RackSimulationCalculator:
    """Special nested class for casting RackSimulationCalculator to subclasses."""

    __parent__: "RackSimulationCalculator"

    @property
    def cutter_simulation_calc(self: "CastSelf") -> "_756.CutterSimulationCalc":
        return self.__parent__._cast(_756.CutterSimulationCalc)

    @property
    def hob_simulation_calculator(self: "CastSelf") -> "_765.HobSimulationCalculator":
        from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import (
            _765,
        )

        return self.__parent__._cast(_765.HobSimulationCalculator)

    @property
    def worm_grinder_simulation_calculator(
        self: "CastSelf",
    ) -> "_773.WormGrinderSimulationCalculator":
        from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import (
            _773,
        )

        return self.__parent__._cast(_773.WormGrinderSimulationCalculator)

    @property
    def rack_simulation_calculator(self: "CastSelf") -> "RackSimulationCalculator":
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
class RackSimulationCalculator(_756.CutterSimulationCalc):
    """RackSimulationCalculator

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RACK_SIMULATION_CALCULATOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def hob_working_depth_delta(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HobWorkingDepthDelta")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_RackSimulationCalculator":
        """Cast to another type.

        Returns:
            _Cast_RackSimulationCalculator
        """
        return _Cast_RackSimulationCalculator(self)
