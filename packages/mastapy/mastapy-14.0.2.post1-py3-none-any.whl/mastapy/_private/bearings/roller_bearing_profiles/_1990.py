"""RollerBearingLundbergProfile"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.roller_bearing_profiles import _1991

_ROLLER_BEARING_LUNDBERG_PROFILE = python_net_import(
    "SMT.MastaAPI.Bearings.RollerBearingProfiles", "RollerBearingLundbergProfile"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RollerBearingLundbergProfile")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RollerBearingLundbergProfile._Cast_RollerBearingLundbergProfile",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollerBearingLundbergProfile",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollerBearingLundbergProfile:
    """Special nested class for casting RollerBearingLundbergProfile to subclasses."""

    __parent__: "RollerBearingLundbergProfile"

    @property
    def roller_bearing_profile(self: "CastSelf") -> "_1991.RollerBearingProfile":
        return self.__parent__._cast(_1991.RollerBearingProfile)

    @property
    def roller_bearing_lundberg_profile(
        self: "CastSelf",
    ) -> "RollerBearingLundbergProfile":
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
class RollerBearingLundbergProfile(_1991.RollerBearingProfile):
    """RollerBearingLundbergProfile

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLER_BEARING_LUNDBERG_PROFILE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def load(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Load")

        if temp is None:
            return 0.0

        return temp

    @load.setter
    @enforce_parameter_types
    def load(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Load", float(value) if value is not None else 0.0
        )

    @property
    def use_bearing_dynamic_capacity(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseBearingDynamicCapacity")

        if temp is None:
            return False

        return temp

    @use_bearing_dynamic_capacity.setter
    @enforce_parameter_types
    def use_bearing_dynamic_capacity(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseBearingDynamicCapacity",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_RollerBearingLundbergProfile":
        """Cast to another type.

        Returns:
            _Cast_RollerBearingLundbergProfile
        """
        return _Cast_RollerBearingLundbergProfile(self)
