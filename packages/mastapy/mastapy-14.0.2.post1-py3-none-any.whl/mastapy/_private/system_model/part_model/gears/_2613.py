"""WormGearSet"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model.gears import _2593

_WORM_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "WormGearSet"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.worm import _985
    from mastapy._private.system_model import _2260
    from mastapy._private.system_model.connections_and_sockets.gears import _2386
    from mastapy._private.system_model.part_model import _2492, _2528, _2537
    from mastapy._private.system_model.part_model.gears import _2612

    Self = TypeVar("Self", bound="WormGearSet")
    CastSelf = TypeVar("CastSelf", bound="WormGearSet._Cast_WormGearSet")


__docformat__ = "restructuredtext en"
__all__ = ("WormGearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormGearSet:
    """Special nested class for casting WormGearSet to subclasses."""

    __parent__: "WormGearSet"

    @property
    def gear_set(self: "CastSelf") -> "_2593.GearSet":
        return self.__parent__._cast(_2593.GearSet)

    @property
    def specialised_assembly(self: "CastSelf") -> "_2537.SpecialisedAssembly":
        from mastapy._private.system_model.part_model import _2537

        return self.__parent__._cast(_2537.SpecialisedAssembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2492.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2492

        return self.__parent__._cast(_2492.AbstractAssembly)

    @property
    def part(self: "CastSelf") -> "_2528.Part":
        from mastapy._private.system_model.part_model import _2528

        return self.__parent__._cast(_2528.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2260.DesignEntity":
        from mastapy._private.system_model import _2260

        return self.__parent__._cast(_2260.DesignEntity)

    @property
    def worm_gear_set(self: "CastSelf") -> "WormGearSet":
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
class WormGearSet(_2593.GearSet):
    """WormGearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def active_gear_set_design(self: "Self") -> "_985.WormGearSetDesign":
        """mastapy.gears.gear_designs.worm.WormGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def worm_gear_set_design(self: "Self") -> "_985.WormGearSetDesign":
        """mastapy.gears.gear_designs.worm.WormGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def worm_gears(self: "Self") -> "List[_2612.WormGear]":
        """List[mastapy.system_model.part_model.gears.WormGear]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def worm_meshes(self: "Self") -> "List[_2386.WormGearMesh]":
        """List[mastapy.system_model.connections_and_sockets.gears.WormGearMesh]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormMeshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_WormGearSet":
        """Cast to another type.

        Returns:
            _Cast_WormGearSet
        """
        return _Cast_WormGearSet(self)
