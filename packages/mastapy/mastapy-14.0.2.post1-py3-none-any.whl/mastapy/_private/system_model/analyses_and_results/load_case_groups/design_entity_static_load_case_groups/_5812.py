"""GearSetStaticLoadCaseGroup"""

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

_GEAR_SET_STATIC_LOAD_CASE_GROUP = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups.DesignEntityStaticLoadCaseGroups",
    "GearSetStaticLoadCaseGroup",
)

if TYPE_CHECKING:
    from typing import Any, List, Type

    from mastapy._private.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import (
        _5809,
        _5810,
        _5811,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7043,
        _7045,
        _7048,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2370
    from mastapy._private.system_model.part_model.gears import _2591, _2593

    Self = TypeVar("Self", bound="GearSetStaticLoadCaseGroup")
    CastSelf = TypeVar(
        "CastSelf", bound="GearSetStaticLoadCaseGroup._Cast_GearSetStaticLoadCaseGroup"
    )

TGearSet = TypeVar("TGearSet", bound="_2593.GearSet")
TGear = TypeVar("TGear", bound="_2591.Gear")
TGearStaticLoad = TypeVar("TGearStaticLoad", bound="_7043.GearLoadCase")
TGearMesh = TypeVar("TGearMesh", bound="_2370.GearMesh")
TGearMeshStaticLoad = TypeVar("TGearMeshStaticLoad", bound="_7045.GearMeshLoadCase")
TGearSetStaticLoad = TypeVar("TGearSetStaticLoad", bound="_7048.GearSetLoadCase")

__docformat__ = "restructuredtext en"
__all__ = ("GearSetStaticLoadCaseGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetStaticLoadCaseGroup:
    """Special nested class for casting GearSetStaticLoadCaseGroup to subclasses."""

    __parent__: "GearSetStaticLoadCaseGroup"

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
    def gear_set_static_load_case_group(
        self: "CastSelf",
    ) -> "GearSetStaticLoadCaseGroup":
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
class GearSetStaticLoadCaseGroup(
    _5813.PartStaticLoadCaseGroup,
    Generic[
        TGearSet,
        TGear,
        TGearStaticLoad,
        TGearMesh,
        TGearMeshStaticLoad,
        TGearSetStaticLoad,
    ],
):
    """GearSetStaticLoadCaseGroup

    This is a mastapy class.

    Generic Types:
        TGearSet
        TGear
        TGearStaticLoad
        TGearMesh
        TGearMeshStaticLoad
        TGearSetStaticLoad
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_STATIC_LOAD_CASE_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def part(self: "Self") -> "TGearSet":
        """TGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Part")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gear_set(self: "Self") -> "TGearSet":
        """TGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def part_load_cases(self: "Self") -> "List[TGearSetStaticLoad]":
        """List[TGearSetStaticLoad]

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
    def gear_set_load_cases(self: "Self") -> "List[TGearSetStaticLoad]":
        """List[TGearSetStaticLoad]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSetLoadCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def gears_load_cases(
        self: "Self",
    ) -> "List[_5809.ComponentStaticLoadCaseGroup[TGear, TGearStaticLoad]]":
        """List[mastapy.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups.ComponentStaticLoadCaseGroup[TGear, TGearStaticLoad]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearsLoadCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def meshes_load_cases(
        self: "Self",
    ) -> "List[_5810.ConnectionStaticLoadCaseGroup[TGearMesh, TGearMeshStaticLoad]]":
        """List[mastapy.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups.ConnectionStaticLoadCaseGroup[TGearMesh, TGearMeshStaticLoad]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshesLoadCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetStaticLoadCaseGroup":
        """Cast to another type.

        Returns:
            _Cast_GearSetStaticLoadCaseGroup
        """
        return _Cast_GearSetStaticLoadCaseGroup(self)
