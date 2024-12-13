"""GearBendingStiffnessNode"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.ltca import _873

_GEAR_BENDING_STIFFNESS_NODE = python_net_import(
    "SMT.MastaAPI.Gears.LTCA", "GearBendingStiffnessNode"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.ltca.conical import _889
    from mastapy._private.gears.ltca.cylindrical import _877
    from mastapy._private.nodal_analysis import _67

    Self = TypeVar("Self", bound="GearBendingStiffnessNode")
    CastSelf = TypeVar(
        "CastSelf", bound="GearBendingStiffnessNode._Cast_GearBendingStiffnessNode"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearBendingStiffnessNode",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearBendingStiffnessNode:
    """Special nested class for casting GearBendingStiffnessNode to subclasses."""

    __parent__: "GearBendingStiffnessNode"

    @property
    def gear_stiffness_node(self: "CastSelf") -> "_873.GearStiffnessNode":
        return self.__parent__._cast(_873.GearStiffnessNode)

    @property
    def fe_stiffness_node(self: "CastSelf") -> "_67.FEStiffnessNode":
        from mastapy._private.nodal_analysis import _67

        return self.__parent__._cast(_67.FEStiffnessNode)

    @property
    def cylindrical_gear_bending_stiffness_node(
        self: "CastSelf",
    ) -> "_877.CylindricalGearBendingStiffnessNode":
        from mastapy._private.gears.ltca.cylindrical import _877

        return self.__parent__._cast(_877.CylindricalGearBendingStiffnessNode)

    @property
    def conical_gear_bending_stiffness_node(
        self: "CastSelf",
    ) -> "_889.ConicalGearBendingStiffnessNode":
        from mastapy._private.gears.ltca.conical import _889

        return self.__parent__._cast(_889.ConicalGearBendingStiffnessNode)

    @property
    def gear_bending_stiffness_node(self: "CastSelf") -> "GearBendingStiffnessNode":
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
class GearBendingStiffnessNode(_873.GearStiffnessNode):
    """GearBendingStiffnessNode

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_BENDING_STIFFNESS_NODE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearBendingStiffnessNode":
        """Cast to another type.

        Returns:
            _Cast_GearBendingStiffnessNode
        """
        return _Cast_GearBendingStiffnessNode(self)
