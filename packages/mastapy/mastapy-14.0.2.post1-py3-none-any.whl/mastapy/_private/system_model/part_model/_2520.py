"""MassDisc"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2540

_MASS_DISC = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "MassDisc")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2260
    from mastapy._private.system_model.part_model import _2502, _2524, _2528

    Self = TypeVar("Self", bound="MassDisc")
    CastSelf = TypeVar("CastSelf", bound="MassDisc._Cast_MassDisc")


__docformat__ = "restructuredtext en"
__all__ = ("MassDisc",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MassDisc:
    """Special nested class for casting MassDisc to subclasses."""

    __parent__: "MassDisc"

    @property
    def virtual_component(self: "CastSelf") -> "_2540.VirtualComponent":
        return self.__parent__._cast(_2540.VirtualComponent)

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
    def mass_disc(self: "CastSelf") -> "MassDisc":
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
class MassDisc(_2540.VirtualComponent):
    """MassDisc

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MASS_DISC

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def density(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Density")

        if temp is None:
            return 0.0

        return temp

    @density.setter
    @enforce_parameter_types
    def density(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Density", float(value) if value is not None else 0.0
        )

    @property
    def disc_rotation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DiscRotation")

        if temp is None:
            return 0.0

        return temp

    @disc_rotation.setter
    @enforce_parameter_types
    def disc_rotation(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DiscRotation", float(value) if value is not None else 0.0
        )

    @property
    def disc_skew(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DiscSkew")

        if temp is None:
            return 0.0

        return temp

    @disc_skew.setter
    @enforce_parameter_types
    def disc_skew(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DiscSkew", float(value) if value is not None else 0.0
        )

    @property
    def inner_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def is_distributed(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsDistributed")

        if temp is None:
            return False

        return temp

    @is_distributed.setter
    @enforce_parameter_types
    def is_distributed(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IsDistributed", bool(value) if value is not None else False
        )

    @property
    def outer_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @outer_diameter.setter
    @enforce_parameter_types
    def outer_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "OuterDiameter", float(value) if value is not None else 0.0
        )

    @property
    def width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return temp

    @width.setter
    @enforce_parameter_types
    def width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_MassDisc":
        """Cast to another type.

        Returns:
            _Cast_MassDisc
        """
        return _Cast_MassDisc(self)
