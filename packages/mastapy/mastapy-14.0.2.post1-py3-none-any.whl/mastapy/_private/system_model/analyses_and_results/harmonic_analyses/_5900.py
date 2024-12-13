"""HarmonicAnalysisFEExportOptions"""

from __future__ import annotations

from enum import Enum
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
from mastapy._private.nodal_analysis.component_mode_synthesis import _237
from mastapy._private.nodal_analysis.fe_export_utility import _174
from mastapy._private.system_model.analyses_and_results import _2743
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _5899
from mastapy._private.system_model.part_model import _2511
from mastapy._private.utility.units_and_measurements import _1662

_HARMONIC_ANALYSIS_FE_EXPORT_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "HarmonicAnalysisFEExportOptions",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.nodal_analysis.dev_tools_analyses import _191
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5888,
        _5949,
    )

    Self = TypeVar("Self", bound="HarmonicAnalysisFEExportOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HarmonicAnalysisFEExportOptions._Cast_HarmonicAnalysisFEExportOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicAnalysisFEExportOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicAnalysisFEExportOptions:
    """Special nested class for casting HarmonicAnalysisFEExportOptions to subclasses."""

    __parent__: "HarmonicAnalysisFEExportOptions"

    @property
    def harmonic_analysis_export_options(
        self: "CastSelf",
    ) -> "_5899.HarmonicAnalysisExportOptions":
        return self.__parent__._cast(_5899.HarmonicAnalysisExportOptions)

    @property
    def harmonic_analysis_fe_export_options(
        self: "CastSelf",
    ) -> "HarmonicAnalysisFEExportOptions":
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
class HarmonicAnalysisFEExportOptions(
    _5899.HarmonicAnalysisExportOptions[
        _2743.IHaveFEPartHarmonicAnalysisResults, _2511.FEPart
    ]
):
    """HarmonicAnalysisFEExportOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HARMONIC_ANALYSIS_FE_EXPORT_OPTIONS

    class ComplexNumberOutput(Enum):
        """ComplexNumberOutput is a nested enum."""

        @classmethod
        def type_(cls) -> "Type":
            return _HARMONIC_ANALYSIS_FE_EXPORT_OPTIONS.ComplexNumberOutput

        REAL_AND_IMAGINARY = 0
        MAGNITUDE_AND_PHASE = 1
        MAGNITUDE_ONLY = 2

    def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
        raise AttributeError("Cannot set the attributes of an Enum.") from None

    def __enum_delattr(self: "Self", attr: str) -> None:
        raise AttributeError("Cannot delete the attributes of an Enum.") from None

    ComplexNumberOutput.__setattr__ = __enum_setattr
    ComplexNumberOutput.__delattr__ = __enum_delattr

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def combine_excitations_from_different_parts(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "CombineExcitationsFromDifferentParts"
        )

        if temp is None:
            return False

        return temp

    @combine_excitations_from_different_parts.setter
    @enforce_parameter_types
    def combine_excitations_from_different_parts(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CombineExcitationsFromDifferentParts",
            bool(value) if value is not None else False,
        )

    @property
    def combine_excitations_of_same_order(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CombineExcitationsOfSameOrder")

        if temp is None:
            return False

        return temp

    @combine_excitations_of_same_order.setter
    @enforce_parameter_types
    def combine_excitations_of_same_order(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CombineExcitationsOfSameOrder",
            bool(value) if value is not None else False,
        )

    @property
    def complex_number_output_option(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ComplexNumberOutput":
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.harmonic_analyses.HarmonicAnalysisFEExportOptions.ComplexNumberOutput]"""
        temp = pythonnet_property_get(self.wrapped, "ComplexNumberOutputOption")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ComplexNumberOutput.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @complex_number_output_option.setter
    @enforce_parameter_types
    def complex_number_output_option(
        self: "Self", value: "HarmonicAnalysisFEExportOptions.ComplexNumberOutput"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ComplexNumberOutput.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ComplexNumberOutputOption", value)

    @property
    def distance_unit(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_Unit":
        """ListWithSelectedItem[mastapy.utility.units_and_measurements.Unit]"""
        temp = pythonnet_property_get(self.wrapped, "DistanceUnit")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Unit",
        )(temp)

    @distance_unit.setter
    @enforce_parameter_types
    def distance_unit(self: "Self", value: "_1662.Unit") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.wrapper_type()
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "DistanceUnit", value)

    @property
    def element_face_group_to_export(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_CMSElementFaceGroup":
        """ListWithSelectedItem[mastapy.nodal_analysis.component_mode_synthesis.CMSElementFaceGroup]"""
        temp = pythonnet_property_get(self.wrapped, "ElementFaceGroupToExport")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_CMSElementFaceGroup",
        )(temp)

    @element_face_group_to_export.setter
    @enforce_parameter_types
    def element_face_group_to_export(
        self: "Self", value: "_237.CMSElementFaceGroup"
    ) -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_CMSElementFaceGroup.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_CMSElementFaceGroup.implicit_type()
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "ElementFaceGroupToExport", value)

    @property
    def export_full_mesh(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ExportFullMesh")

        if temp is None:
            return False

        return temp

    @export_full_mesh.setter
    @enforce_parameter_types
    def export_full_mesh(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ExportFullMesh", bool(value) if value is not None else False
        )

    @property
    def export_results_for_element_face_group_only(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "ExportResultsForElementFaceGroupOnly"
        )

        if temp is None:
            return False

        return temp

    @export_results_for_element_face_group_only.setter
    @enforce_parameter_types
    def export_results_for_element_face_group_only(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ExportResultsForElementFaceGroupOnly",
            bool(value) if value is not None else False,
        )

    @property
    def fe_export_format(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_FEExportFormat":
        """EnumWithSelectedValue[mastapy.nodal_analysis.fe_export_utility.FEExportFormat]"""
        temp = pythonnet_property_get(self.wrapped, "FEExportFormat")

        if temp is None:
            return None

        value = (
            enum_with_selected_value.EnumWithSelectedValue_FEExportFormat.wrapped_type()
        )
        return enum_with_selected_value_runtime.create(temp, value)

    @fe_export_format.setter
    @enforce_parameter_types
    def fe_export_format(self: "Self", value: "_174.FEExportFormat") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FEExportFormat.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "FEExportFormat", value)

    @property
    def force_unit(self: "Self") -> "list_with_selected_item.ListWithSelectedItem_Unit":
        """ListWithSelectedItem[mastapy.utility.units_and_measurements.Unit]"""
        temp = pythonnet_property_get(self.wrapped, "ForceUnit")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Unit",
        )(temp)

    @force_unit.setter
    @enforce_parameter_types
    def force_unit(self: "Self", value: "_1662.Unit") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.wrapper_type()
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "ForceUnit", value)

    @property
    def include_all_fe_models(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeAllFEModels")

        if temp is None:
            return False

        return temp

    @include_all_fe_models.setter
    @enforce_parameter_types
    def include_all_fe_models(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeAllFEModels",
            bool(value) if value is not None else False,
        )

    @property
    def include_all_shafts(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeAllShafts")

        if temp is None:
            return False

        return temp

    @include_all_shafts.setter
    @enforce_parameter_types
    def include_all_shafts(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeAllShafts",
            bool(value) if value is not None else False,
        )

    @property
    def include_midside_nodes(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeMidsideNodes")

        if temp is None:
            return False

        return temp

    @include_midside_nodes.setter
    @enforce_parameter_types
    def include_midside_nodes(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeMidsideNodes",
            bool(value) if value is not None else False,
        )

    @property
    def include_original_fe_file(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeOriginalFEFile")

        if temp is None:
            return False

        return temp

    @include_original_fe_file.setter
    @enforce_parameter_types
    def include_original_fe_file(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeOriginalFEFile",
            bool(value) if value is not None else False,
        )

    @property
    def include_rigid_couplings_and_nodes_added_by_masta(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "IncludeRigidCouplingsAndNodesAddedByMASTA"
        )

        if temp is None:
            return False

        return temp

    @include_rigid_couplings_and_nodes_added_by_masta.setter
    @enforce_parameter_types
    def include_rigid_couplings_and_nodes_added_by_masta(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeRigidCouplingsAndNodesAddedByMASTA",
            bool(value) if value is not None else False,
        )

    @property
    def one_file_per_frequency(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "OneFilePerFrequency")

        if temp is None:
            return False

        return temp

    @one_file_per_frequency.setter
    @enforce_parameter_types
    def one_file_per_frequency(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OneFilePerFrequency",
            bool(value) if value is not None else False,
        )

    @property
    def reference_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ReferenceSpeed")

        if temp is None:
            return 0.0

        return temp

    @reference_speed.setter
    @enforce_parameter_types
    def reference_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ReferenceSpeed", float(value) if value is not None else 0.0
        )

    @property
    def status_message_for_export(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StatusMessageForExport")

        if temp is None:
            return ""

        return temp

    @property
    def use_single_speed(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseSingleSpeed")

        if temp is None:
            return False

        return temp

    @use_single_speed.setter
    @enforce_parameter_types
    def use_single_speed(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "UseSingleSpeed", bool(value) if value is not None else False
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
    def frequency_options(
        self: "Self",
    ) -> "_5888.FrequencyOptionsForHarmonicAnalysisResults":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.FrequencyOptionsForHarmonicAnalysisResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrequencyOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def reference_speed_options(
        self: "Self",
    ) -> "_5949.SpeedOptionsForHarmonicAnalysisResults":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.SpeedOptionsForHarmonicAnalysisResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceSpeedOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @enforce_parameter_types
    def export_to_folder(self: "Self", folder_path: "str") -> "List[str]":
        """List[str]

        Args:
            folder_path (str)
        """
        folder_path = str(folder_path)
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(
                self.wrapped, "ExportToFolder", folder_path if folder_path else ""
            ),
            str,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_HarmonicAnalysisFEExportOptions":
        """Cast to another type.

        Returns:
            _Cast_HarmonicAnalysisFEExportOptions
        """
        return _Cast_HarmonicAnalysisFEExportOptions(self)
