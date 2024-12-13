"""ConicalGearContactStiffnessNode"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.ltca import _861

_CONICAL_GEAR_CONTACT_STIFFNESS_NODE = python_net_import(
    "SMT.MastaAPI.Gears.LTCA.Conical", "ConicalGearContactStiffnessNode"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.ltca import _873
    from mastapy._private.nodal_analysis import _67

    Self = TypeVar("Self", bound="ConicalGearContactStiffnessNode")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearContactStiffnessNode._Cast_ConicalGearContactStiffnessNode",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearContactStiffnessNode",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearContactStiffnessNode:
    """Special nested class for casting ConicalGearContactStiffnessNode to subclasses."""

    __parent__: "ConicalGearContactStiffnessNode"

    @property
    def gear_contact_stiffness_node(
        self: "CastSelf",
    ) -> "_861.GearContactStiffnessNode":
        return self.__parent__._cast(_861.GearContactStiffnessNode)

    @property
    def gear_stiffness_node(self: "CastSelf") -> "_873.GearStiffnessNode":
        from mastapy._private.gears.ltca import _873

        return self.__parent__._cast(_873.GearStiffnessNode)

    @property
    def fe_stiffness_node(self: "CastSelf") -> "_67.FEStiffnessNode":
        from mastapy._private.nodal_analysis import _67

        return self.__parent__._cast(_67.FEStiffnessNode)

    @property
    def conical_gear_contact_stiffness_node(
        self: "CastSelf",
    ) -> "ConicalGearContactStiffnessNode":
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
class ConicalGearContactStiffnessNode(_861.GearContactStiffnessNode):
    """ConicalGearContactStiffnessNode

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_CONTACT_STIFFNESS_NODE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearContactStiffnessNode":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearContactStiffnessNode
        """
        return _Cast_ConicalGearContactStiffnessNode(self)
