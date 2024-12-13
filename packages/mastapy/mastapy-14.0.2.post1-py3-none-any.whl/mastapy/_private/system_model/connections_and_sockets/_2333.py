"""CylindricalSocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2353

_CYLINDRICAL_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "CylindricalSocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2323,
        _2324,
        _2331,
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
    from mastapy._private.system_model.connections_and_sockets.gears import _2367

    Self = TypeVar("Self", bound="CylindricalSocket")
    CastSelf = TypeVar("CastSelf", bound="CylindricalSocket._Cast_CylindricalSocket")


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalSocket:
    """Special nested class for casting CylindricalSocket to subclasses."""

    __parent__: "CylindricalSocket"

    @property
    def socket(self: "CastSelf") -> "_2353.Socket":
        return self.__parent__._cast(_2353.Socket)

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
    def cylindrical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2367.CylindricalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2367

        return self.__parent__._cast(_2367.CylindricalGearTeethSocket)

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
    def cylindrical_socket(self: "CastSelf") -> "CylindricalSocket":
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
class CylindricalSocket(_2353.Socket):
    """CylindricalSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalSocket":
        """Cast to another type.

        Returns:
            _Cast_CylindricalSocket
        """
        return _Cast_CylindricalSocket(self)
