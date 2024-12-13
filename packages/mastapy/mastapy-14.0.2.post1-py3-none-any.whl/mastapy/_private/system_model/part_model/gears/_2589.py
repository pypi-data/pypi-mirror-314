"""FaceGear"""

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

_FACE_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "FaceGear")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.face import _1015
    from mastapy._private.system_model import _2260
    from mastapy._private.system_model.part_model import _2502, _2524, _2528
    from mastapy._private.system_model.part_model.gears import _2592

    Self = TypeVar("Self", bound="FaceGear")
    CastSelf = TypeVar("CastSelf", bound="FaceGear._Cast_FaceGear")


__docformat__ = "restructuredtext en"
__all__ = ("FaceGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FaceGear:
    """Special nested class for casting FaceGear to subclasses."""

    __parent__: "FaceGear"

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
    def face_gear(self: "CastSelf") -> "FaceGear":
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
class FaceGear(_2591.Gear):
    """FaceGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FACE_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def active_gear_design(self: "Self") -> "_1015.FaceGearDesign":
        """mastapy.gears.gear_designs.face.FaceGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def face_gear_design(self: "Self") -> "_1015.FaceGearDesign":
        """mastapy.gears.gear_designs.face.FaceGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceGearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_FaceGear":
        """Cast to another type.

        Returns:
            _Cast_FaceGear
        """
        return _Cast_FaceGear(self)
