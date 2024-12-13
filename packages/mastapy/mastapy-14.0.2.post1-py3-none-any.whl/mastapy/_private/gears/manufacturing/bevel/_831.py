"""PinionFinishMachineSettings"""

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
from mastapy._private.gears import _332

_PINION_FINISH_MACHINE_SETTINGS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "PinionFinishMachineSettings"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.conical import _1211
    from mastapy._private.gears.manufacturing.bevel import (
        _826,
        _827,
        _829,
        _832,
        _833,
        _834,
    )

    Self = TypeVar("Self", bound="PinionFinishMachineSettings")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PinionFinishMachineSettings._Cast_PinionFinishMachineSettings",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PinionFinishMachineSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PinionFinishMachineSettings:
    """Special nested class for casting PinionFinishMachineSettings to subclasses."""

    __parent__: "PinionFinishMachineSettings"

    @property
    def conical_gear_tooth_surface(self: "CastSelf") -> "_332.ConicalGearToothSurface":
        return self.__parent__._cast(_332.ConicalGearToothSurface)

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
    def pinion_finish_machine_settings(
        self: "CastSelf",
    ) -> "PinionFinishMachineSettings":
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
class PinionFinishMachineSettings(_332.ConicalGearToothSurface):
    """PinionFinishMachineSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PINION_FINISH_MACHINE_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def blade_edge_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BladeEdgeRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    def cc_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CCAngle")

        if temp is None:
            return 0.0

        return temp

    @cc_angle.setter
    @enforce_parameter_types
    def cc_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CCAngle", float(value) if value is not None else 0.0
        )

    @property
    def cutter_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CutterRadius")

        if temp is None:
            return 0.0

        return temp

    @cutter_radius.setter
    @enforce_parameter_types
    def cutter_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CutterRadius", float(value) if value is not None else 0.0
        )

    @property
    def ease_off_at_heel_root(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EaseOffAtHeelRoot")

        if temp is None:
            return 0.0

        return temp

    @property
    def ease_off_at_heel_tip(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EaseOffAtHeelTip")

        if temp is None:
            return 0.0

        return temp

    @property
    def ease_off_at_toe_root(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EaseOffAtToeRoot")

        if temp is None:
            return 0.0

        return temp

    @property
    def ease_off_at_toe_tip(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EaseOffAtToeTip")

        if temp is None:
            return 0.0

        return temp

    @property
    def pinion_cutter_blade_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PinionCutterBladeAngle")

        if temp is None:
            return 0.0

        return temp

    @pinion_cutter_blade_angle.setter
    @enforce_parameter_types
    def pinion_cutter_blade_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PinionCutterBladeAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    def toprem_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TopremAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def toprem_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TopremLength")

        if temp is None:
            return 0.0

        return temp

    @property
    def toprem_letter(self: "Self") -> "_1211.TopremLetter":
        """mastapy.gears.gear_designs.conical.TopremLetter

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TopremLetter")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Conical.TopremLetter"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.conical._1211", "TopremLetter"
        )(value)

    @property
    def cast_to(self: "Self") -> "_Cast_PinionFinishMachineSettings":
        """Cast to another type.

        Returns:
            _Cast_PinionFinishMachineSettings
        """
        return _Cast_PinionFinishMachineSettings(self)
