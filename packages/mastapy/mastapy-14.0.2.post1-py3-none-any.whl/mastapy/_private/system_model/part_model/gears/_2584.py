"""ConicalGear"""

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
from mastapy._private.system_model.part_model.gears import _2591

_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGear"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.conical import _1194
    from mastapy._private.system_model import _2260
    from mastapy._private.system_model.part_model import _2502, _2524, _2528
    from mastapy._private.system_model.part_model.gears import (
        _2574,
        _2576,
        _2578,
        _2579,
        _2580,
        _2592,
        _2595,
        _2597,
        _2599,
        _2601,
        _2604,
        _2606,
        _2608,
        _2610,
        _2611,
        _2614,
    )

    Self = TypeVar("Self", bound="ConicalGear")
    CastSelf = TypeVar("CastSelf", bound="ConicalGear._Cast_ConicalGear")


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGear:
    """Special nested class for casting ConicalGear to subclasses."""

    __parent__: "ConicalGear"

    @property
    def gear(self: "CastSelf") -> "_2591.Gear":
        return self.__parent__._cast(_2591.Gear)

    @property
    def mountable_component(self: "CastSelf") -> "_2524.MountableComponent":
        from mastapy._private.system_model.part_model import _2524

        return self.__parent__._cast(_2524.MountableComponent)

    @property
    def component(self: "CastSelf") -> "_2502.Component":
        from mastapy._private.system_model.part_model import _2502

        return self.__parent__._cast(_2502.Component)

    @property
    def part(self: "CastSelf") -> "_2528.Part":
        from mastapy._private.system_model.part_model import _2528

        return self.__parent__._cast(_2528.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2260.DesignEntity":
        from mastapy._private.system_model import _2260

        return self.__parent__._cast(_2260.DesignEntity)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2574.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2574

        return self.__parent__._cast(_2574.AGMAGleasonConicalGear)

    @property
    def bevel_differential_gear(self: "CastSelf") -> "_2576.BevelDifferentialGear":
        from mastapy._private.system_model.part_model.gears import _2576

        return self.__parent__._cast(_2576.BevelDifferentialGear)

    @property
    def bevel_differential_planet_gear(
        self: "CastSelf",
    ) -> "_2578.BevelDifferentialPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2578

        return self.__parent__._cast(_2578.BevelDifferentialPlanetGear)

    @property
    def bevel_differential_sun_gear(
        self: "CastSelf",
    ) -> "_2579.BevelDifferentialSunGear":
        from mastapy._private.system_model.part_model.gears import _2579

        return self.__parent__._cast(_2579.BevelDifferentialSunGear)

    @property
    def bevel_gear(self: "CastSelf") -> "_2580.BevelGear":
        from mastapy._private.system_model.part_model.gears import _2580

        return self.__parent__._cast(_2580.BevelGear)

    @property
    def hypoid_gear(self: "CastSelf") -> "_2595.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2595

        return self.__parent__._cast(_2595.HypoidGear)

    @property
    def klingelnberg_cyclo_palloid_conical_gear(
        self: "CastSelf",
    ) -> "_2597.KlingelnbergCycloPalloidConicalGear":
        from mastapy._private.system_model.part_model.gears import _2597

        return self.__parent__._cast(_2597.KlingelnbergCycloPalloidConicalGear)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear(
        self: "CastSelf",
    ) -> "_2599.KlingelnbergCycloPalloidHypoidGear":
        from mastapy._private.system_model.part_model.gears import _2599

        return self.__parent__._cast(_2599.KlingelnbergCycloPalloidHypoidGear)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "CastSelf",
    ) -> "_2601.KlingelnbergCycloPalloidSpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2601

        return self.__parent__._cast(_2601.KlingelnbergCycloPalloidSpiralBevelGear)

    @property
    def spiral_bevel_gear(self: "CastSelf") -> "_2604.SpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2604

        return self.__parent__._cast(_2604.SpiralBevelGear)

    @property
    def straight_bevel_diff_gear(self: "CastSelf") -> "_2606.StraightBevelDiffGear":
        from mastapy._private.system_model.part_model.gears import _2606

        return self.__parent__._cast(_2606.StraightBevelDiffGear)

    @property
    def straight_bevel_gear(self: "CastSelf") -> "_2608.StraightBevelGear":
        from mastapy._private.system_model.part_model.gears import _2608

        return self.__parent__._cast(_2608.StraightBevelGear)

    @property
    def straight_bevel_planet_gear(self: "CastSelf") -> "_2610.StraightBevelPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2610

        return self.__parent__._cast(_2610.StraightBevelPlanetGear)

    @property
    def straight_bevel_sun_gear(self: "CastSelf") -> "_2611.StraightBevelSunGear":
        from mastapy._private.system_model.part_model.gears import _2611

        return self.__parent__._cast(_2611.StraightBevelSunGear)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2614.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2614

        return self.__parent__._cast(_2614.ZerolBevelGear)

    @property
    def conical_gear(self: "CastSelf") -> "ConicalGear":
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
class ConicalGear(_2591.Gear):
    """ConicalGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Length")

        if temp is None:
            return 0.0

        return temp

    @property
    def orientation(self: "Self") -> "_2592.GearOrientations":
        """mastapy.system_model.part_model.gears.GearOrientations"""
        temp = pythonnet_property_get(self.wrapped, "Orientation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.SystemModel.PartModel.Gears.GearOrientations"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.part_model.gears._2592", "GearOrientations"
        )(value)

    @orientation.setter
    @enforce_parameter_types
    def orientation(self: "Self", value: "_2592.GearOrientations") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.SystemModel.PartModel.Gears.GearOrientations"
        )
        pythonnet_property_set(self.wrapped, "Orientation", value)

    @property
    def active_gear_design(self: "Self") -> "_1194.ConicalGearDesign":
        """mastapy.gears.gear_designs.conical.ConicalGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def conical_gear_design(self: "Self") -> "_1194.ConicalGearDesign":
        """mastapy.gears.gear_designs.conical.ConicalGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGear":
        """Cast to another type.

        Returns:
            _Cast_ConicalGear
        """
        return _Cast_ConicalGear(self)
