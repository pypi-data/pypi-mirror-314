"""FESubstructureWithSelectionComponents"""

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
from mastapy._private._math.vector_3d import Vector3D
from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
    _221,
    _222,
    _223,
    _224,
    _225,
    _226,
    _227,
    _228,
)
from mastapy._private.system_model.fe import _2448

_FE_SUBSTRUCTURE_WITH_SELECTION_COMPONENTS = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "FESubstructureWithSelectionComponents"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility import _1550
    from mastapy._private.system_model.fe import _2417, _2424, _2425, _2434, _2457
    from mastapy._private.system_model.fe.links import _2478

    Self = TypeVar("Self", bound="FESubstructureWithSelectionComponents")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FESubstructureWithSelectionComponents._Cast_FESubstructureWithSelectionComponents",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FESubstructureWithSelectionComponents",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FESubstructureWithSelectionComponents:
    """Special nested class for casting FESubstructureWithSelectionComponents to subclasses."""

    __parent__: "FESubstructureWithSelectionComponents"

    @property
    def fe_substructure_with_selection(
        self: "CastSelf",
    ) -> "_2448.FESubstructureWithSelection":
        return self.__parent__._cast(_2448.FESubstructureWithSelection)

    @property
    def base_fe_with_selection(self: "CastSelf") -> "_2417.BaseFEWithSelection":
        from mastapy._private.system_model.fe import _2417

        return self.__parent__._cast(_2417.BaseFEWithSelection)

    @property
    def fe_substructure_with_selection_components(
        self: "CastSelf",
    ) -> "FESubstructureWithSelectionComponents":
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
class FESubstructureWithSelectionComponents(_2448.FESubstructureWithSelection):
    """FESubstructureWithSelectionComponents

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_SUBSTRUCTURE_WITH_SELECTION_COMPONENTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def radius_of_circle_through_selected_nodes(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RadiusOfCircleThroughSelectedNodes"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def centre_of_circle_through_selected_nodes(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CentreOfCircleThroughSelectedNodes"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def distance_between_selected_nodes(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DistanceBetweenSelectedNodes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def manual_alignment(self: "Self") -> "_1550.CoordinateSystemEditor":
        """mastapy.math_utility.CoordinateSystemEditor

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ManualAlignment")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def midpoint_of_selected_nodes(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MidpointOfSelectedNodes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def beam_element_properties(
        self: "Self",
    ) -> "List[_2434.ElementPropertiesWithSelection[_222.ElementPropertiesBeam]]":
        """List[mastapy.system_model.fe.ElementPropertiesWithSelection[mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.ElementPropertiesBeam]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BeamElementProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_links(self: "Self") -> "List[_2478.FELinkWithSelection]":
        """List[mastapy.system_model.fe.links.FELinkWithSelection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLinks")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def contact_pairs(self: "Self") -> "List[_2424.ContactPairWithSelection]":
        """List[mastapy.system_model.fe.ContactPairWithSelection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactPairs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def coordinate_systems(self: "Self") -> "List[_2425.CoordinateSystemWithSelection]":
        """List[mastapy.system_model.fe.CoordinateSystemWithSelection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CoordinateSystems")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def interface_element_properties(
        self: "Self",
    ) -> "List[_2434.ElementPropertiesWithSelection[_223.ElementPropertiesInterface]]":
        """List[mastapy.system_model.fe.ElementPropertiesWithSelection[mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.ElementPropertiesInterface]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InterfaceElementProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def links_for_electric_machine(self: "Self") -> "List[_2478.FELinkWithSelection]":
        """List[mastapy.system_model.fe.links.FELinkWithSelection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinksForElectricMachine")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def links_for_selected_component(self: "Self") -> "List[_2478.FELinkWithSelection]":
        """List[mastapy.system_model.fe.links.FELinkWithSelection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinksForSelectedComponent")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def mass_element_properties(
        self: "Self",
    ) -> "List[_2434.ElementPropertiesWithSelection[_224.ElementPropertiesMass]]":
        """List[mastapy.system_model.fe.ElementPropertiesWithSelection[mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.ElementPropertiesMass]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MassElementProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def materials(self: "Self") -> "List[_2457.MaterialPropertiesWithSelection]":
        """List[mastapy.system_model.fe.MaterialPropertiesWithSelection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Materials")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def other_element_properties(
        self: "Self",
    ) -> "List[_2434.ElementPropertiesWithSelection[_221.ElementPropertiesBase]]":
        """List[mastapy.system_model.fe.ElementPropertiesWithSelection[mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.ElementPropertiesBase]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OtherElementProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def rigid_element_properties(
        self: "Self",
    ) -> "List[_2434.ElementPropertiesWithSelection[_225.ElementPropertiesRigid]]":
        """List[mastapy.system_model.fe.ElementPropertiesWithSelection[mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.ElementPropertiesRigid]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RigidElementProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def shell_element_properties(
        self: "Self",
    ) -> "List[_2434.ElementPropertiesWithSelection[_226.ElementPropertiesShell]]":
        """List[mastapy.system_model.fe.ElementPropertiesWithSelection[mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.ElementPropertiesShell]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShellElementProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def solid_element_properties(
        self: "Self",
    ) -> "List[_2434.ElementPropertiesWithSelection[_227.ElementPropertiesSolid]]":
        """List[mastapy.system_model.fe.ElementPropertiesWithSelection[mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.ElementPropertiesSolid]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SolidElementProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def spring_dashpot_element_properties(
        self: "Self",
    ) -> "List[_2434.ElementPropertiesWithSelection[_228.ElementPropertiesSpringDashpot]]":
        """List[mastapy.system_model.fe.ElementPropertiesWithSelection[mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.ElementPropertiesSpringDashpot]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpringDashpotElementProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    def auto_select_node_ring(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AutoSelectNodeRing")

    def replace_selected_shaft(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ReplaceSelectedShaft")

    def use_selected_component_for_alignment(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "UseSelectedComponentForAlignment")

    @property
    def cast_to(self: "Self") -> "_Cast_FESubstructureWithSelectionComponents":
        """Cast to another type.

        Returns:
            _Cast_FESubstructureWithSelectionComponents
        """
        return _Cast_FESubstructureWithSelectionComponents(self)
