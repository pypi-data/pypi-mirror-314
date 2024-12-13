"""CycloidalDiscCentralBearingConnectionParametricStudyTool"""

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
    _4433,
)

_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "CycloidalDiscCentralBearingConnectionParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2742
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7712
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4412,
        _4444,
        _4526,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import _2392

    Self = TypeVar(
        "Self", bound="CycloidalDiscCentralBearingConnectionParametricStudyTool"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="CycloidalDiscCentralBearingConnectionParametricStudyTool._Cast_CycloidalDiscCentralBearingConnectionParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalDiscCentralBearingConnectionParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDiscCentralBearingConnectionParametricStudyTool:
    """Special nested class for casting CycloidalDiscCentralBearingConnectionParametricStudyTool to subclasses."""

    __parent__: "CycloidalDiscCentralBearingConnectionParametricStudyTool"

    @property
    def coaxial_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4433.CoaxialConnectionParametricStudyTool":
        return self.__parent__._cast(_4433.CoaxialConnectionParametricStudyTool)

    @property
    def shaft_to_mountable_component_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4526.ShaftToMountableComponentConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4526,
        )

        return self.__parent__._cast(
            _4526.ShaftToMountableComponentConnectionParametricStudyTool
        )

    @property
    def abstract_shaft_to_mountable_component_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4412.AbstractShaftToMountableComponentConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4412,
        )

        return self.__parent__._cast(
            _4412.AbstractShaftToMountableComponentConnectionParametricStudyTool
        )

    @property
    def connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4444.ConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4444,
        )

        return self.__parent__._cast(_4444.ConnectionParametricStudyTool)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7712.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7712,
        )

        return self.__parent__._cast(_7712.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2738.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2738

        return self.__parent__._cast(_2738.ConnectionAnalysis)

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
    def cycloidal_disc_central_bearing_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "CycloidalDiscCentralBearingConnectionParametricStudyTool":
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
class CycloidalDiscCentralBearingConnectionParametricStudyTool(
    _4433.CoaxialConnectionParametricStudyTool
):
    """CycloidalDiscCentralBearingConnectionParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_PARAMETRIC_STUDY_TOOL
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(
        self: "Self",
    ) -> "_2392.CycloidalDiscCentralBearingConnection":
        """mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscCentralBearingConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_CycloidalDiscCentralBearingConnectionParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDiscCentralBearingConnectionParametricStudyTool
        """
        return _Cast_CycloidalDiscCentralBearingConnectionParametricStudyTool(self)
