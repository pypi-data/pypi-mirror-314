"""LoadedAxialThrustNeedleRollerBearingElement"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_results.rolling import _2049

_LOADED_AXIAL_THRUST_NEEDLE_ROLLER_BEARING_ELEMENT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedAxialThrustNeedleRollerBearingElement",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2070, _2083, _2084

    Self = TypeVar("Self", bound="LoadedAxialThrustNeedleRollerBearingElement")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedAxialThrustNeedleRollerBearingElement._Cast_LoadedAxialThrustNeedleRollerBearingElement",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedAxialThrustNeedleRollerBearingElement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedAxialThrustNeedleRollerBearingElement:
    """Special nested class for casting LoadedAxialThrustNeedleRollerBearingElement to subclasses."""

    __parent__: "LoadedAxialThrustNeedleRollerBearingElement"

    @property
    def loaded_axial_thrust_cylindrical_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2049.LoadedAxialThrustCylindricalRollerBearingElement":
        return self.__parent__._cast(
            _2049.LoadedAxialThrustCylindricalRollerBearingElement
        )

    @property
    def loaded_non_barrel_roller_element(
        self: "CastSelf",
    ) -> "_2083.LoadedNonBarrelRollerElement":
        from mastapy._private.bearings.bearing_results.rolling import _2083

        return self.__parent__._cast(_2083.LoadedNonBarrelRollerElement)

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
    def loaded_axial_thrust_needle_roller_bearing_element(
        self: "CastSelf",
    ) -> "LoadedAxialThrustNeedleRollerBearingElement":
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
class LoadedAxialThrustNeedleRollerBearingElement(
    _2049.LoadedAxialThrustCylindricalRollerBearingElement
):
    """LoadedAxialThrustNeedleRollerBearingElement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_AXIAL_THRUST_NEEDLE_ROLLER_BEARING_ELEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedAxialThrustNeedleRollerBearingElement":
        """Cast to another type.

        Returns:
            _Cast_LoadedAxialThrustNeedleRollerBearingElement
        """
        return _Cast_LoadedAxialThrustNeedleRollerBearingElement(self)
