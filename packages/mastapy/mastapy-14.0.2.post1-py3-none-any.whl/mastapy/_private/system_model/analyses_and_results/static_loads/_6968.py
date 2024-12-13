"""AGMAGleasonConicalGearSetLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.static_loads import _7001

_AGMA_GLEASON_CONICAL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AGMAGleasonConicalGearSetLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.manufacturing.bevel import _818
    from mastapy._private.system_model.analyses_and_results import _2740, _2742, _2746
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6959,
        _6966,
        _6967,
        _6977,
        _6982,
        _7048,
        _7060,
        _7083,
        _7107,
        _7110,
        _7116,
        _7119,
        _7142,
    )
    from mastapy._private.system_model.part_model.gears import _2575

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearSetLoadCase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearSetLoadCase._Cast_AGMAGleasonConicalGearSetLoadCase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearSetLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearSetLoadCase:
    """Special nested class for casting AGMAGleasonConicalGearSetLoadCase to subclasses."""

    __parent__: "AGMAGleasonConicalGearSetLoadCase"

    @property
    def conical_gear_set_load_case(self: "CastSelf") -> "_7001.ConicalGearSetLoadCase":
        return self.__parent__._cast(_7001.ConicalGearSetLoadCase)

    @property
    def gear_set_load_case(self: "CastSelf") -> "_7048.GearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7048,
        )

        return self.__parent__._cast(_7048.GearSetLoadCase)

    @property
    def specialised_assembly_load_case(
        self: "CastSelf",
    ) -> "_7107.SpecialisedAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7107,
        )

        return self.__parent__._cast(_7107.SpecialisedAssemblyLoadCase)

    @property
    def abstract_assembly_load_case(
        self: "CastSelf",
    ) -> "_6959.AbstractAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6959,
        )

        return self.__parent__._cast(_6959.AbstractAssemblyLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7083.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7083,
        )

        return self.__parent__._cast(_7083.PartLoadCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2746.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2746

        return self.__parent__._cast(_2746.PartAnalysis)

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
    def bevel_differential_gear_set_load_case(
        self: "CastSelf",
    ) -> "_6977.BevelDifferentialGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6977,
        )

        return self.__parent__._cast(_6977.BevelDifferentialGearSetLoadCase)

    @property
    def bevel_gear_set_load_case(self: "CastSelf") -> "_6982.BevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6982,
        )

        return self.__parent__._cast(_6982.BevelGearSetLoadCase)

    @property
    def hypoid_gear_set_load_case(self: "CastSelf") -> "_7060.HypoidGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7060,
        )

        return self.__parent__._cast(_7060.HypoidGearSetLoadCase)

    @property
    def spiral_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7110.SpiralBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7110,
        )

        return self.__parent__._cast(_7110.SpiralBevelGearSetLoadCase)

    @property
    def straight_bevel_diff_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7116.StraightBevelDiffGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7116,
        )

        return self.__parent__._cast(_7116.StraightBevelDiffGearSetLoadCase)

    @property
    def straight_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7119.StraightBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7119,
        )

        return self.__parent__._cast(_7119.StraightBevelGearSetLoadCase)

    @property
    def zerol_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7142.ZerolBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7142,
        )

        return self.__parent__._cast(_7142.ZerolBevelGearSetLoadCase)

    @property
    def agma_gleason_conical_gear_set_load_case(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearSetLoadCase":
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
class AGMAGleasonConicalGearSetLoadCase(_7001.ConicalGearSetLoadCase):
    """AGMAGleasonConicalGearSetLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR_SET_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def override_manufacturing_config_micro_geometry(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "OverrideManufacturingConfigMicroGeometry"
        )

        if temp is None:
            return False

        return temp

    @override_manufacturing_config_micro_geometry.setter
    @enforce_parameter_types
    def override_manufacturing_config_micro_geometry(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverrideManufacturingConfigMicroGeometry",
            bool(value) if value is not None else False,
        )

    @property
    def assembly_design(self: "Self") -> "_2575.AGMAGleasonConicalGearSet":
        """mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def overridden_manufacturing_config_micro_geometry(
        self: "Self",
    ) -> "_818.ConicalSetMicroGeometryConfigBase":
        """mastapy.gears.manufacturing.bevel.ConicalSetMicroGeometryConfigBase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "OverriddenManufacturingConfigMicroGeometry"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def conical_gears_load_case(
        self: "Self",
    ) -> "List[_6966.AGMAGleasonConicalGearLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearsLoadCase")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def agma_gleason_conical_gears_load_case(
        self: "Self",
    ) -> "List[_6966.AGMAGleasonConicalGearLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AGMAGleasonConicalGearsLoadCase")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def conical_meshes_load_case(
        self: "Self",
    ) -> "List[_6967.AGMAGleasonConicalGearMeshLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalMeshesLoadCase")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def agma_gleason_conical_meshes_load_case(
        self: "Self",
    ) -> "List[_6967.AGMAGleasonConicalGearMeshLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AGMAGleasonConicalMeshesLoadCase")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalGearSetLoadCase":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearSetLoadCase
        """
        return _Cast_AGMAGleasonConicalGearSetLoadCase(self)
