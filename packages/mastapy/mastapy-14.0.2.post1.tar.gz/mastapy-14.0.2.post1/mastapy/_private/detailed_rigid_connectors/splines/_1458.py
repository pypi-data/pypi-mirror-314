"""SAESplineJointDesign"""

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
from mastapy._private.detailed_rigid_connectors.splines import _1470

_SAE_SPLINE_JOINT_DESIGN = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines", "SAESplineJointDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.detailed_rigid_connectors import _1437
    from mastapy._private.detailed_rigid_connectors.splines import _1445, _1465

    Self = TypeVar("Self", bound="SAESplineJointDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="SAESplineJointDesign._Cast_SAESplineJointDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SAESplineJointDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SAESplineJointDesign:
    """Special nested class for casting SAESplineJointDesign to subclasses."""

    __parent__: "SAESplineJointDesign"

    @property
    def standard_spline_joint_design(
        self: "CastSelf",
    ) -> "_1470.StandardSplineJointDesign":
        return self.__parent__._cast(_1470.StandardSplineJointDesign)

    @property
    def spline_joint_design(self: "CastSelf") -> "_1465.SplineJointDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1465

        return self.__parent__._cast(_1465.SplineJointDesign)

    @property
    def detailed_rigid_connector_design(
        self: "CastSelf",
    ) -> "_1437.DetailedRigidConnectorDesign":
        from mastapy._private.detailed_rigid_connectors import _1437

        return self.__parent__._cast(_1437.DetailedRigidConnectorDesign)

    @property
    def sae_spline_joint_design(self: "CastSelf") -> "SAESplineJointDesign":
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
class SAESplineJointDesign(_1470.StandardSplineJointDesign):
    """SAESplineJointDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SAE_SPLINE_JOINT_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def fit_type(self: "Self") -> "_1445.FitTypes":
        """mastapy.detailed_rigid_connectors.splines.FitTypes"""
        temp = pythonnet_property_get(self.wrapped, "FitType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.DetailedRigidConnectors.Splines.FitTypes"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.detailed_rigid_connectors.splines._1445", "FitTypes"
        )(value)

    @fit_type.setter
    @enforce_parameter_types
    def fit_type(self: "Self", value: "_1445.FitTypes") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.DetailedRigidConnectors.Splines.FitTypes"
        )
        pythonnet_property_set(self.wrapped, "FitType", value)

    @property
    def form_clearance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FormClearance")

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_effective_clearance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumEffectiveClearance")

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_tip_chamfer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumTipChamfer")

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_effective_clearance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumEffectiveClearance")

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_tip_chamfer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumTipChamfer")

        if temp is None:
            return 0.0

        return temp

    @property
    def number_of_teeth(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @number_of_teeth.setter
    @enforce_parameter_types
    def number_of_teeth(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfTeeth", int(value) if value is not None else 0
        )

    @property
    def use_internal_half_minimum_minor_diameter_for_external_half_form_diameter_calculation(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "UseInternalHalfMinimumMinorDiameterForExternalHalfFormDiameterCalculation",
        )

        if temp is None:
            return False

        return temp

    @use_internal_half_minimum_minor_diameter_for_external_half_form_diameter_calculation.setter
    @enforce_parameter_types
    def use_internal_half_minimum_minor_diameter_for_external_half_form_diameter_calculation(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseInternalHalfMinimumMinorDiameterForExternalHalfFormDiameterCalculation",
            bool(value) if value is not None else False,
        )

    @property
    def use_saeb921b_1996(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseSAEB921b1996")

        if temp is None:
            return False

        return temp

    @use_saeb921b_1996.setter
    @enforce_parameter_types
    def use_saeb921b_1996(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "UseSAEB921b1996", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_SAESplineJointDesign":
        """Cast to another type.

        Returns:
            _Cast_SAESplineJointDesign
        """
        return _Cast_SAESplineJointDesign(self)
