"""StraightBevelDiffMeshedGearRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.conical import _558

_STRAIGHT_BEVEL_DIFF_MESHED_GEAR_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.StraightBevelDiff", "StraightBevelDiffMeshedGearRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="StraightBevelDiffMeshedGearRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelDiffMeshedGearRating._Cast_StraightBevelDiffMeshedGearRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelDiffMeshedGearRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelDiffMeshedGearRating:
    """Special nested class for casting StraightBevelDiffMeshedGearRating to subclasses."""

    __parent__: "StraightBevelDiffMeshedGearRating"

    @property
    def conical_meshed_gear_rating(self: "CastSelf") -> "_558.ConicalMeshedGearRating":
        return self.__parent__._cast(_558.ConicalMeshedGearRating)

    @property
    def straight_bevel_diff_meshed_gear_rating(
        self: "CastSelf",
    ) -> "StraightBevelDiffMeshedGearRating":
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
class StraightBevelDiffMeshedGearRating(_558.ConicalMeshedGearRating):
    """StraightBevelDiffMeshedGearRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_DIFF_MESHED_GEAR_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def allowable_bending_stress_for_peak_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AllowableBendingStressForPeakTorque"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def allowable_bending_stress_for_performance_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AllowableBendingStressForPerformanceTorque"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def calculated_bending_stress_for_peak_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CalculatedBendingStressForPeakTorque"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def calculated_bending_stress_for_performance_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CalculatedBendingStressForPerformanceTorque"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def peak_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PeakTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    def performance_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PerformanceTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    def rating_result(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatingResult")

        if temp is None:
            return ""

        return temp

    @property
    def safety_factor_for_peak_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorForPeakTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    def safety_factor_for_performance_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorForPerformanceTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    def strength_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StrengthFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def total_torque_transmitted(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalTorqueTransmitted")

        if temp is None:
            return 0.0

        return temp

    @property
    def total_transmitted_peak_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalTransmittedPeakTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelDiffMeshedGearRating":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelDiffMeshedGearRating
        """
        return _Cast_StraightBevelDiffMeshedGearRating(self)
