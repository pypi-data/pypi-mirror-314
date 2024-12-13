"""WoundFieldSynchronousRotor"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
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
from mastapy._private.electric_machines import _1321

_WOUND_FIELD_SYNCHRONOUS_ROTOR = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "WoundFieldSynchronousRotor"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.electric_machines import _1337, _1340

    Self = TypeVar("Self", bound="WoundFieldSynchronousRotor")
    CastSelf = TypeVar(
        "CastSelf", bound="WoundFieldSynchronousRotor._Cast_WoundFieldSynchronousRotor"
    )


__docformat__ = "restructuredtext en"
__all__ = ("WoundFieldSynchronousRotor",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WoundFieldSynchronousRotor:
    """Special nested class for casting WoundFieldSynchronousRotor to subclasses."""

    __parent__: "WoundFieldSynchronousRotor"

    @property
    def interior_permanent_magnet_and_synchronous_reluctance_rotor(
        self: "CastSelf",
    ) -> "_1321.InteriorPermanentMagnetAndSynchronousReluctanceRotor":
        return self.__parent__._cast(
            _1321.InteriorPermanentMagnetAndSynchronousReluctanceRotor
        )

    @property
    def permanent_magnet_rotor(self: "CastSelf") -> "_1337.PermanentMagnetRotor":
        from mastapy._private.electric_machines import _1337

        return self.__parent__._cast(_1337.PermanentMagnetRotor)

    @property
    def rotor(self: "CastSelf") -> "_1340.Rotor":
        from mastapy._private.electric_machines import _1340

        return self.__parent__._cast(_1340.Rotor)

    @property
    def wound_field_synchronous_rotor(self: "CastSelf") -> "WoundFieldSynchronousRotor":
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
class WoundFieldSynchronousRotor(
    _1321.InteriorPermanentMagnetAndSynchronousReluctanceRotor
):
    """WoundFieldSynchronousRotor

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WOUND_FIELD_SYNCHRONOUS_ROTOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def pole_depth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PoleDepth")

        if temp is None:
            return 0.0

        return temp

    @pole_depth.setter
    @enforce_parameter_types
    def pole_depth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PoleDepth", float(value) if value is not None else 0.0
        )

    @property
    def pole_tip_depth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PoleTipDepth")

        if temp is None:
            return 0.0

        return temp

    @pole_tip_depth.setter
    @enforce_parameter_types
    def pole_tip_depth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PoleTipDepth", float(value) if value is not None else 0.0
        )

    @property
    def pole_tip_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "PoleTipRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @pole_tip_radius.setter
    @enforce_parameter_types
    def pole_tip_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "PoleTipRadius", value)

    @property
    def pole_tip_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PoleTipWidth")

        if temp is None:
            return 0.0

        return temp

    @pole_tip_width.setter
    @enforce_parameter_types
    def pole_tip_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PoleTipWidth", float(value) if value is not None else 0.0
        )

    @property
    def pole_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PoleWidth")

        if temp is None:
            return 0.0

        return temp

    @pole_width.setter
    @enforce_parameter_types
    def pole_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PoleWidth", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_WoundFieldSynchronousRotor":
        """Cast to another type.

        Returns:
            _Cast_WoundFieldSynchronousRotor
        """
        return _Cast_WoundFieldSynchronousRotor(self)
