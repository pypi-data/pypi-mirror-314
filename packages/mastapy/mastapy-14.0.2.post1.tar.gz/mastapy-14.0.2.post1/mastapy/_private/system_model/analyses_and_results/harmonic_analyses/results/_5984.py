"""ExcitationSourceSelectionBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_EXCITATION_SOURCE_SELECTION_BASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Results",
    "ExcitationSourceSelectionBase",
)

if TYPE_CHECKING:
    from typing import Any, Optional, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results import (
        _5983,
        _5985,
    )

    Self = TypeVar("Self", bound="ExcitationSourceSelectionBase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ExcitationSourceSelectionBase._Cast_ExcitationSourceSelectionBase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ExcitationSourceSelectionBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ExcitationSourceSelectionBase:
    """Special nested class for casting ExcitationSourceSelectionBase to subclasses."""

    __parent__: "ExcitationSourceSelectionBase"

    @property
    def excitation_source_selection(
        self: "CastSelf",
    ) -> "_5983.ExcitationSourceSelection":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results import (
            _5983,
        )

        return self.__parent__._cast(_5983.ExcitationSourceSelection)

    @property
    def excitation_source_selection_group(
        self: "CastSelf",
    ) -> "_5985.ExcitationSourceSelectionGroup":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results import (
            _5985,
        )

        return self.__parent__._cast(_5985.ExcitationSourceSelectionGroup)

    @property
    def excitation_source_selection_base(
        self: "CastSelf",
    ) -> "ExcitationSourceSelectionBase":
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
class ExcitationSourceSelectionBase(_0.APIBase):
    """ExcitationSourceSelectionBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _EXCITATION_SOURCE_SELECTION_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def included(self: "Self") -> "Optional[bool]":
        """Optional[bool]"""
        temp = pythonnet_property_get(self.wrapped, "Included")

        if temp is None:
            return None

        return temp

    @included.setter
    @enforce_parameter_types
    def included(self: "Self", value: "Optional[bool]") -> None:
        pythonnet_property_set(self.wrapped, "Included", value)

    @property
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ExcitationSourceSelectionBase":
        """Cast to another type.

        Returns:
            _Cast_ExcitationSourceSelectionBase
        """
        return _Cast_ExcitationSourceSelectionBase(self)
