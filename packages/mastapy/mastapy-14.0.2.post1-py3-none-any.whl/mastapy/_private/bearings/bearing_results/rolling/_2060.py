"""LoadedCrossedRollerBearingElement"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_results.rolling import _2084

_LOADED_CROSSED_ROLLER_BEARING_ELEMENT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedCrossedRollerBearingElement"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2070

    Self = TypeVar("Self", bound="LoadedCrossedRollerBearingElement")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedCrossedRollerBearingElement._Cast_LoadedCrossedRollerBearingElement",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedCrossedRollerBearingElement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedCrossedRollerBearingElement:
    """Special nested class for casting LoadedCrossedRollerBearingElement to subclasses."""

    __parent__: "LoadedCrossedRollerBearingElement"

    @property
    def loaded_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2084.LoadedRollerBearingElement":
        return self.__parent__._cast(_2084.LoadedRollerBearingElement)

    @property
    def loaded_element(self: "CastSelf") -> "_2070.LoadedElement":
        from mastapy._private.bearings.bearing_results.rolling import _2070

        return self.__parent__._cast(_2070.LoadedElement)

    @property
    def loaded_crossed_roller_bearing_element(
        self: "CastSelf",
    ) -> "LoadedCrossedRollerBearingElement":
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
class LoadedCrossedRollerBearingElement(_2084.LoadedRollerBearingElement):
    """LoadedCrossedRollerBearingElement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_CROSSED_ROLLER_BEARING_ELEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedCrossedRollerBearingElement":
        """Cast to another type.

        Returns:
            _Cast_LoadedCrossedRollerBearingElement
        """
        return _Cast_LoadedCrossedRollerBearingElement(self)
