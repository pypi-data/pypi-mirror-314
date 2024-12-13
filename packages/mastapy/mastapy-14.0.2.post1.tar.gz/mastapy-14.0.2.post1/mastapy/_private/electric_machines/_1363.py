"""WindingMaterial"""

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
from mastapy._private.materials import _282

_WINDING_MATERIAL = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "WindingMaterial"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.databases import _1884

    Self = TypeVar("Self", bound="WindingMaterial")
    CastSelf = TypeVar("CastSelf", bound="WindingMaterial._Cast_WindingMaterial")


__docformat__ = "restructuredtext en"
__all__ = ("WindingMaterial",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WindingMaterial:
    """Special nested class for casting WindingMaterial to subclasses."""

    __parent__: "WindingMaterial"

    @property
    def material(self: "CastSelf") -> "_282.Material":
        return self.__parent__._cast(_282.Material)

    @property
    def named_database_item(self: "CastSelf") -> "_1884.NamedDatabaseItem":
        from mastapy._private.utility.databases import _1884

        return self.__parent__._cast(_1884.NamedDatabaseItem)

    @property
    def winding_material(self: "CastSelf") -> "WindingMaterial":
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
class WindingMaterial(_282.Material):
    """WindingMaterial

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WINDING_MATERIAL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def relative_permeability(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RelativePermeability")

        if temp is None:
            return 0.0

        return temp

    @relative_permeability.setter
    @enforce_parameter_types
    def relative_permeability(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RelativePermeability",
            float(value) if value is not None else 0.0,
        )

    @property
    def temperature_coefficient_for_winding_resistivity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "TemperatureCoefficientForWindingResistivity"
        )

        if temp is None:
            return 0.0

        return temp

    @temperature_coefficient_for_winding_resistivity.setter
    @enforce_parameter_types
    def temperature_coefficient_for_winding_resistivity(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "TemperatureCoefficientForWindingResistivity",
            float(value) if value is not None else 0.0,
        )

    @property
    def winding_resistivity_at_20_degrees_c(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WindingResistivityAt20DegreesC")

        if temp is None:
            return 0.0

        return temp

    @winding_resistivity_at_20_degrees_c.setter
    @enforce_parameter_types
    def winding_resistivity_at_20_degrees_c(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WindingResistivityAt20DegreesC",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_WindingMaterial":
        """Cast to another type.

        Returns:
            _Cast_WindingMaterial
        """
        return _Cast_WindingMaterial(self)
