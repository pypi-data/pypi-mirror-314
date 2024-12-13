"""GearMeshFELink"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.fe import _2443
from mastapy._private.system_model.fe.links import _2481

_GEAR_MESH_FE_LINK = python_net_import(
    "SMT.MastaAPI.SystemModel.FE.Links", "GearMeshFELink"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.fe.links import _2476, _2483

    Self = TypeVar("Self", bound="GearMeshFELink")
    CastSelf = TypeVar("CastSelf", bound="GearMeshFELink._Cast_GearMeshFELink")


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshFELink",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshFELink:
    """Special nested class for casting GearMeshFELink to subclasses."""

    __parent__: "GearMeshFELink"

    @property
    def multi_angle_connection_fe_link(
        self: "CastSelf",
    ) -> "_2481.MultiAngleConnectionFELink":
        return self.__parent__._cast(_2481.MultiAngleConnectionFELink)

    @property
    def multi_node_fe_link(self: "CastSelf") -> "_2483.MultiNodeFELink":
        from mastapy._private.system_model.fe.links import _2483

        return self.__parent__._cast(_2483.MultiNodeFELink)

    @property
    def fe_link(self: "CastSelf") -> "_2476.FELink":
        from mastapy._private.system_model.fe.links import _2476

        return self.__parent__._cast(_2476.FELink)

    @property
    def gear_mesh_fe_link(self: "CastSelf") -> "GearMeshFELink":
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
class GearMeshFELink(_2481.MultiAngleConnectionFELink):
    """GearMeshFELink

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_FE_LINK

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def reference_fe_substructure_node_for_misalignments(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_FESubstructureNode":
        """ListWithSelectedItem[mastapy.system_model.fe.FESubstructureNode]"""
        temp = pythonnet_property_get(
            self.wrapped, "ReferenceFESubstructureNodeForMisalignments"
        )

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_FESubstructureNode",
        )(temp)

    @reference_fe_substructure_node_for_misalignments.setter
    @enforce_parameter_types
    def reference_fe_substructure_node_for_misalignments(
        self: "Self", value: "_2443.FESubstructureNode"
    ) -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_FESubstructureNode.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_FESubstructureNode.implicit_type()
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(
            self.wrapped, "ReferenceFESubstructureNodeForMisalignments", value
        )

    @property
    def use_active_mesh_node_for_reference_fe_substructure_node_for_misalignments(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "UseActiveMeshNodeForReferenceFESubstructureNodeForMisalignments",
        )

        if temp is None:
            return False

        return temp

    @use_active_mesh_node_for_reference_fe_substructure_node_for_misalignments.setter
    @enforce_parameter_types
    def use_active_mesh_node_for_reference_fe_substructure_node_for_misalignments(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseActiveMeshNodeForReferenceFESubstructureNodeForMisalignments",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshFELink":
        """Cast to another type.

        Returns:
            _Cast_GearMeshFELink
        """
        return _Cast_GearMeshFELink(self)
