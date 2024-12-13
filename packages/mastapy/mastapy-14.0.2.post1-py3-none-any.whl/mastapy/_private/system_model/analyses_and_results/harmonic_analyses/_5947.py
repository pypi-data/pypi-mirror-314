"""SingleNodePeriodicExcitationWithReferenceShaft"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _5930

_SINGLE_NODE_PERIODIC_EXCITATION_WITH_REFERENCE_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "SingleNodePeriodicExcitationWithReferenceShaft",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5815,
        _5895,
        _5973,
    )

    Self = TypeVar("Self", bound="SingleNodePeriodicExcitationWithReferenceShaft")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SingleNodePeriodicExcitationWithReferenceShaft._Cast_SingleNodePeriodicExcitationWithReferenceShaft",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SingleNodePeriodicExcitationWithReferenceShaft",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SingleNodePeriodicExcitationWithReferenceShaft:
    """Special nested class for casting SingleNodePeriodicExcitationWithReferenceShaft to subclasses."""

    __parent__: "SingleNodePeriodicExcitationWithReferenceShaft"

    @property
    def periodic_excitation_with_reference_shaft(
        self: "CastSelf",
    ) -> "_5930.PeriodicExcitationWithReferenceShaft":
        return self.__parent__._cast(_5930.PeriodicExcitationWithReferenceShaft)

    @property
    def abstract_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "_5815.AbstractPeriodicExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5815,
        )

        return self.__parent__._cast(_5815.AbstractPeriodicExcitationDetail)

    @property
    def general_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "_5895.GeneralPeriodicExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5895,
        )

        return self.__parent__._cast(_5895.GeneralPeriodicExcitationDetail)

    @property
    def unbalanced_mass_excitation_detail(
        self: "CastSelf",
    ) -> "_5973.UnbalancedMassExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5973,
        )

        return self.__parent__._cast(_5973.UnbalancedMassExcitationDetail)

    @property
    def single_node_periodic_excitation_with_reference_shaft(
        self: "CastSelf",
    ) -> "SingleNodePeriodicExcitationWithReferenceShaft":
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
class SingleNodePeriodicExcitationWithReferenceShaft(
    _5930.PeriodicExcitationWithReferenceShaft
):
    """SingleNodePeriodicExcitationWithReferenceShaft

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SINGLE_NODE_PERIODIC_EXCITATION_WITH_REFERENCE_SHAFT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_SingleNodePeriodicExcitationWithReferenceShaft":
        """Cast to another type.

        Returns:
            _Cast_SingleNodePeriodicExcitationWithReferenceShaft
        """
        return _Cast_SingleNodePeriodicExcitationWithReferenceShaft(self)
