"""ConceptGearDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs import _973

_CONCEPT_GEAR_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Concept", "ConceptGearDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears import _345
    from mastapy._private.gears.gear_designs import _974

    Self = TypeVar("Self", bound="ConceptGearDesign")
    CastSelf = TypeVar("CastSelf", bound="ConceptGearDesign._Cast_ConceptGearDesign")


__docformat__ = "restructuredtext en"
__all__ = ("ConceptGearDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConceptGearDesign:
    """Special nested class for casting ConceptGearDesign to subclasses."""

    __parent__: "ConceptGearDesign"

    @property
    def gear_design(self: "CastSelf") -> "_973.GearDesign":
        return self.__parent__._cast(_973.GearDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_974.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _974

        return self.__parent__._cast(_974.GearDesignComponent)

    @property
    def concept_gear_design(self: "CastSelf") -> "ConceptGearDesign":
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
class ConceptGearDesign(_973.GearDesign):
    """ConceptGearDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCEPT_GEAR_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def hand(self: "Self") -> "_345.Hand":
        """mastapy.gears.Hand"""
        temp = pythonnet_property_get(self.wrapped, "Hand")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Gears.Hand")

        if value is None:
            return None

        return constructor.new_from_mastapy("mastapy._private.gears._345", "Hand")(
            value
        )

    @hand.setter
    @enforce_parameter_types
    def hand(self: "Self", value: "_345.Hand") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Gears.Hand")
        pythonnet_property_set(self.wrapped, "Hand", value)

    @property
    def mean_point_to_crossing_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanPointToCrossingPoint")

        if temp is None:
            return 0.0

        return temp

    @property
    def pitch_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PitchAngle")

        if temp is None:
            return 0.0

        return temp

    @pitch_angle.setter
    @enforce_parameter_types
    def pitch_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PitchAngle", float(value) if value is not None else 0.0
        )

    @property
    def pitch_apex_to_crossing_point(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PitchApexToCrossingPoint")

        if temp is None:
            return 0.0

        return temp

    @pitch_apex_to_crossing_point.setter
    @enforce_parameter_types
    def pitch_apex_to_crossing_point(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PitchApexToCrossingPoint",
            float(value) if value is not None else 0.0,
        )

    @property
    def working_helix_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WorkingHelixAngle")

        if temp is None:
            return 0.0

        return temp

    @working_helix_angle.setter
    @enforce_parameter_types
    def working_helix_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WorkingHelixAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    def working_pitch_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WorkingPitchDiameter")

        if temp is None:
            return 0.0

        return temp

    @working_pitch_diameter.setter
    @enforce_parameter_types
    def working_pitch_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WorkingPitchDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ConceptGearDesign":
        """Cast to another type.

        Returns:
            _Cast_ConceptGearDesign
        """
        return _Cast_ConceptGearDesign(self)
