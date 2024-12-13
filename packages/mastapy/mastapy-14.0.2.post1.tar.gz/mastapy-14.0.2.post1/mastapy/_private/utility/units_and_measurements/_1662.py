"""Unit"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_UNIT = python_net_import("SMT.MastaAPI.Utility.UnitsAndMeasurements", "Unit")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.units_and_measurements import (
        _1654,
        _1655,
        _1656,
        _1660,
        _1661,
        _1663,
    )

    Self = TypeVar("Self", bound="Unit")
    CastSelf = TypeVar("CastSelf", bound="Unit._Cast_Unit")


__docformat__ = "restructuredtext en"
__all__ = ("Unit",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Unit:
    """Special nested class for casting Unit to subclasses."""

    __parent__: "Unit"

    @property
    def degrees_minutes_seconds(self: "CastSelf") -> "_1654.DegreesMinutesSeconds":
        from mastapy._private.utility.units_and_measurements import _1654

        return self.__parent__._cast(_1654.DegreesMinutesSeconds)

    @property
    def enum_unit(self: "CastSelf") -> "_1655.EnumUnit":
        from mastapy._private.utility.units_and_measurements import _1655

        return self.__parent__._cast(_1655.EnumUnit)

    @property
    def inverse_unit(self: "CastSelf") -> "_1656.InverseUnit":
        from mastapy._private.utility.units_and_measurements import _1656

        return self.__parent__._cast(_1656.InverseUnit)

    @property
    def safety_factor_unit(self: "CastSelf") -> "_1660.SafetyFactorUnit":
        from mastapy._private.utility.units_and_measurements import _1660

        return self.__parent__._cast(_1660.SafetyFactorUnit)

    @property
    def time_unit(self: "CastSelf") -> "_1661.TimeUnit":
        from mastapy._private.utility.units_and_measurements import _1661

        return self.__parent__._cast(_1661.TimeUnit)

    @property
    def unit_gradient(self: "CastSelf") -> "_1663.UnitGradient":
        from mastapy._private.utility.units_and_measurements import _1663

        return self.__parent__._cast(_1663.UnitGradient)

    @property
    def unit(self: "CastSelf") -> "Unit":
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
class Unit(_0.APIBase):
    """Unit

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _UNIT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def html_symbol(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HTMLSymbol")

        if temp is None:
            return ""

        return temp

    @property
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def offset(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Offset")

        if temp is None:
            return 0.0

        return temp

    @property
    def scale(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Scale")

        if temp is None:
            return 0.0

        return temp

    @property
    def symbol(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Symbol")

        if temp is None:
            return ""

        return temp

    @enforce_parameter_types
    def convert_from_si_unit(self: "Self", d: "float") -> "float":
        """float

        Args:
            d (float)
        """
        d = float(d)
        method_result = pythonnet_method_call(
            self.wrapped, "ConvertFromSIUnit", d if d else 0.0
        )
        return method_result

    @enforce_parameter_types
    def convert_to_si_unit(self: "Self", d: "float") -> "float":
        """float

        Args:
            d (float)
        """
        d = float(d)
        method_result = pythonnet_method_call(
            self.wrapped, "ConvertToSIUnit", d if d else 0.0
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_Unit":
        """Cast to another type.

        Returns:
            _Cast_Unit
        """
        return _Cast_Unit(self)
