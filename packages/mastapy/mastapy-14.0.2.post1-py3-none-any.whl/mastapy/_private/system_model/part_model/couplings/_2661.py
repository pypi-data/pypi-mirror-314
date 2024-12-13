"""RollingRingAssembly"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2537

_ROLLING_RING_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "RollingRingAssembly"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model import _2260
    from mastapy._private.system_model.part_model import _2492, _2528
    from mastapy._private.system_model.part_model.couplings import _2660

    Self = TypeVar("Self", bound="RollingRingAssembly")
    CastSelf = TypeVar(
        "CastSelf", bound="RollingRingAssembly._Cast_RollingRingAssembly"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollingRingAssembly",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollingRingAssembly:
    """Special nested class for casting RollingRingAssembly to subclasses."""

    __parent__: "RollingRingAssembly"

    @property
    def specialised_assembly(self: "CastSelf") -> "_2537.SpecialisedAssembly":
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
    def rolling_ring_assembly(self: "CastSelf") -> "RollingRingAssembly":
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
class RollingRingAssembly(_2537.SpecialisedAssembly):
    """RollingRingAssembly

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLING_RING_ASSEMBLY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Angle")

        if temp is None:
            return 0.0

        return temp

    @angle.setter
    @enforce_parameter_types
    def angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Angle", float(value) if value is not None else 0.0
        )

    @property
    def rolling_rings(self: "Self") -> "List[_2660.RollingRing]":
        """List[mastapy.system_model.part_model.couplings.RollingRing]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollingRings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_RollingRingAssembly":
        """Cast to another type.

        Returns:
            _Cast_RollingRingAssembly
        """
        return _Cast_RollingRingAssembly(self)
