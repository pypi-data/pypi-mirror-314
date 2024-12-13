"""PermanentMagnetAssistedSynchronousReluctanceMachine"""

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

_PERMANENT_MAGNET_ASSISTED_SYNCHRONOUS_RELUCTANCE_MACHINE = python_net_import(
    "SMT.MastaAPI.ElectricMachines",
    "PermanentMagnetAssistedSynchronousReluctanceMachine",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines import _1304, _1321

    Self = TypeVar("Self", bound="PermanentMagnetAssistedSynchronousReluctanceMachine")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PermanentMagnetAssistedSynchronousReluctanceMachine._Cast_PermanentMagnetAssistedSynchronousReluctanceMachine",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PermanentMagnetAssistedSynchronousReluctanceMachine",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PermanentMagnetAssistedSynchronousReluctanceMachine:
    """Special nested class for casting PermanentMagnetAssistedSynchronousReluctanceMachine to subclasses."""

    __parent__: "PermanentMagnetAssistedSynchronousReluctanceMachine"

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
    def permanent_magnet_assisted_synchronous_reluctance_machine(
        self: "CastSelf",
    ) -> "PermanentMagnetAssistedSynchronousReluctanceMachine":
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
class PermanentMagnetAssistedSynchronousReluctanceMachine(
    _1333.NonCADElectricMachineDetail
):
    """PermanentMagnetAssistedSynchronousReluctanceMachine

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PERMANENT_MAGNET_ASSISTED_SYNCHRONOUS_RELUCTANCE_MACHINE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def rotor(
        self: "Self",
    ) -> "_1321.InteriorPermanentMagnetAndSynchronousReluctanceRotor":
        """mastapy.electric_machines.InteriorPermanentMagnetAndSynchronousReluctanceRotor

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rotor")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_PermanentMagnetAssistedSynchronousReluctanceMachine":
        """Cast to another type.

        Returns:
            _Cast_PermanentMagnetAssistedSynchronousReluctanceMachine
        """
        return _Cast_PermanentMagnetAssistedSynchronousReluctanceMachine(self)
