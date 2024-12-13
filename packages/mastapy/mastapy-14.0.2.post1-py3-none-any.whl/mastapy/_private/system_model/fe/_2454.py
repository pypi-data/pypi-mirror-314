"""IndependentMASTACreatedCondensationNode"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private._math.vector_3d import Vector3D

_INDEPENDENT_MASTA_CREATED_CONDENSATION_NODE = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "IndependentMASTACreatedCondensationNode"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.dev_tools_analyses import _215
    from mastapy._private.system_model.fe import _2443

    Self = TypeVar("Self", bound="IndependentMASTACreatedCondensationNode")
    CastSelf = TypeVar(
        "CastSelf",
        bound="IndependentMASTACreatedCondensationNode._Cast_IndependentMASTACreatedCondensationNode",
    )


__docformat__ = "restructuredtext en"
__all__ = ("IndependentMASTACreatedCondensationNode",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_IndependentMASTACreatedCondensationNode:
    """Special nested class for casting IndependentMASTACreatedCondensationNode to subclasses."""

    __parent__: "IndependentMASTACreatedCondensationNode"

    @property
    def independent_masta_created_condensation_node(
        self: "CastSelf",
    ) -> "IndependentMASTACreatedCondensationNode":
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
class IndependentMASTACreatedCondensationNode(_0.APIBase):
    """IndependentMASTACreatedCondensationNode

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INDEPENDENT_MASTA_CREATED_CONDENSATION_NODE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def rigid_coupling_type(self: "Self") -> "_215.RigidCouplingType":
        """mastapy.nodal_analysis.dev_tools_analyses.RigidCouplingType"""
        temp = pythonnet_property_get(self.wrapped, "RigidCouplingType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.RigidCouplingType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis.dev_tools_analyses._215",
            "RigidCouplingType",
        )(value)

    @rigid_coupling_type.setter
    @enforce_parameter_types
    def rigid_coupling_type(self: "Self", value: "_215.RigidCouplingType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.RigidCouplingType"
        )
        pythonnet_property_set(self.wrapped, "RigidCouplingType", value)

    @property
    def fe_substructure_node(self: "Self") -> "_2443.FESubstructureNode":
        """mastapy.system_model.fe.FESubstructureNode

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FESubstructureNode")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def node_position(self: "Self") -> "Vector3D":
        """Vector3D"""
        temp = pythonnet_property_get(self.wrapped, "NodePosition")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @node_position.setter
    @enforce_parameter_types
    def node_position(self: "Self", value: "Vector3D") -> None:
        value = conversion.mp_to_pn_vector3d(value)
        pythonnet_property_set(self.wrapped, "NodePosition", value)

    def delete(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Delete")

    @property
    def cast_to(self: "Self") -> "_Cast_IndependentMASTACreatedCondensationNode":
        """Cast to another type.

        Returns:
            _Cast_IndependentMASTACreatedCondensationNode
        """
        return _Cast_IndependentMASTACreatedCondensationNode(self)
