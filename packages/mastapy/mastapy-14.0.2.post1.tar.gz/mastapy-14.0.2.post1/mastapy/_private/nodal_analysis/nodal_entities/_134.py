"""ComponentNodalComposite"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _145

_COMPONENT_NODAL_COMPOSITE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "ComponentNodalComposite"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import (
        _128,
        _129,
        _130,
        _135,
        _140,
        _146,
        _150,
        _153,
        _154,
        _155,
    )

    Self = TypeVar("Self", bound="ComponentNodalComposite")
    CastSelf = TypeVar(
        "CastSelf", bound="ComponentNodalComposite._Cast_ComponentNodalComposite"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ComponentNodalComposite",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentNodalComposite:
    """Special nested class for casting ComponentNodalComposite to subclasses."""

    __parent__: "ComponentNodalComposite"

    @property
    def nodal_composite(self: "CastSelf") -> "_145.NodalComposite":
        return self.__parent__._cast(_145.NodalComposite)

    @property
    def nodal_entity(self: "CastSelf") -> "_146.NodalEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _146

        return self.__parent__._cast(_146.NodalEntity)

    @property
    def bar_elastic_mbd(self: "CastSelf") -> "_128.BarElasticMBD":
        from mastapy._private.nodal_analysis.nodal_entities import _128

        return self.__parent__._cast(_128.BarElasticMBD)

    @property
    def bar_mbd(self: "CastSelf") -> "_129.BarMBD":
        from mastapy._private.nodal_analysis.nodal_entities import _129

        return self.__parent__._cast(_129.BarMBD)

    @property
    def bar_rigid_mbd(self: "CastSelf") -> "_130.BarRigidMBD":
        from mastapy._private.nodal_analysis.nodal_entities import _130

        return self.__parent__._cast(_130.BarRigidMBD)

    @property
    def concentric_connection_nodal_component(
        self: "CastSelf",
    ) -> "_135.ConcentricConnectionNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _135

        return self.__parent__._cast(_135.ConcentricConnectionNodalComponent)

    @property
    def gear_mesh_point_on_flank_contact(
        self: "CastSelf",
    ) -> "_140.GearMeshPointOnFlankContact":
        from mastapy._private.nodal_analysis.nodal_entities import _140

        return self.__parent__._cast(_140.GearMeshPointOnFlankContact)

    @property
    def simple_bar(self: "CastSelf") -> "_150.SimpleBar":
        from mastapy._private.nodal_analysis.nodal_entities import _150

        return self.__parent__._cast(_150.SimpleBar)

    @property
    def torsional_friction_node_pair(
        self: "CastSelf",
    ) -> "_153.TorsionalFrictionNodePair":
        from mastapy._private.nodal_analysis.nodal_entities import _153

        return self.__parent__._cast(_153.TorsionalFrictionNodePair)

    @property
    def torsional_friction_node_pair_simple_locked_stiffness(
        self: "CastSelf",
    ) -> "_154.TorsionalFrictionNodePairSimpleLockedStiffness":
        from mastapy._private.nodal_analysis.nodal_entities import _154

        return self.__parent__._cast(
            _154.TorsionalFrictionNodePairSimpleLockedStiffness
        )

    @property
    def two_body_connection_nodal_component(
        self: "CastSelf",
    ) -> "_155.TwoBodyConnectionNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _155

        return self.__parent__._cast(_155.TwoBodyConnectionNodalComponent)

    @property
    def component_nodal_composite(self: "CastSelf") -> "ComponentNodalComposite":
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
class ComponentNodalComposite(_145.NodalComposite):
    """ComponentNodalComposite

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT_NODAL_COMPOSITE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ComponentNodalComposite":
        """Cast to another type.

        Returns:
            _Cast_ComponentNodalComposite
        """
        return _Cast_ComponentNodalComposite(self)
