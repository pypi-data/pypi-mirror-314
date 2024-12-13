"""BevelDifferentialGearMesh"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.connections_and_sockets.gears import _2360

_BEVEL_DIFFERENTIAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "BevelDifferentialGearMesh"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.bevel import _1221
    from mastapy._private.system_model import _2260
    from mastapy._private.system_model.connections_and_sockets import _2329, _2338
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2356,
        _2364,
        _2370,
    )

    Self = TypeVar("Self", bound="BevelDifferentialGearMesh")
    CastSelf = TypeVar(
        "CastSelf", bound="BevelDifferentialGearMesh._Cast_BevelDifferentialGearMesh"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelDifferentialGearMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelDifferentialGearMesh:
    """Special nested class for casting BevelDifferentialGearMesh to subclasses."""

    __parent__: "BevelDifferentialGearMesh"

    @property
    def bevel_gear_mesh(self: "CastSelf") -> "_2360.BevelGearMesh":
        return self.__parent__._cast(_2360.BevelGearMesh)

    @property
    def agma_gleason_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2356.AGMAGleasonConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2356

        return self.__parent__._cast(_2356.AGMAGleasonConicalGearMesh)

    @property
    def conical_gear_mesh(self: "CastSelf") -> "_2364.ConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2364

        return self.__parent__._cast(_2364.ConicalGearMesh)

    @property
    def gear_mesh(self: "CastSelf") -> "_2370.GearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2370

        return self.__parent__._cast(_2370.GearMesh)

    @property
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2338.InterMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2338

        return self.__parent__._cast(_2338.InterMountableComponentConnection)

    @property
    def connection(self: "CastSelf") -> "_2329.Connection":
        from mastapy._private.system_model.connections_and_sockets import _2329

        return self.__parent__._cast(_2329.Connection)

    @property
    def design_entity(self: "CastSelf") -> "_2260.DesignEntity":
        from mastapy._private.system_model import _2260

        return self.__parent__._cast(_2260.DesignEntity)

    @property
    def bevel_differential_gear_mesh(self: "CastSelf") -> "BevelDifferentialGearMesh":
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
class BevelDifferentialGearMesh(_2360.BevelGearMesh):
    """BevelDifferentialGearMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_DIFFERENTIAL_GEAR_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def bevel_gear_mesh_design(self: "Self") -> "_1221.BevelGearMeshDesign":
        """mastapy.gears.gear_designs.bevel.BevelGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearMeshDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_BevelDifferentialGearMesh":
        """Cast to another type.

        Returns:
            _Cast_BevelDifferentialGearMesh
        """
        return _Cast_BevelDifferentialGearMesh(self)
