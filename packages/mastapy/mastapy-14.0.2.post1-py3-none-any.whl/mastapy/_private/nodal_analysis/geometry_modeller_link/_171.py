"""MeshRequestResult"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.nodal_analysis.geometry_modeller_link import _164

_MESH_REQUEST_RESULT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.GeometryModellerLink", "MeshRequestResult"
)

if TYPE_CHECKING:
    from typing import Any, Dict, Type, TypeVar

    from mastapy._private.geometry.two_d import _323
    from mastapy._private.math_utility import _1561
    from mastapy._private.nodal_analysis.geometry_modeller_link import _163

    Self = TypeVar("Self", bound="MeshRequestResult")
    CastSelf = TypeVar("CastSelf", bound="MeshRequestResult._Cast_MeshRequestResult")


__docformat__ = "restructuredtext en"
__all__ = ("MeshRequestResult",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MeshRequestResult:
    """Special nested class for casting MeshRequestResult to subclasses."""

    __parent__: "MeshRequestResult"

    @property
    def mesh_request_result(self: "CastSelf") -> "MeshRequestResult":
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
class MeshRequestResult(_0.APIBase):
    """MeshRequestResult

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MESH_REQUEST_RESULT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def aborted(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "Aborted")

        if temp is None:
            return False

        return temp

    @aborted.setter
    @enforce_parameter_types
    def aborted(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "Aborted", bool(value) if value is not None else False
        )

    @property
    def body_moniker(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "BodyMoniker")

        if temp is None:
            return ""

        return temp

    @body_moniker.setter
    @enforce_parameter_types
    def body_moniker(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "BodyMoniker", str(value) if value is not None else ""
        )

    @property
    def cad_face_group(self: "Self") -> "_323.CADFaceGroup":
        """mastapy.geometry.two_d.CADFaceGroup"""
        temp = pythonnet_property_get(self.wrapped, "CADFaceGroup")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @cad_face_group.setter
    @enforce_parameter_types
    def cad_face_group(self: "Self", value: "_323.CADFaceGroup") -> None:
        pythonnet_property_set(self.wrapped, "CADFaceGroup", value.wrapped)

    @property
    def data_file_name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "DataFileName")

        if temp is None:
            return ""

        return temp

    @data_file_name.setter
    @enforce_parameter_types
    def data_file_name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "DataFileName", str(value) if value is not None else ""
        )

    @property
    def error_message(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "ErrorMessage")

        if temp is None:
            return ""

        return temp

    @error_message.setter
    @enforce_parameter_types
    def error_message(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "ErrorMessage", str(value) if value is not None else ""
        )

    @property
    def faceted_body(self: "Self") -> "_1561.FacetedBody":
        """mastapy.math_utility.FacetedBody"""
        temp = pythonnet_property_get(self.wrapped, "FacetedBody")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @faceted_body.setter
    @enforce_parameter_types
    def faceted_body(self: "Self", value: "_1561.FacetedBody") -> None:
        pythonnet_property_set(self.wrapped, "FacetedBody", value.wrapped)

    @property
    def geometry_modeller_design_information(
        self: "Self",
    ) -> "_163.GeometryModellerDesignInformation":
        """mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDesignInformation"""
        temp = pythonnet_property_get(self.wrapped, "GeometryModellerDesignInformation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @geometry_modeller_design_information.setter
    @enforce_parameter_types
    def geometry_modeller_design_information(
        self: "Self", value: "_163.GeometryModellerDesignInformation"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "GeometryModellerDesignInformation", value.wrapped
        )

    @enforce_parameter_types
    def set_geometry_modeller_dimensions(
        self: "Self", dimensions: "Dict[str, _164.GeometryModellerDimension]"
    ) -> None:
        """Method does not return.

        Args:
            dimensions (Dict[str, mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDimension])
        """
        pythonnet_method_call(self.wrapped, "SetGeometryModellerDimensions", dimensions)

    @property
    def cast_to(self: "Self") -> "_Cast_MeshRequestResult":
        """Cast to another type.

        Returns:
            _Cast_MeshRequestResult
        """
        return _Cast_MeshRequestResult(self)
