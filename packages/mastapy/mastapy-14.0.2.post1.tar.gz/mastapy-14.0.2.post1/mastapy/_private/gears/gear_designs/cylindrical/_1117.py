"""TolerancedValueSpecification"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.cylindrical import _1100

_TOLERANCED_VALUE_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "TolerancedValueSpecification"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, Union

    from mastapy._private.gears.gear_designs.cylindrical import _1069, _1072
    from mastapy._private.gears.gear_designs.cylindrical.thickness_stock_and_backlash import (
        _1125,
        _1126,
    )

    Self = TypeVar("Self", bound="TolerancedValueSpecification")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TolerancedValueSpecification._Cast_TolerancedValueSpecification",
    )

T = TypeVar("T")

__docformat__ = "restructuredtext en"
__all__ = ("TolerancedValueSpecification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TolerancedValueSpecification:
    """Special nested class for casting TolerancedValueSpecification to subclasses."""

    __parent__: "TolerancedValueSpecification"

    @property
    def relative_measurement_view_model(
        self: "CastSelf",
    ) -> "_1100.RelativeMeasurementViewModel":
        return self.__parent__._cast(_1100.RelativeMeasurementViewModel)

    @property
    def cylindrical_mesh_angular_backlash(
        self: "CastSelf",
    ) -> "_1069.CylindricalMeshAngularBacklash":
        from mastapy._private.gears.gear_designs.cylindrical import _1069

        return self.__parent__._cast(_1069.CylindricalMeshAngularBacklash)

    @property
    def cylindrical_mesh_linear_backlash_specification(
        self: "CastSelf",
    ) -> "_1072.CylindricalMeshLinearBacklashSpecification":
        from mastapy._private.gears.gear_designs.cylindrical import _1072

        return self.__parent__._cast(_1072.CylindricalMeshLinearBacklashSpecification)

    @property
    def nominal_value_specification(
        self: "CastSelf",
    ) -> "_1125.NominalValueSpecification":
        from mastapy._private.gears.gear_designs.cylindrical.thickness_stock_and_backlash import (
            _1125,
        )

        return self.__parent__._cast(_1125.NominalValueSpecification)

    @property
    def no_value_specification(self: "CastSelf") -> "_1126.NoValueSpecification":
        from mastapy._private.gears.gear_designs.cylindrical.thickness_stock_and_backlash import (
            _1126,
        )

        return self.__parent__._cast(_1126.NoValueSpecification)

    @property
    def toleranced_value_specification(
        self: "CastSelf",
    ) -> "TolerancedValueSpecification":
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
class TolerancedValueSpecification(_1100.RelativeMeasurementViewModel[T]):
    """TolerancedValueSpecification

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _TOLERANCED_VALUE_SPECIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def average_mean(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "AverageMean")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @average_mean.setter
    @enforce_parameter_types
    def average_mean(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AverageMean", value)

    @property
    def maximum(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Maximum")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum.setter
    @enforce_parameter_types
    def maximum(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Maximum", value)

    @property
    def minimum(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Minimum")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum.setter
    @enforce_parameter_types
    def minimum(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Minimum", value)

    @property
    def spread(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Spread")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @spread.setter
    @enforce_parameter_types
    def spread(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Spread", value)

    @property
    def cast_to(self: "Self") -> "_Cast_TolerancedValueSpecification":
        """Cast to another type.

        Returns:
            _Cast_TolerancedValueSpecification
        """
        return _Cast_TolerancedValueSpecification(self)
