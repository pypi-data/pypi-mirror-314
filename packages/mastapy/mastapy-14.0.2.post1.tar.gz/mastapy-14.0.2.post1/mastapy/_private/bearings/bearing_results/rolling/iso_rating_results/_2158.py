"""BallISOTS162812008Results"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import _2162

_BALL_ISOTS162812008_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.IsoRatingResults",
    "BallISOTS162812008Results",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
        _2161,
    )

    Self = TypeVar("Self", bound="BallISOTS162812008Results")
    CastSelf = TypeVar(
        "CastSelf", bound="BallISOTS162812008Results._Cast_BallISOTS162812008Results"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BallISOTS162812008Results",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BallISOTS162812008Results:
    """Special nested class for casting BallISOTS162812008Results to subclasses."""

    __parent__: "BallISOTS162812008Results"

    @property
    def isots162812008_results(self: "CastSelf") -> "_2162.ISOTS162812008Results":
        return self.__parent__._cast(_2162.ISOTS162812008Results)

    @property
    def iso_results(self: "CastSelf") -> "_2161.ISOResults":
        from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
            _2161,
        )

        return self.__parent__._cast(_2161.ISOResults)

    @property
    def ball_isots162812008_results(self: "CastSelf") -> "BallISOTS162812008Results":
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
class BallISOTS162812008Results(_2162.ISOTS162812008Results):
    """BallISOTS162812008Results

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BALL_ISOTS162812008_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def contact_stiffness_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactStiffnessInner")

        if temp is None:
            return 0.0

        return temp

    @property
    def contact_stiffness_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactStiffnessOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_BallISOTS162812008Results":
        """Cast to another type.

        Returns:
            _Cast_BallISOTS162812008Results
        """
        return _Cast_BallISOTS162812008Results(self)
