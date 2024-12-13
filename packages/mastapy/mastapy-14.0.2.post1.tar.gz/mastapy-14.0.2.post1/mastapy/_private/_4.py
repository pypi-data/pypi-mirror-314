"""UtilityMethods"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_UTILITY_METHODS = python_net_import("SMT.MastaAPI", "UtilityMethods")

if TYPE_CHECKING:
    from typing import Any, Callable, NoReturn, Type, TypeVar

    from mastapy._private import _0

    T_is_read_only = TypeVar("T_is_read_only", bound="_0.APIBase")
    T_is_valid = TypeVar("T_is_valid", bound="_0.APIBase")
    T_is_method_valid = TypeVar("T_is_method_valid", bound="_0.APIBase")
    T_is_method_read_only = TypeVar("T_is_method_read_only", bound="_0.APIBase")


__docformat__ = "restructuredtext en"
__all__ = ("UtilityMethods",)


class UtilityMethods:
    """UtilityMethods

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _UTILITY_METHODS

    def __new__(
        cls: "Type[UtilityMethods]", *args: "Any", **kwargs: "Any"
    ) -> "NoReturn":
        """Override of the new magic method.

        Note:
            This class cannot be instantiated and this method will always throw an
            exception.

        Args:
            cls (Type[UtilityMethods]: The class to instantiate.
            *args (Any): Arguments.
            **kwargs (Any): Keyword arguments.

        Returns:
            NoReturn
        """
        raise TypeError("Class cannot be instantiated. Please use statically.")

    @staticmethod
    @enforce_parameter_types
    def is_read_only(
        entity: "UtilityMethods.T_is_read_only",
        property_: "Callable[[UtilityMethods.T_is_read_only], object]",
    ) -> "bool":
        """bool

        Args:
            entity (T_is_read_only)
            property_ (Callable[[UtilityMethods.T_is_read_only], object])
        """
        method_result = pythonnet_method_call(
            UtilityMethods.TYPE, "IsReadOnly", entity, property_
        )
        return method_result

    @staticmethod
    @enforce_parameter_types
    def is_valid(
        entity: "UtilityMethods.T_is_valid",
        property_: "Callable[[UtilityMethods.T_is_valid], object]",
    ) -> "bool":
        """bool

        Args:
            entity (T_is_valid)
            property_ (Callable[[UtilityMethods.T_is_valid], object])
        """
        method_result = pythonnet_method_call(
            UtilityMethods.TYPE, "IsValid", entity, property_
        )
        return method_result

    @staticmethod
    @enforce_parameter_types
    def is_method_valid(
        entity: "UtilityMethods.T_is_method_valid",
        method: "Callable[[UtilityMethods.T_is_method_valid], Callable[..., None]]",
    ) -> "bool":
        """bool

        Args:
            entity (T_is_method_valid)
            method (Callable[[UtilityMethods.T_is_method_valid], Callable[..., None]])
        """
        method_result = pythonnet_method_call(
            UtilityMethods.TYPE, "IsMethodValid", entity, method
        )
        return method_result

    @staticmethod
    @enforce_parameter_types
    def is_method_read_only(
        entity: "UtilityMethods.T_is_method_read_only",
        method: "Callable[[UtilityMethods.T_is_method_read_only], Callable[..., None]]",
    ) -> "bool":
        """bool

        Args:
            entity (T_is_method_read_only)
            method (Callable[[UtilityMethods.T_is_method_read_only], Callable[..., None]])
        """
        method_result = pythonnet_method_call(
            UtilityMethods.TYPE, "IsMethodReadOnly", entity, method
        )
        return method_result

    @staticmethod
    @enforce_parameter_types
    def initialise_api_access(installation_directory: "str") -> None:
        """Method does not return.

        Args:
            installation_directory (str)
        """
        installation_directory = str(installation_directory)
        pythonnet_method_call(
            UtilityMethods.TYPE,
            "InitialiseApiAccess",
            installation_directory if installation_directory else "",
        )

    @staticmethod
    def initialise_dot_net_program_access() -> None:
        """Method does not return."""
        pythonnet_method_call(UtilityMethods.TYPE, "InitialiseDotNetProgramAccess")
