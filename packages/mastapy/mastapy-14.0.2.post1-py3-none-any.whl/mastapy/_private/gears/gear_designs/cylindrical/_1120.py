"""ToothThicknessSpecificationBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
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
from mastapy._private.utility.units_and_measurements.measurements import _1719, _1740

_TOOTH_THICKNESS_SPECIFICATION_BASE = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "ToothThicknessSpecificationBase"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.gear_designs.cylindrical import (
        _1068,
        _1078,
        _1099,
        _1119,
    )

    Self = TypeVar("Self", bound="ToothThicknessSpecificationBase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ToothThicknessSpecificationBase._Cast_ToothThicknessSpecificationBase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ToothThicknessSpecificationBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ToothThicknessSpecificationBase:
    """Special nested class for casting ToothThicknessSpecificationBase to subclasses."""

    __parent__: "ToothThicknessSpecificationBase"

    @property
    def finish_tooth_thickness_design_specification(
        self: "CastSelf",
    ) -> "_1078.FinishToothThicknessDesignSpecification":
        from mastapy._private.gears.gear_designs.cylindrical import _1078

        return self.__parent__._cast(_1078.FinishToothThicknessDesignSpecification)

    @property
    def readonly_tooth_thickness_specification(
        self: "CastSelf",
    ) -> "_1099.ReadonlyToothThicknessSpecification":
        from mastapy._private.gears.gear_designs.cylindrical import _1099

        return self.__parent__._cast(_1099.ReadonlyToothThicknessSpecification)

    @property
    def tooth_thickness_specification(
        self: "CastSelf",
    ) -> "_1119.ToothThicknessSpecification":
        from mastapy._private.gears.gear_designs.cylindrical import _1119

        return self.__parent__._cast(_1119.ToothThicknessSpecification)

    @property
    def tooth_thickness_specification_base(
        self: "CastSelf",
    ) -> "ToothThicknessSpecificationBase":
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
class ToothThicknessSpecificationBase(_0.APIBase):
    """ToothThicknessSpecificationBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TOOTH_THICKNESS_SPECIFICATION_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def ball_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "BallDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @ball_diameter.setter
    @enforce_parameter_types
    def ball_diameter(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "BallDiameter", value)

    @property
    def ball_diameter_at_form_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BallDiameterAtFormDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def ball_diameter_at_tip_form_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BallDiameterAtTipFormDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def diameter_at_thickness_measurement(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "DiameterAtThicknessMeasurement")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @diameter_at_thickness_measurement.setter
    @enforce_parameter_types
    def diameter_at_thickness_measurement(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DiameterAtThicknessMeasurement", value)

    @property
    def maximum_number_of_teeth_for_chordal_span_test(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumNumberOfTeethForChordalSpanTest"
        )

        if temp is None:
            return 0

        return temp

    @property
    def minimum_number_of_teeth_for_chordal_span_test(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumNumberOfTeethForChordalSpanTest"
        )

        if temp is None:
            return 0

        return temp

    @property
    def number_of_teeth_for_chordal_span_test(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeethForChordalSpanTest")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_teeth_for_chordal_span_test.setter
    @enforce_parameter_types
    def number_of_teeth_for_chordal_span_test(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NumberOfTeethForChordalSpanTest", value)

    @property
    def chordal_span(
        self: "Self",
    ) -> "_1068.CylindricalGearToothThicknessSpecification[_1719.LengthShort]":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearToothThicknessSpecification[mastapy.utility.units_and_measurements.measurements.LengthShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ChordalSpan")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1719.LengthShort](temp)

    @property
    def normal_thickness(
        self: "Self",
    ) -> "_1068.CylindricalGearToothThicknessSpecification[_1719.LengthShort]":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearToothThicknessSpecification[mastapy.utility.units_and_measurements.measurements.LengthShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalThickness")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1719.LengthShort](temp)

    @property
    def normal_thickness_at_specified_diameter(
        self: "Self",
    ) -> "_1068.CylindricalGearToothThicknessSpecification[_1719.LengthShort]":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearToothThicknessSpecification[mastapy.utility.units_and_measurements.measurements.LengthShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NormalThicknessAtSpecifiedDiameter"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1719.LengthShort](temp)

    @property
    def over_balls(
        self: "Self",
    ) -> "_1068.CylindricalGearToothThicknessSpecification[_1719.LengthShort]":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearToothThicknessSpecification[mastapy.utility.units_and_measurements.measurements.LengthShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverBalls")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1719.LengthShort](temp)

    @property
    def over_two_pins_free_pin_method(
        self: "Self",
    ) -> "_1068.CylindricalGearToothThicknessSpecification[_1719.LengthShort]":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearToothThicknessSpecification[mastapy.utility.units_and_measurements.measurements.LengthShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverTwoPinsFreePinMethod")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1719.LengthShort](temp)

    @property
    def over_two_pins_transverse_method(
        self: "Self",
    ) -> "_1068.CylindricalGearToothThicknessSpecification[_1719.LengthShort]":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearToothThicknessSpecification[mastapy.utility.units_and_measurements.measurements.LengthShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverTwoPinsTransverseMethod")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1719.LengthShort](temp)

    @property
    def profile_shift(
        self: "Self",
    ) -> "_1068.CylindricalGearToothThicknessSpecification[_1719.LengthShort]":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearToothThicknessSpecification[mastapy.utility.units_and_measurements.measurements.LengthShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileShift")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1719.LengthShort](temp)

    @property
    def profile_shift_coefficient(
        self: "Self",
    ) -> "_1068.CylindricalGearToothThicknessSpecification[_1740.Number]":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearToothThicknessSpecification[mastapy.utility.units_and_measurements.measurements.Number]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileShiftCoefficient")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1740.Number](temp)

    @property
    def transverse_thickness(
        self: "Self",
    ) -> "_1068.CylindricalGearToothThicknessSpecification[_1719.LengthShort]":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearToothThicknessSpecification[mastapy.utility.units_and_measurements.measurements.LengthShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseThickness")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1719.LengthShort](temp)

    @property
    def transverse_thickness_at_specified_diameter(
        self: "Self",
    ) -> "_1068.CylindricalGearToothThicknessSpecification[_1719.LengthShort]":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearToothThicknessSpecification[mastapy.utility.units_and_measurements.measurements.LengthShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseThicknessAtSpecifiedDiameter"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1719.LengthShort](temp)

    @property
    def tooth_thickness(
        self: "Self",
    ) -> "List[_1068.CylindricalGearToothThicknessSpecification[_1719.LengthShort]]":
        """List[mastapy.gears.gear_designs.cylindrical.CylindricalGearToothThicknessSpecification[mastapy.utility.units_and_measurements.measurements.LengthShort]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothThickness")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ToothThicknessSpecificationBase":
        """Cast to another type.

        Returns:
            _Cast_ToothThicknessSpecificationBase
        """
        return _Cast_ToothThicknessSpecificationBase(self)
