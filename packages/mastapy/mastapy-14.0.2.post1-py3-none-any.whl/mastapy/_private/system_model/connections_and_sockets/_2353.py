"""Socket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_COMPONENT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Component")
_SOCKET = python_net_import("SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "Socket")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2323,
        _2324,
        _2329,
        _2331,
        _2333,
        _2335,
        _2336,
        _2337,
        _2339,
        _2340,
        _2341,
        _2342,
        _2343,
        _2345,
        _2346,
        _2347,
        _2350,
        _2351,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import (
        _2400,
        _2402,
        _2404,
        _2406,
        _2408,
        _2410,
        _2411,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2390,
        _2391,
        _2393,
        _2394,
        _2396,
        _2397,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2357,
        _2359,
        _2361,
        _2363,
        _2365,
        _2367,
        _2369,
        _2371,
        _2373,
        _2374,
        _2378,
        _2379,
        _2381,
        _2383,
        _2385,
        _2387,
        _2389,
    )
    from mastapy._private.system_model.part_model import _2502, _2503

    Self = TypeVar("Self", bound="Socket")
    CastSelf = TypeVar("CastSelf", bound="Socket._Cast_Socket")


__docformat__ = "restructuredtext en"
__all__ = ("Socket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Socket:
    """Special nested class for casting Socket to subclasses."""

    __parent__: "Socket"

    @property
    def bearing_inner_socket(self: "CastSelf") -> "_2323.BearingInnerSocket":
        from mastapy._private.system_model.connections_and_sockets import _2323

        return self.__parent__._cast(_2323.BearingInnerSocket)

    @property
    def bearing_outer_socket(self: "CastSelf") -> "_2324.BearingOuterSocket":
        from mastapy._private.system_model.connections_and_sockets import _2324

        return self.__parent__._cast(_2324.BearingOuterSocket)

    @property
    def cvt_pulley_socket(self: "CastSelf") -> "_2331.CVTPulleySocket":
        from mastapy._private.system_model.connections_and_sockets import _2331

        return self.__parent__._cast(_2331.CVTPulleySocket)

    @property
    def cylindrical_socket(self: "CastSelf") -> "_2333.CylindricalSocket":
        from mastapy._private.system_model.connections_and_sockets import _2333

        return self.__parent__._cast(_2333.CylindricalSocket)

    @property
    def electric_machine_stator_socket(
        self: "CastSelf",
    ) -> "_2335.ElectricMachineStatorSocket":
        from mastapy._private.system_model.connections_and_sockets import _2335

        return self.__parent__._cast(_2335.ElectricMachineStatorSocket)

    @property
    def inner_shaft_socket(self: "CastSelf") -> "_2336.InnerShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2336

        return self.__parent__._cast(_2336.InnerShaftSocket)

    @property
    def inner_shaft_socket_base(self: "CastSelf") -> "_2337.InnerShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2337

        return self.__parent__._cast(_2337.InnerShaftSocketBase)

    @property
    def mountable_component_inner_socket(
        self: "CastSelf",
    ) -> "_2339.MountableComponentInnerSocket":
        from mastapy._private.system_model.connections_and_sockets import _2339

        return self.__parent__._cast(_2339.MountableComponentInnerSocket)

    @property
    def mountable_component_outer_socket(
        self: "CastSelf",
    ) -> "_2340.MountableComponentOuterSocket":
        from mastapy._private.system_model.connections_and_sockets import _2340

        return self.__parent__._cast(_2340.MountableComponentOuterSocket)

    @property
    def mountable_component_socket(
        self: "CastSelf",
    ) -> "_2341.MountableComponentSocket":
        from mastapy._private.system_model.connections_and_sockets import _2341

        return self.__parent__._cast(_2341.MountableComponentSocket)

    @property
    def outer_shaft_socket(self: "CastSelf") -> "_2342.OuterShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2342

        return self.__parent__._cast(_2342.OuterShaftSocket)

    @property
    def outer_shaft_socket_base(self: "CastSelf") -> "_2343.OuterShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2343

        return self.__parent__._cast(_2343.OuterShaftSocketBase)

    @property
    def planetary_socket(self: "CastSelf") -> "_2345.PlanetarySocket":
        from mastapy._private.system_model.connections_and_sockets import _2345

        return self.__parent__._cast(_2345.PlanetarySocket)

    @property
    def planetary_socket_base(self: "CastSelf") -> "_2346.PlanetarySocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2346

        return self.__parent__._cast(_2346.PlanetarySocketBase)

    @property
    def pulley_socket(self: "CastSelf") -> "_2347.PulleySocket":
        from mastapy._private.system_model.connections_and_sockets import _2347

        return self.__parent__._cast(_2347.PulleySocket)

    @property
    def rolling_ring_socket(self: "CastSelf") -> "_2350.RollingRingSocket":
        from mastapy._private.system_model.connections_and_sockets import _2350

        return self.__parent__._cast(_2350.RollingRingSocket)

    @property
    def shaft_socket(self: "CastSelf") -> "_2351.ShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2351

        return self.__parent__._cast(_2351.ShaftSocket)

    @property
    def agma_gleason_conical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2357.AGMAGleasonConicalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2357

        return self.__parent__._cast(_2357.AGMAGleasonConicalGearTeethSocket)

    @property
    def bevel_differential_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2359.BevelDifferentialGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2359

        return self.__parent__._cast(_2359.BevelDifferentialGearTeethSocket)

    @property
    def bevel_gear_teeth_socket(self: "CastSelf") -> "_2361.BevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2361

        return self.__parent__._cast(_2361.BevelGearTeethSocket)

    @property
    def concept_gear_teeth_socket(self: "CastSelf") -> "_2363.ConceptGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2363

        return self.__parent__._cast(_2363.ConceptGearTeethSocket)

    @property
    def conical_gear_teeth_socket(self: "CastSelf") -> "_2365.ConicalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2365

        return self.__parent__._cast(_2365.ConicalGearTeethSocket)

    @property
    def cylindrical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2367.CylindricalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2367

        return self.__parent__._cast(_2367.CylindricalGearTeethSocket)

    @property
    def face_gear_teeth_socket(self: "CastSelf") -> "_2369.FaceGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2369

        return self.__parent__._cast(_2369.FaceGearTeethSocket)

    @property
    def gear_teeth_socket(self: "CastSelf") -> "_2371.GearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2371

        return self.__parent__._cast(_2371.GearTeethSocket)

    @property
    def hypoid_gear_teeth_socket(self: "CastSelf") -> "_2373.HypoidGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2373

        return self.__parent__._cast(_2373.HypoidGearTeethSocket)

    @property
    def klingelnberg_conical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2374.KlingelnbergConicalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2374

        return self.__parent__._cast(_2374.KlingelnbergConicalGearTeethSocket)

    @property
    def klingelnberg_hypoid_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2378.KlingelnbergHypoidGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2378

        return self.__parent__._cast(_2378.KlingelnbergHypoidGearTeethSocket)

    @property
    def klingelnberg_spiral_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2379.KlingelnbergSpiralBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2379

        return self.__parent__._cast(_2379.KlingelnbergSpiralBevelGearTeethSocket)

    @property
    def spiral_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2381.SpiralBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2381

        return self.__parent__._cast(_2381.SpiralBevelGearTeethSocket)

    @property
    def straight_bevel_diff_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2383.StraightBevelDiffGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2383

        return self.__parent__._cast(_2383.StraightBevelDiffGearTeethSocket)

    @property
    def straight_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2385.StraightBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2385

        return self.__parent__._cast(_2385.StraightBevelGearTeethSocket)

    @property
    def worm_gear_teeth_socket(self: "CastSelf") -> "_2387.WormGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2387

        return self.__parent__._cast(_2387.WormGearTeethSocket)

    @property
    def zerol_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2389.ZerolBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2389

        return self.__parent__._cast(_2389.ZerolBevelGearTeethSocket)

    @property
    def cycloidal_disc_axial_left_socket(
        self: "CastSelf",
    ) -> "_2390.CycloidalDiscAxialLeftSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2390,
        )

        return self.__parent__._cast(_2390.CycloidalDiscAxialLeftSocket)

    @property
    def cycloidal_disc_axial_right_socket(
        self: "CastSelf",
    ) -> "_2391.CycloidalDiscAxialRightSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2391,
        )

        return self.__parent__._cast(_2391.CycloidalDiscAxialRightSocket)

    @property
    def cycloidal_disc_inner_socket(
        self: "CastSelf",
    ) -> "_2393.CycloidalDiscInnerSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2393,
        )

        return self.__parent__._cast(_2393.CycloidalDiscInnerSocket)

    @property
    def cycloidal_disc_outer_socket(
        self: "CastSelf",
    ) -> "_2394.CycloidalDiscOuterSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2394,
        )

        return self.__parent__._cast(_2394.CycloidalDiscOuterSocket)

    @property
    def cycloidal_disc_planetary_bearing_socket(
        self: "CastSelf",
    ) -> "_2396.CycloidalDiscPlanetaryBearingSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2396,
        )

        return self.__parent__._cast(_2396.CycloidalDiscPlanetaryBearingSocket)

    @property
    def ring_pins_socket(self: "CastSelf") -> "_2397.RingPinsSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2397,
        )

        return self.__parent__._cast(_2397.RingPinsSocket)

    @property
    def clutch_socket(self: "CastSelf") -> "_2400.ClutchSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2400,
        )

        return self.__parent__._cast(_2400.ClutchSocket)

    @property
    def concept_coupling_socket(self: "CastSelf") -> "_2402.ConceptCouplingSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2402,
        )

        return self.__parent__._cast(_2402.ConceptCouplingSocket)

    @property
    def coupling_socket(self: "CastSelf") -> "_2404.CouplingSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2404,
        )

        return self.__parent__._cast(_2404.CouplingSocket)

    @property
    def part_to_part_shear_coupling_socket(
        self: "CastSelf",
    ) -> "_2406.PartToPartShearCouplingSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2406,
        )

        return self.__parent__._cast(_2406.PartToPartShearCouplingSocket)

    @property
    def spring_damper_socket(self: "CastSelf") -> "_2408.SpringDamperSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2408,
        )

        return self.__parent__._cast(_2408.SpringDamperSocket)

    @property
    def torque_converter_pump_socket(
        self: "CastSelf",
    ) -> "_2410.TorqueConverterPumpSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2410,
        )

        return self.__parent__._cast(_2410.TorqueConverterPumpSocket)

    @property
    def torque_converter_turbine_socket(
        self: "CastSelf",
    ) -> "_2411.TorqueConverterTurbineSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2411,
        )

        return self.__parent__._cast(_2411.TorqueConverterTurbineSocket)

    @property
    def socket(self: "CastSelf") -> "Socket":
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
class Socket(_0.APIBase):
    """Socket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def connected_components(self: "Self") -> "List[_2502.Component]":
        """List[mastapy.system_model.part_model.Component]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectedComponents")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connections(self: "Self") -> "List[_2329.Connection]":
        """List[mastapy.system_model.connections_and_sockets.Connection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Connections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def owner(self: "Self") -> "_2502.Component":
        """mastapy.system_model.part_model.Component

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Owner")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @enforce_parameter_types
    def connect_to(
        self: "Self", component: "_2502.Component"
    ) -> "_2503.ComponentsConnectedResult":
        """mastapy.system_model.part_model.ComponentsConnectedResult

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ConnectTo",
            [_COMPONENT],
            component.wrapped if component else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def connect_to_socket(
        self: "Self", socket: "Socket"
    ) -> "_2503.ComponentsConnectedResult":
        """mastapy.system_model.part_model.ComponentsConnectedResult

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped, "ConnectTo", [_SOCKET], socket.wrapped if socket else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def connection_to(self: "Self", socket: "Socket") -> "_2329.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "ConnectionTo", socket.wrapped if socket else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def get_possible_sockets_to_connect_to(
        self: "Self", component_to_connect_to: "_2502.Component"
    ) -> "List[Socket]":
        """List[mastapy.system_model.connections_and_sockets.Socket]

        Args:
            component_to_connect_to (mastapy.system_model.part_model.Component)
        """
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(
                self.wrapped,
                "GetPossibleSocketsToConnectTo",
                component_to_connect_to.wrapped if component_to_connect_to else None,
            )
        )

    @property
    def cast_to(self: "Self") -> "_Cast_Socket":
        """Cast to another type.

        Returns:
            _Cast_Socket
        """
        return _Cast_Socket(self)
