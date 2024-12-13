"""ConicalGearMeshDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs import _975

_CONICAL_GEAR_MESH_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Conical", "ConicalGearMeshDesign"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.gear_designs import _974
    from mastapy._private.gears.gear_designs.agma_gleason_conical import _1234
    from mastapy._private.gears.gear_designs.bevel import _1221, _1224, _1227, _1228
    from mastapy._private.gears.gear_designs.hypoid import _1012
    from mastapy._private.gears.gear_designs.klingelnberg_conical import _1008
    from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1004
    from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1000
    from mastapy._private.gears.gear_designs.spiral_bevel import _996
    from mastapy._private.gears.gear_designs.straight_bevel import _988
    from mastapy._private.gears.gear_designs.straight_bevel_diff import _992
    from mastapy._private.gears.gear_designs.zerol_bevel import _979

    Self = TypeVar("Self", bound="ConicalGearMeshDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="ConicalGearMeshDesign._Cast_ConicalGearMeshDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearMeshDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearMeshDesign:
    """Special nested class for casting ConicalGearMeshDesign to subclasses."""

    __parent__: "ConicalGearMeshDesign"

    @property
    def gear_mesh_design(self: "CastSelf") -> "_975.GearMeshDesign":
        return self.__parent__._cast(_975.GearMeshDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_974.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _974

        return self.__parent__._cast(_974.GearDesignComponent)

    @property
    def zerol_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_979.ZerolBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _979

        return self.__parent__._cast(_979.ZerolBevelGearMeshDesign)

    @property
    def straight_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_988.StraightBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _988

        return self.__parent__._cast(_988.StraightBevelGearMeshDesign)

    @property
    def straight_bevel_diff_gear_mesh_design(
        self: "CastSelf",
    ) -> "_992.StraightBevelDiffGearMeshDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _992

        return self.__parent__._cast(_992.StraightBevelDiffGearMeshDesign)

    @property
    def spiral_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_996.SpiralBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _996

        return self.__parent__._cast(_996.SpiralBevelGearMeshDesign)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1000.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1000

        return self.__parent__._cast(
            _1000.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1004.KlingelnbergCycloPalloidHypoidGearMeshDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1004

        return self.__parent__._cast(_1004.KlingelnbergCycloPalloidHypoidGearMeshDesign)

    @property
    def klingelnberg_conical_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1008.KlingelnbergConicalGearMeshDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_conical import _1008

        return self.__parent__._cast(_1008.KlingelnbergConicalGearMeshDesign)

    @property
    def hypoid_gear_mesh_design(self: "CastSelf") -> "_1012.HypoidGearMeshDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1012

        return self.__parent__._cast(_1012.HypoidGearMeshDesign)

    @property
    def bevel_gear_mesh_design(self: "CastSelf") -> "_1221.BevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.bevel import _1221

        return self.__parent__._cast(_1221.BevelGearMeshDesign)

    @property
    def agma_gleason_conical_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1234.AGMAGleasonConicalGearMeshDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1234

        return self.__parent__._cast(_1234.AGMAGleasonConicalGearMeshDesign)

    @property
    def conical_gear_mesh_design(self: "CastSelf") -> "ConicalGearMeshDesign":
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
class ConicalGearMeshDesign(_975.GearMeshDesign):
    """ConicalGearMeshDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_MESH_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def driven_machine_characteristic(
        self: "Self",
    ) -> "_1227.MachineCharacteristicAGMAKlingelnberg":
        """mastapy.gears.gear_designs.bevel.MachineCharacteristicAGMAKlingelnberg"""
        temp = pythonnet_property_get(self.wrapped, "DrivenMachineCharacteristic")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Bevel.MachineCharacteristicAGMAKlingelnberg",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.bevel._1227",
            "MachineCharacteristicAGMAKlingelnberg",
        )(value)

    @driven_machine_characteristic.setter
    @enforce_parameter_types
    def driven_machine_characteristic(
        self: "Self", value: "_1227.MachineCharacteristicAGMAKlingelnberg"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Bevel.MachineCharacteristicAGMAKlingelnberg",
        )
        pythonnet_property_set(self.wrapped, "DrivenMachineCharacteristic", value)

    @property
    def driven_machine_characteristic_gleason(
        self: "Self",
    ) -> "_1224.DrivenMachineCharacteristicGleason":
        """mastapy.gears.gear_designs.bevel.DrivenMachineCharacteristicGleason"""
        temp = pythonnet_property_get(
            self.wrapped, "DrivenMachineCharacteristicGleason"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Bevel.DrivenMachineCharacteristicGleason",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.bevel._1224",
            "DrivenMachineCharacteristicGleason",
        )(value)

    @driven_machine_characteristic_gleason.setter
    @enforce_parameter_types
    def driven_machine_characteristic_gleason(
        self: "Self", value: "_1224.DrivenMachineCharacteristicGleason"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Bevel.DrivenMachineCharacteristicGleason",
        )
        pythonnet_property_set(
            self.wrapped, "DrivenMachineCharacteristicGleason", value
        )

    @property
    def maximum_normal_backlash(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalBacklash")

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_normal_backlash(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumNormalBacklash")

        if temp is None:
            return 0.0

        return temp

    @property
    def overload_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OverloadFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @overload_factor.setter
    @enforce_parameter_types
    def overload_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OverloadFactor", value)

    @property
    def pinion_full_circle_edge_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionFullCircleEdgeRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    def prime_mover_characteristic(
        self: "Self",
    ) -> "_1227.MachineCharacteristicAGMAKlingelnberg":
        """mastapy.gears.gear_designs.bevel.MachineCharacteristicAGMAKlingelnberg"""
        temp = pythonnet_property_get(self.wrapped, "PrimeMoverCharacteristic")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Bevel.MachineCharacteristicAGMAKlingelnberg",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.bevel._1227",
            "MachineCharacteristicAGMAKlingelnberg",
        )(value)

    @prime_mover_characteristic.setter
    @enforce_parameter_types
    def prime_mover_characteristic(
        self: "Self", value: "_1227.MachineCharacteristicAGMAKlingelnberg"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Bevel.MachineCharacteristicAGMAKlingelnberg",
        )
        pythonnet_property_set(self.wrapped, "PrimeMoverCharacteristic", value)

    @property
    def prime_mover_characteristic_gleason(
        self: "Self",
    ) -> "_1228.PrimeMoverCharacteristicGleason":
        """mastapy.gears.gear_designs.bevel.PrimeMoverCharacteristicGleason"""
        temp = pythonnet_property_get(self.wrapped, "PrimeMoverCharacteristicGleason")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Bevel.PrimeMoverCharacteristicGleason"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.bevel._1228",
            "PrimeMoverCharacteristicGleason",
        )(value)

    @prime_mover_characteristic_gleason.setter
    @enforce_parameter_types
    def prime_mover_characteristic_gleason(
        self: "Self", value: "_1228.PrimeMoverCharacteristicGleason"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Bevel.PrimeMoverCharacteristicGleason",
        )
        pythonnet_property_set(self.wrapped, "PrimeMoverCharacteristicGleason", value)

    @property
    def shaft_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShaftAngle")

        if temp is None:
            return 0.0

        return temp

    @shaft_angle.setter
    @enforce_parameter_types
    def shaft_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ShaftAngle", float(value) if value is not None else 0.0
        )

    @property
    def specified_backlash_range_max(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedBacklashRangeMax")

        if temp is None:
            return 0.0

        return temp

    @specified_backlash_range_max.setter
    @enforce_parameter_types
    def specified_backlash_range_max(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifiedBacklashRangeMax",
            float(value) if value is not None else 0.0,
        )

    @property
    def specified_backlash_range_min(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedBacklashRangeMin")

        if temp is None:
            return 0.0

        return temp

    @specified_backlash_range_min.setter
    @enforce_parameter_types
    def specified_backlash_range_min(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifiedBacklashRangeMin",
            float(value) if value is not None else 0.0,
        )

    @property
    def specify_backlash(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SpecifyBacklash")

        if temp is None:
            return False

        return temp

    @specify_backlash.setter
    @enforce_parameter_types
    def specify_backlash(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "SpecifyBacklash", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearMeshDesign":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearMeshDesign
        """
        return _Cast_ConicalGearMeshDesign(self)
