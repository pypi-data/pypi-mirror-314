"""ConicalGearFlankMicroGeometry"""

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
from mastapy._private.gears.micro_geometry import _583

_CONICAL_GEAR_FLANK_MICRO_GEOMETRY = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Conical.MicroGeometry",
    "ConicalGearFlankMicroGeometry",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears import _348
    from mastapy._private.gears.gear_designs.conical import _1194
    from mastapy._private.gears.gear_designs.conical.micro_geometry import (
        _1212,
        _1214,
        _1215,
    )

    Self = TypeVar("Self", bound="ConicalGearFlankMicroGeometry")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearFlankMicroGeometry._Cast_ConicalGearFlankMicroGeometry",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearFlankMicroGeometry",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearFlankMicroGeometry:
    """Special nested class for casting ConicalGearFlankMicroGeometry to subclasses."""

    __parent__: "ConicalGearFlankMicroGeometry"

    @property
    def flank_micro_geometry(self: "CastSelf") -> "_583.FlankMicroGeometry":
        return self.__parent__._cast(_583.FlankMicroGeometry)

    @property
    def conical_gear_flank_micro_geometry(
        self: "CastSelf",
    ) -> "ConicalGearFlankMicroGeometry":
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
class ConicalGearFlankMicroGeometry(_583.FlankMicroGeometry):
    """ConicalGearFlankMicroGeometry

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_FLANK_MICRO_GEOMETRY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def micro_geometry_input_type(self: "Self") -> "_348.MicroGeometryInputTypes":
        """mastapy.gears.MicroGeometryInputTypes"""
        temp = pythonnet_property_get(self.wrapped, "MicroGeometryInputType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.MicroGeometryInputTypes"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._348", "MicroGeometryInputTypes"
        )(value)

    @micro_geometry_input_type.setter
    @enforce_parameter_types
    def micro_geometry_input_type(
        self: "Self", value: "_348.MicroGeometryInputTypes"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.MicroGeometryInputTypes"
        )
        pythonnet_property_set(self.wrapped, "MicroGeometryInputType", value)

    @property
    def bias(self: "Self") -> "_1212.ConicalGearBiasModification":
        """mastapy.gears.gear_designs.conical.micro_geometry.ConicalGearBiasModification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Bias")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def lead_relief(self: "Self") -> "_1214.ConicalGearLeadModification":
        """mastapy.gears.gear_designs.conical.micro_geometry.ConicalGearLeadModification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeadRelief")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def profile_relief(self: "Self") -> "_1215.ConicalGearProfileModification":
        """mastapy.gears.gear_designs.conical.micro_geometry.ConicalGearProfileModification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileRelief")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gear_design(self: "Self") -> "_1194.ConicalGearDesign":
        """mastapy.gears.gear_designs.conical.ConicalGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearFlankMicroGeometry":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearFlankMicroGeometry
        """
        return _Cast_ConicalGearFlankMicroGeometry(self)
