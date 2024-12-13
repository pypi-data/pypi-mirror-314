"""CylindricalGearFESettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility import _1645

_CYLINDRICAL_GEAR_FE_SETTINGS = python_net_import(
    "SMT.MastaAPI.Gears.LTCA.Cylindrical", "CylindricalGearFESettings"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility import _1646

    Self = TypeVar("Self", bound="CylindricalGearFESettings")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalGearFESettings._Cast_CylindricalGearFESettings"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearFESettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearFESettings:
    """Special nested class for casting CylindricalGearFESettings to subclasses."""

    __parent__: "CylindricalGearFESettings"

    @property
    def per_machine_settings(self: "CastSelf") -> "_1645.PerMachineSettings":
        return self.__parent__._cast(_1645.PerMachineSettings)

    @property
    def persistent_singleton(self: "CastSelf") -> "_1646.PersistentSingleton":
        from mastapy._private.utility import _1646

        return self.__parent__._cast(_1646.PersistentSingleton)

    @property
    def cylindrical_gear_fe_settings(self: "CastSelf") -> "CylindricalGearFESettings":
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
class CylindricalGearFESettings(_1645.PerMachineSettings):
    """CylindricalGearFESettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_FE_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearFESettings":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearFESettings
        """
        return _Cast_CylindricalGearFESettings(self)
