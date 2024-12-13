"""WindTurbineCertificationReport"""

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
from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
    _6412,
)
from mastapy._private.system_model.analyses_and_results.load_case_groups import _5800
from mastapy._private.system_model.analyses_and_results.static_loads import _6957

_WIND_TURBINE_CERTIFICATION_REPORT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.FlexiblePinAnalyses",
    "WindTurbineCertificationReport",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2891,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _3039,
    )
    from mastapy._private.system_model.part_model import _2535

    Self = TypeVar("Self", bound="WindTurbineCertificationReport")
    CastSelf = TypeVar(
        "CastSelf",
        bound="WindTurbineCertificationReport._Cast_WindTurbineCertificationReport",
    )


__docformat__ = "restructuredtext en"
__all__ = ("WindTurbineCertificationReport",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WindTurbineCertificationReport:
    """Special nested class for casting WindTurbineCertificationReport to subclasses."""

    __parent__: "WindTurbineCertificationReport"

    @property
    def combination_analysis(self: "CastSelf") -> "_6412.CombinationAnalysis":
        return self.__parent__._cast(_6412.CombinationAnalysis)

    @property
    def wind_turbine_certification_report(
        self: "CastSelf",
    ) -> "WindTurbineCertificationReport":
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
class WindTurbineCertificationReport(_6412.CombinationAnalysis):
    """WindTurbineCertificationReport

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WIND_TURBINE_CERTIFICATION_REPORT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def extreme_load_case(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_StaticLoadCase":
        """ListWithSelectedItem[mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase]"""
        temp = pythonnet_property_get(self.wrapped, "ExtremeLoadCase")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_StaticLoadCase",
        )(temp)

    @extreme_load_case.setter
    @enforce_parameter_types
    def extreme_load_case(self: "Self", value: "_6957.StaticLoadCase") -> None:
        wrapper_type = (
            list_with_selected_item.ListWithSelectedItem_StaticLoadCase.wrapper_type()
        )
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "ExtremeLoadCase", value)

    @property
    def ldd(self: "Self") -> "list_with_selected_item.ListWithSelectedItem_DutyCycle":
        """ListWithSelectedItem[mastapy.system_model.analyses_and_results.load_case_groups.DutyCycle]"""
        temp = pythonnet_property_get(self.wrapped, "LDD")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_DutyCycle",
        )(temp)

    @ldd.setter
    @enforce_parameter_types
    def ldd(self: "Self", value: "_5800.DutyCycle") -> None:
        wrapper_type = (
            list_with_selected_item.ListWithSelectedItem_DutyCycle.wrapper_type()
        )
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_DutyCycle.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "LDD", value)

    @property
    def nominal_load_case(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_StaticLoadCase":
        """ListWithSelectedItem[mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase]"""
        temp = pythonnet_property_get(self.wrapped, "NominalLoadCase")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_StaticLoadCase",
        )(temp)

    @nominal_load_case.setter
    @enforce_parameter_types
    def nominal_load_case(self: "Self", value: "_6957.StaticLoadCase") -> None:
        wrapper_type = (
            list_with_selected_item.ListWithSelectedItem_StaticLoadCase.wrapper_type()
        )
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "NominalLoadCase", value)

    @property
    def design(self: "Self") -> "_2535.RootAssembly":
        """mastapy.system_model.part_model.RootAssembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Design")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def extreme_load_case_static_analysis(
        self: "Self",
    ) -> "_2891.RootAssemblySystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.RootAssemblySystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExtremeLoadCaseStaticAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def ldd_static_analysis(
        self: "Self",
    ) -> "_3039.RootAssemblyCompoundSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.compound.RootAssemblyCompoundSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LDDStaticAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def nominal_load_case_static_analysis(
        self: "Self",
    ) -> "_2891.RootAssemblySystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.RootAssemblySystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalLoadCaseStaticAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_WindTurbineCertificationReport":
        """Cast to another type.

        Returns:
            _Cast_WindTurbineCertificationReport
        """
        return _Cast_WindTurbineCertificationReport(self)
