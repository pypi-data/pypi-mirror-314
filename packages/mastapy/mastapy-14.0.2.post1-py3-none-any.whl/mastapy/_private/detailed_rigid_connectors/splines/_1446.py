"""GBT3478SplineHalfDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.detailed_rigid_connectors.splines import _1449

_GBT3478_SPLINE_HALF_DESIGN = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines", "GBT3478SplineHalfDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.detailed_rigid_connectors import _1438
    from mastapy._private.detailed_rigid_connectors.splines import _1464, _1469

    Self = TypeVar("Self", bound="GBT3478SplineHalfDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="GBT3478SplineHalfDesign._Cast_GBT3478SplineHalfDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GBT3478SplineHalfDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GBT3478SplineHalfDesign:
    """Special nested class for casting GBT3478SplineHalfDesign to subclasses."""

    __parent__: "GBT3478SplineHalfDesign"

    @property
    def iso4156_spline_half_design(self: "CastSelf") -> "_1449.ISO4156SplineHalfDesign":
        return self.__parent__._cast(_1449.ISO4156SplineHalfDesign)

    @property
    def standard_spline_half_design(
        self: "CastSelf",
    ) -> "_1469.StandardSplineHalfDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1469

        return self.__parent__._cast(_1469.StandardSplineHalfDesign)

    @property
    def spline_half_design(self: "CastSelf") -> "_1464.SplineHalfDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1464

        return self.__parent__._cast(_1464.SplineHalfDesign)

    @property
    def detailed_rigid_connector_half_design(
        self: "CastSelf",
    ) -> "_1438.DetailedRigidConnectorHalfDesign":
        from mastapy._private.detailed_rigid_connectors import _1438

        return self.__parent__._cast(_1438.DetailedRigidConnectorHalfDesign)

    @property
    def gbt3478_spline_half_design(self: "CastSelf") -> "GBT3478SplineHalfDesign":
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
class GBT3478SplineHalfDesign(_1449.ISO4156SplineHalfDesign):
    """GBT3478SplineHalfDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GBT3478_SPLINE_HALF_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GBT3478SplineHalfDesign":
        """Cast to another type.

        Returns:
            _Cast_GBT3478SplineHalfDesign
        """
        return _Cast_GBT3478SplineHalfDesign(self)
