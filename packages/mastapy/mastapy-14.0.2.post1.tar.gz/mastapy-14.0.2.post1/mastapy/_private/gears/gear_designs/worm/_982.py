"""WormDesign"""

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
from mastapy._private.gears.gear_designs.worm import _983

_WORM_DESIGN = python_net_import("SMT.MastaAPI.Gears.GearDesigns.Worm", "WormDesign")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears import _362
    from mastapy._private.gears.gear_designs import _973, _974

    Self = TypeVar("Self", bound="WormDesign")
    CastSelf = TypeVar("CastSelf", bound="WormDesign._Cast_WormDesign")


__docformat__ = "restructuredtext en"
__all__ = ("WormDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormDesign:
    """Special nested class for casting WormDesign to subclasses."""

    __parent__: "WormDesign"

    @property
    def worm_gear_design(self: "CastSelf") -> "_983.WormGearDesign":
        return self.__parent__._cast(_983.WormGearDesign)

    @property
    def gear_design(self: "CastSelf") -> "_973.GearDesign":
        from mastapy._private.gears.gear_designs import _973

        return self.__parent__._cast(_973.GearDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_974.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _974

        return self.__parent__._cast(_974.GearDesignComponent)

    @property
    def worm_design(self: "CastSelf") -> "WormDesign":
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
class WormDesign(_983.WormGearDesign):
    """WormDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def addendum(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Addendum")

        if temp is None:
            return 0.0

        return temp

    @property
    def addendum_factor(self: "Self") -> "_362.WormAddendumFactor":
        """mastapy.gears.WormAddendumFactor"""
        temp = pythonnet_property_get(self.wrapped, "AddendumFactor")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Gears.WormAddendumFactor")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._362", "WormAddendumFactor"
        )(value)

    @addendum_factor.setter
    @enforce_parameter_types
    def addendum_factor(self: "Self", value: "_362.WormAddendumFactor") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Gears.WormAddendumFactor")
        pythonnet_property_set(self.wrapped, "AddendumFactor", value)

    @property
    def axial_pitch(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialPitch")

        if temp is None:
            return 0.0

        return temp

    @property
    def axial_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    def clearance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Clearance")

        if temp is None:
            return 0.0

        return temp

    @property
    def clearance_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ClearanceFactor")

        if temp is None:
            return 0.0

        return temp

    @clearance_factor.setter
    @enforce_parameter_types
    def clearance_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ClearanceFactor", float(value) if value is not None else 0.0
        )

    @property
    def dedendum(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Dedendum")

        if temp is None:
            return 0.0

        return temp

    @property
    def diameter_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DiameterFactor")

        if temp is None:
            return 0.0

        return temp

    @diameter_factor.setter
    @enforce_parameter_types
    def diameter_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DiameterFactor", float(value) if value is not None else 0.0
        )

    @property
    def face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    def fillet_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FilletRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    def fillet_radius_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FilletRadiusFactor")

        if temp is None:
            return 0.0

        return temp

    @fillet_radius_factor.setter
    @enforce_parameter_types
    def fillet_radius_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FilletRadiusFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def lead(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Lead")

        if temp is None:
            return 0.0

        return temp

    @property
    def normal_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    def reference_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ReferenceDiameter")

        if temp is None:
            return 0.0

        return temp

    @reference_diameter.setter
    @enforce_parameter_types
    def reference_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReferenceDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    def reference_lead_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceLeadAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def tip_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TipDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def working_depth_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorkingDepthFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def working_pitch_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorkingPitchDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def working_pitch_lead_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorkingPitchLeadAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def worm_starts(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "WormStarts")

        if temp is None:
            return 0

        return temp

    @worm_starts.setter
    @enforce_parameter_types
    def worm_starts(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "WormStarts", int(value) if value is not None else 0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_WormDesign":
        """Cast to another type.

        Returns:
            _Cast_WormDesign
        """
        return _Cast_WormDesign(self)
