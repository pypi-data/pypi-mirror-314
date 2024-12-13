"""ConicalGearCutter"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_CONICAL_GEAR_CUTTER = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Conical", "ConicalGearCutter"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.conical import (
        _1201,
        _1202,
        _1203,
        _1210,
        _1211,
    )
    from mastapy._private.gears.manufacturing.bevel.cutters import (
        _838,
        _839,
        _840,
        _841,
    )

    Self = TypeVar("Self", bound="ConicalGearCutter")
    CastSelf = TypeVar("CastSelf", bound="ConicalGearCutter._Cast_ConicalGearCutter")


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearCutter",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearCutter:
    """Special nested class for casting ConicalGearCutter to subclasses."""

    __parent__: "ConicalGearCutter"

    @property
    def pinion_finish_cutter(self: "CastSelf") -> "_838.PinionFinishCutter":
        from mastapy._private.gears.manufacturing.bevel.cutters import _838

        return self.__parent__._cast(_838.PinionFinishCutter)

    @property
    def pinion_rough_cutter(self: "CastSelf") -> "_839.PinionRoughCutter":
        from mastapy._private.gears.manufacturing.bevel.cutters import _839

        return self.__parent__._cast(_839.PinionRoughCutter)

    @property
    def wheel_finish_cutter(self: "CastSelf") -> "_840.WheelFinishCutter":
        from mastapy._private.gears.manufacturing.bevel.cutters import _840

        return self.__parent__._cast(_840.WheelFinishCutter)

    @property
    def wheel_rough_cutter(self: "CastSelf") -> "_841.WheelRoughCutter":
        from mastapy._private.gears.manufacturing.bevel.cutters import _841

        return self.__parent__._cast(_841.WheelRoughCutter)

    @property
    def dummy_conical_gear_cutter(self: "CastSelf") -> "_1203.DummyConicalGearCutter":
        from mastapy._private.gears.gear_designs.conical import _1203

        return self.__parent__._cast(_1203.DummyConicalGearCutter)

    @property
    def conical_gear_cutter(self: "CastSelf") -> "ConicalGearCutter":
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
class ConicalGearCutter(_0.APIBase):
    """ConicalGearCutter

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_CUTTER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def calculated_point_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CalculatedPointWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    def cutter_blade_type(self: "Self") -> "_1201.CutterBladeType":
        """mastapy.gears.gear_designs.conical.CutterBladeType"""
        temp = pythonnet_property_get(self.wrapped, "CutterBladeType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Conical.CutterBladeType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.conical._1201", "CutterBladeType"
        )(value)

    @cutter_blade_type.setter
    @enforce_parameter_types
    def cutter_blade_type(self: "Self", value: "_1201.CutterBladeType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.GearDesigns.Conical.CutterBladeType"
        )
        pythonnet_property_set(self.wrapped, "CutterBladeType", value)

    @property
    def cutter_gauge_length(self: "Self") -> "_1202.CutterGaugeLengths":
        """mastapy.gears.gear_designs.conical.CutterGaugeLengths"""
        temp = pythonnet_property_get(self.wrapped, "CutterGaugeLength")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Conical.CutterGaugeLengths"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.conical._1202", "CutterGaugeLengths"
        )(value)

    @cutter_gauge_length.setter
    @enforce_parameter_types
    def cutter_gauge_length(self: "Self", value: "_1202.CutterGaugeLengths") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.GearDesigns.Conical.CutterGaugeLengths"
        )
        pythonnet_property_set(self.wrapped, "CutterGaugeLength", value)

    @property
    def inner_blade_angle_convex(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerBladeAngleConvex")

        if temp is None:
            return 0.0

        return temp

    @inner_blade_angle_convex.setter
    @enforce_parameter_types
    def inner_blade_angle_convex(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InnerBladeAngleConvex",
            float(value) if value is not None else 0.0,
        )

    @property
    def inner_blade_point_radius_convex(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerBladePointRadiusConvex")

        if temp is None:
            return 0.0

        return temp

    @inner_blade_point_radius_convex.setter
    @enforce_parameter_types
    def inner_blade_point_radius_convex(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InnerBladePointRadiusConvex",
            float(value) if value is not None else 0.0,
        )

    @property
    def inner_edge_radius_convex(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerEdgeRadiusConvex")

        if temp is None:
            return 0.0

        return temp

    @inner_edge_radius_convex.setter
    @enforce_parameter_types
    def inner_edge_radius_convex(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InnerEdgeRadiusConvex",
            float(value) if value is not None else 0.0,
        )

    @property
    def inner_parabolic_apex_location_convex(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerParabolicApexLocationConvex")

        if temp is None:
            return 0.0

        return temp

    @inner_parabolic_apex_location_convex.setter
    @enforce_parameter_types
    def inner_parabolic_apex_location_convex(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InnerParabolicApexLocationConvex",
            float(value) if value is not None else 0.0,
        )

    @property
    def inner_parabolic_coefficient_convex(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerParabolicCoefficientConvex")

        if temp is None:
            return 0.0

        return temp

    @inner_parabolic_coefficient_convex.setter
    @enforce_parameter_types
    def inner_parabolic_coefficient_convex(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InnerParabolicCoefficientConvex",
            float(value) if value is not None else 0.0,
        )

    @property
    def inner_spherical_radius_convex(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerSphericalRadiusConvex")

        if temp is None:
            return 0.0

        return temp

    @inner_spherical_radius_convex.setter
    @enforce_parameter_types
    def inner_spherical_radius_convex(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InnerSphericalRadiusConvex",
            float(value) if value is not None else 0.0,
        )

    @property
    def inner_toprem_angle_convex(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerTopremAngleConvex")

        if temp is None:
            return 0.0

        return temp

    @inner_toprem_angle_convex.setter
    @enforce_parameter_types
    def inner_toprem_angle_convex(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InnerTopremAngleConvex",
            float(value) if value is not None else 0.0,
        )

    @property
    def inner_toprem_length_convex(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerTopremLengthConvex")

        if temp is None:
            return 0.0

        return temp

    @inner_toprem_length_convex.setter
    @enforce_parameter_types
    def inner_toprem_length_convex(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InnerTopremLengthConvex",
            float(value) if value is not None else 0.0,
        )

    @property
    def inner_toprem_letter_convex(self: "Self") -> "_1211.TopremLetter":
        """mastapy.gears.gear_designs.conical.TopremLetter"""
        temp = pythonnet_property_get(self.wrapped, "InnerTopremLetterConvex")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Conical.TopremLetter"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.conical._1211", "TopremLetter"
        )(value)

    @inner_toprem_letter_convex.setter
    @enforce_parameter_types
    def inner_toprem_letter_convex(self: "Self", value: "_1211.TopremLetter") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.GearDesigns.Conical.TopremLetter"
        )
        pythonnet_property_set(self.wrapped, "InnerTopremLetterConvex", value)

    @property
    def input_toprem_as(self: "Self") -> "_1210.TopremEntryType":
        """mastapy.gears.gear_designs.conical.TopremEntryType"""
        temp = pythonnet_property_get(self.wrapped, "InputTopremAs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Conical.TopremEntryType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.conical._1210", "TopremEntryType"
        )(value)

    @input_toprem_as.setter
    @enforce_parameter_types
    def input_toprem_as(self: "Self", value: "_1210.TopremEntryType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.GearDesigns.Conical.TopremEntryType"
        )
        pythonnet_property_set(self.wrapped, "InputTopremAs", value)

    @property
    def outer_blade_angle_concave(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterBladeAngleConcave")

        if temp is None:
            return 0.0

        return temp

    @outer_blade_angle_concave.setter
    @enforce_parameter_types
    def outer_blade_angle_concave(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OuterBladeAngleConcave",
            float(value) if value is not None else 0.0,
        )

    @property
    def outer_blade_point_radius_concave(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterBladePointRadiusConcave")

        if temp is None:
            return 0.0

        return temp

    @outer_blade_point_radius_concave.setter
    @enforce_parameter_types
    def outer_blade_point_radius_concave(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OuterBladePointRadiusConcave",
            float(value) if value is not None else 0.0,
        )

    @property
    def outer_edge_radius_concave(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterEdgeRadiusConcave")

        if temp is None:
            return 0.0

        return temp

    @outer_edge_radius_concave.setter
    @enforce_parameter_types
    def outer_edge_radius_concave(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OuterEdgeRadiusConcave",
            float(value) if value is not None else 0.0,
        )

    @property
    def outer_parabolic_apex_location_concave(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterParabolicApexLocationConcave")

        if temp is None:
            return 0.0

        return temp

    @outer_parabolic_apex_location_concave.setter
    @enforce_parameter_types
    def outer_parabolic_apex_location_concave(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OuterParabolicApexLocationConcave",
            float(value) if value is not None else 0.0,
        )

    @property
    def outer_parabolic_coefficient_concave(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterParabolicCoefficientConcave")

        if temp is None:
            return 0.0

        return temp

    @outer_parabolic_coefficient_concave.setter
    @enforce_parameter_types
    def outer_parabolic_coefficient_concave(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OuterParabolicCoefficientConcave",
            float(value) if value is not None else 0.0,
        )

    @property
    def outer_spherical_radius_concave(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterSphericalRadiusConcave")

        if temp is None:
            return 0.0

        return temp

    @outer_spherical_radius_concave.setter
    @enforce_parameter_types
    def outer_spherical_radius_concave(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OuterSphericalRadiusConcave",
            float(value) if value is not None else 0.0,
        )

    @property
    def outer_toprem_angle_concave(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterTopremAngleConcave")

        if temp is None:
            return 0.0

        return temp

    @outer_toprem_angle_concave.setter
    @enforce_parameter_types
    def outer_toprem_angle_concave(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OuterTopremAngleConcave",
            float(value) if value is not None else 0.0,
        )

    @property
    def outer_toprem_length_concave(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterTopremLengthConcave")

        if temp is None:
            return 0.0

        return temp

    @outer_toprem_length_concave.setter
    @enforce_parameter_types
    def outer_toprem_length_concave(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OuterTopremLengthConcave",
            float(value) if value is not None else 0.0,
        )

    @property
    def outer_toprem_letter_concave(self: "Self") -> "_1211.TopremLetter":
        """mastapy.gears.gear_designs.conical.TopremLetter"""
        temp = pythonnet_property_get(self.wrapped, "OuterTopremLetterConcave")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Conical.TopremLetter"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.conical._1211", "TopremLetter"
        )(value)

    @outer_toprem_letter_concave.setter
    @enforce_parameter_types
    def outer_toprem_letter_concave(self: "Self", value: "_1211.TopremLetter") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.GearDesigns.Conical.TopremLetter"
        )
        pythonnet_property_set(self.wrapped, "OuterTopremLetterConcave", value)

    @property
    def protuberance_at_concave_blade(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProtuberanceAtConcaveBlade")

        if temp is None:
            return 0.0

        return temp

    @protuberance_at_concave_blade.setter
    @enforce_parameter_types
    def protuberance_at_concave_blade(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProtuberanceAtConcaveBlade",
            float(value) if value is not None else 0.0,
        )

    @property
    def protuberance_at_convex_blade(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProtuberanceAtConvexBlade")

        if temp is None:
            return 0.0

        return temp

    @protuberance_at_convex_blade.setter
    @enforce_parameter_types
    def protuberance_at_convex_blade(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProtuberanceAtConvexBlade",
            float(value) if value is not None else 0.0,
        )

    @property
    def radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Radius")

        if temp is None:
            return 0.0

        return temp

    @radius.setter
    @enforce_parameter_types
    def radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Radius", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearCutter":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearCutter
        """
        return _Cast_ConicalGearCutter(self)
