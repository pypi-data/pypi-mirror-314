"""ConicalGearMesh"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.connections_and_sockets.gears import _2370

_CONICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "ConicalGearMesh"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2260
    from mastapy._private.system_model.connections_and_sockets import _2329, _2338
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2356,
        _2358,
        _2360,
        _2372,
        _2375,
        _2376,
        _2377,
        _2380,
        _2382,
        _2384,
        _2388,
    )

    Self = TypeVar("Self", bound="ConicalGearMesh")
    CastSelf = TypeVar("CastSelf", bound="ConicalGearMesh._Cast_ConicalGearMesh")


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearMesh:
    """Special nested class for casting ConicalGearMesh to subclasses."""

    __parent__: "ConicalGearMesh"

    @property
    def gear_mesh(self: "CastSelf") -> "_2370.GearMesh":
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
    def agma_gleason_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2356.AGMAGleasonConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2356

        return self.__parent__._cast(_2356.AGMAGleasonConicalGearMesh)

    @property
    def bevel_differential_gear_mesh(
        self: "CastSelf",
    ) -> "_2358.BevelDifferentialGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2358

        return self.__parent__._cast(_2358.BevelDifferentialGearMesh)

    @property
    def bevel_gear_mesh(self: "CastSelf") -> "_2360.BevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2360

        return self.__parent__._cast(_2360.BevelGearMesh)

    @property
    def hypoid_gear_mesh(self: "CastSelf") -> "_2372.HypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2372

        return self.__parent__._cast(_2372.HypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2375.KlingelnbergCycloPalloidConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2375

        return self.__parent__._cast(_2375.KlingelnbergCycloPalloidConicalGearMesh)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh(
        self: "CastSelf",
    ) -> "_2376.KlingelnbergCycloPalloidHypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2376

        return self.__parent__._cast(_2376.KlingelnbergCycloPalloidHypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(
        self: "CastSelf",
    ) -> "_2377.KlingelnbergCycloPalloidSpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2377

        return self.__parent__._cast(_2377.KlingelnbergCycloPalloidSpiralBevelGearMesh)

    @property
    def spiral_bevel_gear_mesh(self: "CastSelf") -> "_2380.SpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2380

        return self.__parent__._cast(_2380.SpiralBevelGearMesh)

    @property
    def straight_bevel_diff_gear_mesh(
        self: "CastSelf",
    ) -> "_2382.StraightBevelDiffGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2382

        return self.__parent__._cast(_2382.StraightBevelDiffGearMesh)

    @property
    def straight_bevel_gear_mesh(self: "CastSelf") -> "_2384.StraightBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2384

        return self.__parent__._cast(_2384.StraightBevelGearMesh)

    @property
    def zerol_bevel_gear_mesh(self: "CastSelf") -> "_2388.ZerolBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2388

        return self.__parent__._cast(_2388.ZerolBevelGearMesh)

    @property
    def conical_gear_mesh(self: "CastSelf") -> "ConicalGearMesh":
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
class ConicalGearMesh(_2370.GearMesh):
    """ConicalGearMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def crowning(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Crowning")

        if temp is None:
            return 0.0

        return temp

    @crowning.setter
    @enforce_parameter_types
    def crowning(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Crowning", float(value) if value is not None else 0.0
        )

    @property
    def pinion_drop_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PinionDropAngle")

        if temp is None:
            return 0.0

        return temp

    @pinion_drop_angle.setter
    @enforce_parameter_types
    def pinion_drop_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PinionDropAngle", float(value) if value is not None else 0.0
        )

    @property
    def wheel_drop_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WheelDropAngle")

        if temp is None:
            return 0.0

        return temp

    @wheel_drop_angle.setter
    @enforce_parameter_types
    def wheel_drop_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "WheelDropAngle", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearMesh":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearMesh
        """
        return _Cast_ConicalGearMesh(self)
