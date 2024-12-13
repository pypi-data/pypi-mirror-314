"""CylindricalPlanetGear"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model.gears import _2586

_CYLINDRICAL_PLANET_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalPlanetGear"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2260
    from mastapy._private.system_model.part_model import _2502, _2524, _2528
    from mastapy._private.system_model.part_model.gears import _2591

    Self = TypeVar("Self", bound="CylindricalPlanetGear")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalPlanetGear._Cast_CylindricalPlanetGear"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalPlanetGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalPlanetGear:
    """Special nested class for casting CylindricalPlanetGear to subclasses."""

    __parent__: "CylindricalPlanetGear"

    @property
    def cylindrical_gear(self: "CastSelf") -> "_2586.CylindricalGear":
        return self.__parent__._cast(_2586.CylindricalGear)

    @property
    def gear(self: "CastSelf") -> "_2591.Gear":
        from mastapy._private.system_model.part_model.gears import _2591

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
    def cylindrical_planet_gear(self: "CastSelf") -> "CylindricalPlanetGear":
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
class CylindricalPlanetGear(_2586.CylindricalGear):
    """CylindricalPlanetGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_PLANET_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalPlanetGear":
        """Cast to another type.

        Returns:
            _Cast_CylindricalPlanetGear
        """
        return _Cast_CylindricalPlanetGear(self)
