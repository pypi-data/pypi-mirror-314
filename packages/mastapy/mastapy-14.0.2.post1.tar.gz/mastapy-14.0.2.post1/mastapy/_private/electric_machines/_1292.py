"""CADStator"""

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
from mastapy._private.electric_machines import _1284

_CAD_STATOR = python_net_import("SMT.MastaAPI.ElectricMachines", "CADStator")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines import _1293

    Self = TypeVar("Self", bound="CADStator")
    CastSelf = TypeVar("CastSelf", bound="CADStator._Cast_CADStator")


__docformat__ = "restructuredtext en"
__all__ = ("CADStator",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CADStator:
    """Special nested class for casting CADStator to subclasses."""

    __parent__: "CADStator"

    @property
    def abstract_stator(self: "CastSelf") -> "_1284.AbstractStator":
        return self.__parent__._cast(_1284.AbstractStator)

    @property
    def cad_stator(self: "CastSelf") -> "CADStator":
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
class CADStator(_1284.AbstractStator):
    """CADStator

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CAD_STATOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def design_has_unequal_notches_between_adjacent_teeth(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "DesignHasUnequalNotchesBetweenAdjacentTeeth"
        )

        if temp is None:
            return False

        return temp

    @design_has_unequal_notches_between_adjacent_teeth.setter
    @enforce_parameter_types
    def design_has_unequal_notches_between_adjacent_teeth(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "DesignHasUnequalNotchesBetweenAdjacentTeeth",
            bool(value) if value is not None else False,
        )

    @property
    def importing_full_stator(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ImportingFullStator")

        if temp is None:
            return False

        return temp

    @importing_full_stator.setter
    @enforce_parameter_types
    def importing_full_stator(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ImportingFullStator",
            bool(value) if value is not None else False,
        )

    @property
    def number_of_slots_for_imported_sector(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfSlotsForImportedSector")

        if temp is None:
            return 0

        return temp

    @number_of_slots_for_imported_sector.setter
    @enforce_parameter_types
    def number_of_slots_for_imported_sector(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfSlotsForImportedSector",
            int(value) if value is not None else 0,
        )

    @property
    def tooth_and_slot(self: "Self") -> "_1293.CADToothAndSlot":
        """mastapy.electric_machines.CADToothAndSlot

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothAndSlot")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CADStator":
        """Cast to another type.

        Returns:
            _Cast_CADStator
        """
        return _Cast_CADStator(self)
