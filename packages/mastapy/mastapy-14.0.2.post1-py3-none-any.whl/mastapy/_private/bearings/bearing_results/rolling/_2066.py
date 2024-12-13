"""LoadedCylindricalRollerBearingRow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results.rolling import _2081

_LOADED_CYLINDRICAL_ROLLER_BEARING_ROW = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedCylindricalRollerBearingRow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import (
        _2065,
        _2078,
        _2086,
        _2090,
    )

    Self = TypeVar("Self", bound="LoadedCylindricalRollerBearingRow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedCylindricalRollerBearingRow._Cast_LoadedCylindricalRollerBearingRow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedCylindricalRollerBearingRow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedCylindricalRollerBearingRow:
    """Special nested class for casting LoadedCylindricalRollerBearingRow to subclasses."""

    __parent__: "LoadedCylindricalRollerBearingRow"

    @property
    def loaded_non_barrel_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2081.LoadedNonBarrelRollerBearingRow":
        return self.__parent__._cast(_2081.LoadedNonBarrelRollerBearingRow)

    @property
    def loaded_roller_bearing_row(self: "CastSelf") -> "_2086.LoadedRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2086

        return self.__parent__._cast(_2086.LoadedRollerBearingRow)

    @property
    def loaded_rolling_bearing_row(self: "CastSelf") -> "_2090.LoadedRollingBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2090

        return self.__parent__._cast(_2090.LoadedRollingBearingRow)

    @property
    def loaded_needle_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2078.LoadedNeedleRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2078

        return self.__parent__._cast(_2078.LoadedNeedleRollerBearingRow)

    @property
    def loaded_cylindrical_roller_bearing_row(
        self: "CastSelf",
    ) -> "LoadedCylindricalRollerBearingRow":
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
class LoadedCylindricalRollerBearingRow(_2081.LoadedNonBarrelRollerBearingRow):
    """LoadedCylindricalRollerBearingRow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_CYLINDRICAL_ROLLER_BEARING_ROW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def loaded_bearing(self: "Self") -> "_2065.LoadedCylindricalRollerBearingResults":
        """mastapy.bearings.bearing_results.rolling.LoadedCylindricalRollerBearingResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadedBearing")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedCylindricalRollerBearingRow":
        """Cast to another type.

        Returns:
            _Cast_LoadedCylindricalRollerBearingRow
        """
        return _Cast_LoadedCylindricalRollerBearingRow(self)
