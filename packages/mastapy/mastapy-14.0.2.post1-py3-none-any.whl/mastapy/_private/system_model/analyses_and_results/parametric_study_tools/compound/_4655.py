"""ShaftCompoundParametricStudyTool"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
    _4559,
)

_SHAFT_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
    "ShaftCompoundParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.shafts import _19
    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4525,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
        _4560,
        _4583,
        _4639,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7105
    from mastapy._private.system_model.part_model.shaft_model import _2543

    Self = TypeVar("Self", bound="ShaftCompoundParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShaftCompoundParametricStudyTool._Cast_ShaftCompoundParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftCompoundParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftCompoundParametricStudyTool:
    """Special nested class for casting ShaftCompoundParametricStudyTool to subclasses."""

    __parent__: "ShaftCompoundParametricStudyTool"

    @property
    def abstract_shaft_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4559.AbstractShaftCompoundParametricStudyTool":
        return self.__parent__._cast(_4559.AbstractShaftCompoundParametricStudyTool)

    @property
    def abstract_shaft_or_housing_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4560.AbstractShaftOrHousingCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4560,
        )

        return self.__parent__._cast(
            _4560.AbstractShaftOrHousingCompoundParametricStudyTool
        )

    @property
    def component_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4583.ComponentCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4583,
        )

        return self.__parent__._cast(_4583.ComponentCompoundParametricStudyTool)

    @property
    def part_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4639.PartCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4639,
        )

        return self.__parent__._cast(_4639.PartCompoundParametricStudyTool)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7720.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7720,
        )

        return self.__parent__._cast(_7720.PartCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7717.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7717,
        )

        return self.__parent__._cast(_7717.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2740.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2740

        return self.__parent__._cast(_2740.DesignEntityAnalysis)

    @property
    def shaft_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "ShaftCompoundParametricStudyTool":
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
class ShaftCompoundParametricStudyTool(_4559.AbstractShaftCompoundParametricStudyTool):
    """ShaftCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_COMPOUND_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2543.Shaft":
        """mastapy.system_model.part_model.shaft_model.Shaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def properties_changing_all_load_cases(self: "Self") -> "_7105.ShaftLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PropertiesChangingAllLoadCases")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def shaft_duty_cycle_results(self: "Self") -> "_19.ShaftDamageResults":
        """mastapy.shafts.ShaftDamageResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftDutyCycleResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4525.ShaftParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.ShaftParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def planetaries(self: "Self") -> "List[ShaftCompoundParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ShaftCompoundParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planetaries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_4525.ShaftParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.ShaftParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftCompoundParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_ShaftCompoundParametricStudyTool
        """
        return _Cast_ShaftCompoundParametricStudyTool(self)
