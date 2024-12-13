"""ConicalGearSetDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs import _976

_CONICAL_GEAR_SET_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Conical", "ConicalGearSetDesign"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs import _974
    from mastapy._private.gears.gear_designs.agma_gleason_conical import _1235
    from mastapy._private.gears.gear_designs.bevel import _1222
    from mastapy._private.gears.gear_designs.conical import _1195
    from mastapy._private.gears.gear_designs.hypoid import _1013
    from mastapy._private.gears.gear_designs.klingelnberg_conical import _1009
    from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1005
    from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1001
    from mastapy._private.gears.gear_designs.spiral_bevel import _997
    from mastapy._private.gears.gear_designs.straight_bevel import _989
    from mastapy._private.gears.gear_designs.straight_bevel_diff import _993
    from mastapy._private.gears.gear_designs.zerol_bevel import _980

    Self = TypeVar("Self", bound="ConicalGearSetDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="ConicalGearSetDesign._Cast_ConicalGearSetDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearSetDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearSetDesign:
    """Special nested class for casting ConicalGearSetDesign to subclasses."""

    __parent__: "ConicalGearSetDesign"

    @property
    def gear_set_design(self: "CastSelf") -> "_976.GearSetDesign":
        return self.__parent__._cast(_976.GearSetDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_974.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _974

        return self.__parent__._cast(_974.GearDesignComponent)

    @property
    def zerol_bevel_gear_set_design(self: "CastSelf") -> "_980.ZerolBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _980

        return self.__parent__._cast(_980.ZerolBevelGearSetDesign)

    @property
    def straight_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_989.StraightBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _989

        return self.__parent__._cast(_989.StraightBevelGearSetDesign)

    @property
    def straight_bevel_diff_gear_set_design(
        self: "CastSelf",
    ) -> "_993.StraightBevelDiffGearSetDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _993

        return self.__parent__._cast(_993.StraightBevelDiffGearSetDesign)

    @property
    def spiral_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_997.SpiralBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _997

        return self.__parent__._cast(_997.SpiralBevelGearSetDesign)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_1001.KlingelnbergCycloPalloidSpiralBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1001

        return self.__parent__._cast(
            _1001.KlingelnbergCycloPalloidSpiralBevelGearSetDesign
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_design(
        self: "CastSelf",
    ) -> "_1005.KlingelnbergCycloPalloidHypoidGearSetDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1005

        return self.__parent__._cast(_1005.KlingelnbergCycloPalloidHypoidGearSetDesign)

    @property
    def klingelnberg_conical_gear_set_design(
        self: "CastSelf",
    ) -> "_1009.KlingelnbergConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_conical import _1009

        return self.__parent__._cast(_1009.KlingelnbergConicalGearSetDesign)

    @property
    def hypoid_gear_set_design(self: "CastSelf") -> "_1013.HypoidGearSetDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1013

        return self.__parent__._cast(_1013.HypoidGearSetDesign)

    @property
    def bevel_gear_set_design(self: "CastSelf") -> "_1222.BevelGearSetDesign":
        from mastapy._private.gears.gear_designs.bevel import _1222

        return self.__parent__._cast(_1222.BevelGearSetDesign)

    @property
    def agma_gleason_conical_gear_set_design(
        self: "CastSelf",
    ) -> "_1235.AGMAGleasonConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1235

        return self.__parent__._cast(_1235.AGMAGleasonConicalGearSetDesign)

    @property
    def conical_gear_set_design(self: "CastSelf") -> "ConicalGearSetDesign":
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
class ConicalGearSetDesign(_976.GearSetDesign):
    """ConicalGearSetDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_SET_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def circular_pitch(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CircularPitch")

        if temp is None:
            return 0.0

        return temp

    @property
    def cutter_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CutterRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    def dominant_pinion(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "DominantPinion")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @dominant_pinion.setter
    @enforce_parameter_types
    def dominant_pinion(self: "Self", value: "str") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else ""
        )
        pythonnet_property_set(self.wrapped, "DominantPinion", value)

    @property
    def imported_xml_file_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ImportedXMLFileName")

        if temp is None:
            return ""

        return temp

    @property
    def mean_normal_module(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MeanNormalModule")

        if temp is None:
            return 0.0

        return temp

    @mean_normal_module.setter
    @enforce_parameter_types
    def mean_normal_module(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MeanNormalModule", float(value) if value is not None else 0.0
        )

    @property
    def module(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Module")

        if temp is None:
            return 0.0

        return temp

    @module.setter
    @enforce_parameter_types
    def module(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Module", float(value) if value is not None else 0.0
        )

    @property
    def wheel_finish_cutter_point_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WheelFinishCutterPointWidth")

        if temp is None:
            return 0.0

        return temp

    @wheel_finish_cutter_point_width.setter
    @enforce_parameter_types
    def wheel_finish_cutter_point_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WheelFinishCutterPointWidth",
            float(value) if value is not None else 0.0,
        )

    @property
    def wheel_mean_cone_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelMeanConeDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    def wheel_outer_cone_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelOuterConeDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    def wheel_pitch_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WheelPitchDiameter")

        if temp is None:
            return 0.0

        return temp

    @wheel_pitch_diameter.setter
    @enforce_parameter_types
    def wheel_pitch_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WheelPitchDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    def conical_meshes(self: "Self") -> "List[_1195.ConicalGearMeshDesign]":
        """List[mastapy.gears.gear_designs.conical.ConicalGearMeshDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalMeshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearSetDesign":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearSetDesign
        """
        return _Cast_ConicalGearSetDesign(self)
