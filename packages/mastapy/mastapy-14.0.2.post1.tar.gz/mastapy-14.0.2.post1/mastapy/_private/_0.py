"""APIBase"""

from __future__ import annotations

from sys import modules
from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _7727
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.deprecation import deprecated
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_API_BASE = python_net_import("SMT.MastaAPI", "APIBase")

if TYPE_CHECKING:
    from typing import Any, List, Optional, Type, TypeVar

    T = TypeVar("T")
    Self = TypeVar("Self", bound="APIBase")
    CastSelf = TypeVar("CastSelf", bound="APIBase._Cast_APIBase")


__docformat__ = "restructuredtext en"
__all__ = ("APIBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_APIBase:
    """Special nested class for casting APIBase to subclasses."""

    __parent__: "APIBase"

    @property
    def api_base(self: "CastSelf") -> "APIBase":
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
class APIBase(_7727.MarshalByRefObjectPermanent):
    """APIBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _API_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def invalid_properties(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InvalidProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @property
    def read_only_properties(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReadOnlyProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @property
    def all_properties_are_read_only(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllPropertiesAreReadOnly")

        if temp is None:
            return False

        return temp

    @property
    def all_properties_are_invalid(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllPropertiesAreInvalid")

        if temp is None:
            return False

        return temp

    @enforce_parameter_types
    def is_instance_of_wrapped_type(self: "Self", type_: "type") -> "bool":
        """bool

        Args:
            type_ (type)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "IsInstanceOfWrappedType", type_
        )
        return method_result

    @enforce_parameter_types
    def set_property(self: "Self", name: "str", value: "object") -> None:
        """Method does not return.

        Args:
            name (str)
            value (object)
        """
        name = str(name)
        pythonnet_method_call(self.wrapped, "SetProperty", name if name else "", value)

    @enforce_parameter_types
    def is_valid(self: "Self", property_name: "str") -> "bool":
        """bool

        Args:
            property_name (str)
        """
        property_name = str(property_name)
        method_result = pythonnet_method_call(
            self.wrapped, "IsValid", property_name if property_name else ""
        )
        return method_result

    @enforce_parameter_types
    def is_read_only(self: "Self", property_name: "str") -> "bool":
        """bool

        Args:
            property_name (str)
        """
        property_name = str(property_name)
        method_result = pythonnet_method_call(
            self.wrapped, "IsReadOnly", property_name if property_name else ""
        )
        return method_result

    def documentation_url(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(self.wrapped, "DocumentationUrl")
        return method_result

    def __hash__(self: "Self") -> "int":
        """int"""
        method_result = pythonnet_method_call(self.wrapped, "GetHashCode")
        return method_result

    @enforce_parameter_types
    def __eq__(self: "Self", other: "APIBase") -> "bool":
        """bool

        Args:
            other (mastapy.APIBase)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "op_Equality", self.wrapped, other.wrapped if other else None
        )
        return method_result

    @enforce_parameter_types
    def __ne__(self: "Self", other: "APIBase") -> "bool":
        """bool

        Args:
            other (mastapy.APIBase)
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "op_Inequality",
            self.wrapped,
            other.wrapped if other else None,
        )
        return method_result

    def get_property(self: "Self", name: str, type_: "Type[T]") -> "Optional[T]":
        """Get a property from the MASTA API by name and expected return type.

        Args:
            name (str): Name of the property.
            type_ (Type[T]): Expected return type.

        Returns:
            T | None
        """
        name = str(name)
        type_ = getattr(type_, "TYPE", type_)

        try:
            method_result = self.wrapped.GetProperty[type_](name if name else "")
        except Exception:
            name = name.replace(" ", "")
            name = utility.snake(name)
            name = utility.camel_spaced(name)
            name = utility.strip_punctuation(name)

            try:
                method_result = self.wrapped.GetProperty[type_](name if name else "")
            except Exception:
                return None

        try:
            type_ = method_result.GetType()
            return (
                constructor.new(type_.Namespace, type_.Name)(method_result)
                if method_result is not None
                else None
            )
        except AttributeError:
            return method_result

    def __del__(self: "Self") -> None:
        """Override of the del magic method."""
        self.wrapped.reference_count -= 1
        if self.wrapped.reference_count <= 0:
            self.disconnect_from_masta()

    def disconnect_from_masta(self: "Self") -> None:
        """Disconnect the object from MASTA."""
        import contextlib

        with contextlib.suppress(TypeError, ImportError):
            self.wrapped.DisconnectFromMASTA()

    def _cast(self: "Self", type_: "Type[T]") -> "T":
        return type_(self.wrapped)

    def is_of_type(self: "Self", type_: "Type") -> bool:
        """Method for checking if a mastapy object can be cast to another type.

        Note:
            This method follows all standard casting rules from other languages.

        Args:
            type_ (Type): The type to check.

        Returns:
            bool
        """
        a = type(self.wrapped)
        b = getattr(modules[type_.__module__], type_.__name__).TYPE

        return b in a.__mro__

    def cast_or_none(self: "Self", type_: "Type[T]") -> "Optional[T]":
        """Method for casting one mastapy object to another.

        Note:
            This method follows all standard casting rules from other languages.
            This method will return None if the cast fails.

        Args:
            type_ (Type[T]): The type to cast to.

        Returns:
            T | None
        """
        if not self.is_of_type(type_):
            return None

        return self._cast(type_)

    @deprecated('Use the "cast_to" property or "cast_or_none" function instead.')
    def cast(self: "Self", type_: "Type[T]") -> "T":
        """Method for casting one mastapy object to another.

        Note:
            This method follows all standard casting rules from other languages.
            This method will raise a CastException if the cast fails.

        Args:
            type_ (Type[T]): The type to cast to.

        Returns:
            T
        """
        if not self.is_of_type(type_):
            raise CastException(
                "Could not cast {} to type {}. Is it a mastapy type?".format(
                    type(self), type_
                )
            ) from None

        return self._cast(type_)

    def __str__(self: "Self") -> str:
        """Override of the str magic method.

        Returns:
            str
        """
        return self.wrapped.ToString()

    def __repr__(self: "Self") -> str:
        """Override of the repr magic method.

        Returns:
            str
        """
        type_name = self.wrapped.GetType().Name
        part_name = self.unique_name if hasattr(self, "unique_name") else str(self)
        return f"<{type_name} : {part_name}>"

    @property
    def cast_to(self: "Self") -> "_Cast_APIBase":
        """Cast to another type.

        Returns:
            _Cast_APIBase
        """
        return _Cast_APIBase(self)
