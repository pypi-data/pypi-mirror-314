"""SpringDamperConnection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.connections_and_sockets.couplings import _2403

_SPRING_DAMPER_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings", "SpringDamperConnection"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis import _72
    from mastapy._private.system_model import _2258, _2260
    from mastapy._private.system_model.connections_and_sockets import _2329, _2338

    Self = TypeVar("Self", bound="SpringDamperConnection")
    CastSelf = TypeVar(
        "CastSelf", bound="SpringDamperConnection._Cast_SpringDamperConnection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpringDamperConnection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpringDamperConnection:
    """Special nested class for casting SpringDamperConnection to subclasses."""

    __parent__: "SpringDamperConnection"

    @property
    def coupling_connection(self: "CastSelf") -> "_2403.CouplingConnection":
        return self.__parent__._cast(_2403.CouplingConnection)

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
    def spring_damper_connection(self: "CastSelf") -> "SpringDamperConnection":
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
class SpringDamperConnection(_2403.CouplingConnection):
    """SpringDamperConnection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPRING_DAMPER_CONNECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def damping_option(self: "Self") -> "_2258.ComponentDampingOption":
        """mastapy.system_model.ComponentDampingOption"""
        temp = pythonnet_property_get(self.wrapped, "DampingOption")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.SystemModel.ComponentDampingOption"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model._2258", "ComponentDampingOption"
        )(value)

    @damping_option.setter
    @enforce_parameter_types
    def damping_option(self: "Self", value: "_2258.ComponentDampingOption") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.SystemModel.ComponentDampingOption"
        )
        pythonnet_property_set(self.wrapped, "DampingOption", value)

    @property
    def damping(self: "Self") -> "_72.LinearDampingConnectionProperties":
        """mastapy.nodal_analysis.LinearDampingConnectionProperties

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Damping")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SpringDamperConnection":
        """Cast to another type.

        Returns:
            _Cast_SpringDamperConnection
        """
        return _Cast_SpringDamperConnection(self)
