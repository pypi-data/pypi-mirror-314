"""GenericMatrix"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_GENERIC_MATRIX = python_net_import("SMT.MastaAPI.MathUtility", "GenericMatrix")

if TYPE_CHECKING:
    from typing import Any, List, Type

    from mastapy._private.math_utility import (
        _1544,
        _1546,
        _1547,
        _1548,
        _1559,
        _1574,
        _1575,
        _1576,
        _1581,
        _1586,
    )

    Self = TypeVar("Self", bound="GenericMatrix")
    CastSelf = TypeVar("CastSelf", bound="GenericMatrix._Cast_GenericMatrix")

TElement = TypeVar("TElement", bound="object")
TMatrix = TypeVar("TMatrix", bound="GenericMatrix")

__docformat__ = "restructuredtext en"
__all__ = ("GenericMatrix",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GenericMatrix:
    """Special nested class for casting GenericMatrix to subclasses."""

    __parent__: "GenericMatrix"

    @property
    def complex_matrix(self: "CastSelf") -> "_1544.ComplexMatrix":
        from mastapy._private.math_utility import _1544

        return self.__parent__._cast(_1544.ComplexMatrix)

    @property
    def complex_vector(self: "CastSelf") -> "_1546.ComplexVector":
        from mastapy._private.math_utility import _1546

        return self.__parent__._cast(_1546.ComplexVector)

    @property
    def complex_vector_3d(self: "CastSelf") -> "_1547.ComplexVector3D":
        from mastapy._private.math_utility import _1547

        return self.__parent__._cast(_1547.ComplexVector3D)

    @property
    def complex_vector_6d(self: "CastSelf") -> "_1548.ComplexVector6D":
        from mastapy._private.math_utility import _1548

        return self.__parent__._cast(_1548.ComplexVector6D)

    @property
    def euler_parameters(self: "CastSelf") -> "_1559.EulerParameters":
        from mastapy._private.math_utility import _1559

        return self.__parent__._cast(_1559.EulerParameters)

    @property
    def quaternion(self: "CastSelf") -> "_1574.Quaternion":
        from mastapy._private.math_utility import _1574

        return self.__parent__._cast(_1574.Quaternion)

    @property
    def real_matrix(self: "CastSelf") -> "_1575.RealMatrix":
        from mastapy._private.math_utility import _1575

        return self.__parent__._cast(_1575.RealMatrix)

    @property
    def real_vector(self: "CastSelf") -> "_1576.RealVector":
        from mastapy._private.math_utility import _1576

        return self.__parent__._cast(_1576.RealVector)

    @property
    def square_matrix(self: "CastSelf") -> "_1581.SquareMatrix":
        from mastapy._private.math_utility import _1581

        return self.__parent__._cast(_1581.SquareMatrix)

    @property
    def vector_6d(self: "CastSelf") -> "_1586.Vector6D":
        from mastapy._private.math_utility import _1586

        return self.__parent__._cast(_1586.Vector6D)

    @property
    def generic_matrix(self: "CastSelf") -> "GenericMatrix":
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
class GenericMatrix(_0.APIBase, Generic[TElement, TMatrix]):
    """GenericMatrix

    This is a mastapy class.

    Generic Types:
        TElement
        TMatrix
    """

    TYPE: ClassVar["Type"] = _GENERIC_MATRIX

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def number_of_columns(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfColumns")

        if temp is None:
            return 0

        return temp

    @property
    def number_of_entries(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfEntries")

        if temp is None:
            return 0

        return temp

    @property
    def number_of_rows(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfRows")

        if temp is None:
            return 0

        return temp

    @property
    def data(self: "Self") -> "List[TElement]":
        """List[TElement]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Data")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @enforce_parameter_types
    def get_column_at(self: "Self", index: "int") -> "List[TElement]":
        """List[TElement]

        Args:
            index (int)
        """
        index = int(index)
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(self.wrapped, "GetColumnAt", index if index else 0)
        )

    @enforce_parameter_types
    def get_row_at(self: "Self", row_index: "int") -> "List[TElement]":
        """List[TElement]

        Args:
            row_index (int)
        """
        row_index = int(row_index)
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(
                self.wrapped, "GetRowAt", row_index if row_index else 0
            )
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GenericMatrix":
        """Cast to another type.

        Returns:
            _Cast_GenericMatrix
        """
        return _Cast_GenericMatrix(self)
