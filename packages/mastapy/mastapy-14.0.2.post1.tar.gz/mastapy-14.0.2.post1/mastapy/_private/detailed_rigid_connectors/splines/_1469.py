"""StandardSplineHalfDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.detailed_rigid_connectors.splines import _1464

_STANDARD_SPLINE_HALF_DESIGN = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines", "StandardSplineHalfDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.detailed_rigid_connectors import _1438
    from mastapy._private.detailed_rigid_connectors.splines import (
        _1442,
        _1446,
        _1449,
        _1457,
    )

    Self = TypeVar("Self", bound="StandardSplineHalfDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="StandardSplineHalfDesign._Cast_StandardSplineHalfDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("StandardSplineHalfDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StandardSplineHalfDesign:
    """Special nested class for casting StandardSplineHalfDesign to subclasses."""

    __parent__: "StandardSplineHalfDesign"

    @property
    def spline_half_design(self: "CastSelf") -> "_1464.SplineHalfDesign":
        return self.__parent__._cast(_1464.SplineHalfDesign)

    @property
    def detailed_rigid_connector_half_design(
        self: "CastSelf",
    ) -> "_1438.DetailedRigidConnectorHalfDesign":
        from mastapy._private.detailed_rigid_connectors import _1438

        return self.__parent__._cast(_1438.DetailedRigidConnectorHalfDesign)

    @property
    def din5480_spline_half_design(self: "CastSelf") -> "_1442.DIN5480SplineHalfDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1442

        return self.__parent__._cast(_1442.DIN5480SplineHalfDesign)

    @property
    def gbt3478_spline_half_design(self: "CastSelf") -> "_1446.GBT3478SplineHalfDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1446

        return self.__parent__._cast(_1446.GBT3478SplineHalfDesign)

    @property
    def iso4156_spline_half_design(self: "CastSelf") -> "_1449.ISO4156SplineHalfDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1449

        return self.__parent__._cast(_1449.ISO4156SplineHalfDesign)

    @property
    def sae_spline_half_design(self: "CastSelf") -> "_1457.SAESplineHalfDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1457

        return self.__parent__._cast(_1457.SAESplineHalfDesign)

    @property
    def standard_spline_half_design(self: "CastSelf") -> "StandardSplineHalfDesign":
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
class StandardSplineHalfDesign(_1464.SplineHalfDesign):
    """StandardSplineHalfDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STANDARD_SPLINE_HALF_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_StandardSplineHalfDesign":
        """Cast to another type.

        Returns:
            _Cast_StandardSplineHalfDesign
        """
        return _Cast_StandardSplineHalfDesign(self)
