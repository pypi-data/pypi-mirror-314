"""OilSeal"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import enum_with_selected_value, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.materials.efficiency import _312
from mastapy._private.system_model.part_model import _2505

_OIL_SEAL = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "OilSeal")

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings.bearing_results import _2016
    from mastapy._private.materials.efficiency import _313
    from mastapy._private.math_utility import _1585
    from mastapy._private.system_model import _2260
    from mastapy._private.system_model.part_model import _2502, _2524, _2528

    Self = TypeVar("Self", bound="OilSeal")
    CastSelf = TypeVar("CastSelf", bound="OilSeal._Cast_OilSeal")


__docformat__ = "restructuredtext en"
__all__ = ("OilSeal",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OilSeal:
    """Special nested class for casting OilSeal to subclasses."""

    __parent__: "OilSeal"

    @property
    def connector(self: "CastSelf") -> "_2505.Connector":
        return self.__parent__._cast(_2505.Connector)

    @property
    def mountable_component(self: "CastSelf") -> "_2524.MountableComponent":
        from mastapy._private.system_model.part_model import _2524

        return self.__parent__._cast(_2524.MountableComponent)

    @property
    def component(self: "CastSelf") -> "_2502.Component":
        from mastapy._private.system_model.part_model import _2502

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
    def oil_seal(self: "CastSelf") -> "OilSeal":
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
class OilSeal(_2505.Connector):
    """OilSeal

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _OIL_SEAL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def drag_torque_vs_rotational_speed(self: "Self") -> "_1585.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "DragTorqueVsRotationalSpeed")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @drag_torque_vs_rotational_speed.setter
    @enforce_parameter_types
    def drag_torque_vs_rotational_speed(
        self: "Self", value: "_1585.Vector2DListAccessor"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "DragTorqueVsRotationalSpeed", value.wrapped
        )

    @property
    def inner_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def intercept_of_linear_equation_defining_the_effect_of_temperature(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "InterceptOfLinearEquationDefiningTheEffectOfTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @intercept_of_linear_equation_defining_the_effect_of_temperature.setter
    @enforce_parameter_types
    def intercept_of_linear_equation_defining_the_effect_of_temperature(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "InterceptOfLinearEquationDefiningTheEffectOfTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    def oil_seal_characteristic_life(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OilSealCharacteristicLife")

        if temp is None:
            return 0.0

        return temp

    @oil_seal_characteristic_life.setter
    @enforce_parameter_types
    def oil_seal_characteristic_life(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OilSealCharacteristicLife",
            float(value) if value is not None else 0.0,
        )

    @property
    def oil_seal_frictional_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OilSealFrictionalTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    def oil_seal_loss_calculation_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_OilSealLossCalculationMethod":
        """EnumWithSelectedValue[mastapy.materials.efficiency.OilSealLossCalculationMethod]"""
        temp = pythonnet_property_get(self.wrapped, "OilSealLossCalculationMethod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_OilSealLossCalculationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @oil_seal_loss_calculation_method.setter
    @enforce_parameter_types
    def oil_seal_loss_calculation_method(
        self: "Self", value: "_312.OilSealLossCalculationMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_OilSealLossCalculationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "OilSealLossCalculationMethod", value)

    @property
    def oil_seal_material(self: "Self") -> "_313.OilSealMaterialType":
        """mastapy.materials.efficiency.OilSealMaterialType"""
        temp = pythonnet_property_get(self.wrapped, "OilSealMaterial")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.Efficiency.OilSealMaterialType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials.efficiency._313", "OilSealMaterialType"
        )(value)

    @oil_seal_material.setter
    @enforce_parameter_types
    def oil_seal_material(self: "Self", value: "_313.OilSealMaterialType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.Efficiency.OilSealMaterialType"
        )
        pythonnet_property_set(self.wrapped, "OilSealMaterial", value)

    @property
    def oil_seal_mean_time_before_failure(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OilSealMeanTimeBeforeFailure")

        if temp is None:
            return 0.0

        return temp

    @oil_seal_mean_time_before_failure.setter
    @enforce_parameter_types
    def oil_seal_mean_time_before_failure(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OilSealMeanTimeBeforeFailure",
            float(value) if value is not None else 0.0,
        )

    @property
    def oil_seal_orientation(self: "Self") -> "_2016.Orientations":
        """mastapy.bearings.bearing_results.Orientations"""
        temp = pythonnet_property_get(self.wrapped, "OilSealOrientation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.BearingResults.Orientations"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.bearing_results._2016", "Orientations"
        )(value)

    @oil_seal_orientation.setter
    @enforce_parameter_types
    def oil_seal_orientation(self: "Self", value: "_2016.Orientations") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.BearingResults.Orientations"
        )
        pythonnet_property_set(self.wrapped, "OilSealOrientation", value)

    @property
    def slope_of_linear_equation_defining_the_effect_of_temperature(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "SlopeOfLinearEquationDefiningTheEffectOfTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @slope_of_linear_equation_defining_the_effect_of_temperature.setter
    @enforce_parameter_types
    def slope_of_linear_equation_defining_the_effect_of_temperature(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "SlopeOfLinearEquationDefiningTheEffectOfTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    def thickness_in_radial_direction(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ThicknessInRadialDirection")

        if temp is None:
            return 0.0

        return temp

    @thickness_in_radial_direction.setter
    @enforce_parameter_types
    def thickness_in_radial_direction(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ThicknessInRadialDirection",
            float(value) if value is not None else 0.0,
        )

    @property
    def width(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @width.setter
    @enforce_parameter_types
    def width(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Width", value)

    @property
    def cast_to(self: "Self") -> "_Cast_OilSeal":
        """Cast to another type.

        Returns:
            _Cast_OilSeal
        """
        return _Cast_OilSeal(self)
