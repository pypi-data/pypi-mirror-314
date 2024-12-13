"""NodalComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _146

_NODAL_COMPONENT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "NodalComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import (
        _126,
        _127,
        _132,
        _133,
        _136,
        _137,
        _139,
        _142,
        _143,
        _148,
        _149,
        _152,
    )
    from mastapy._private.nodal_analysis.nodal_entities.external_force import (
        _156,
        _157,
        _158,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2894,
    )

    Self = TypeVar("Self", bound="NodalComponent")
    CastSelf = TypeVar("CastSelf", bound="NodalComponent._Cast_NodalComponent")


__docformat__ = "restructuredtext en"
__all__ = ("NodalComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NodalComponent:
    """Special nested class for casting NodalComponent to subclasses."""

    __parent__: "NodalComponent"

    @property
    def nodal_entity(self: "CastSelf") -> "_146.NodalEntity":
        return self.__parent__._cast(_146.NodalEntity)

    @property
    def arbitrary_nodal_component(self: "CastSelf") -> "_126.ArbitraryNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _126

        return self.__parent__._cast(_126.ArbitraryNodalComponent)

    @property
    def bar(self: "CastSelf") -> "_127.Bar":
        from mastapy._private.nodal_analysis.nodal_entities import _127

        return self.__parent__._cast(_127.Bar)

    @property
    def bearing_axial_mounting_clearance(
        self: "CastSelf",
    ) -> "_132.BearingAxialMountingClearance":
        from mastapy._private.nodal_analysis.nodal_entities import _132

        return self.__parent__._cast(_132.BearingAxialMountingClearance)

    @property
    def cms_nodal_component(self: "CastSelf") -> "_133.CMSNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _133

        return self.__parent__._cast(_133.CMSNodalComponent)

    @property
    def distributed_rigid_bar_coupling(
        self: "CastSelf",
    ) -> "_136.DistributedRigidBarCoupling":
        from mastapy._private.nodal_analysis.nodal_entities import _136

        return self.__parent__._cast(_136.DistributedRigidBarCoupling)

    @property
    def friction_nodal_component(self: "CastSelf") -> "_137.FrictionNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _137

        return self.__parent__._cast(_137.FrictionNodalComponent)

    @property
    def gear_mesh_node_pair(self: "CastSelf") -> "_139.GearMeshNodePair":
        from mastapy._private.nodal_analysis.nodal_entities import _139

        return self.__parent__._cast(_139.GearMeshNodePair)

    @property
    def inertial_force_component(self: "CastSelf") -> "_142.InertialForceComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _142

        return self.__parent__._cast(_142.InertialForceComponent)

    @property
    def line_contact_stiffness_entity(
        self: "CastSelf",
    ) -> "_143.LineContactStiffnessEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _143

        return self.__parent__._cast(_143.LineContactStiffnessEntity)

    @property
    def pid_control_nodal_component(
        self: "CastSelf",
    ) -> "_148.PIDControlNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _148

        return self.__parent__._cast(_148.PIDControlNodalComponent)

    @property
    def rigid_bar(self: "CastSelf") -> "_149.RigidBar":
        from mastapy._private.nodal_analysis.nodal_entities import _149

        return self.__parent__._cast(_149.RigidBar)

    @property
    def surface_to_surface_contact_stiffness_entity(
        self: "CastSelf",
    ) -> "_152.SurfaceToSurfaceContactStiffnessEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _152

        return self.__parent__._cast(_152.SurfaceToSurfaceContactStiffnessEntity)

    @property
    def external_force_entity(self: "CastSelf") -> "_156.ExternalForceEntity":
        from mastapy._private.nodal_analysis.nodal_entities.external_force import _156

        return self.__parent__._cast(_156.ExternalForceEntity)

    @property
    def external_force_line_contact_entity(
        self: "CastSelf",
    ) -> "_157.ExternalForceLineContactEntity":
        from mastapy._private.nodal_analysis.nodal_entities.external_force import _157

        return self.__parent__._cast(_157.ExternalForceLineContactEntity)

    @property
    def external_force_single_point_entity(
        self: "CastSelf",
    ) -> "_158.ExternalForceSinglePointEntity":
        from mastapy._private.nodal_analysis.nodal_entities.external_force import _158

        return self.__parent__._cast(_158.ExternalForceSinglePointEntity)

    @property
    def shaft_section_system_deflection(
        self: "CastSelf",
    ) -> "_2894.ShaftSectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2894,
        )

        return self.__parent__._cast(_2894.ShaftSectionSystemDeflection)

    @property
    def nodal_component(self: "CastSelf") -> "NodalComponent":
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
class NodalComponent(_146.NodalEntity):
    """NodalComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NODAL_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_NodalComponent":
        """Cast to another type.

        Returns:
            _Cast_NodalComponent
        """
        return _Cast_NodalComponent(self)
