"""PinionBevelGeneratingTiltMachineSettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.bevel import _831

_PINION_BEVEL_GENERATING_TILT_MACHINE_SETTINGS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "PinionBevelGeneratingTiltMachineSettings"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears import _332

    Self = TypeVar("Self", bound="PinionBevelGeneratingTiltMachineSettings")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PinionBevelGeneratingTiltMachineSettings._Cast_PinionBevelGeneratingTiltMachineSettings",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PinionBevelGeneratingTiltMachineSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PinionBevelGeneratingTiltMachineSettings:
    """Special nested class for casting PinionBevelGeneratingTiltMachineSettings to subclasses."""

    __parent__: "PinionBevelGeneratingTiltMachineSettings"

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
    def pinion_bevel_generating_tilt_machine_settings(
        self: "CastSelf",
    ) -> "PinionBevelGeneratingTiltMachineSettings":
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
class PinionBevelGeneratingTiltMachineSettings(_831.PinionFinishMachineSettings):
    """PinionBevelGeneratingTiltMachineSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PINION_BEVEL_GENERATING_TILT_MACHINE_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_PinionBevelGeneratingTiltMachineSettings":
        """Cast to another type.

        Returns:
            _Cast_PinionBevelGeneratingTiltMachineSettings
        """
        return _Cast_PinionBevelGeneratingTiltMachineSettings(self)
