"""FrequencyResponseAnalysisOptions"""

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
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7710
from mastapy._private.system_model.analyses_and_results.static_loads import _6956

_FREQUENCY_RESPONSE_ANALYSIS_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "FrequencyResponseAnalysisOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FrequencyResponseAnalysisOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FrequencyResponseAnalysisOptions._Cast_FrequencyResponseAnalysisOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FrequencyResponseAnalysisOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FrequencyResponseAnalysisOptions:
    """Special nested class for casting FrequencyResponseAnalysisOptions to subclasses."""

    __parent__: "FrequencyResponseAnalysisOptions"

    @property
    def abstract_analysis_options(self: "CastSelf") -> "_7710.AbstractAnalysisOptions":
        return self.__parent__._cast(_7710.AbstractAnalysisOptions)

    @property
    def frequency_response_analysis_options(
        self: "CastSelf",
    ) -> "FrequencyResponseAnalysisOptions":
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
class FrequencyResponseAnalysisOptions(_7710.AbstractAnalysisOptions[_6956.LoadCase]):
    """FrequencyResponseAnalysisOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FREQUENCY_RESPONSE_ANALYSIS_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def number_of_bearing_harmonics(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfBearingHarmonics")

        if temp is None:
            return 0

        return temp

    @number_of_bearing_harmonics.setter
    @enforce_parameter_types
    def number_of_bearing_harmonics(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfBearingHarmonics",
            int(value) if value is not None else 0,
        )

    @property
    def number_of_gear_mesh_harmonics(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfGearMeshHarmonics")

        if temp is None:
            return 0

        return temp

    @number_of_gear_mesh_harmonics.setter
    @enforce_parameter_types
    def number_of_gear_mesh_harmonics(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfGearMeshHarmonics",
            int(value) if value is not None else 0,
        )

    @property
    def number_of_input_shaft_harmonics(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfInputShaftHarmonics")

        if temp is None:
            return 0

        return temp

    @number_of_input_shaft_harmonics.setter
    @enforce_parameter_types
    def number_of_input_shaft_harmonics(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfInputShaftHarmonics",
            int(value) if value is not None else 0,
        )

    @property
    def number_of_shaft_harmonics(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfShaftHarmonics")

        if temp is None:
            return 0

        return temp

    @number_of_shaft_harmonics.setter
    @enforce_parameter_types
    def number_of_shaft_harmonics(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfShaftHarmonics",
            int(value) if value is not None else 0,
        )

    @property
    def reference_power_load(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "ReferencePowerLoad")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @reference_power_load.setter
    @enforce_parameter_types
    def reference_power_load(self: "Self", value: "str") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else ""
        )
        pythonnet_property_set(self.wrapped, "ReferencePowerLoad", value)

    @property
    def threshold_for_significant_kinetic_energy(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ThresholdForSignificantKineticEnergy"
        )

        if temp is None:
            return 0.0

        return temp

    @threshold_for_significant_kinetic_energy.setter
    @enforce_parameter_types
    def threshold_for_significant_kinetic_energy(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ThresholdForSignificantKineticEnergy",
            float(value) if value is not None else 0.0,
        )

    @property
    def threshold_for_significant_strain_energy(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ThresholdForSignificantStrainEnergy"
        )

        if temp is None:
            return 0.0

        return temp

    @threshold_for_significant_strain_energy.setter
    @enforce_parameter_types
    def threshold_for_significant_strain_energy(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ThresholdForSignificantStrainEnergy",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_FrequencyResponseAnalysisOptions":
        """Cast to another type.

        Returns:
            _Cast_FrequencyResponseAnalysisOptions
        """
        return _Cast_FrequencyResponseAnalysisOptions(self)
