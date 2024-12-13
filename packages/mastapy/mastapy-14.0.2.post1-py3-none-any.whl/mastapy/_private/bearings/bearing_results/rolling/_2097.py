"""LoadedSphericalRollerRadialBearingRow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results.rolling import _2086

_LOADED_SPHERICAL_ROLLER_RADIAL_BEARING_ROW = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedSphericalRollerRadialBearingRow",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2090, _2096

    Self = TypeVar("Self", bound="LoadedSphericalRollerRadialBearingRow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedSphericalRollerRadialBearingRow._Cast_LoadedSphericalRollerRadialBearingRow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedSphericalRollerRadialBearingRow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedSphericalRollerRadialBearingRow:
    """Special nested class for casting LoadedSphericalRollerRadialBearingRow to subclasses."""

    __parent__: "LoadedSphericalRollerRadialBearingRow"

    @property
    def loaded_roller_bearing_row(self: "CastSelf") -> "_2086.LoadedRollerBearingRow":
        return self.__parent__._cast(_2086.LoadedRollerBearingRow)

    @property
    def loaded_rolling_bearing_row(self: "CastSelf") -> "_2090.LoadedRollingBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2090

        return self.__parent__._cast(_2090.LoadedRollingBearingRow)

    @property
    def loaded_spherical_roller_radial_bearing_row(
        self: "CastSelf",
    ) -> "LoadedSphericalRollerRadialBearingRow":
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
class LoadedSphericalRollerRadialBearingRow(_2086.LoadedRollerBearingRow):
    """LoadedSphericalRollerRadialBearingRow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_SPHERICAL_ROLLER_RADIAL_BEARING_ROW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def loaded_bearing(
        self: "Self",
    ) -> "_2096.LoadedSphericalRollerRadialBearingResults":
        """mastapy.bearings.bearing_results.rolling.LoadedSphericalRollerRadialBearingResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadedBearing")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedSphericalRollerRadialBearingRow":
        """Cast to another type.

        Returns:
            _Cast_LoadedSphericalRollerRadialBearingRow
        """
        return _Cast_LoadedSphericalRollerRadialBearingRow(self)
