"""CouplingHalfCompoundModalAnalysisAtASpeed"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
    _5453,
)

_COUPLING_HALF_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound",
    "CouplingHalfCompoundModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5280,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
        _5397,
        _5399,
        _5402,
        _5416,
        _5455,
        _5458,
        _5464,
        _5468,
        _5480,
        _5490,
        _5491,
        _5492,
        _5495,
        _5496,
    )

    Self = TypeVar("Self", bound="CouplingHalfCompoundModalAnalysisAtASpeed")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingHalfCompoundModalAnalysisAtASpeed._Cast_CouplingHalfCompoundModalAnalysisAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalfCompoundModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingHalfCompoundModalAnalysisAtASpeed:
    """Special nested class for casting CouplingHalfCompoundModalAnalysisAtASpeed to subclasses."""

    __parent__: "CouplingHalfCompoundModalAnalysisAtASpeed"

    @property
    def mountable_component_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5453.MountableComponentCompoundModalAnalysisAtASpeed":
        return self.__parent__._cast(
            _5453.MountableComponentCompoundModalAnalysisAtASpeed
        )

    @property
    def component_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5399.ComponentCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5399,
        )

        return self.__parent__._cast(_5399.ComponentCompoundModalAnalysisAtASpeed)

    @property
    def part_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5455.PartCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5455,
        )

        return self.__parent__._cast(_5455.PartCompoundModalAnalysisAtASpeed)

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
    def clutch_half_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5397.ClutchHalfCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5397,
        )

        return self.__parent__._cast(_5397.ClutchHalfCompoundModalAnalysisAtASpeed)

    @property
    def concept_coupling_half_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5402.ConceptCouplingHalfCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5402,
        )

        return self.__parent__._cast(
            _5402.ConceptCouplingHalfCompoundModalAnalysisAtASpeed
        )

    @property
    def cvt_pulley_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5416.CVTPulleyCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5416,
        )

        return self.__parent__._cast(_5416.CVTPulleyCompoundModalAnalysisAtASpeed)

    @property
    def part_to_part_shear_coupling_half_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5458.PartToPartShearCouplingHalfCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5458,
        )

        return self.__parent__._cast(
            _5458.PartToPartShearCouplingHalfCompoundModalAnalysisAtASpeed
        )

    @property
    def pulley_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5464.PulleyCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5464,
        )

        return self.__parent__._cast(_5464.PulleyCompoundModalAnalysisAtASpeed)

    @property
    def rolling_ring_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5468.RollingRingCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5468,
        )

        return self.__parent__._cast(_5468.RollingRingCompoundModalAnalysisAtASpeed)

    @property
    def spring_damper_half_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5480.SpringDamperHalfCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5480,
        )

        return self.__parent__._cast(
            _5480.SpringDamperHalfCompoundModalAnalysisAtASpeed
        )

    @property
    def synchroniser_half_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5490.SynchroniserHalfCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5490,
        )

        return self.__parent__._cast(
            _5490.SynchroniserHalfCompoundModalAnalysisAtASpeed
        )

    @property
    def synchroniser_part_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5491.SynchroniserPartCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5491,
        )

        return self.__parent__._cast(
            _5491.SynchroniserPartCompoundModalAnalysisAtASpeed
        )

    @property
    def synchroniser_sleeve_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5492.SynchroniserSleeveCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5492,
        )

        return self.__parent__._cast(
            _5492.SynchroniserSleeveCompoundModalAnalysisAtASpeed
        )

    @property
    def torque_converter_pump_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5495.TorqueConverterPumpCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5495,
        )

        return self.__parent__._cast(
            _5495.TorqueConverterPumpCompoundModalAnalysisAtASpeed
        )

    @property
    def torque_converter_turbine_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5496.TorqueConverterTurbineCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5496,
        )

        return self.__parent__._cast(
            _5496.TorqueConverterTurbineCompoundModalAnalysisAtASpeed
        )

    @property
    def coupling_half_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "CouplingHalfCompoundModalAnalysisAtASpeed":
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
class CouplingHalfCompoundModalAnalysisAtASpeed(
    _5453.MountableComponentCompoundModalAnalysisAtASpeed
):
    """CouplingHalfCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_HALF_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_5280.CouplingHalfModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.CouplingHalfModalAnalysisAtASpeed]

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
    ) -> "List[_5280.CouplingHalfModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.CouplingHalfModalAnalysisAtASpeed]

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
    def cast_to(self: "Self") -> "_Cast_CouplingHalfCompoundModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_CouplingHalfCompoundModalAnalysisAtASpeed
        """
        return _Cast_CouplingHalfCompoundModalAnalysisAtASpeed(self)
