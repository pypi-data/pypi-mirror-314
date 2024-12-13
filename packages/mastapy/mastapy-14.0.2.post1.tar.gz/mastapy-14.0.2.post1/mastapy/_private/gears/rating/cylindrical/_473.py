"""CylindricalGearRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating import _374

_CYLINDRICAL_GEAR_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "CylindricalGearRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1255
    from mastapy._private.gears.gear_designs.cylindrical import _1044
    from mastapy._private.gears.rating import _366, _371
    from mastapy._private.gears.rating.cylindrical import _501

    Self = TypeVar("Self", bound="CylindricalGearRating")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalGearRating._Cast_CylindricalGearRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearRating:
    """Special nested class for casting CylindricalGearRating to subclasses."""

    __parent__: "CylindricalGearRating"

    @property
    def gear_rating(self: "CastSelf") -> "_374.GearRating":
        return self.__parent__._cast(_374.GearRating)

    @property
    def abstract_gear_rating(self: "CastSelf") -> "_366.AbstractGearRating":
        from mastapy._private.gears.rating import _366

        return self.__parent__._cast(_366.AbstractGearRating)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1255.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1255

        return self.__parent__._cast(_1255.AbstractGearAnalysis)

    @property
    def cylindrical_gear_rating(self: "CastSelf") -> "CylindricalGearRating":
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
class CylindricalGearRating(_374.GearRating):
    """CylindricalGearRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def damage_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DamageBending")

        if temp is None:
            return 0.0

        return temp

    @property
    def damage_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DamageContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def worst_crack_initiation_safety_factor_with_influence_of_rim(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WorstCrackInitiationSafetyFactorWithInfluenceOfRim"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def worst_fatigue_fracture_safety_factor_with_influence_of_rim(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WorstFatigueFractureSafetyFactorWithInfluenceOfRim"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def worst_permanent_deformation_safety_factor_with_influence_of_rim(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WorstPermanentDeformationSafetyFactorWithInfluenceOfRim"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cylindrical_gear(self: "Self") -> "_1044.CylindricalGearDesign":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGear")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def left_flank_rating(self: "Self") -> "_371.GearFlankRating":
        """mastapy.gears.rating.GearFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftFlankRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def right_flank_rating(self: "Self") -> "_371.GearFlankRating":
        """mastapy.gears.rating.GearFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightFlankRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def vdi2737_safety_factor(
        self: "Self",
    ) -> "_501.VDI2737SafetyFactorReportingObject":
        """mastapy.gears.rating.cylindrical.VDI2737SafetyFactorReportingObject

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VDI2737SafetyFactor")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearRating":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearRating
        """
        return _Cast_CylindricalGearRating(self)
