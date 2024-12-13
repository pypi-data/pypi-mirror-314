"""LoadedSphericalThrustRollerBearingElement"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_results.rolling import _2095

_LOADED_SPHERICAL_THRUST_ROLLER_BEARING_ELEMENT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedSphericalThrustRollerBearingElement",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2070, _2084

    Self = TypeVar("Self", bound="LoadedSphericalThrustRollerBearingElement")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedSphericalThrustRollerBearingElement._Cast_LoadedSphericalThrustRollerBearingElement",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedSphericalThrustRollerBearingElement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedSphericalThrustRollerBearingElement:
    """Special nested class for casting LoadedSphericalThrustRollerBearingElement to subclasses."""

    __parent__: "LoadedSphericalThrustRollerBearingElement"

    @property
    def loaded_spherical_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2095.LoadedSphericalRollerBearingElement":
        return self.__parent__._cast(_2095.LoadedSphericalRollerBearingElement)

    @property
    def loaded_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2084.LoadedRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2084

        return self.__parent__._cast(_2084.LoadedRollerBearingElement)

    @property
    def loaded_element(self: "CastSelf") -> "_2070.LoadedElement":
        from mastapy._private.bearings.bearing_results.rolling import _2070

        return self.__parent__._cast(_2070.LoadedElement)

    @property
    def loaded_spherical_thrust_roller_bearing_element(
        self: "CastSelf",
    ) -> "LoadedSphericalThrustRollerBearingElement":
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
class LoadedSphericalThrustRollerBearingElement(
    _2095.LoadedSphericalRollerBearingElement
):
    """LoadedSphericalThrustRollerBearingElement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_SPHERICAL_THRUST_ROLLER_BEARING_ELEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedSphericalThrustRollerBearingElement":
        """Cast to another type.

        Returns:
            _Cast_LoadedSphericalThrustRollerBearingElement
        """
        return _Cast_LoadedSphericalThrustRollerBearingElement(self)
