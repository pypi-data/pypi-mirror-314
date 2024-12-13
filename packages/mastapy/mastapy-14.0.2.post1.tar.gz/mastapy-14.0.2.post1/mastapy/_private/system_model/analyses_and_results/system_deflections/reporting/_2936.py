"""MeshDeflectionResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_MESH_DEFLECTION_RESULTS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Reporting",
    "MeshDeflectionResults",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
        _2935,
    )

    Self = TypeVar("Self", bound="MeshDeflectionResults")
    CastSelf = TypeVar(
        "CastSelf", bound="MeshDeflectionResults._Cast_MeshDeflectionResults"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MeshDeflectionResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MeshDeflectionResults:
    """Special nested class for casting MeshDeflectionResults to subclasses."""

    __parent__: "MeshDeflectionResults"

    @property
    def mesh_deflection_results(self: "CastSelf") -> "MeshDeflectionResults":
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
class MeshDeflectionResults(_0.APIBase):
    """MeshDeflectionResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MESH_DEFLECTION_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def offset(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Offset")

        if temp is None:
            return 0.0

        return temp

    @property
    def total_microgeometry(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalMicrogeometry")

        if temp is None:
            return 0.0

        return temp

    @property
    def total_transverse_deflection(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalTransverseDeflection")

        if temp is None:
            return 0.0

        return temp

    @property
    def total_transverse_deflection_with_microgeometry(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalTransverseDeflectionWithMicrogeometry"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def gears(self: "Self") -> "List[_2935.GearInMeshDeflectionResults]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.reporting.GearInMeshDeflectionResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Gears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_MeshDeflectionResults":
        """Cast to another type.

        Returns:
            _Cast_MeshDeflectionResults
        """
        return _Cast_MeshDeflectionResults(self)
