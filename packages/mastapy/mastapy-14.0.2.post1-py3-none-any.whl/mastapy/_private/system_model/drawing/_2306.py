"""HarmonicAnalysisViewable"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import (
    enum_with_selected_value,
    list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.math_utility import _1579
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
    _5815,
    _5906,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses import _4744
from mastapy._private.system_model.analyses_and_results.system_deflections import _2848
from mastapy._private.system_model.drawing import _2305
from mastapy._private.system_model.drawing.options import _2319

_HARMONIC_ANALYSIS_VIEWABLE = python_net_import(
    "SMT.MastaAPI.SystemModel.Drawing", "HarmonicAnalysisViewable"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6474,
    )
    from mastapy._private.system_model.drawing import _2310

    Self = TypeVar("Self", bound="HarmonicAnalysisViewable")
    CastSelf = TypeVar(
        "CastSelf", bound="HarmonicAnalysisViewable._Cast_HarmonicAnalysisViewable"
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicAnalysisViewable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicAnalysisViewable:
    """Special nested class for casting HarmonicAnalysisViewable to subclasses."""

    __parent__: "HarmonicAnalysisViewable"

    @property
    def dynamic_analysis_viewable(self: "CastSelf") -> "_2305.DynamicAnalysisViewable":
        return self.__parent__._cast(_2305.DynamicAnalysisViewable)

    @property
    def part_analysis_case_with_contour_viewable(
        self: "CastSelf",
    ) -> "_2310.PartAnalysisCaseWithContourViewable":
        from mastapy._private.system_model.drawing import _2310

        return self.__parent__._cast(_2310.PartAnalysisCaseWithContourViewable)

    @property
    def harmonic_analysis_viewable(self: "CastSelf") -> "HarmonicAnalysisViewable":
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
class HarmonicAnalysisViewable(_2305.DynamicAnalysisViewable):
    """HarmonicAnalysisViewable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HARMONIC_ANALYSIS_VIEWABLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def animate_acoustic_result(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "AnimateAcousticResult")

        if temp is None:
            return False

        return temp

    @animate_acoustic_result.setter
    @enforce_parameter_types
    def animate_acoustic_result(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AnimateAcousticResult",
            bool(value) if value is not None else False,
        )

    @property
    def excitation(
        self: "Self",
    ) -> (
        "list_with_selected_item.ListWithSelectedItem_AbstractPeriodicExcitationDetail"
    ):
        """ListWithSelectedItem[mastapy.system_model.analyses_and_results.harmonic_analyses.AbstractPeriodicExcitationDetail]"""
        temp = pythonnet_property_get(self.wrapped, "Excitation")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_AbstractPeriodicExcitationDetail",
        )(temp)

    @excitation.setter
    @enforce_parameter_types
    def excitation(
        self: "Self", value: "_5815.AbstractPeriodicExcitationDetail"
    ) -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_AbstractPeriodicExcitationDetail.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_AbstractPeriodicExcitationDetail.implicit_type()
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "Excitation", value)

    @property
    def frequency(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_NamedTuple1_float":
        """ListWithSelectedItem[mastapy.utility.generics.NamedTuple1[float]]"""
        temp = pythonnet_property_get(self.wrapped, "Frequency")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_NamedTuple1_float",
        )(temp)

    @frequency.setter
    @enforce_parameter_types
    def frequency(self: "Self", value: "float") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_NamedTuple1_float.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_NamedTuple1_float.implicit_type()
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "Frequency", value)

    @property
    def harmonic(self: "Self") -> "list_with_selected_item.ListWithSelectedItem_int":
        """ListWithSelectedItem[int]"""
        temp = pythonnet_property_get(self.wrapped, "Harmonic")

        if temp is None:
            return 0

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_int",
        )(temp)

    @harmonic.setter
    @enforce_parameter_types
    def harmonic(self: "Self", value: "int") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_int.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_int.implicit_type()
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0
        )
        pythonnet_property_set(self.wrapped, "Harmonic", value)

    @property
    def harmonic_analysis_with_varying_stiffness_step(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_HarmonicAnalysisWithVaryingStiffnessStaticLoadCase":
        """ListWithSelectedItem[mastapy.system_model.analyses_and_results.harmonic_analyses.HarmonicAnalysisWithVaryingStiffnessStaticLoadCase]"""
        temp = pythonnet_property_get(
            self.wrapped, "HarmonicAnalysisWithVaryingStiffnessStep"
        )

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_HarmonicAnalysisWithVaryingStiffnessStaticLoadCase",
        )(temp)

    @harmonic_analysis_with_varying_stiffness_step.setter
    @enforce_parameter_types
    def harmonic_analysis_with_varying_stiffness_step(
        self: "Self", value: "_5906.HarmonicAnalysisWithVaryingStiffnessStaticLoadCase"
    ) -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_HarmonicAnalysisWithVaryingStiffnessStaticLoadCase.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_HarmonicAnalysisWithVaryingStiffnessStaticLoadCase.implicit_type()
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(
            self.wrapped, "HarmonicAnalysisWithVaryingStiffnessStep", value
        )

    @property
    def order(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_RoundedOrder":
        """ListWithSelectedItem[mastapy.math_utility.RoundedOrder]"""
        temp = pythonnet_property_get(self.wrapped, "Order")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_RoundedOrder",
        )(temp)

    @order.setter
    @enforce_parameter_types
    def order(self: "Self", value: "_1579.RoundedOrder") -> None:
        wrapper_type = (
            list_with_selected_item.ListWithSelectedItem_RoundedOrder.wrapper_type()
        )
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_RoundedOrder.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "Order", value)

    @property
    def reference_power_load_speed(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_NamedTuple1_float":
        """ListWithSelectedItem[mastapy.utility.generics.NamedTuple1[float]]"""
        temp = pythonnet_property_get(self.wrapped, "ReferencePowerLoadSpeed")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_NamedTuple1_float",
        )(temp)

    @reference_power_load_speed.setter
    @enforce_parameter_types
    def reference_power_load_speed(self: "Self", value: "float") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_NamedTuple1_float.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_NamedTuple1_float.implicit_type()
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "ReferencePowerLoadSpeed", value)

    @property
    def sound_response_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType":
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.modal_analyses.DynamicsResponseType]"""
        temp = pythonnet_property_get(self.wrapped, "SoundResponseType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @sound_response_type.setter
    @enforce_parameter_types
    def sound_response_type(self: "Self", value: "_4744.DynamicsResponseType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "SoundResponseType", value)

    @property
    def uncoupled_mesh(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_GearMeshSystemDeflection":
        """ListWithSelectedItem[mastapy.system_model.analyses_and_results.system_deflections.GearMeshSystemDeflection]"""
        temp = pythonnet_property_get(self.wrapped, "UncoupledMesh")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_GearMeshSystemDeflection",
        )(temp)

    @uncoupled_mesh.setter
    @enforce_parameter_types
    def uncoupled_mesh(self: "Self", value: "_2848.GearMeshSystemDeflection") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_GearMeshSystemDeflection.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_GearMeshSystemDeflection.implicit_type()
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "UncoupledMesh", value)

    @property
    def view_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ExcitationAnalysisViewOption":
        """EnumWithSelectedValue[mastapy.system_model.drawing.options.ExcitationAnalysisViewOption]"""
        temp = pythonnet_property_get(self.wrapped, "ViewType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ExcitationAnalysisViewOption.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @view_type.setter
    @enforce_parameter_types
    def view_type(self: "Self", value: "_2319.ExcitationAnalysisViewOption") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ExcitationAnalysisViewOption.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ViewType", value)

    @property
    def dynamic_analysis_draw_style(self: "Self") -> "_6474.DynamicAnalysisDrawStyle":
        """mastapy.system_model.analyses_and_results.dynamic_analyses.DynamicAnalysisDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicAnalysisDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    def calculate_result_for_selected_surfaces(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CalculateResultForSelectedSurfaces")

    @property
    def cast_to(self: "Self") -> "_Cast_HarmonicAnalysisViewable":
        """Cast to another type.

        Returns:
            _Cast_HarmonicAnalysisViewable
        """
        return _Cast_HarmonicAnalysisViewable(self)
