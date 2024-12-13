"""Datum"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2502

_DATUM = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Datum")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2260
    from mastapy._private.system_model.part_model import _2528

    Self = TypeVar("Self", bound="Datum")
    CastSelf = TypeVar("CastSelf", bound="Datum._Cast_Datum")


__docformat__ = "restructuredtext en"
__all__ = ("Datum",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Datum:
    """Special nested class for casting Datum to subclasses."""

    __parent__: "Datum"

    @property
    def component(self: "CastSelf") -> "_2502.Component":
        return self.__parent__._cast(_2502.Component)

    @property
    def part(self: "CastSelf") -> "_2528.Part":
        from mastapy._private.system_model.part_model import _2528

        return self.__parent__._cast(_2528.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2260.DesignEntity":
        from mastapy._private.system_model import _2260

        return self.__parent__._cast(_2260.DesignEntity)

    @property
    def datum(self: "CastSelf") -> "Datum":
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
class Datum(_2502.Component):
    """Datum

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DATUM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def drawing_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DrawingDiameter")

        if temp is None:
            return 0.0

        return temp

    @drawing_diameter.setter
    @enforce_parameter_types
    def drawing_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DrawingDiameter", float(value) if value is not None else 0.0
        )

    @property
    def offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Offset")

        if temp is None:
            return 0.0

        return temp

    @offset.setter
    @enforce_parameter_types
    def offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Offset", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_Datum":
        """Cast to another type.

        Returns:
            _Cast_Datum
        """
        return _Cast_Datum(self)
