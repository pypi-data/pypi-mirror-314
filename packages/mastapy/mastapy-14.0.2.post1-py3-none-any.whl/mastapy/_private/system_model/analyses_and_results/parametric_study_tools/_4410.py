"""AbstractShaftOrHousingParametricStudyTool"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
    _4434,
)

_ABSTRACT_SHAFT_OR_HOUSING_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "AbstractShaftOrHousingParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740, _2742, _2746
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7719
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4411,
        _4454,
        _4472,
        _4508,
        _4525,
    )
    from mastapy._private.system_model.part_model import _2494

    Self = TypeVar("Self", bound="AbstractShaftOrHousingParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftOrHousingParametricStudyTool._Cast_AbstractShaftOrHousingParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftOrHousingParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftOrHousingParametricStudyTool:
    """Special nested class for casting AbstractShaftOrHousingParametricStudyTool to subclasses."""

    __parent__: "AbstractShaftOrHousingParametricStudyTool"

    @property
    def component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4434.ComponentParametricStudyTool":
        return self.__parent__._cast(_4434.ComponentParametricStudyTool)

    @property
    def part_parametric_study_tool(self: "CastSelf") -> "_4508.PartParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4508,
        )

        return self.__parent__._cast(_4508.PartParametricStudyTool)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7719.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7719,
        )

        return self.__parent__._cast(_7719.PartAnalysisCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2746.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2746

        return self.__parent__._cast(_2746.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2742.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2742

        return self.__parent__._cast(_2742.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2740.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2740

        return self.__parent__._cast(_2740.DesignEntityAnalysis)

    @property
    def abstract_shaft_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4411.AbstractShaftParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4411,
        )

        return self.__parent__._cast(_4411.AbstractShaftParametricStudyTool)

    @property
    def cycloidal_disc_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4454.CycloidalDiscParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4454,
        )

        return self.__parent__._cast(_4454.CycloidalDiscParametricStudyTool)

    @property
    def fe_part_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4472.FEPartParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4472,
        )

        return self.__parent__._cast(_4472.FEPartParametricStudyTool)

    @property
    def shaft_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4525.ShaftParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4525,
        )

        return self.__parent__._cast(_4525.ShaftParametricStudyTool)

    @property
    def abstract_shaft_or_housing_parametric_study_tool(
        self: "CastSelf",
    ) -> "AbstractShaftOrHousingParametricStudyTool":
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
class AbstractShaftOrHousingParametricStudyTool(_4434.ComponentParametricStudyTool):
    """AbstractShaftOrHousingParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_SHAFT_OR_HOUSING_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2494.AbstractShaftOrHousing":
        """mastapy.system_model.part_model.AbstractShaftOrHousing

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractShaftOrHousingParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftOrHousingParametricStudyTool
        """
        return _Cast_AbstractShaftOrHousingParametricStudyTool(self)
