"""UserSpecifiedRollerRaceProfilePoint"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.roller_bearing_profiles import _1994

_USER_SPECIFIED_ROLLER_RACE_PROFILE_POINT = python_net_import(
    "SMT.MastaAPI.Bearings.RollerBearingProfiles", "UserSpecifiedRollerRaceProfilePoint"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="UserSpecifiedRollerRaceProfilePoint")
    CastSelf = TypeVar(
        "CastSelf",
        bound="UserSpecifiedRollerRaceProfilePoint._Cast_UserSpecifiedRollerRaceProfilePoint",
    )


__docformat__ = "restructuredtext en"
__all__ = ("UserSpecifiedRollerRaceProfilePoint",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_UserSpecifiedRollerRaceProfilePoint:
    """Special nested class for casting UserSpecifiedRollerRaceProfilePoint to subclasses."""

    __parent__: "UserSpecifiedRollerRaceProfilePoint"

    @property
    def roller_race_profile_point(self: "CastSelf") -> "_1994.RollerRaceProfilePoint":
        return self.__parent__._cast(_1994.RollerRaceProfilePoint)

    @property
    def user_specified_roller_race_profile_point(
        self: "CastSelf",
    ) -> "UserSpecifiedRollerRaceProfilePoint":
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
class UserSpecifiedRollerRaceProfilePoint(_1994.RollerRaceProfilePoint):
    """UserSpecifiedRollerRaceProfilePoint

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _USER_SPECIFIED_ROLLER_RACE_PROFILE_POINT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def race_deviation_used_in_analysis(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RaceDeviationUsedInAnalysis")

        if temp is None:
            return 0.0

        return temp

    @property
    def roller_deviation_used_in_analysis(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollerDeviationUsedInAnalysis")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_UserSpecifiedRollerRaceProfilePoint":
        """Cast to another type.

        Returns:
            _Cast_UserSpecifiedRollerRaceProfilePoint
        """
        return _Cast_UserSpecifiedRollerRaceProfilePoint(self)
