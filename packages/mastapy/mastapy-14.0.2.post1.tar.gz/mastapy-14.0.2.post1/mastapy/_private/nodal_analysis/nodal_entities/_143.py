"""LineContactStiffnessEntity"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.nodal_analysis.nodal_entities import _126

_LINE_CONTACT_STIFFNESS_ENTITY = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "LineContactStiffnessEntity"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis import _79
    from mastapy._private.nodal_analysis.nodal_entities import _144, _146

    Self = TypeVar("Self", bound="LineContactStiffnessEntity")
    CastSelf = TypeVar(
        "CastSelf", bound="LineContactStiffnessEntity._Cast_LineContactStiffnessEntity"
    )


__docformat__ = "restructuredtext en"
__all__ = ("LineContactStiffnessEntity",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LineContactStiffnessEntity:
    """Special nested class for casting LineContactStiffnessEntity to subclasses."""

    __parent__: "LineContactStiffnessEntity"

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
    def line_contact_stiffness_entity(self: "CastSelf") -> "LineContactStiffnessEntity":
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
class LineContactStiffnessEntity(_126.ArbitraryNodalComponent):
    """LineContactStiffnessEntity

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LINE_CONTACT_STIFFNESS_ENTITY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def stiffness_in_local_coordinate_system(self: "Self") -> "_79.NodalMatrix":
        """mastapy.nodal_analysis.NodalMatrix

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessInLocalCoordinateSystem")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_LineContactStiffnessEntity":
        """Cast to another type.

        Returns:
            _Cast_LineContactStiffnessEntity
        """
        return _Cast_LineContactStiffnessEntity(self)
