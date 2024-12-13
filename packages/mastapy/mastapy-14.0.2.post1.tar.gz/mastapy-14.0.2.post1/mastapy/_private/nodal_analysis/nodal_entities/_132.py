"""BearingAxialMountingClearance"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _126

_BEARING_AXIAL_MOUNTING_CLEARANCE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "BearingAxialMountingClearance"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import _144, _146

    Self = TypeVar("Self", bound="BearingAxialMountingClearance")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BearingAxialMountingClearance._Cast_BearingAxialMountingClearance",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingAxialMountingClearance",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BearingAxialMountingClearance:
    """Special nested class for casting BearingAxialMountingClearance to subclasses."""

    __parent__: "BearingAxialMountingClearance"

    @property
    def arbitrary_nodal_component(self: "CastSelf") -> "_126.ArbitraryNodalComponent":
        return self.__parent__._cast(_126.ArbitraryNodalComponent)

    @property
    def nodal_component(self: "CastSelf") -> "_144.NodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _144

        return self.__parent__._cast(_144.NodalComponent)

    @property
    def nodal_entity(self: "CastSelf") -> "_146.NodalEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _146

        return self.__parent__._cast(_146.NodalEntity)

    @property
    def bearing_axial_mounting_clearance(
        self: "CastSelf",
    ) -> "BearingAxialMountingClearance":
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
class BearingAxialMountingClearance(_126.ArbitraryNodalComponent):
    """BearingAxialMountingClearance

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING_AXIAL_MOUNTING_CLEARANCE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_BearingAxialMountingClearance":
        """Cast to another type.

        Returns:
            _Cast_BearingAxialMountingClearance
        """
        return _Cast_BearingAxialMountingClearance(self)
