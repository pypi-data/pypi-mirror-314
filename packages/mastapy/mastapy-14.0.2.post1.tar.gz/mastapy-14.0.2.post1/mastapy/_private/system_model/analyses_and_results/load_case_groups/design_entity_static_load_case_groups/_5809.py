"""ComponentStaticLoadCaseGroup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import (
    _5813,
)

_COMPONENT_STATIC_LOAD_CASE_GROUP = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups.DesignEntityStaticLoadCaseGroups",
    "ComponentStaticLoadCaseGroup",
)

if TYPE_CHECKING:
    from typing import Any, List, Type

    from mastapy._private.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import (
        _5811,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _6990
    from mastapy._private.system_model.part_model import _2502

    Self = TypeVar("Self", bound="ComponentStaticLoadCaseGroup")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ComponentStaticLoadCaseGroup._Cast_ComponentStaticLoadCaseGroup",
    )

TReal = TypeVar("TReal", bound="_2502.Component")
TComponentStaticLoad = TypeVar("TComponentStaticLoad", bound="_6990.ComponentLoadCase")

__docformat__ = "restructuredtext en"
__all__ = ("ComponentStaticLoadCaseGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentStaticLoadCaseGroup:
    """Special nested class for casting ComponentStaticLoadCaseGroup to subclasses."""

    __parent__: "ComponentStaticLoadCaseGroup"

    @property
    def part_static_load_case_group(
        self: "CastSelf",
    ) -> "_5813.PartStaticLoadCaseGroup":
        return self.__parent__._cast(_5813.PartStaticLoadCaseGroup)

    @property
    def design_entity_static_load_case_group(
        self: "CastSelf",
    ) -> "_5811.DesignEntityStaticLoadCaseGroup":
        from mastapy._private.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import (
            _5811,
        )

        return self.__parent__._cast(_5811.DesignEntityStaticLoadCaseGroup)

    @property
    def component_static_load_case_group(
        self: "CastSelf",
    ) -> "ComponentStaticLoadCaseGroup":
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
class ComponentStaticLoadCaseGroup(
    _5813.PartStaticLoadCaseGroup, Generic[TReal, TComponentStaticLoad]
):
    """ComponentStaticLoadCaseGroup

    This is a mastapy class.

    Generic Types:
        TReal
        TComponentStaticLoad
    """

    TYPE: ClassVar["Type"] = _COMPONENT_STATIC_LOAD_CASE_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def part(self: "Self") -> "TReal":
        """TReal

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Part")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component(self: "Self") -> "TReal":
        """TReal

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Component")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def part_load_cases(self: "Self") -> "List[TComponentStaticLoad]":
        """List[TComponentStaticLoad]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PartLoadCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_load_cases(self: "Self") -> "List[TComponentStaticLoad]":
        """List[TComponentStaticLoad]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ComponentStaticLoadCaseGroup":
        """Cast to another type.

        Returns:
            _Cast_ComponentStaticLoadCaseGroup
        """
        return _Cast_ComponentStaticLoadCaseGroup(self)
