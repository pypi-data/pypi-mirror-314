"""TransformMatrix3D"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.tuple_with_name import TupleWithName
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private._math.matrix_4x4 import Matrix4x4
from mastapy._private._math.vector_3d import Vector3D
from mastapy._private.math_utility import _1575

_TRANSFORM_MATRIX_3D = python_net_import(
    "SMT.MastaAPI.MathUtility", "TransformMatrix3D"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1564

    Self = TypeVar("Self", bound="TransformMatrix3D")
    CastSelf = TypeVar("CastSelf", bound="TransformMatrix3D._Cast_TransformMatrix3D")


__docformat__ = "restructuredtext en"
__all__ = ("TransformMatrix3D",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TransformMatrix3D:
    """Special nested class for casting TransformMatrix3D to subclasses."""

    __parent__: "TransformMatrix3D"

    @property
    def real_matrix(self: "CastSelf") -> "_1575.RealMatrix":
        return self.__parent__._cast(_1575.RealMatrix)

    @property
    def generic_matrix(self: "CastSelf") -> "_1564.GenericMatrix":
        from mastapy._private.math_utility import _1564

        return self.__parent__._cast(_1564.GenericMatrix)

    @property
    def transform_matrix_3d(self: "CastSelf") -> "TransformMatrix3D":
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
class TransformMatrix3D(_1575.RealMatrix):
    """TransformMatrix3D

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TRANSFORM_MATRIX_3D

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def is_identity(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsIdentity")

        if temp is None:
            return False

        return temp

    @property
    def translation(self: "Self") -> "Vector3D":
        """Vector3D"""
        temp = pythonnet_property_get(self.wrapped, "Translation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @translation.setter
    @enforce_parameter_types
    def translation(self: "Self", value: "Vector3D") -> None:
        value = conversion.mp_to_pn_vector3d(value)
        pythonnet_property_set(self.wrapped, "Translation", value)

    @property
    def x_axis(self: "Self") -> "Vector3D":
        """Vector3D"""
        temp = pythonnet_property_get(self.wrapped, "XAxis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @x_axis.setter
    @enforce_parameter_types
    def x_axis(self: "Self", value: "Vector3D") -> None:
        value = conversion.mp_to_pn_vector3d(value)
        pythonnet_property_set(self.wrapped, "XAxis", value)

    @property
    def y_axis(self: "Self") -> "Vector3D":
        """Vector3D"""
        temp = pythonnet_property_get(self.wrapped, "YAxis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @y_axis.setter
    @enforce_parameter_types
    def y_axis(self: "Self", value: "Vector3D") -> None:
        value = conversion.mp_to_pn_vector3d(value)
        pythonnet_property_set(self.wrapped, "YAxis", value)

    @property
    def z_axis(self: "Self") -> "Vector3D":
        """Vector3D"""
        temp = pythonnet_property_get(self.wrapped, "ZAxis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @z_axis.setter
    @enforce_parameter_types
    def z_axis(self: "Self", value: "Vector3D") -> None:
        value = conversion.mp_to_pn_vector3d(value)
        pythonnet_property_set(self.wrapped, "ZAxis", value)

    @enforce_parameter_types
    def has_rotation(self: "Self", tolerance: "float" = 0.0) -> "bool":
        """bool

        Args:
            tolerance (float, optional)
        """
        tolerance = float(tolerance)
        method_result = pythonnet_method_call(
            self.wrapped, "HasRotation", tolerance if tolerance else 0.0
        )
        return method_result

    @enforce_parameter_types
    def has_translation(self: "Self", tolerance: "float" = 0.0) -> "bool":
        """bool

        Args:
            tolerance (float, optional)
        """
        tolerance = float(tolerance)
        method_result = pythonnet_method_call(
            self.wrapped, "HasTranslation", tolerance if tolerance else 0.0
        )
        return method_result

    def negated(self: "Self") -> "Matrix4x4":
        """Matrix4x4"""
        return conversion.pn_to_mp_matrix4x4(
            pythonnet_method_call(self.wrapped, "Negated")
        )

    def rigid_inverse(self: "Self") -> "Matrix4x4":
        """Matrix4x4"""
        return conversion.pn_to_mp_matrix4x4(
            pythonnet_method_call(self.wrapped, "RigidInverse")
        )

    @enforce_parameter_types
    def rotate(self: "Self", angular: "Vector3D") -> "Vector3D":
        """Vector3D

        Args:
            angular (Vector3D)
        """
        angular = conversion.mp_to_pn_vector3d(angular)
        return conversion.pn_to_mp_vector3d(
            pythonnet_method_call(self.wrapped, "Rotate", angular)
        )

    @enforce_parameter_types
    def transform(self: "Self", linear: "Vector3D") -> "Vector3D":
        """Vector3D

        Args:
            linear (Vector3D)
        """
        linear = conversion.mp_to_pn_vector3d(linear)
        return conversion.pn_to_mp_vector3d(
            pythonnet_method_call(self.wrapped, "Transform", linear)
        )

    @enforce_parameter_types
    def transform_linear_and_angular_components(
        self: "Self", linear: "Vector3D", angular: "Vector3D"
    ) -> "TupleWithName":
        """TupleWithName

        Args:
            linear (Vector3D)
            angular (Vector3D)
        """
        linear = conversion.mp_to_pn_vector3d(linear)
        angular = conversion.mp_to_pn_vector3d(angular)
        return conversion.pn_to_mp_tuple_with_name(
            pythonnet_method_call(
                self.wrapped, "TransformLinearAndAngularComponents", linear, angular
            ),
            (conversion.pn_to_mp_vector3d, conversion.pn_to_mp_vector3d),
        )

    def transposed(self: "Self") -> "Matrix4x4":
        """Matrix4x4"""
        return conversion.pn_to_mp_matrix4x4(
            pythonnet_method_call(self.wrapped, "Transposed")
        )

    @property
    def cast_to(self: "Self") -> "_Cast_TransformMatrix3D":
        """Cast to another type.

        Returns:
            _Cast_TransformMatrix3D
        """
        return _Cast_TransformMatrix3D(self)
