"""LeadModification"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.micro_geometry import _592

_LEAD_MODIFICATION = python_net_import(
    "SMT.MastaAPI.Gears.MicroGeometry", "LeadModification"
)

if TYPE_CHECKING:
    from typing import Any, Optional, Type, TypeVar

    from mastapy._private.gears.gear_designs.conical.micro_geometry import _1214
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1130,
        _1131,
    )
    from mastapy._private.math_utility import _1585

    Self = TypeVar("Self", bound="LeadModification")
    CastSelf = TypeVar("CastSelf", bound="LeadModification._Cast_LeadModification")


__docformat__ = "restructuredtext en"
__all__ = ("LeadModification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LeadModification:
    """Special nested class for casting LeadModification to subclasses."""

    __parent__: "LeadModification"

    @property
    def modification(self: "CastSelf") -> "_592.Modification":
        return self.__parent__._cast(_592.Modification)

    @property
    def cylindrical_gear_lead_modification(
        self: "CastSelf",
    ) -> "_1130.CylindricalGearLeadModification":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1130

        return self.__parent__._cast(_1130.CylindricalGearLeadModification)

    @property
    def cylindrical_gear_lead_modification_at_profile_position(
        self: "CastSelf",
    ) -> "_1131.CylindricalGearLeadModificationAtProfilePosition":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1131

        return self.__parent__._cast(
            _1131.CylindricalGearLeadModificationAtProfilePosition
        )

    @property
    def conical_gear_lead_modification(
        self: "CastSelf",
    ) -> "_1214.ConicalGearLeadModification":
        from mastapy._private.gears.gear_designs.conical.micro_geometry import _1214

        return self.__parent__._cast(_1214.ConicalGearLeadModification)

    @property
    def lead_modification(self: "CastSelf") -> "LeadModification":
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
class LeadModification(_592.Modification):
    """LeadModification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LEAD_MODIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cad_composed_drawing(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CADComposedDrawing")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def crowning_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CrowningRelief")

        if temp is None:
            return 0.0

        return temp

    @crowning_relief.setter
    @enforce_parameter_types
    def crowning_relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CrowningRelief", float(value) if value is not None else 0.0
        )

    @property
    def evaluation_left_limit_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EvaluationLeftLimitFactor")

        if temp is None:
            return 0.0

        return temp

    @evaluation_left_limit_factor.setter
    @enforce_parameter_types
    def evaluation_left_limit_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationLeftLimitFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def evaluation_of_linear_left_relief_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationOfLinearLeftReliefFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_linear_left_relief_factor.setter
    @enforce_parameter_types
    def evaluation_of_linear_left_relief_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfLinearLeftReliefFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def evaluation_of_linear_right_relief_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationOfLinearRightReliefFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_linear_right_relief_factor.setter
    @enforce_parameter_types
    def evaluation_of_linear_right_relief_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfLinearRightReliefFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def evaluation_of_linear_side_relief_factor(self: "Self") -> "Optional[float]":
        """Optional[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationOfLinearSideReliefFactor"
        )

        if temp is None:
            return None

        return temp

    @evaluation_of_linear_side_relief_factor.setter
    @enforce_parameter_types
    def evaluation_of_linear_side_relief_factor(
        self: "Self", value: "Optional[float]"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "EvaluationOfLinearSideReliefFactor", value
        )

    @property
    def evaluation_of_parabolic_left_relief_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationOfParabolicLeftReliefFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_parabolic_left_relief_factor.setter
    @enforce_parameter_types
    def evaluation_of_parabolic_left_relief_factor(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfParabolicLeftReliefFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def evaluation_of_parabolic_right_relief_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationOfParabolicRightReliefFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_parabolic_right_relief_factor.setter
    @enforce_parameter_types
    def evaluation_of_parabolic_right_relief_factor(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfParabolicRightReliefFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def evaluation_of_parabolic_side_relief_factor(self: "Self") -> "Optional[float]":
        """Optional[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationOfParabolicSideReliefFactor"
        )

        if temp is None:
            return None

        return temp

    @evaluation_of_parabolic_side_relief_factor.setter
    @enforce_parameter_types
    def evaluation_of_parabolic_side_relief_factor(
        self: "Self", value: "Optional[float]"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "EvaluationOfParabolicSideReliefFactor", value
        )

    @property
    def evaluation_right_limit_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EvaluationRightLimitFactor")

        if temp is None:
            return 0.0

        return temp

    @evaluation_right_limit_factor.setter
    @enforce_parameter_types
    def evaluation_right_limit_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationRightLimitFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def evaluation_side_limit_factor(self: "Self") -> "Optional[float]":
        """Optional[float]"""
        temp = pythonnet_property_get(self.wrapped, "EvaluationSideLimitFactor")

        if temp is None:
            return None

        return temp

    @evaluation_side_limit_factor.setter
    @enforce_parameter_types
    def evaluation_side_limit_factor(self: "Self", value: "Optional[float]") -> None:
        pythonnet_property_set(self.wrapped, "EvaluationSideLimitFactor", value)

    @property
    def linear_left_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LinearLeftRelief")

        if temp is None:
            return 0.0

        return temp

    @linear_left_relief.setter
    @enforce_parameter_types
    def linear_left_relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "LinearLeftRelief", float(value) if value is not None else 0.0
        )

    @property
    def linear_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LinearRelief")

        if temp is None:
            return 0.0

        return temp

    @linear_relief.setter
    @enforce_parameter_types
    def linear_relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "LinearRelief", float(value) if value is not None else 0.0
        )

    @property
    def linear_right_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LinearRightRelief")

        if temp is None:
            return 0.0

        return temp

    @linear_right_relief.setter
    @enforce_parameter_types
    def linear_right_relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LinearRightRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    def linear_side_relief(self: "Self") -> "Optional[float]":
        """Optional[float]"""
        temp = pythonnet_property_get(self.wrapped, "LinearSideRelief")

        if temp is None:
            return None

        return temp

    @linear_side_relief.setter
    @enforce_parameter_types
    def linear_side_relief(self: "Self", value: "Optional[float]") -> None:
        pythonnet_property_set(self.wrapped, "LinearSideRelief", value)

    @property
    def measured_data(self: "Self") -> "_1585.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "MeasuredData")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @measured_data.setter
    @enforce_parameter_types
    def measured_data(self: "Self", value: "_1585.Vector2DListAccessor") -> None:
        pythonnet_property_set(self.wrapped, "MeasuredData", value.wrapped)

    @property
    def parabolic_left_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ParabolicLeftRelief")

        if temp is None:
            return 0.0

        return temp

    @parabolic_left_relief.setter
    @enforce_parameter_types
    def parabolic_left_relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ParabolicLeftRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    def parabolic_right_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ParabolicRightRelief")

        if temp is None:
            return 0.0

        return temp

    @parabolic_right_relief.setter
    @enforce_parameter_types
    def parabolic_right_relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ParabolicRightRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    def parabolic_side_relief(self: "Self") -> "Optional[float]":
        """Optional[float]"""
        temp = pythonnet_property_get(self.wrapped, "ParabolicSideRelief")

        if temp is None:
            return None

        return temp

    @parabolic_side_relief.setter
    @enforce_parameter_types
    def parabolic_side_relief(self: "Self", value: "Optional[float]") -> None:
        pythonnet_property_set(self.wrapped, "ParabolicSideRelief", value)

    @property
    def start_of_linear_left_relief_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartOfLinearLeftReliefFactor")

        if temp is None:
            return 0.0

        return temp

    @start_of_linear_left_relief_factor.setter
    @enforce_parameter_types
    def start_of_linear_left_relief_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfLinearLeftReliefFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def start_of_linear_right_relief_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartOfLinearRightReliefFactor")

        if temp is None:
            return 0.0

        return temp

    @start_of_linear_right_relief_factor.setter
    @enforce_parameter_types
    def start_of_linear_right_relief_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfLinearRightReliefFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def start_of_linear_side_relief_factor(self: "Self") -> "Optional[float]":
        """Optional[float]"""
        temp = pythonnet_property_get(self.wrapped, "StartOfLinearSideReliefFactor")

        if temp is None:
            return None

        return temp

    @start_of_linear_side_relief_factor.setter
    @enforce_parameter_types
    def start_of_linear_side_relief_factor(
        self: "Self", value: "Optional[float]"
    ) -> None:
        pythonnet_property_set(self.wrapped, "StartOfLinearSideReliefFactor", value)

    @property
    def start_of_parabolic_left_relief_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartOfParabolicLeftReliefFactor")

        if temp is None:
            return 0.0

        return temp

    @start_of_parabolic_left_relief_factor.setter
    @enforce_parameter_types
    def start_of_parabolic_left_relief_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfParabolicLeftReliefFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def start_of_parabolic_right_relief_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartOfParabolicRightReliefFactor")

        if temp is None:
            return 0.0

        return temp

    @start_of_parabolic_right_relief_factor.setter
    @enforce_parameter_types
    def start_of_parabolic_right_relief_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfParabolicRightReliefFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def start_of_parabolic_side_relief_factor(self: "Self") -> "Optional[float]":
        """Optional[float]"""
        temp = pythonnet_property_get(self.wrapped, "StartOfParabolicSideReliefFactor")

        if temp is None:
            return None

        return temp

    @start_of_parabolic_side_relief_factor.setter
    @enforce_parameter_types
    def start_of_parabolic_side_relief_factor(
        self: "Self", value: "Optional[float]"
    ) -> None:
        pythonnet_property_set(self.wrapped, "StartOfParabolicSideReliefFactor", value)

    @property
    def use_measured_data(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseMeasuredData")

        if temp is None:
            return False

        return temp

    @use_measured_data.setter
    @enforce_parameter_types
    def use_measured_data(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "UseMeasuredData", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_LeadModification":
        """Cast to another type.

        Returns:
            _Cast_LeadModification
        """
        return _Cast_LeadModification(self)
