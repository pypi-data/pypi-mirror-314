"""LicenceServer"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion
from mastapy._private._internal.class_property import classproperty
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ARRAY = python_net_import("System", "Array")
_LICENCE_SERVER = python_net_import("SMT.MastaAPI.Licensing", "LicenceServer")

if TYPE_CHECKING:
    from typing import Any, Iterable, List, NoReturn, Type

    from mastapy._private.licensing import _7746, _7747, _7748


__docformat__ = "restructuredtext en"
__all__ = ("LicenceServer",)


class LicenceServer:
    """LicenceServer

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LICENCE_SERVER

    def __new__(
        cls: "Type[LicenceServer]", *args: "Any", **kwargs: "Any"
    ) -> "NoReturn":
        """Override of the new magic method.

        Note:
            This class cannot be instantiated and this method will always throw an
            exception.

        Args:
            cls (Type[LicenceServer]: The class to instantiate.
            *args (Any): Arguments.
            **kwargs (Any): Keyword arguments.

        Returns:
            NoReturn
        """
        raise TypeError("Class cannot be instantiated. Please use statically.")

    @classproperty
    def server_address(cls) -> "str":
        """str"""
        temp = pythonnet_property_get(LicenceServer.TYPE, "ServerAddress")

        if temp is None:
            return ""

        return temp

    @server_address.setter
    @enforce_parameter_types
    def server_address(cls, value: "str") -> None:
        pythonnet_property_set(
            LicenceServer.TYPE, "ServerAddress", str(value) if value is not None else ""
        )

    @classproperty
    def server_port(cls) -> "int":
        """int"""
        temp = pythonnet_property_get(LicenceServer.TYPE, "ServerPort")

        if temp is None:
            return 0

        return temp

    @server_port.setter
    @enforce_parameter_types
    def server_port(cls, value: "int") -> None:
        pythonnet_property_set(
            LicenceServer.TYPE, "ServerPort", int(value) if value is not None else 0
        )

    @classproperty
    def web_server_port(cls) -> "int":
        """int"""
        temp = pythonnet_property_get(LicenceServer.TYPE, "WebServerPort")

        if temp is None:
            return 0

        return temp

    @web_server_port.setter
    @enforce_parameter_types
    def web_server_port(cls, value: "int") -> None:
        pythonnet_property_set(
            LicenceServer.TYPE, "WebServerPort", int(value) if value is not None else 0
        )

    @staticmethod
    @enforce_parameter_types
    def update_server_settings(server_details: "_7746.LicenceServerDetails") -> None:
        """Method does not return.

        Args:
            server_details (mastapy.licensing.LicenceServerDetails)
        """
        pythonnet_method_call(
            LicenceServer.TYPE,
            "UpdateServerSettings",
            server_details.wrapped if server_details else None,
        )

    @staticmethod
    def get_server_settings() -> "_7746.LicenceServerDetails":
        """mastapy.licensing.LicenceServerDetails"""
        method_result = pythonnet_method_call(LicenceServer.TYPE, "GetServerSettings")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @staticmethod
    @enforce_parameter_types
    def request_module(module_code: "str") -> "bool":
        """bool

        Args:
            module_code (str)
        """
        module_code = str(module_code)
        method_result = pythonnet_method_call(
            LicenceServer.TYPE, "RequestModule", module_code if module_code else ""
        )
        return method_result

    @staticmethod
    @enforce_parameter_types
    def request_module_and_prerequisites(module_code: "str") -> "bool":
        """bool

        Args:
            module_code (str)
        """
        module_code = str(module_code)
        method_result = pythonnet_method_call(
            LicenceServer.TYPE,
            "RequestModuleAndPrerequisites",
            module_code if module_code else "",
        )
        return method_result

    @staticmethod
    @enforce_parameter_types
    def request_modules(module_codes: "List[str]") -> "bool":
        """bool

        Args:
            module_codes (List[str])
        """
        module_codes = conversion.to_list_any(module_codes)
        method_result = pythonnet_method_call(
            LicenceServer.TYPE, "RequestModules", module_codes
        )
        return method_result

    @staticmethod
    @enforce_parameter_types
    def get_module_prerequisites(module_code: "str") -> "Iterable[str]":
        """Iterable[str]

        Args:
            module_code (str)
        """
        module_code = str(module_code)
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call(
                LicenceServer.TYPE,
                "GetModulePrerequisites",
                module_code if module_code else "",
            ),
            str,
        )

    @staticmethod
    def get_requested_module_codes() -> "Iterable[str]":
        """Iterable[str]"""
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call(LicenceServer.TYPE, "GetRequestedModuleCodes"), str
        )

    @staticmethod
    @enforce_parameter_types
    def remove_module(module_code: "str") -> None:
        """Method does not return.

        Args:
            module_code (str)
        """
        module_code = str(module_code)
        pythonnet_method_call(
            LicenceServer.TYPE, "RemoveModule", module_code if module_code else ""
        )

    @staticmethod
    @enforce_parameter_types
    def remove_modules(module_codes: "List[str]") -> None:
        """Method does not return.

        Args:
            module_codes (List[str])
        """
        module_codes = conversion.to_list_any(module_codes)
        pythonnet_method_call(LicenceServer.TYPE, "RemoveModules", module_codes)

    @staticmethod
    def get_licensed_module_details() -> "Iterable[_7747.ModuleDetails]":
        """Iterable[mastapy.licensing.ModuleDetails]"""
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call(LicenceServer.TYPE, "GetLicensedModuleDetails")
        )

    @staticmethod
    def get_available_module_details() -> "Iterable[_7747.ModuleDetails]":
        """Iterable[mastapy.licensing.ModuleDetails]"""
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call(LicenceServer.TYPE, "GetAvailableModuleDetails")
        )

    @staticmethod
    def get_requested_module_statuses() -> "Iterable[_7748.ModuleLicenceStatus]":
        """Iterable[mastapy.licensing.ModuleLicenceStatus]"""
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call(LicenceServer.TYPE, "GetRequestedModuleStatuses")
        )
