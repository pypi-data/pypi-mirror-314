"""SpringDamper"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model.couplings import _2646

_SPRING_DAMPER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SpringDamper"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2260
    from mastapy._private.system_model.connections_and_sockets.couplings import _2407
    from mastapy._private.system_model.part_model import _2492, _2528, _2537

    Self = TypeVar("Self", bound="SpringDamper")
    CastSelf = TypeVar("CastSelf", bound="SpringDamper._Cast_SpringDamper")


__docformat__ = "restructuredtext en"
__all__ = ("SpringDamper",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpringDamper:
    """Special nested class for casting SpringDamper to subclasses."""

    __parent__: "SpringDamper"

    @property
    def coupling(self: "CastSelf") -> "_2646.Coupling":
        return self.__parent__._cast(_2646.Coupling)

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
    def spring_damper(self: "CastSelf") -> "SpringDamper":
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
class SpringDamper(_2646.Coupling):
    """SpringDamper

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPRING_DAMPER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection(self: "Self") -> "_2407.SpringDamperConnection":
        """mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Connection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SpringDamper":
        """Cast to another type.

        Returns:
            _Cast_SpringDamper
        """
        return _Cast_SpringDamper(self)
