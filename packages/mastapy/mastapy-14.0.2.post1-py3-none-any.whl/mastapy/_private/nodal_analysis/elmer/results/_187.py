"""Data"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_DATA = python_net_import("SMT.MastaAPI.NodalAnalysis.Elmer.Results", "Data")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.elmer.results import _188, _189

    Self = TypeVar("Self", bound="Data")
    CastSelf = TypeVar("CastSelf", bound="Data._Cast_Data")


__docformat__ = "restructuredtext en"
__all__ = ("Data",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Data:
    """Special nested class for casting Data to subclasses."""

    __parent__: "Data"

    @property
    def data_1d(self: "CastSelf") -> "_188.Data1D":
        from mastapy._private.nodal_analysis.elmer.results import _188

        return self.__parent__._cast(_188.Data1D)

    @property
    def data_3d(self: "CastSelf") -> "_189.Data3D":
        from mastapy._private.nodal_analysis.elmer.results import _189

        return self.__parent__._cast(_189.Data3D)

    @property
    def data(self: "CastSelf") -> "Data":
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
class Data(_0.APIBase):
    """Data

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DATA

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def quantity_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "QuantityName")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_Data":
        """Cast to another type.

        Returns:
            _Cast_Data
        """
        return _Cast_Data(self)
