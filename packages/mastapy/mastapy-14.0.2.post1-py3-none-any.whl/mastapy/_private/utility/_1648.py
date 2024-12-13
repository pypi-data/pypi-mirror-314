"""PushbulletSettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility import _1645

_PUSHBULLET_SETTINGS = python_net_import("SMT.MastaAPI.Utility", "PushbulletSettings")

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.utility import _1646

    Self = TypeVar("Self", bound="PushbulletSettings")
    CastSelf = TypeVar("CastSelf", bound="PushbulletSettings._Cast_PushbulletSettings")


__docformat__ = "restructuredtext en"
__all__ = ("PushbulletSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PushbulletSettings:
    """Special nested class for casting PushbulletSettings to subclasses."""

    __parent__: "PushbulletSettings"

    @property
    def per_machine_settings(self: "CastSelf") -> "_1645.PerMachineSettings":
        return self.__parent__._cast(_1645.PerMachineSettings)

    @property
    def persistent_singleton(self: "CastSelf") -> "_1646.PersistentSingleton":
        from mastapy._private.utility import _1646

        return self.__parent__._cast(_1646.PersistentSingleton)

    @property
    def pushbullet_settings(self: "CastSelf") -> "PushbulletSettings":
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
class PushbulletSettings(_1645.PerMachineSettings):
    """PushbulletSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PUSHBULLET_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def enable_pushbullet(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "EnablePushbullet")

        if temp is None:
            return False

        return temp

    @enable_pushbullet.setter
    @enforce_parameter_types
    def enable_pushbullet(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EnablePushbullet",
            bool(value) if value is not None else False,
        )

    @property
    def pushbullet_token(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "PushbulletToken")

        if temp is None:
            return ""

        return temp

    @pushbullet_token.setter
    @enforce_parameter_types
    def pushbullet_token(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "PushbulletToken", str(value) if value is not None else ""
        )

    @property
    def send_progress_screenshot_interval_minutes(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(
            self.wrapped, "SendProgressScreenshotIntervalMinutes"
        )

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @send_progress_screenshot_interval_minutes.setter
    @enforce_parameter_types
    def send_progress_screenshot_interval_minutes(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "SendProgressScreenshotIntervalMinutes", value
        )

    def generate_pushbullet_token(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "GeneratePushbulletToken")

    @property
    def cast_to(self: "Self") -> "_Cast_PushbulletSettings":
        """Cast to another type.

        Returns:
            _Cast_PushbulletSettings
        """
        return _Cast_PushbulletSettings(self)
