"""SurfacePermanentMagnetMachine"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.electric_machines import _1333

_SURFACE_PERMANENT_MAGNET_MACHINE = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "SurfacePermanentMagnetMachine"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines import _1304, _1351

    Self = TypeVar("Self", bound="SurfacePermanentMagnetMachine")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SurfacePermanentMagnetMachine._Cast_SurfacePermanentMagnetMachine",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SurfacePermanentMagnetMachine",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SurfacePermanentMagnetMachine:
    """Special nested class for casting SurfacePermanentMagnetMachine to subclasses."""

    __parent__: "SurfacePermanentMagnetMachine"

    @property
    def non_cad_electric_machine_detail(
        self: "CastSelf",
    ) -> "_1333.NonCADElectricMachineDetail":
        return self.__parent__._cast(_1333.NonCADElectricMachineDetail)

    @property
    def electric_machine_detail(self: "CastSelf") -> "_1304.ElectricMachineDetail":
        from mastapy._private.electric_machines import _1304

        return self.__parent__._cast(_1304.ElectricMachineDetail)

    @property
    def surface_permanent_magnet_machine(
        self: "CastSelf",
    ) -> "SurfacePermanentMagnetMachine":
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
class SurfacePermanentMagnetMachine(_1333.NonCADElectricMachineDetail):
    """SurfacePermanentMagnetMachine

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SURFACE_PERMANENT_MAGNET_MACHINE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def rotor(self: "Self") -> "_1351.SurfacePermanentMagnetRotor":
        """mastapy.electric_machines.SurfacePermanentMagnetRotor

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rotor")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SurfacePermanentMagnetMachine":
        """Cast to another type.

        Returns:
            _Cast_SurfacePermanentMagnetMachine
        """
        return _Cast_SurfacePermanentMagnetMachine(self)
