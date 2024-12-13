"""TaperRollerBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.bearing_designs.rolling import _2217

_TAPER_ROLLER_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "TaperRollerBearing"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings import _1931
    from mastapy._private.bearings.bearing_designs import _2186, _2187, _2190
    from mastapy._private.bearings.bearing_designs.rolling import _2218, _2221

    Self = TypeVar("Self", bound="TaperRollerBearing")
    CastSelf = TypeVar("CastSelf", bound="TaperRollerBearing._Cast_TaperRollerBearing")


__docformat__ = "restructuredtext en"
__all__ = ("TaperRollerBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TaperRollerBearing:
    """Special nested class for casting TaperRollerBearing to subclasses."""

    __parent__: "TaperRollerBearing"

    @property
    def non_barrel_roller_bearing(self: "CastSelf") -> "_2217.NonBarrelRollerBearing":
        return self.__parent__._cast(_2217.NonBarrelRollerBearing)

    @property
    def roller_bearing(self: "CastSelf") -> "_2218.RollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2218

        return self.__parent__._cast(_2218.RollerBearing)

    @property
    def rolling_bearing(self: "CastSelf") -> "_2221.RollingBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2221

        return self.__parent__._cast(_2221.RollingBearing)

    @property
    def detailed_bearing(self: "CastSelf") -> "_2187.DetailedBearing":
        from mastapy._private.bearings.bearing_designs import _2187

        return self.__parent__._cast(_2187.DetailedBearing)

    @property
    def non_linear_bearing(self: "CastSelf") -> "_2190.NonLinearBearing":
        from mastapy._private.bearings.bearing_designs import _2190

        return self.__parent__._cast(_2190.NonLinearBearing)

    @property
    def bearing_design(self: "CastSelf") -> "_2186.BearingDesign":
        from mastapy._private.bearings.bearing_designs import _2186

        return self.__parent__._cast(_2186.BearingDesign)

    @property
    def taper_roller_bearing(self: "CastSelf") -> "TaperRollerBearing":
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
class TaperRollerBearing(_2217.NonBarrelRollerBearing):
    """TaperRollerBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TAPER_ROLLER_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembled_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AssembledWidth")

        if temp is None:
            return 0.0

        return temp

    @assembled_width.setter
    @enforce_parameter_types
    def assembled_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "AssembledWidth", float(value) if value is not None else 0.0
        )

    @property
    def bearing_measurement_type(self: "Self") -> "_1931.BearingMeasurementType":
        """mastapy.bearings.BearingMeasurementType"""
        temp = pythonnet_property_get(self.wrapped, "BearingMeasurementType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.BearingMeasurementType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._1931", "BearingMeasurementType"
        )(value)

    @bearing_measurement_type.setter
    @enforce_parameter_types
    def bearing_measurement_type(
        self: "Self", value: "_1931.BearingMeasurementType"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.BearingMeasurementType"
        )
        pythonnet_property_set(self.wrapped, "BearingMeasurementType", value)

    @property
    def cone_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ConeAngle")

        if temp is None:
            return 0.0

        return temp

    @cone_angle.setter
    @enforce_parameter_types
    def cone_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ConeAngle", float(value) if value is not None else 0.0
        )

    @property
    def cup_angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CupAngle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cup_angle.setter
    @enforce_parameter_types
    def cup_angle(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CupAngle", value)

    @property
    def effective_centre_from_front_face(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EffectiveCentreFromFrontFace")

        if temp is None:
            return 0.0

        return temp

    @effective_centre_from_front_face.setter
    @enforce_parameter_types
    def effective_centre_from_front_face(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EffectiveCentreFromFrontFace",
            float(value) if value is not None else 0.0,
        )

    @property
    def effective_centre_to_front_face_set_by_changing_outer_ring_offset(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EffectiveCentreToFrontFaceSetByChangingOuterRingOffset"
        )

        if temp is None:
            return 0.0

        return temp

    @effective_centre_to_front_face_set_by_changing_outer_ring_offset.setter
    @enforce_parameter_types
    def effective_centre_to_front_face_set_by_changing_outer_ring_offset(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EffectiveCentreToFrontFaceSetByChangingOuterRingOffset",
            float(value) if value is not None else 0.0,
        )

    @property
    def element_taper_angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ElementTaperAngle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @element_taper_angle.setter
    @enforce_parameter_types
    def element_taper_angle(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ElementTaperAngle", value)

    @property
    def inner_ring_back_face_corner_radius(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerRingBackFaceCornerRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_ring_back_face_corner_radius.setter
    @enforce_parameter_types
    def inner_ring_back_face_corner_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InnerRingBackFaceCornerRadius", value)

    @property
    def inner_ring_front_face_corner_radius(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerRingFrontFaceCornerRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_ring_front_face_corner_radius.setter
    @enforce_parameter_types
    def inner_ring_front_face_corner_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InnerRingFrontFaceCornerRadius", value)

    @property
    def left_element_corner_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "LeftElementCornerRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @left_element_corner_radius.setter
    @enforce_parameter_types
    def left_element_corner_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "LeftElementCornerRadius", value)

    @property
    def mean_inner_race_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanInnerRaceDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def mean_outer_race_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanOuterRaceDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def outer_ring_back_face_corner_radius(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterRingBackFaceCornerRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_ring_back_face_corner_radius.setter
    @enforce_parameter_types
    def outer_ring_back_face_corner_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterRingBackFaceCornerRadius", value)

    @property
    def outer_ring_front_face_corner_radius(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterRingFrontFaceCornerRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_ring_front_face_corner_radius.setter
    @enforce_parameter_types
    def outer_ring_front_face_corner_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterRingFrontFaceCornerRadius", value)

    @property
    def right_element_corner_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RightElementCornerRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @right_element_corner_radius.setter
    @enforce_parameter_types
    def right_element_corner_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RightElementCornerRadius", value)

    @property
    def width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return temp

    @width.setter
    @enforce_parameter_types
    def width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", float(value) if value is not None else 0.0
        )

    @property
    def width_setting_inner_and_outer_ring_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "WidthSettingInnerAndOuterRingWidth"
        )

        if temp is None:
            return 0.0

        return temp

    @width_setting_inner_and_outer_ring_width.setter
    @enforce_parameter_types
    def width_setting_inner_and_outer_ring_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WidthSettingInnerAndOuterRingWidth",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_TaperRollerBearing":
        """Cast to another type.

        Returns:
            _Cast_TaperRollerBearing
        """
        return _Cast_TaperRollerBearing(self)
