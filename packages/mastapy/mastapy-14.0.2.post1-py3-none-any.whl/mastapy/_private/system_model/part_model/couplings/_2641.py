"""ClutchHalf"""

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
from mastapy._private.system_model.part_model.couplings import _2647

_CLUTCH_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ClutchHalf"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2260
    from mastapy._private.system_model.part_model import _2502, _2524, _2528

    Self = TypeVar("Self", bound="ClutchHalf")
    CastSelf = TypeVar("CastSelf", bound="ClutchHalf._Cast_ClutchHalf")


__docformat__ = "restructuredtext en"
__all__ = ("ClutchHalf",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ClutchHalf:
    """Special nested class for casting ClutchHalf to subclasses."""

    __parent__: "ClutchHalf"

    @property
    def coupling_half(self: "CastSelf") -> "_2647.CouplingHalf":
        return self.__parent__._cast(_2647.CouplingHalf)

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
    def clutch_half(self: "CastSelf") -> "ClutchHalf":
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
class ClutchHalf(_2647.CouplingHalf):
    """ClutchHalf

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CLUTCH_HALF

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def is_mounted_on_shaft_outer(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsMountedOnShaftOuter")

        if temp is None:
            return False

        return temp

    @is_mounted_on_shaft_outer.setter
    @enforce_parameter_types
    def is_mounted_on_shaft_outer(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsMountedOnShaftOuter",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ClutchHalf":
        """Cast to another type.

        Returns:
            _Cast_ClutchHalf
        """
        return _Cast_ClutchHalf(self)
