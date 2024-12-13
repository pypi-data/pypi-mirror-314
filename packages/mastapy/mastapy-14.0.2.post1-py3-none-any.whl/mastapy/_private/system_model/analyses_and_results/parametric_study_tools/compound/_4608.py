"""CylindricalPlanetGearCompoundParametricStudyTool"""

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
    _4605,
)

_CYLINDRICAL_PLANET_GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
    "CylindricalPlanetGearCompoundParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4459,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
        _4583,
        _4616,
        _4637,
        _4639,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7019

    Self = TypeVar("Self", bound="CylindricalPlanetGearCompoundParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalPlanetGearCompoundParametricStudyTool._Cast_CylindricalPlanetGearCompoundParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalPlanetGearCompoundParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalPlanetGearCompoundParametricStudyTool:
    """Special nested class for casting CylindricalPlanetGearCompoundParametricStudyTool to subclasses."""

    __parent__: "CylindricalPlanetGearCompoundParametricStudyTool"

    @property
    def cylindrical_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4605.CylindricalGearCompoundParametricStudyTool":
        return self.__parent__._cast(_4605.CylindricalGearCompoundParametricStudyTool)

    @property
    def gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4616.GearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4616,
        )

        return self.__parent__._cast(_4616.GearCompoundParametricStudyTool)

    @property
    def mountable_component_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4637.MountableComponentCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4637,
        )

        return self.__parent__._cast(
            _4637.MountableComponentCompoundParametricStudyTool
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
    def cylindrical_planet_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "CylindricalPlanetGearCompoundParametricStudyTool":
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
class CylindricalPlanetGearCompoundParametricStudyTool(
    _4605.CylindricalGearCompoundParametricStudyTool
):
    """CylindricalPlanetGearCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_PLANET_GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def properties_changing_all_load_cases(
        self: "Self",
    ) -> "_7019.CylindricalPlanetGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PropertiesChangingAllLoadCases")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4459.CylindricalPlanetGearParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalPlanetGearParametricStudyTool]

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
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_4459.CylindricalPlanetGearParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalPlanetGearParametricStudyTool]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_CylindricalPlanetGearCompoundParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_CylindricalPlanetGearCompoundParametricStudyTool
        """
        return _Cast_CylindricalPlanetGearCompoundParametricStudyTool(self)
