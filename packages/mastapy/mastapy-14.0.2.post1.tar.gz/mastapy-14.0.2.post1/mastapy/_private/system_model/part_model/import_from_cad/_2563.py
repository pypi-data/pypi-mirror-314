"""CylindricalSunGearFromCAD"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model.import_from_cad import _2560

_CYLINDRICAL_SUN_GEAR_FROM_CAD = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD", "CylindricalSunGearFromCAD"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model.import_from_cad import (
        _2556,
        _2559,
        _2565,
    )

    Self = TypeVar("Self", bound="CylindricalSunGearFromCAD")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalSunGearFromCAD._Cast_CylindricalSunGearFromCAD"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalSunGearFromCAD",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalSunGearFromCAD:
    """Special nested class for casting CylindricalSunGearFromCAD to subclasses."""

    __parent__: "CylindricalSunGearFromCAD"

    @property
    def cylindrical_gear_in_planetary_set_from_cad(
        self: "CastSelf",
    ) -> "_2560.CylindricalGearInPlanetarySetFromCAD":
        return self.__parent__._cast(_2560.CylindricalGearInPlanetarySetFromCAD)

    @property
    def cylindrical_gear_from_cad(self: "CastSelf") -> "_2559.CylindricalGearFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2559

        return self.__parent__._cast(_2559.CylindricalGearFromCAD)

    @property
    def mountable_component_from_cad(
        self: "CastSelf",
    ) -> "_2565.MountableComponentFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2565

        return self.__parent__._cast(_2565.MountableComponentFromCAD)

    @property
    def component_from_cad(self: "CastSelf") -> "_2556.ComponentFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2556

        return self.__parent__._cast(_2556.ComponentFromCAD)

    @property
    def cylindrical_sun_gear_from_cad(self: "CastSelf") -> "CylindricalSunGearFromCAD":
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
class CylindricalSunGearFromCAD(_2560.CylindricalGearInPlanetarySetFromCAD):
    """CylindricalSunGearFromCAD

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_SUN_GEAR_FROM_CAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalSunGearFromCAD":
        """Cast to another type.

        Returns:
            _Cast_CylindricalSunGearFromCAD
        """
        return _Cast_CylindricalSunGearFromCAD(self)
