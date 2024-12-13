"""GearMeshPointOnFlankContact"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _155

_GEAR_MESH_POINT_ON_FLANK_CONTACT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "GearMeshPointOnFlankContact"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import _134, _145, _146

    Self = TypeVar("Self", bound="GearMeshPointOnFlankContact")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearMeshPointOnFlankContact._Cast_GearMeshPointOnFlankContact",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshPointOnFlankContact",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshPointOnFlankContact:
    """Special nested class for casting GearMeshPointOnFlankContact to subclasses."""

    __parent__: "GearMeshPointOnFlankContact"

    @property
    def two_body_connection_nodal_component(
        self: "CastSelf",
    ) -> "_155.TwoBodyConnectionNodalComponent":
        return self.__parent__._cast(_155.TwoBodyConnectionNodalComponent)

    @property
    def component_nodal_composite(self: "CastSelf") -> "_134.ComponentNodalComposite":
        from mastapy._private.nodal_analysis.nodal_entities import _134

        return self.__parent__._cast(_134.ComponentNodalComposite)

    @property
    def nodal_composite(self: "CastSelf") -> "_145.NodalComposite":
        from mastapy._private.nodal_analysis.nodal_entities import _145

        return self.__parent__._cast(_145.NodalComposite)

    @property
    def nodal_entity(self: "CastSelf") -> "_146.NodalEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _146

        return self.__parent__._cast(_146.NodalEntity)

    @property
    def gear_mesh_point_on_flank_contact(
        self: "CastSelf",
    ) -> "GearMeshPointOnFlankContact":
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
class GearMeshPointOnFlankContact(_155.TwoBodyConnectionNodalComponent):
    """GearMeshPointOnFlankContact

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_POINT_ON_FLANK_CONTACT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshPointOnFlankContact":
        """Cast to another type.

        Returns:
            _Cast_GearMeshPointOnFlankContact
        """
        return _Cast_GearMeshPointOnFlankContact(self)
