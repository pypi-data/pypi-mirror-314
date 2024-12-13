"""RollerBearingProfile"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ROLLER_BEARING_PROFILE = python_net_import(
    "SMT.MastaAPI.Bearings.RollerBearingProfiles", "RollerBearingProfile"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.roller_bearing_profiles import (
        _1985,
        _1986,
        _1987,
        _1988,
        _1989,
        _1990,
        _1992,
        _1993,
    )

    Self = TypeVar("Self", bound="RollerBearingProfile")
    CastSelf = TypeVar(
        "CastSelf", bound="RollerBearingProfile._Cast_RollerBearingProfile"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollerBearingProfile",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollerBearingProfile:
    """Special nested class for casting RollerBearingProfile to subclasses."""

    __parent__: "RollerBearingProfile"

    @property
    def roller_bearing_conical_profile(
        self: "CastSelf",
    ) -> "_1985.RollerBearingConicalProfile":
        from mastapy._private.bearings.roller_bearing_profiles import _1985

        return self.__parent__._cast(_1985.RollerBearingConicalProfile)

    @property
    def roller_bearing_crowned_profile(
        self: "CastSelf",
    ) -> "_1986.RollerBearingCrownedProfile":
        from mastapy._private.bearings.roller_bearing_profiles import _1986

        return self.__parent__._cast(_1986.RollerBearingCrownedProfile)

    @property
    def roller_bearing_din_lundberg_profile(
        self: "CastSelf",
    ) -> "_1987.RollerBearingDinLundbergProfile":
        from mastapy._private.bearings.roller_bearing_profiles import _1987

        return self.__parent__._cast(_1987.RollerBearingDinLundbergProfile)

    @property
    def roller_bearing_flat_profile(
        self: "CastSelf",
    ) -> "_1988.RollerBearingFlatProfile":
        from mastapy._private.bearings.roller_bearing_profiles import _1988

        return self.__parent__._cast(_1988.RollerBearingFlatProfile)

    @property
    def roller_bearing_johns_gohar_profile(
        self: "CastSelf",
    ) -> "_1989.RollerBearingJohnsGoharProfile":
        from mastapy._private.bearings.roller_bearing_profiles import _1989

        return self.__parent__._cast(_1989.RollerBearingJohnsGoharProfile)

    @property
    def roller_bearing_lundberg_profile(
        self: "CastSelf",
    ) -> "_1990.RollerBearingLundbergProfile":
        from mastapy._private.bearings.roller_bearing_profiles import _1990

        return self.__parent__._cast(_1990.RollerBearingLundbergProfile)

    @property
    def roller_bearing_tangential_crowned_profile(
        self: "CastSelf",
    ) -> "_1992.RollerBearingTangentialCrownedProfile":
        from mastapy._private.bearings.roller_bearing_profiles import _1992

        return self.__parent__._cast(_1992.RollerBearingTangentialCrownedProfile)

    @property
    def roller_bearing_user_specified_profile(
        self: "CastSelf",
    ) -> "_1993.RollerBearingUserSpecifiedProfile":
        from mastapy._private.bearings.roller_bearing_profiles import _1993

        return self.__parent__._cast(_1993.RollerBearingUserSpecifiedProfile)

    @property
    def roller_bearing_profile(self: "CastSelf") -> "RollerBearingProfile":
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
class RollerBearingProfile(_0.APIBase):
    """RollerBearingProfile

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLER_BEARING_PROFILE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def covers_two_rows_of_elements(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CoversTwoRowsOfElements")

        if temp is None:
            return False

        return temp

    @covers_two_rows_of_elements.setter
    @enforce_parameter_types
    def covers_two_rows_of_elements(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CoversTwoRowsOfElements",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_RollerBearingProfile":
        """Cast to another type.

        Returns:
            _Cast_RollerBearingProfile
        """
        return _Cast_RollerBearingProfile(self)
