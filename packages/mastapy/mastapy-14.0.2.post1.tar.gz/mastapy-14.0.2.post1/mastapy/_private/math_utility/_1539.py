"""Range"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_RANGE = python_net_import("SMT.MastaAPI.MathUtility", "Range")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Range")
    CastSelf = TypeVar("CastSelf", bound="Range._Cast_Range")


__docformat__ = "restructuredtext en"
__all__ = ("Range",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Range:
    """Special nested class for casting Range to subclasses."""

    __parent__: "Range"

    @property
    def range(self: "CastSelf") -> "Range":
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
class Range:
    """Range

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RANGE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @enforce_parameter_types
    def __eq__(self: "Self", other: "Range") -> "bool":
        """bool

        Args:
            other (mastapy.math_utility.Range)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "op_Equality", self.wrapped, other.wrapped if other else None
        )
        return method_result

    @enforce_parameter_types
    def __ne__(self: "Self", other: "Range") -> "bool":
        """bool

        Args:
            other (mastapy.math_utility.Range)
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "op_Inequality",
            self.wrapped,
            other.wrapped if other else None,
        )
        return method_result

    def __hash__(self: "Self") -> "int":
        """int"""
        method_result = pythonnet_method_call(self.wrapped, "GetHashCode")
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_Range":
        """Cast to another type.

        Returns:
            _Cast_Range
        """
        return _Cast_Range(self)
