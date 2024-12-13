"""BaseGeometryModellerDimension"""

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

_BASE_GEOMETRY_MODELLER_DIMENSION = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.GeometryModellerLink", "BaseGeometryModellerDimension"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.geometry_modeller_link import (
        _161,
        _162,
        _167,
        _169,
    )

    Self = TypeVar("Self", bound="BaseGeometryModellerDimension")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BaseGeometryModellerDimension._Cast_BaseGeometryModellerDimension",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BaseGeometryModellerDimension",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BaseGeometryModellerDimension:
    """Special nested class for casting BaseGeometryModellerDimension to subclasses."""

    __parent__: "BaseGeometryModellerDimension"

    @property
    def geometry_modeller_angle_dimension(
        self: "CastSelf",
    ) -> "_161.GeometryModellerAngleDimension":
        from mastapy._private.nodal_analysis.geometry_modeller_link import _161

        return self.__parent__._cast(_161.GeometryModellerAngleDimension)

    @property
    def geometry_modeller_count_dimension(
        self: "CastSelf",
    ) -> "_162.GeometryModellerCountDimension":
        from mastapy._private.nodal_analysis.geometry_modeller_link import _162

        return self.__parent__._cast(_162.GeometryModellerCountDimension)

    @property
    def geometry_modeller_length_dimension(
        self: "CastSelf",
    ) -> "_167.GeometryModellerLengthDimension":
        from mastapy._private.nodal_analysis.geometry_modeller_link import _167

        return self.__parent__._cast(_167.GeometryModellerLengthDimension)

    @property
    def geometry_modeller_unitless_dimension(
        self: "CastSelf",
    ) -> "_169.GeometryModellerUnitlessDimension":
        from mastapy._private.nodal_analysis.geometry_modeller_link import _169

        return self.__parent__._cast(_169.GeometryModellerUnitlessDimension)

    @property
    def base_geometry_modeller_dimension(
        self: "CastSelf",
    ) -> "BaseGeometryModellerDimension":
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
class BaseGeometryModellerDimension(_0.APIBase):
    """BaseGeometryModellerDimension

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BASE_GEOMETRY_MODELLER_DIMENSION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def cast_to(self: "Self") -> "_Cast_BaseGeometryModellerDimension":
        """Cast to another type.

        Returns:
            _Cast_BaseGeometryModellerDimension
        """
        return _Cast_BaseGeometryModellerDimension(self)
