"""ConnectorCompoundModalAnalysisAtAStiffness"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
    _5190,
)

_CONNECTOR_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound",
    "ConnectorCompoundModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5014,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
        _5119,
        _5136,
        _5191,
        _5192,
        _5209,
    )

    Self = TypeVar("Self", bound="ConnectorCompoundModalAnalysisAtAStiffness")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConnectorCompoundModalAnalysisAtAStiffness._Cast_ConnectorCompoundModalAnalysisAtAStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectorCompoundModalAnalysisAtAStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectorCompoundModalAnalysisAtAStiffness:
    """Special nested class for casting ConnectorCompoundModalAnalysisAtAStiffness to subclasses."""

    __parent__: "ConnectorCompoundModalAnalysisAtAStiffness"

    @property
    def mountable_component_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5190.MountableComponentCompoundModalAnalysisAtAStiffness":
        return self.__parent__._cast(
            _5190.MountableComponentCompoundModalAnalysisAtAStiffness
        )

    @property
    def component_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5136.ComponentCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5136,
        )

        return self.__parent__._cast(_5136.ComponentCompoundModalAnalysisAtAStiffness)

    @property
    def part_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5192.PartCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5192,
        )

        return self.__parent__._cast(_5192.PartCompoundModalAnalysisAtAStiffness)

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
    def bearing_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5119.BearingCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5119,
        )

        return self.__parent__._cast(_5119.BearingCompoundModalAnalysisAtAStiffness)

    @property
    def oil_seal_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5191.OilSealCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5191,
        )

        return self.__parent__._cast(_5191.OilSealCompoundModalAnalysisAtAStiffness)

    @property
    def shaft_hub_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5209.ShaftHubConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5209,
        )

        return self.__parent__._cast(
            _5209.ShaftHubConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def connector_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "ConnectorCompoundModalAnalysisAtAStiffness":
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
class ConnectorCompoundModalAnalysisAtAStiffness(
    _5190.MountableComponentCompoundModalAnalysisAtAStiffness
):
    """ConnectorCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTOR_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_5014.ConnectorModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.ConnectorModalAnalysisAtAStiffness]

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
    ) -> "List[_5014.ConnectorModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.ConnectorModalAnalysisAtAStiffness]

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
    def cast_to(self: "Self") -> "_Cast_ConnectorCompoundModalAnalysisAtAStiffness":
        """Cast to another type.

        Returns:
            _Cast_ConnectorCompoundModalAnalysisAtAStiffness
        """
        return _Cast_ConnectorCompoundModalAnalysisAtAStiffness(self)
