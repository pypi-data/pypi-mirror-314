"""CADMagnetsForLayer"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines import _1327

_CAD_MAGNETS_FOR_LAYER = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "CADMagnetsForLayer"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.electric_machines import _1289

    Self = TypeVar("Self", bound="CADMagnetsForLayer")
    CastSelf = TypeVar("CastSelf", bound="CADMagnetsForLayer._Cast_CADMagnetsForLayer")


__docformat__ = "restructuredtext en"
__all__ = ("CADMagnetsForLayer",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CADMagnetsForLayer:
    """Special nested class for casting CADMagnetsForLayer to subclasses."""

    __parent__: "CADMagnetsForLayer"

    @property
    def magnet_design(self: "CastSelf") -> "_1327.MagnetDesign":
        return self.__parent__._cast(_1327.MagnetDesign)

    @property
    def cad_magnets_for_layer(self: "CastSelf") -> "CADMagnetsForLayer":
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
class CADMagnetsForLayer(_1327.MagnetDesign):
    """CADMagnetsForLayer

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CAD_MAGNETS_FOR_LAYER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def override_magnetisation_directions(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "OverrideMagnetisationDirections")

        if temp is None:
            return False

        return temp

    @override_magnetisation_directions.setter
    @enforce_parameter_types
    def override_magnetisation_directions(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverrideMagnetisationDirections",
            bool(value) if value is not None else False,
        )

    @property
    def cad_magnet_details(self: "Self") -> "List[_1289.CADMagnetDetails]":
        """List[mastapy.electric_machines.CADMagnetDetails]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CADMagnetDetails")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CADMagnetsForLayer":
        """Cast to another type.

        Returns:
            _Cast_CADMagnetsForLayer
        """
        return _Cast_CADMagnetsForLayer(self)
