"""ConicalGearManufacturingControlParameters"""

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

_CONICAL_GEAR_MANUFACTURING_CONTROL_PARAMETERS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel.ControlParameters",
    "ConicalGearManufacturingControlParameters",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.bevel.control_parameters import (
        _843,
        _844,
        _845,
    )

    Self = TypeVar("Self", bound="ConicalGearManufacturingControlParameters")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearManufacturingControlParameters._Cast_ConicalGearManufacturingControlParameters",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearManufacturingControlParameters",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearManufacturingControlParameters:
    """Special nested class for casting ConicalGearManufacturingControlParameters to subclasses."""

    __parent__: "ConicalGearManufacturingControlParameters"

    @property
    def conical_manufacturing_sgm_control_parameters(
        self: "CastSelf",
    ) -> "_843.ConicalManufacturingSGMControlParameters":
        from mastapy._private.gears.manufacturing.bevel.control_parameters import _843

        return self.__parent__._cast(_843.ConicalManufacturingSGMControlParameters)

    @property
    def conical_manufacturing_sgt_control_parameters(
        self: "CastSelf",
    ) -> "_844.ConicalManufacturingSGTControlParameters":
        from mastapy._private.gears.manufacturing.bevel.control_parameters import _844

        return self.__parent__._cast(_844.ConicalManufacturingSGTControlParameters)

    @property
    def conical_manufacturing_smt_control_parameters(
        self: "CastSelf",
    ) -> "_845.ConicalManufacturingSMTControlParameters":
        from mastapy._private.gears.manufacturing.bevel.control_parameters import _845

        return self.__parent__._cast(_845.ConicalManufacturingSMTControlParameters)

    @property
    def conical_gear_manufacturing_control_parameters(
        self: "CastSelf",
    ) -> "ConicalGearManufacturingControlParameters":
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
class ConicalGearManufacturingControlParameters(_0.APIBase):
    """ConicalGearManufacturingControlParameters

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_MANUFACTURING_CONTROL_PARAMETERS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def length_factor_of_contact_pattern(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LengthFactorOfContactPattern")

        if temp is None:
            return 0.0

        return temp

    @length_factor_of_contact_pattern.setter
    @enforce_parameter_types
    def length_factor_of_contact_pattern(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LengthFactorOfContactPattern",
            float(value) if value is not None else 0.0,
        )

    @property
    def pinion_root_relief_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PinionRootReliefLength")

        if temp is None:
            return 0.0

        return temp

    @pinion_root_relief_length.setter
    @enforce_parameter_types
    def pinion_root_relief_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PinionRootReliefLength",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearManufacturingControlParameters":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearManufacturingControlParameters
        """
        return _Cast_ConicalGearManufacturingControlParameters(self)
