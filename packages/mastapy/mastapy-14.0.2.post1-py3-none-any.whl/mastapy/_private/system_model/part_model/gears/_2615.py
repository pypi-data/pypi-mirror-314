"""ZerolBevelGearSet"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model.gears import _2581

_ZEROL_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ZerolBevelGearSet"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.zerol_bevel import _980
    from mastapy._private.system_model import _2260
    from mastapy._private.system_model.connections_and_sockets.gears import _2388
    from mastapy._private.system_model.part_model import _2492, _2528, _2537
    from mastapy._private.system_model.part_model.gears import (
        _2575,
        _2585,
        _2593,
        _2614,
    )

    Self = TypeVar("Self", bound="ZerolBevelGearSet")
    CastSelf = TypeVar("CastSelf", bound="ZerolBevelGearSet._Cast_ZerolBevelGearSet")


__docformat__ = "restructuredtext en"
__all__ = ("ZerolBevelGearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ZerolBevelGearSet:
    """Special nested class for casting ZerolBevelGearSet to subclasses."""

    __parent__: "ZerolBevelGearSet"

    @property
    def bevel_gear_set(self: "CastSelf") -> "_2581.BevelGearSet":
        return self.__parent__._cast(_2581.BevelGearSet)

    @property
    def agma_gleason_conical_gear_set(
        self: "CastSelf",
    ) -> "_2575.AGMAGleasonConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2575

        return self.__parent__._cast(_2575.AGMAGleasonConicalGearSet)

    @property
    def conical_gear_set(self: "CastSelf") -> "_2585.ConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2585

        return self.__parent__._cast(_2585.ConicalGearSet)

    @property
    def gear_set(self: "CastSelf") -> "_2593.GearSet":
        from mastapy._private.system_model.part_model.gears import _2593

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
    def zerol_bevel_gear_set(self: "CastSelf") -> "ZerolBevelGearSet":
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
class ZerolBevelGearSet(_2581.BevelGearSet):
    """ZerolBevelGearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ZEROL_BEVEL_GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def conical_gear_set_design(self: "Self") -> "_980.ZerolBevelGearSetDesign":
        """mastapy.gears.gear_designs.zerol_bevel.ZerolBevelGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def zerol_bevel_gear_set_design(self: "Self") -> "_980.ZerolBevelGearSetDesign":
        """mastapy.gears.gear_designs.zerol_bevel.ZerolBevelGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZerolBevelGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def zerol_bevel_gears(self: "Self") -> "List[_2614.ZerolBevelGear]":
        """List[mastapy.system_model.part_model.gears.ZerolBevelGear]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZerolBevelGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def zerol_bevel_meshes(self: "Self") -> "List[_2388.ZerolBevelGearMesh]":
        """List[mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZerolBevelMeshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ZerolBevelGearSet":
        """Cast to another type.

        Returns:
            _Cast_ZerolBevelGearSet
        """
        return _Cast_ZerolBevelGearSet(self)
