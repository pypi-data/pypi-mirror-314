"""KeyedJointDesign"""

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
from mastapy._private.detailed_rigid_connectors.interference_fits import _1495

_KEYED_JOINT_DESIGN = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.KeyedJoints", "KeyedJointDesign"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.detailed_rigid_connectors import _1437
    from mastapy._private.detailed_rigid_connectors.keyed_joints import _1488, _1490

    Self = TypeVar("Self", bound="KeyedJointDesign")
    CastSelf = TypeVar("CastSelf", bound="KeyedJointDesign._Cast_KeyedJointDesign")


__docformat__ = "restructuredtext en"
__all__ = ("KeyedJointDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KeyedJointDesign:
    """Special nested class for casting KeyedJointDesign to subclasses."""

    __parent__: "KeyedJointDesign"

    @property
    def interference_fit_design(self: "CastSelf") -> "_1495.InterferenceFitDesign":
        return self.__parent__._cast(_1495.InterferenceFitDesign)

    @property
    def detailed_rigid_connector_design(
        self: "CastSelf",
    ) -> "_1437.DetailedRigidConnectorDesign":
        from mastapy._private.detailed_rigid_connectors import _1437

        return self.__parent__._cast(_1437.DetailedRigidConnectorDesign)

    @property
    def keyed_joint_design(self: "CastSelf") -> "KeyedJointDesign":
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
class KeyedJointDesign(_1495.InterferenceFitDesign):
    """KeyedJointDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KEYED_JOINT_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def allowable_contact_stress_for_inner_component(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AllowableContactStressForInnerComponent"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def allowable_contact_stress_for_key(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableContactStressForKey")

        if temp is None:
            return 0.0

        return temp

    @property
    def allowable_contact_stress_for_outer_component(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AllowableContactStressForOuterComponent"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def edge_chamfer(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EdgeChamfer")

        if temp is None:
            return 0.0

        return temp

    @edge_chamfer.setter
    @enforce_parameter_types
    def edge_chamfer(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "EdgeChamfer", float(value) if value is not None else 0.0
        )

    @property
    def geometry_type(self: "Self") -> "_1488.KeyTypes":
        """mastapy.detailed_rigid_connectors.keyed_joints.KeyTypes"""
        temp = pythonnet_property_get(self.wrapped, "GeometryType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.DetailedRigidConnectors.KeyedJoints.KeyTypes"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.detailed_rigid_connectors.keyed_joints._1488", "KeyTypes"
        )(value)

    @geometry_type.setter
    @enforce_parameter_types
    def geometry_type(self: "Self", value: "_1488.KeyTypes") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.DetailedRigidConnectors.KeyedJoints.KeyTypes"
        )
        pythonnet_property_set(self.wrapped, "GeometryType", value)

    @property
    def height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Height")

        if temp is None:
            return 0.0

        return temp

    @height.setter
    @enforce_parameter_types
    def height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Height", float(value) if value is not None else 0.0
        )

    @property
    def inclined_underside_chamfer(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InclinedUndersideChamfer")

        if temp is None:
            return 0.0

        return temp

    @inclined_underside_chamfer.setter
    @enforce_parameter_types
    def inclined_underside_chamfer(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InclinedUndersideChamfer",
            float(value) if value is not None else 0.0,
        )

    @property
    def interference_fit_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InterferenceFitLength")

        if temp is None:
            return 0.0

        return temp

    @interference_fit_length.setter
    @enforce_parameter_types
    def interference_fit_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InterferenceFitLength",
            float(value) if value is not None else 0.0,
        )

    @property
    def is_interference_fit(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsInterferenceFit")

        if temp is None:
            return False

        return temp

    @is_interference_fit.setter
    @enforce_parameter_types
    def is_interference_fit(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsInterferenceFit",
            bool(value) if value is not None else False,
        )

    @property
    def is_key_case_hardened(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsKeyCaseHardened")

        if temp is None:
            return False

        return temp

    @is_key_case_hardened.setter
    @enforce_parameter_types
    def is_key_case_hardened(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsKeyCaseHardened",
            bool(value) if value is not None else False,
        )

    @property
    def key_effective_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KeyEffectiveLength")

        if temp is None:
            return 0.0

        return temp

    @property
    def keyway_depth_inner_component(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "KeywayDepthInnerComponent")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @keyway_depth_inner_component.setter
    @enforce_parameter_types
    def keyway_depth_inner_component(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "KeywayDepthInnerComponent", value)

    @property
    def keyway_depth_outer_component(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "KeywayDepthOuterComponent")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @keyway_depth_outer_component.setter
    @enforce_parameter_types
    def keyway_depth_outer_component(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "KeywayDepthOuterComponent", value)

    @property
    def length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Length")

        if temp is None:
            return 0.0

        return temp

    @length.setter
    @enforce_parameter_types
    def length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Length", float(value) if value is not None else 0.0
        )

    @property
    def number_of_keys(self: "Self") -> "_1490.NumberOfKeys":
        """mastapy.detailed_rigid_connectors.keyed_joints.NumberOfKeys"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfKeys")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.DetailedRigidConnectors.KeyedJoints.NumberOfKeys"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.detailed_rigid_connectors.keyed_joints._1490",
            "NumberOfKeys",
        )(value)

    @number_of_keys.setter
    @enforce_parameter_types
    def number_of_keys(self: "Self", value: "_1490.NumberOfKeys") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.DetailedRigidConnectors.KeyedJoints.NumberOfKeys"
        )
        pythonnet_property_set(self.wrapped, "NumberOfKeys", value)

    @property
    def position_offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PositionOffset")

        if temp is None:
            return 0.0

        return temp

    @position_offset.setter
    @enforce_parameter_types
    def position_offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PositionOffset", float(value) if value is not None else 0.0
        )

    @property
    def tensile_yield_strength(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TensileYieldStrength")

        if temp is None:
            return 0.0

        return temp

    @tensile_yield_strength.setter
    @enforce_parameter_types
    def tensile_yield_strength(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TensileYieldStrength",
            float(value) if value is not None else 0.0,
        )

    @property
    def width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return temp

    @width.setter
    @enforce_parameter_types
    def width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_KeyedJointDesign":
        """Cast to another type.

        Returns:
            _Cast_KeyedJointDesign
        """
        return _Cast_KeyedJointDesign(self)
