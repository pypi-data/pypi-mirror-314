"""CylindricalGearLeadModificationAtProfilePosition"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1130

_CYLINDRICAL_GEAR_LEAD_MODIFICATION_AT_PROFILE_POSITION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "CylindricalGearLeadModificationAtProfilePosition",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1057
    from mastapy._private.gears.micro_geometry import _585, _592

    Self = TypeVar("Self", bound="CylindricalGearLeadModificationAtProfilePosition")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearLeadModificationAtProfilePosition._Cast_CylindricalGearLeadModificationAtProfilePosition",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearLeadModificationAtProfilePosition",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearLeadModificationAtProfilePosition:
    """Special nested class for casting CylindricalGearLeadModificationAtProfilePosition to subclasses."""

    __parent__: "CylindricalGearLeadModificationAtProfilePosition"

    @property
    def cylindrical_gear_lead_modification(
        self: "CastSelf",
    ) -> "_1130.CylindricalGearLeadModification":
        return self.__parent__._cast(_1130.CylindricalGearLeadModification)

    @property
    def lead_modification(self: "CastSelf") -> "_585.LeadModification":
        from mastapy._private.gears.micro_geometry import _585

        return self.__parent__._cast(_585.LeadModification)

    @property
    def modification(self: "CastSelf") -> "_592.Modification":
        from mastapy._private.gears.micro_geometry import _592

        return self.__parent__._cast(_592.Modification)

    @property
    def cylindrical_gear_lead_modification_at_profile_position(
        self: "CastSelf",
    ) -> "CylindricalGearLeadModificationAtProfilePosition":
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
class CylindricalGearLeadModificationAtProfilePosition(
    _1130.CylindricalGearLeadModification
):
    """CylindricalGearLeadModificationAtProfilePosition

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_LEAD_MODIFICATION_AT_PROFILE_POSITION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def position_on_profile_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PositionOnProfileFactor")

        if temp is None:
            return 0.0

        return temp

    @position_on_profile_factor.setter
    @enforce_parameter_types
    def position_on_profile_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PositionOnProfileFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def profile_measurement(self: "Self") -> "_1057.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileMeasurement")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_CylindricalGearLeadModificationAtProfilePosition":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearLeadModificationAtProfilePosition
        """
        return _Cast_CylindricalGearLeadModificationAtProfilePosition(self)
