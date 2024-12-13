"""ConicalGearToothSurface"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import

_CONICAL_GEAR_TOOTH_SURFACE = python_net_import(
    "SMT.MastaAPI.Gears", "ConicalGearToothSurface"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears import _339
    from mastapy._private.gears.manufacturing.bevel import (
        _805,
        _826,
        _827,
        _829,
        _831,
        _832,
        _833,
        _834,
    )

    Self = TypeVar("Self", bound="ConicalGearToothSurface")
    CastSelf = TypeVar(
        "CastSelf", bound="ConicalGearToothSurface._Cast_ConicalGearToothSurface"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearToothSurface",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearToothSurface:
    """Special nested class for casting ConicalGearToothSurface to subclasses."""

    __parent__: "ConicalGearToothSurface"

    @property
    def gear_nurbs_surface(self: "CastSelf") -> "_339.GearNURBSSurface":
        from mastapy._private.gears import _339

        return self.__parent__._cast(_339.GearNURBSSurface)

    @property
    def conical_meshed_wheel_flank_manufacturing_config(
        self: "CastSelf",
    ) -> "_805.ConicalMeshedWheelFlankManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _805

        return self.__parent__._cast(_805.ConicalMeshedWheelFlankManufacturingConfig)

    @property
    def pinion_bevel_generating_modified_roll_machine_settings(
        self: "CastSelf",
    ) -> "_826.PinionBevelGeneratingModifiedRollMachineSettings":
        from mastapy._private.gears.manufacturing.bevel import _826

        return self.__parent__._cast(
            _826.PinionBevelGeneratingModifiedRollMachineSettings
        )

    @property
    def pinion_bevel_generating_tilt_machine_settings(
        self: "CastSelf",
    ) -> "_827.PinionBevelGeneratingTiltMachineSettings":
        from mastapy._private.gears.manufacturing.bevel import _827

        return self.__parent__._cast(_827.PinionBevelGeneratingTiltMachineSettings)

    @property
    def pinion_conical_machine_settings_specified(
        self: "CastSelf",
    ) -> "_829.PinionConicalMachineSettingsSpecified":
        from mastapy._private.gears.manufacturing.bevel import _829

        return self.__parent__._cast(_829.PinionConicalMachineSettingsSpecified)

    @property
    def pinion_finish_machine_settings(
        self: "CastSelf",
    ) -> "_831.PinionFinishMachineSettings":
        from mastapy._private.gears.manufacturing.bevel import _831

        return self.__parent__._cast(_831.PinionFinishMachineSettings)

    @property
    def pinion_hypoid_formate_tilt_machine_settings(
        self: "CastSelf",
    ) -> "_832.PinionHypoidFormateTiltMachineSettings":
        from mastapy._private.gears.manufacturing.bevel import _832

        return self.__parent__._cast(_832.PinionHypoidFormateTiltMachineSettings)

    @property
    def pinion_hypoid_generating_tilt_machine_settings(
        self: "CastSelf",
    ) -> "_833.PinionHypoidGeneratingTiltMachineSettings":
        from mastapy._private.gears.manufacturing.bevel import _833

        return self.__parent__._cast(_833.PinionHypoidGeneratingTiltMachineSettings)

    @property
    def pinion_machine_settings_smt(
        self: "CastSelf",
    ) -> "_834.PinionMachineSettingsSMT":
        from mastapy._private.gears.manufacturing.bevel import _834

        return self.__parent__._cast(_834.PinionMachineSettingsSMT)

    @property
    def conical_gear_tooth_surface(self: "CastSelf") -> "ConicalGearToothSurface":
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
class ConicalGearToothSurface(_0.APIBase):
    """ConicalGearToothSurface

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_TOOTH_SURFACE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearToothSurface":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearToothSurface
        """
        return _Cast_ConicalGearToothSurface(self)
