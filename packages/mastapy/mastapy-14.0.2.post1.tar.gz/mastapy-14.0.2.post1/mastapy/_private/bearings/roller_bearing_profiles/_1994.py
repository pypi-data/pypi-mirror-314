"""RollerRaceProfilePoint"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_ROLLER_RACE_PROFILE_POINT = python_net_import(
    "SMT.MastaAPI.Bearings.RollerBearingProfiles", "RollerRaceProfilePoint"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.roller_bearing_profiles import _1996

    Self = TypeVar("Self", bound="RollerRaceProfilePoint")
    CastSelf = TypeVar(
        "CastSelf", bound="RollerRaceProfilePoint._Cast_RollerRaceProfilePoint"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollerRaceProfilePoint",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollerRaceProfilePoint:
    """Special nested class for casting RollerRaceProfilePoint to subclasses."""

    __parent__: "RollerRaceProfilePoint"

    @property
    def user_specified_roller_race_profile_point(
        self: "CastSelf",
    ) -> "_1996.UserSpecifiedRollerRaceProfilePoint":
        from mastapy._private.bearings.roller_bearing_profiles import _1996

        return self.__parent__._cast(_1996.UserSpecifiedRollerRaceProfilePoint)

    @property
    def roller_race_profile_point(self: "CastSelf") -> "RollerRaceProfilePoint":
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
class RollerRaceProfilePoint(_0.APIBase):
    """RollerRaceProfilePoint

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLER_RACE_PROFILE_POINT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def offset_from_roller_centre(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OffsetFromRollerCentre")

        if temp is None:
            return 0.0

        return temp

    @property
    def race_deviation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RaceDeviation")

        if temp is None:
            return 0.0

        return temp

    @property
    def roller_deviation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollerDeviation")

        if temp is None:
            return 0.0

        return temp

    @property
    def total_deviation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalDeviation")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_RollerRaceProfilePoint":
        """Cast to another type.

        Returns:
            _Cast_RollerRaceProfilePoint
        """
        return _Cast_RollerRaceProfilePoint(self)
