"""CouplingCompoundSteadyStateSynchronousResponseAtASpeed"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
    _3837,
)

_COUPLING_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound",
    "CouplingCompoundSteadyStateSynchronousResponseAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3644,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
        _3737,
        _3758,
        _3763,
        _3818,
        _3819,
        _3841,
        _3856,
    )

    Self = TypeVar(
        "Self", bound="CouplingCompoundSteadyStateSynchronousResponseAtASpeed"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingCompoundSteadyStateSynchronousResponseAtASpeed._Cast_CouplingCompoundSteadyStateSynchronousResponseAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingCompoundSteadyStateSynchronousResponseAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingCompoundSteadyStateSynchronousResponseAtASpeed:
    """Special nested class for casting CouplingCompoundSteadyStateSynchronousResponseAtASpeed to subclasses."""

    __parent__: "CouplingCompoundSteadyStateSynchronousResponseAtASpeed"

    @property
    def specialised_assembly_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3837.SpecialisedAssemblyCompoundSteadyStateSynchronousResponseAtASpeed":
        return self.__parent__._cast(
            _3837.SpecialisedAssemblyCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def abstract_assembly_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3737.AbstractAssemblyCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3737,
        )

        return self.__parent__._cast(
            _3737.AbstractAssemblyCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def part_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3818.PartCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3818,
        )

        return self.__parent__._cast(
            _3818.PartCompoundSteadyStateSynchronousResponseAtASpeed
        )

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
    def clutch_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3758.ClutchCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3758,
        )

        return self.__parent__._cast(
            _3758.ClutchCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def concept_coupling_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3763.ConceptCouplingCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3763,
        )

        return self.__parent__._cast(
            _3763.ConceptCouplingCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def part_to_part_shear_coupling_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3819.PartToPartShearCouplingCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3819,
        )

        return self.__parent__._cast(
            _3819.PartToPartShearCouplingCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def spring_damper_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3841.SpringDamperCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3841,
        )

        return self.__parent__._cast(
            _3841.SpringDamperCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def torque_converter_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3856.TorqueConverterCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3856,
        )

        return self.__parent__._cast(
            _3856.TorqueConverterCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def coupling_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "CouplingCompoundSteadyStateSynchronousResponseAtASpeed":
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
class CouplingCompoundSteadyStateSynchronousResponseAtASpeed(
    _3837.SpecialisedAssemblyCompoundSteadyStateSynchronousResponseAtASpeed
):
    """CouplingCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _COUPLING_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_3644.CouplingSteadyStateSynchronousResponseAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.CouplingSteadyStateSynchronousResponseAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_3644.CouplingSteadyStateSynchronousResponseAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.CouplingSteadyStateSynchronousResponseAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_CouplingCompoundSteadyStateSynchronousResponseAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_CouplingCompoundSteadyStateSynchronousResponseAtASpeed
        """
        return _Cast_CouplingCompoundSteadyStateSynchronousResponseAtASpeed(self)
