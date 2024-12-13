"""FESubstructureWithSelectionForModalAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import list_with_selected_item, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.fe import _2448

_FE_SUBSTRUCTURE_WITH_SELECTION_FOR_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "FESubstructureWithSelectionForModalAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.nodal_analysis import _64
    from mastapy._private.nodal_analysis.dev_tools_analyses import _191, _201
    from mastapy._private.system_model.fe import _2417, _2445

    Self = TypeVar("Self", bound="FESubstructureWithSelectionForModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FESubstructureWithSelectionForModalAnalysis._Cast_FESubstructureWithSelectionForModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FESubstructureWithSelectionForModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FESubstructureWithSelectionForModalAnalysis:
    """Special nested class for casting FESubstructureWithSelectionForModalAnalysis to subclasses."""

    __parent__: "FESubstructureWithSelectionForModalAnalysis"

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
    def fe_substructure_with_selection_for_modal_analysis(
        self: "CastSelf",
    ) -> "FESubstructureWithSelectionForModalAnalysis":
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
class FESubstructureWithSelectionForModalAnalysis(_2448.FESubstructureWithSelection):
    """FESubstructureWithSelectionForModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_SUBSTRUCTURE_WITH_SELECTION_FOR_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def invert_y_axis_of_mac_chart(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "InvertYAxisOfMACChart")

        if temp is None:
            return False

        return temp

    @invert_y_axis_of_mac_chart.setter
    @enforce_parameter_types
    def invert_y_axis_of_mac_chart(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InvertYAxisOfMACChart",
            bool(value) if value is not None else False,
        )

    @property
    def max_displacement_scaling(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MaxDisplacementScaling")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @max_displacement_scaling.setter
    @enforce_parameter_types
    def max_displacement_scaling(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaxDisplacementScaling", value)

    @property
    def mode_to_draw(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_int":
        """ListWithSelectedItem[int]"""
        temp = pythonnet_property_get(self.wrapped, "ModeToDraw")

        if temp is None:
            return 0

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_int",
        )(temp)

    @mode_to_draw.setter
    @enforce_parameter_types
    def mode_to_draw(self: "Self", value: "int") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_int.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_int.implicit_type()
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0
        )
        pythonnet_property_set(self.wrapped, "ModeToDraw", value)

    @property
    def show_full_fe_mode_shapes(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowFullFEModeShapes")

        if temp is None:
            return False

        return temp

    @show_full_fe_mode_shapes.setter
    @enforce_parameter_types
    def show_full_fe_mode_shapes(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowFullFEModeShapes",
            bool(value) if value is not None else False,
        )

    @property
    def eigenvalue_options(self: "Self") -> "_191.EigenvalueOptions":
        """mastapy.nodal_analysis.dev_tools_analyses.EigenvalueOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EigenvalueOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def modal_draw_style(self: "Self") -> "_201.FEModelModalAnalysisDrawStyle":
        """mastapy.nodal_analysis.dev_tools_analyses.FEModelModalAnalysisDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModalDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def fe_modal_frequencies(self: "Self") -> "List[_64.FEModalFrequencyComparison]":
        """List[mastapy.nodal_analysis.FEModalFrequencyComparison]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FEModalFrequencies")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def full_fe_mode_shapes_at_condensation_nodes(
        self: "Self",
    ) -> "List[_2445.FESubstructureNodeModeShapes]":
        """List[mastapy.system_model.fe.FESubstructureNodeModeShapes]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FullFEModeShapesAtCondensationNodes"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    def calculate_full_fe_modes(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CalculateFullFEModes")

    @property
    def cast_to(self: "Self") -> "_Cast_FESubstructureWithSelectionForModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_FESubstructureWithSelectionForModalAnalysis
        """
        return _Cast_FESubstructureWithSelectionForModalAnalysis(self)
