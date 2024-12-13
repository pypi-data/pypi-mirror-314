"""IntegerRange"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_INTEGER_RANGE = python_net_import("SMT.MastaAPI.Utility", "IntegerRange")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="IntegerRange")
    CastSelf = TypeVar("CastSelf", bound="IntegerRange._Cast_IntegerRange")


__docformat__ = "restructuredtext en"
__all__ = ("IntegerRange",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_IntegerRange:
    """Special nested class for casting IntegerRange to subclasses."""

    __parent__: "IntegerRange"

    @property
    def integer_range(self: "CastSelf") -> "IntegerRange":
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
class IntegerRange(_0.APIBase):
    """IntegerRange

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INTEGER_RANGE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def max(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "Max")

        if temp is None:
            return 0

        return temp

    @max.setter
    @enforce_parameter_types
    def max(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "Max", int(value) if value is not None else 0
        )

    @property
    def min(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "Min")

        if temp is None:
            return 0

        return temp

    @min.setter
    @enforce_parameter_types
    def min(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "Min", int(value) if value is not None else 0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_IntegerRange":
        """Cast to another type.

        Returns:
            _Cast_IntegerRange
        """
        return _Cast_IntegerRange(self)
