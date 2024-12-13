"""CVT"""

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
from mastapy._private.system_model.part_model.couplings import _2638

_CVT = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Couplings", "CVT")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2260
    from mastapy._private.system_model.part_model import _2492, _2528, _2537

    Self = TypeVar("Self", bound="CVT")
    CastSelf = TypeVar("CastSelf", bound="CVT._Cast_CVT")


__docformat__ = "restructuredtext en"
__all__ = ("CVT",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CVT:
    """Special nested class for casting CVT to subclasses."""

    __parent__: "CVT"

    @property
    def belt_drive(self: "CastSelf") -> "_2638.BeltDrive":
        return self.__parent__._cast(_2638.BeltDrive)

    @property
    def specialised_assembly(self: "CastSelf") -> "_2537.SpecialisedAssembly":
        from mastapy._private.system_model.part_model import _2537

        return self.__parent__._cast(_2537.SpecialisedAssembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2492.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2492

        return self.__parent__._cast(_2492.AbstractAssembly)

    @property
    def part(self: "CastSelf") -> "_2528.Part":
        from mastapy._private.system_model.part_model import _2528

        return self.__parent__._cast(_2528.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2260.DesignEntity":
        from mastapy._private.system_model import _2260

        return self.__parent__._cast(_2260.DesignEntity)

    @property
    def cvt(self: "CastSelf") -> "CVT":
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
class CVT(_2638.BeltDrive):
    """CVT

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CVT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def belt_loss_constant(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BeltLossConstant")

        if temp is None:
            return 0.0

        return temp

    @belt_loss_constant.setter
    @enforce_parameter_types
    def belt_loss_constant(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "BeltLossConstant", float(value) if value is not None else 0.0
        )

    @property
    def coefficient_of_static_friction_with_lubrication(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "CoefficientOfStaticFrictionWithLubrication"
        )

        if temp is None:
            return 0.0

        return temp

    @coefficient_of_static_friction_with_lubrication.setter
    @enforce_parameter_types
    def coefficient_of_static_friction_with_lubrication(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "CoefficientOfStaticFrictionWithLubrication",
            float(value) if value is not None else 0.0,
        )

    @property
    def contact_stiffness_for_unit_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ContactStiffnessForUnitLength")

        if temp is None:
            return 0.0

        return temp

    @contact_stiffness_for_unit_length.setter
    @enforce_parameter_types
    def contact_stiffness_for_unit_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ContactStiffnessForUnitLength",
            float(value) if value is not None else 0.0,
        )

    @property
    def cross_sectional_area_of_the_pump_outlet(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CrossSectionalAreaOfThePumpOutlet")

        if temp is None:
            return 0.0

        return temp

    @cross_sectional_area_of_the_pump_outlet.setter
    @enforce_parameter_types
    def cross_sectional_area_of_the_pump_outlet(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CrossSectionalAreaOfThePumpOutlet",
            float(value) if value is not None else 0.0,
        )

    @property
    def pulley_sheave_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PulleySheaveAngle")

        if temp is None:
            return 0.0

        return temp

    @pulley_sheave_angle.setter
    @enforce_parameter_types
    def pulley_sheave_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PulleySheaveAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    def pump_displacement_per_revolution(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PumpDisplacementPerRevolution")

        if temp is None:
            return 0.0

        return temp

    @pump_displacement_per_revolution.setter
    @enforce_parameter_types
    def pump_displacement_per_revolution(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PumpDisplacementPerRevolution",
            float(value) if value is not None else 0.0,
        )

    @property
    def pump_pressure_loss_constant(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PumpPressureLossConstant")

        if temp is None:
            return 0.0

        return temp

    @pump_pressure_loss_constant.setter
    @enforce_parameter_types
    def pump_pressure_loss_constant(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PumpPressureLossConstant",
            float(value) if value is not None else 0.0,
        )

    @property
    def pump_speed_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PumpSpeedFactor")

        if temp is None:
            return 0.0

        return temp

    @pump_speed_factor.setter
    @enforce_parameter_types
    def pump_speed_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PumpSpeedFactor", float(value) if value is not None else 0.0
        )

    @property
    def pump_speed_loss_constant(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PumpSpeedLossConstant")

        if temp is None:
            return 0.0

        return temp

    @pump_speed_loss_constant.setter
    @enforce_parameter_types
    def pump_speed_loss_constant(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PumpSpeedLossConstant",
            float(value) if value is not None else 0.0,
        )

    @property
    def tangential_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TangentialStiffness")

        if temp is None:
            return 0.0

        return temp

    @tangential_stiffness.setter
    @enforce_parameter_types
    def tangential_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TangentialStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    def use_improved_model(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseImprovedModel")

        if temp is None:
            return False

        return temp

    @use_improved_model.setter
    @enforce_parameter_types
    def use_improved_model(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseImprovedModel",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CVT":
        """Cast to another type.

        Returns:
            _Cast_CVT
        """
        return _Cast_CVT(self)
