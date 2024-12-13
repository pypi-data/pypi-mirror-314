"""PinionHypoidFormateTiltMachineSettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.bevel import _831

_PINION_HYPOID_FORMATE_TILT_MACHINE_SETTINGS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "PinionHypoidFormateTiltMachineSettings"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears import _332

    Self = TypeVar("Self", bound="PinionHypoidFormateTiltMachineSettings")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PinionHypoidFormateTiltMachineSettings._Cast_PinionHypoidFormateTiltMachineSettings",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PinionHypoidFormateTiltMachineSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PinionHypoidFormateTiltMachineSettings:
    """Special nested class for casting PinionHypoidFormateTiltMachineSettings to subclasses."""

    __parent__: "PinionHypoidFormateTiltMachineSettings"

    @property
    def pinion_finish_machine_settings(
        self: "CastSelf",
    ) -> "_831.PinionFinishMachineSettings":
        return self.__parent__._cast(_831.PinionFinishMachineSettings)

    @property
    def conical_gear_tooth_surface(self: "CastSelf") -> "_332.ConicalGearToothSurface":
        from mastapy._private.gears import _332

        return self.__parent__._cast(_332.ConicalGearToothSurface)

    @property
    def pinion_hypoid_formate_tilt_machine_settings(
        self: "CastSelf",
    ) -> "PinionHypoidFormateTiltMachineSettings":
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
class PinionHypoidFormateTiltMachineSettings(_831.PinionFinishMachineSettings):
    """PinionHypoidFormateTiltMachineSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PINION_HYPOID_FORMATE_TILT_MACHINE_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_PinionHypoidFormateTiltMachineSettings":
        """Cast to another type.

        Returns:
            _Cast_PinionHypoidFormateTiltMachineSettings
        """
        return _Cast_PinionHypoidFormateTiltMachineSettings(self)
