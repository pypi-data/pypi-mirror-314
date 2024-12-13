"""FinishStockSpecification"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.cylindrical import _1101

_FINISH_STOCK_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.ThicknessStockAndBacklash",
    "FinishStockSpecification",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1117
    from mastapy._private.gears.gear_designs.cylindrical.thickness_stock_and_backlash import (
        _1124,
    )

    Self = TypeVar("Self", bound="FinishStockSpecification")
    CastSelf = TypeVar(
        "CastSelf", bound="FinishStockSpecification._Cast_FinishStockSpecification"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FinishStockSpecification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FinishStockSpecification:
    """Special nested class for casting FinishStockSpecification to subclasses."""

    __parent__: "FinishStockSpecification"

    @property
    def relative_values_specification(
        self: "CastSelf",
    ) -> "_1101.RelativeValuesSpecification":
        pass

        return self.__parent__._cast(_1101.RelativeValuesSpecification)

    @property
    def finish_stock_specification(self: "CastSelf") -> "FinishStockSpecification":
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
class FinishStockSpecification(
    _1101.RelativeValuesSpecification["FinishStockSpecification"]
):
    """FinishStockSpecification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FINISH_STOCK_SPECIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def finish_stock_rough_thickness_specification_method(
        self: "Self",
    ) -> "_1124.FinishStockType":
        """mastapy.gears.gear_designs.cylindrical.thickness_stock_and_backlash.FinishStockType"""
        temp = pythonnet_property_get(
            self.wrapped, "FinishStockRoughThicknessSpecificationMethod"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.ThicknessStockAndBacklash.FinishStockType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical.thickness_stock_and_backlash._1124",
            "FinishStockType",
        )(value)

    @finish_stock_rough_thickness_specification_method.setter
    @enforce_parameter_types
    def finish_stock_rough_thickness_specification_method(
        self: "Self", value: "_1124.FinishStockType"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.ThicknessStockAndBacklash.FinishStockType",
        )
        pythonnet_property_set(
            self.wrapped, "FinishStockRoughThicknessSpecificationMethod", value
        )

    @property
    def normal(
        self: "Self",
    ) -> "_1117.TolerancedValueSpecification[FinishStockSpecification]":
        """mastapy.gears.gear_designs.cylindrical.TolerancedValueSpecification[mastapy.gears.gear_designs.cylindrical.thickness_stock_and_backlash.FinishStockSpecification]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Normal")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[FinishStockSpecification](
            temp
        )

    @property
    def tangent_to_reference_circle(
        self: "Self",
    ) -> "_1117.TolerancedValueSpecification[FinishStockSpecification]":
        """mastapy.gears.gear_designs.cylindrical.TolerancedValueSpecification[mastapy.gears.gear_designs.cylindrical.thickness_stock_and_backlash.FinishStockSpecification]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TangentToReferenceCircle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[FinishStockSpecification](
            temp
        )

    @property
    def cast_to(self: "Self") -> "_Cast_FinishStockSpecification":
        """Cast to another type.

        Returns:
            _Cast_FinishStockSpecification
        """
        return _Cast_FinishStockSpecification(self)
