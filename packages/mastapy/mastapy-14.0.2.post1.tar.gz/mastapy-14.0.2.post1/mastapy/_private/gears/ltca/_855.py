"""CylindricalGearFilletNodeStressResultsRow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.ltca import _864

_CYLINDRICAL_GEAR_FILLET_NODE_STRESS_RESULTS_ROW = python_net_import(
    "SMT.MastaAPI.Gears.LTCA", "CylindricalGearFilletNodeStressResultsRow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalGearFilletNodeStressResultsRow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearFilletNodeStressResultsRow._Cast_CylindricalGearFilletNodeStressResultsRow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearFilletNodeStressResultsRow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearFilletNodeStressResultsRow:
    """Special nested class for casting CylindricalGearFilletNodeStressResultsRow to subclasses."""

    __parent__: "CylindricalGearFilletNodeStressResultsRow"

    @property
    def gear_fillet_node_stress_results_row(
        self: "CastSelf",
    ) -> "_864.GearFilletNodeStressResultsRow":
        return self.__parent__._cast(_864.GearFilletNodeStressResultsRow)

    @property
    def cylindrical_gear_fillet_node_stress_results_row(
        self: "CastSelf",
    ) -> "CylindricalGearFilletNodeStressResultsRow":
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
class CylindricalGearFilletNodeStressResultsRow(_864.GearFilletNodeStressResultsRow):
    """CylindricalGearFilletNodeStressResultsRow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_FILLET_NODE_STRESS_RESULTS_ROW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Diameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def distance_along_fillet(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DistanceAlongFillet")

        if temp is None:
            return 0.0

        return temp

    @property
    def radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Radius")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearFilletNodeStressResultsRow":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearFilletNodeStressResultsRow
        """
        return _Cast_CylindricalGearFilletNodeStressResultsRow(self)
