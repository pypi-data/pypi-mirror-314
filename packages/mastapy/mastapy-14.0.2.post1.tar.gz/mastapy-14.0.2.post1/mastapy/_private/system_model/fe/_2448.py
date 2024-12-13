"""FESubstructureWithSelection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.system_model.fe import _2417

_FE_SUBSTRUCTURE_WITH_SELECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "FESubstructureWithSelection"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.fe import (
        _2433,
        _2441,
        _2449,
        _2450,
        _2451,
        _2452,
        _2459,
    )

    Self = TypeVar("Self", bound="FESubstructureWithSelection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FESubstructureWithSelection._Cast_FESubstructureWithSelection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FESubstructureWithSelection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FESubstructureWithSelection:
    """Special nested class for casting FESubstructureWithSelection to subclasses."""

    __parent__: "FESubstructureWithSelection"

    @property
    def base_fe_with_selection(self: "CastSelf") -> "_2417.BaseFEWithSelection":
        return self.__parent__._cast(_2417.BaseFEWithSelection)

    @property
    def fe_substructure_with_selection_components(
        self: "CastSelf",
    ) -> "_2449.FESubstructureWithSelectionComponents":
        from mastapy._private.system_model.fe import _2449

        return self.__parent__._cast(_2449.FESubstructureWithSelectionComponents)

    @property
    def fe_substructure_with_selection_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "_2450.FESubstructureWithSelectionForHarmonicAnalysis":
        from mastapy._private.system_model.fe import _2450

        return self.__parent__._cast(
            _2450.FESubstructureWithSelectionForHarmonicAnalysis
        )

    @property
    def fe_substructure_with_selection_for_modal_analysis(
        self: "CastSelf",
    ) -> "_2451.FESubstructureWithSelectionForModalAnalysis":
        from mastapy._private.system_model.fe import _2451

        return self.__parent__._cast(_2451.FESubstructureWithSelectionForModalAnalysis)

    @property
    def fe_substructure_with_selection_for_static_analysis(
        self: "CastSelf",
    ) -> "_2452.FESubstructureWithSelectionForStaticAnalysis":
        from mastapy._private.system_model.fe import _2452

        return self.__parent__._cast(_2452.FESubstructureWithSelectionForStaticAnalysis)

    @property
    def fe_substructure_with_selection(
        self: "CastSelf",
    ) -> "FESubstructureWithSelection":
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
class FESubstructureWithSelection(_2417.BaseFEWithSelection):
    """FESubstructureWithSelection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_SUBSTRUCTURE_WITH_SELECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def selected_nodes(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SelectedNodes")

        if temp is None:
            return ""

        return temp

    @property
    def fe_substructure(self: "Self") -> "_2441.FESubstructure":
        """mastapy.system_model.fe.FESubstructure

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FESubstructure")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def element_face_groups(
        self: "Self",
    ) -> "List[_2433.ElementFaceGroupWithSelection]":
        """List[mastapy.system_model.fe.ElementFaceGroupWithSelection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementFaceGroups")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def node_groups(self: "Self") -> "List[_2459.NodeGroupWithSelection]":
        """List[mastapy.system_model.fe.NodeGroupWithSelection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NodeGroups")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    def create_condensation_node_connected_to_current_selection(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "CreateCondensationNodeConnectedToCurrentSelection"
        )

    def create_element_face_group(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CreateElementFaceGroup")

    def create_node_group(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CreateNodeGroup")

    def ground_selected_faces(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "GroundSelectedFaces")

    def remove_grounding_on_selected_faces(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "RemoveGroundingOnSelectedFaces")

    @property
    def cast_to(self: "Self") -> "_Cast_FESubstructureWithSelection":
        """Cast to another type.

        Returns:
            _Cast_FESubstructureWithSelection
        """
        return _Cast_FESubstructureWithSelection(self)
