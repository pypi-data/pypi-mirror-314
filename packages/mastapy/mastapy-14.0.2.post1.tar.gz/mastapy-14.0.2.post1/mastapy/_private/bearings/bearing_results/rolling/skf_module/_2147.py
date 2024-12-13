"""MinimumLoad"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results.rolling.skf_module import _2152

_MINIMUM_LOAD = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule", "MinimumLoad"
)

if TYPE_CHECKING:
    from typing import Any, Optional, Type, TypeVar

    Self = TypeVar("Self", bound="MinimumLoad")
    CastSelf = TypeVar("CastSelf", bound="MinimumLoad._Cast_MinimumLoad")


__docformat__ = "restructuredtext en"
__all__ = ("MinimumLoad",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MinimumLoad:
    """Special nested class for casting MinimumLoad to subclasses."""

    __parent__: "MinimumLoad"

    @property
    def skf_calculation_result(self: "CastSelf") -> "_2152.SKFCalculationResult":
        return self.__parent__._cast(_2152.SKFCalculationResult)

    @property
    def minimum_load(self: "CastSelf") -> "MinimumLoad":
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
class MinimumLoad(_2152.SKFCalculationResult):
    """MinimumLoad

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MINIMUM_LOAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def minimum_axial_load(self: "Self") -> "Optional[float]":
        """Optional[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumAxialLoad")

        if temp is None:
            return None

        return temp

    @property
    def minimum_equivalent_load(self: "Self") -> "Optional[float]":
        """Optional[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumEquivalentLoad")

        if temp is None:
            return None

        return temp

    @property
    def minimum_radial_load(self: "Self") -> "Optional[float]":
        """Optional[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumRadialLoad")

        if temp is None:
            return None

        return temp

    @property
    def requirement_met(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RequirementMet")

        if temp is None:
            return False

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_MinimumLoad":
        """Cast to another type.

        Returns:
            _Cast_MinimumLoad
        """
        return _Cast_MinimumLoad(self)
