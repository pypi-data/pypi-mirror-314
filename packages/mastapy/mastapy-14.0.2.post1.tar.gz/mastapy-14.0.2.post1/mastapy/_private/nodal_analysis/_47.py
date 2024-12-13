"""AbstractNodalMatrix"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import

_ABSTRACT_NODAL_MATRIX = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "AbstractNodalMatrix"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis import _79, _89

    Self = TypeVar("Self", bound="AbstractNodalMatrix")
    CastSelf = TypeVar(
        "CastSelf", bound="AbstractNodalMatrix._Cast_AbstractNodalMatrix"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractNodalMatrix",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractNodalMatrix:
    """Special nested class for casting AbstractNodalMatrix to subclasses."""

    __parent__: "AbstractNodalMatrix"

    @property
    def nodal_matrix(self: "CastSelf") -> "_79.NodalMatrix":
        from mastapy._private.nodal_analysis import _79

        return self.__parent__._cast(_79.NodalMatrix)

    @property
    def sparse_nodal_matrix(self: "CastSelf") -> "_89.SparseNodalMatrix":
        from mastapy._private.nodal_analysis import _89

        return self.__parent__._cast(_89.SparseNodalMatrix)

    @property
    def abstract_nodal_matrix(self: "CastSelf") -> "AbstractNodalMatrix":
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
class AbstractNodalMatrix(_0.APIBase):
    """AbstractNodalMatrix

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_NODAL_MATRIX

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractNodalMatrix":
        """Cast to another type.

        Returns:
            _Cast_AbstractNodalMatrix
        """
        return _Cast_AbstractNodalMatrix(self)
