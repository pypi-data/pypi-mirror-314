"""Implementations of 'ListWithSelectedItem' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, mixins
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _5906

_ARRAY = python_net_import("System", "Array")
_LIST_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Property", "ListWithSelectedItem"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self",
        bound="ListWithSelectedItem_HarmonicAnalysisWithVaryingStiffnessStaticLoadCase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ListWithSelectedItem_HarmonicAnalysisWithVaryingStiffnessStaticLoadCase",)


class ListWithSelectedItem_HarmonicAnalysisWithVaryingStiffnessStaticLoadCase(
    _5906.HarmonicAnalysisWithVaryingStiffnessStaticLoadCase,
    mixins.ListWithSelectedItemMixin,
):
    """ListWithSelectedItem_HarmonicAnalysisWithVaryingStiffnessStaticLoadCase

    A specific implementation of 'ListWithSelectedItem' for 'HarmonicAnalysisWithVaryingStiffnessStaticLoadCase' types.
    """

    __qualname__ = "HarmonicAnalysisWithVaryingStiffnessStaticLoadCase"

    def __init__(self: "Self", instance_to_wrap: "Any") -> None:
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(
        cls: "Type[ListWithSelectedItem_HarmonicAnalysisWithVaryingStiffnessStaticLoadCase]",
    ) -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(
        cls: "Type[ListWithSelectedItem_HarmonicAnalysisWithVaryingStiffnessStaticLoadCase]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _5906.HarmonicAnalysisWithVaryingStiffnessStaticLoadCase.TYPE

    @property
    def selected_value(
        self: "Self",
    ) -> "_5906.HarmonicAnalysisWithVaryingStiffnessStaticLoadCase":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.HarmonicAnalysisWithVaryingStiffnessStaticLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.enclosing, "SelectedValue")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def available_values(
        self: "Self",
    ) -> "List[_5906.HarmonicAnalysisWithVaryingStiffnessStaticLoadCase]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.HarmonicAnalysisWithVaryingStiffnessStaticLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.enclosing, "AvailableValues")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value
