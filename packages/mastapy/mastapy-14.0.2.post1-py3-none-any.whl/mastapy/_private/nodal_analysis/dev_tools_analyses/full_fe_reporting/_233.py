"""RigidElementNodeDegreesOfFreedom"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_RIGID_ELEMENT_NODE_DEGREES_OF_FREEDOM = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting",
    "RigidElementNodeDegreesOfFreedom",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
        _218,
    )

    Self = TypeVar("Self", bound="RigidElementNodeDegreesOfFreedom")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RigidElementNodeDegreesOfFreedom._Cast_RigidElementNodeDegreesOfFreedom",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RigidElementNodeDegreesOfFreedom",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RigidElementNodeDegreesOfFreedom:
    """Special nested class for casting RigidElementNodeDegreesOfFreedom to subclasses."""

    __parent__: "RigidElementNodeDegreesOfFreedom"

    @property
    def rigid_element_node_degrees_of_freedom(
        self: "CastSelf",
    ) -> "RigidElementNodeDegreesOfFreedom":
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
class RigidElementNodeDegreesOfFreedom(_0.APIBase):
    """RigidElementNodeDegreesOfFreedom

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RIGID_ELEMENT_NODE_DEGREES_OF_FREEDOM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def index(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Index")

        if temp is None:
            return 0

        return temp

    @property
    def type_(self: "Self") -> "_218.DegreeOfFreedomType":
        """mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.DegreeOfFreedomType

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Type")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting.DegreeOfFreedomType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting._218",
            "DegreeOfFreedomType",
        )(value)

    @property
    def x(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "X")

        if temp is None:
            return False

        return temp

    @x.setter
    @enforce_parameter_types
    def x(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "X", bool(value) if value is not None else False
        )

    @property
    def y(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "Y")

        if temp is None:
            return False

        return temp

    @y.setter
    @enforce_parameter_types
    def y(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "Y", bool(value) if value is not None else False
        )

    @property
    def z(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "Z")

        if temp is None:
            return False

        return temp

    @z.setter
    @enforce_parameter_types
    def z(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "Z", bool(value) if value is not None else False
        )

    @property
    def theta_x(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ThetaX")

        if temp is None:
            return False

        return temp

    @theta_x.setter
    @enforce_parameter_types
    def theta_x(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ThetaX", bool(value) if value is not None else False
        )

    @property
    def theta_y(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ThetaY")

        if temp is None:
            return False

        return temp

    @theta_y.setter
    @enforce_parameter_types
    def theta_y(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ThetaY", bool(value) if value is not None else False
        )

    @property
    def theta_z(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ThetaZ")

        if temp is None:
            return False

        return temp

    @theta_z.setter
    @enforce_parameter_types
    def theta_z(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ThetaZ", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_RigidElementNodeDegreesOfFreedom":
        """Cast to another type.

        Returns:
            _Cast_RigidElementNodeDegreesOfFreedom
        """
        return _Cast_RigidElementNodeDegreesOfFreedom(self)
