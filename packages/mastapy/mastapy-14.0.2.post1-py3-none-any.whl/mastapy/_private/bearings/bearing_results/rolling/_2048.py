"""LoadedAxialThrustCylindricalRollerBearingDutyCycle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_results.rolling import _2079

_LOADED_AXIAL_THRUST_CYLINDRICAL_ROLLER_BEARING_DUTY_CYCLE = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedAxialThrustCylindricalRollerBearingDutyCycle",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2004, _2012, _2015

    Self = TypeVar("Self", bound="LoadedAxialThrustCylindricalRollerBearingDutyCycle")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedAxialThrustCylindricalRollerBearingDutyCycle._Cast_LoadedAxialThrustCylindricalRollerBearingDutyCycle",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedAxialThrustCylindricalRollerBearingDutyCycle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedAxialThrustCylindricalRollerBearingDutyCycle:
    """Special nested class for casting LoadedAxialThrustCylindricalRollerBearingDutyCycle to subclasses."""

    __parent__: "LoadedAxialThrustCylindricalRollerBearingDutyCycle"

    @property
    def loaded_non_barrel_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2079.LoadedNonBarrelRollerBearingDutyCycle":
        return self.__parent__._cast(_2079.LoadedNonBarrelRollerBearingDutyCycle)

    @property
    def loaded_rolling_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2015.LoadedRollingBearingDutyCycle":
        from mastapy._private.bearings.bearing_results import _2015

        return self.__parent__._cast(_2015.LoadedRollingBearingDutyCycle)

    @property
    def loaded_non_linear_bearing_duty_cycle_results(
        self: "CastSelf",
    ) -> "_2012.LoadedNonLinearBearingDutyCycleResults":
        from mastapy._private.bearings.bearing_results import _2012

        return self.__parent__._cast(_2012.LoadedNonLinearBearingDutyCycleResults)

    @property
    def loaded_bearing_duty_cycle(self: "CastSelf") -> "_2004.LoadedBearingDutyCycle":
        from mastapy._private.bearings.bearing_results import _2004

        return self.__parent__._cast(_2004.LoadedBearingDutyCycle)

    @property
    def loaded_axial_thrust_cylindrical_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "LoadedAxialThrustCylindricalRollerBearingDutyCycle":
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
class LoadedAxialThrustCylindricalRollerBearingDutyCycle(
    _2079.LoadedNonBarrelRollerBearingDutyCycle
):
    """LoadedAxialThrustCylindricalRollerBearingDutyCycle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_AXIAL_THRUST_CYLINDRICAL_ROLLER_BEARING_DUTY_CYCLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_LoadedAxialThrustCylindricalRollerBearingDutyCycle":
        """Cast to another type.

        Returns:
            _Cast_LoadedAxialThrustCylindricalRollerBearingDutyCycle
        """
        return _Cast_LoadedAxialThrustCylindricalRollerBearingDutyCycle(self)
