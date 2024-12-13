"""SKFSettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility import _1645

_SKF_SETTINGS = python_net_import("SMT.MastaAPI.Bearings", "SKFSettings")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling.skf_module import _2151
    from mastapy._private.utility import _1646

    Self = TypeVar("Self", bound="SKFSettings")
    CastSelf = TypeVar("CastSelf", bound="SKFSettings._Cast_SKFSettings")


__docformat__ = "restructuredtext en"
__all__ = ("SKFSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SKFSettings:
    """Special nested class for casting SKFSettings to subclasses."""

    __parent__: "SKFSettings"

    @property
    def per_machine_settings(self: "CastSelf") -> "_1645.PerMachineSettings":
        return self.__parent__._cast(_1645.PerMachineSettings)

    @property
    def persistent_singleton(self: "CastSelf") -> "_1646.PersistentSingleton":
        from mastapy._private.utility import _1646

        return self.__parent__._cast(_1646.PersistentSingleton)

    @property
    def skf_settings(self: "CastSelf") -> "SKFSettings":
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
class SKFSettings(_1645.PerMachineSettings):
    """SKFSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SKF_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def enable_skf_module(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "EnableSKFModule")

        if temp is None:
            return False

        return temp

    @enable_skf_module.setter
    @enforce_parameter_types
    def enable_skf_module(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "EnableSKFModule", bool(value) if value is not None else False
        )

    @property
    def log_file_path(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LogFilePath")

        if temp is None:
            return ""

        return temp

    @property
    def log_http_requests(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "LogHTTPRequests")

        if temp is None:
            return False

        return temp

    @log_http_requests.setter
    @enforce_parameter_types
    def log_http_requests(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "LogHTTPRequests", bool(value) if value is not None else False
        )

    @property
    def skf_authentication(self: "Self") -> "_2151.SKFAuthentication":
        """mastapy.bearings.bearing_results.rolling.skf_module.SKFAuthentication

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SKFAuthentication")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SKFSettings":
        """Cast to another type.

        Returns:
            _Cast_SKFSettings
        """
        return _Cast_SKFSettings(self)
