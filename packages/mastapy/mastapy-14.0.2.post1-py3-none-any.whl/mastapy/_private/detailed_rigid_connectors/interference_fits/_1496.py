"""InterferenceFitHalfDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
from mastapy._private.detailed_rigid_connectors import _1438

_INTERFERENCE_FIT_HALF_DESIGN = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.InterferenceFits", "InterferenceFitHalfDesign"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings.tolerances import _1977
    from mastapy._private.detailed_rigid_connectors.interference_fits import _1497
    from mastapy._private.detailed_rigid_connectors.keyed_joints import _1489

    Self = TypeVar("Self", bound="InterferenceFitHalfDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="InterferenceFitHalfDesign._Cast_InterferenceFitHalfDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterferenceFitHalfDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterferenceFitHalfDesign:
    """Special nested class for casting InterferenceFitHalfDesign to subclasses."""

    __parent__: "InterferenceFitHalfDesign"

    @property
    def detailed_rigid_connector_half_design(
        self: "CastSelf",
    ) -> "_1438.DetailedRigidConnectorHalfDesign":
        return self.__parent__._cast(_1438.DetailedRigidConnectorHalfDesign)

    @property
    def keyway_joint_half_design(self: "CastSelf") -> "_1489.KeywayJointHalfDesign":
        from mastapy._private.detailed_rigid_connectors.keyed_joints import _1489

        return self.__parent__._cast(_1489.KeywayJointHalfDesign)

    @property
    def interference_fit_half_design(self: "CastSelf") -> "InterferenceFitHalfDesign":
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
class InterferenceFitHalfDesign(_1438.DetailedRigidConnectorHalfDesign):
    """InterferenceFitHalfDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INTERFERENCE_FIT_HALF_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def average_joint_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageJointDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def average_surface_roughness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AverageSurfaceRoughness")

        if temp is None:
            return 0.0

        return temp

    @average_surface_roughness.setter
    @enforce_parameter_types
    def average_surface_roughness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AverageSurfaceRoughness",
            float(value) if value is not None else 0.0,
        )

    @property
    def designation(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Designation")

        if temp is None:
            return ""

        return temp

    @property
    def diameter_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DiameterRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    def joint_pressure_for_fully_plastic_part(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "JointPressureForFullyPlasticPart")

        if temp is None:
            return 0.0

        return temp

    @property
    def lower_deviation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LowerDeviation")

        if temp is None:
            return 0.0

        return temp

    @property
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def nominal_joint_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "NominalJointDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @nominal_joint_diameter.setter
    @enforce_parameter_types
    def nominal_joint_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NominalJointDiameter", value)

    @property
    def permissible_joint_pressure_for_fully_elastic_part(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleJointPressureForFullyElasticPart"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def permissible_relative_interference_for_fully_elastic_part(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleRelativeInterferenceForFullyElasticPart"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def required_safety_against_plastic_strain(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "RequiredSafetyAgainstPlasticStrain"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @required_safety_against_plastic_strain.setter
    @enforce_parameter_types
    def required_safety_against_plastic_strain(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "RequiredSafetyAgainstPlasticStrain", value
        )

    @property
    def stress_region(self: "Self") -> "_1497.StressRegions":
        """mastapy.detailed_rigid_connectors.interference_fits.StressRegions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StressRegion")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.DetailedRigidConnectors.InterferenceFits.StressRegions"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.detailed_rigid_connectors.interference_fits._1497",
            "StressRegions",
        )(value)

    @property
    def upper_deviation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UpperDeviation")

        if temp is None:
            return 0.0

        return temp

    @property
    def tolerance(self: "Self") -> "_1977.SupportTolerance":
        """mastapy.bearings.tolerances.SupportTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Tolerance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_InterferenceFitHalfDesign":
        """Cast to another type.

        Returns:
            _Cast_InterferenceFitHalfDesign
        """
        return _Cast_InterferenceFitHalfDesign(self)
