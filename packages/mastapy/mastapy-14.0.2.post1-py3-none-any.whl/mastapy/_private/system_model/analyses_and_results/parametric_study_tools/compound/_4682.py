"""VirtualComponentCompoundParametricStudyTool"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
    _4637,
)

_VIRTUAL_COMPONENT_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
    "VirtualComponentCompoundParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4551,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
        _4583,
        _4633,
        _4634,
        _4639,
        _4646,
        _4647,
        _4681,
    )

    Self = TypeVar("Self", bound="VirtualComponentCompoundParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="VirtualComponentCompoundParametricStudyTool._Cast_VirtualComponentCompoundParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VirtualComponentCompoundParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualComponentCompoundParametricStudyTool:
    """Special nested class for casting VirtualComponentCompoundParametricStudyTool to subclasses."""

    __parent__: "VirtualComponentCompoundParametricStudyTool"

    @property
    def mountable_component_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4637.MountableComponentCompoundParametricStudyTool":
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
    def mass_disc_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4633.MassDiscCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4633,
        )

        return self.__parent__._cast(_4633.MassDiscCompoundParametricStudyTool)

    @property
    def measurement_component_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4634.MeasurementComponentCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4634,
        )

        return self.__parent__._cast(
            _4634.MeasurementComponentCompoundParametricStudyTool
        )

    @property
    def point_load_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4646.PointLoadCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4646,
        )

        return self.__parent__._cast(_4646.PointLoadCompoundParametricStudyTool)

    @property
    def power_load_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4647.PowerLoadCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4647,
        )

        return self.__parent__._cast(_4647.PowerLoadCompoundParametricStudyTool)

    @property
    def unbalanced_mass_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4681.UnbalancedMassCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4681,
        )

        return self.__parent__._cast(_4681.UnbalancedMassCompoundParametricStudyTool)

    @property
    def virtual_component_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "VirtualComponentCompoundParametricStudyTool":
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
class VirtualComponentCompoundParametricStudyTool(
    _4637.MountableComponentCompoundParametricStudyTool
):
    """VirtualComponentCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VIRTUAL_COMPONENT_COMPOUND_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_4551.VirtualComponentParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.VirtualComponentParametricStudyTool]

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
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4551.VirtualComponentParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.VirtualComponentParametricStudyTool]

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
    def cast_to(self: "Self") -> "_Cast_VirtualComponentCompoundParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_VirtualComponentCompoundParametricStudyTool
        """
        return _Cast_VirtualComponentCompoundParametricStudyTool(self)
