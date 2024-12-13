"""TiltingPadJournalBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
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
from mastapy._private.bearings.bearing_designs.fluid_film import _2244

_TILTING_PAD_JOURNAL_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm", "TiltingPadJournalBearing"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings.bearing_designs import _2186, _2187, _2190

    Self = TypeVar("Self", bound="TiltingPadJournalBearing")
    CastSelf = TypeVar(
        "CastSelf", bound="TiltingPadJournalBearing._Cast_TiltingPadJournalBearing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TiltingPadJournalBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TiltingPadJournalBearing:
    """Special nested class for casting TiltingPadJournalBearing to subclasses."""

    __parent__: "TiltingPadJournalBearing"

    @property
    def pad_fluid_film_bearing(self: "CastSelf") -> "_2244.PadFluidFilmBearing":
        return self.__parent__._cast(_2244.PadFluidFilmBearing)

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
    def tilting_pad_journal_bearing(self: "CastSelf") -> "TiltingPadJournalBearing":
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
class TiltingPadJournalBearing(_2244.PadFluidFilmBearing):
    """TiltingPadJournalBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TILTING_PAD_JOURNAL_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def bearing_aspect_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BearingAspectRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    def difference_between_pad_contact_surface_radius_and_bearing_inner_radius(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "DifferenceBetweenPadContactSurfaceRadiusAndBearingInnerRadius",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def pad_contact_surface_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "PadContactSurfaceRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @pad_contact_surface_radius.setter
    @enforce_parameter_types
    def pad_contact_surface_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "PadContactSurfaceRadius", value)

    @property
    def pivot_angular_offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PivotAngularOffset")

        if temp is None:
            return 0.0

        return temp

    @pivot_angular_offset.setter
    @enforce_parameter_types
    def pivot_angular_offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PivotAngularOffset",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_TiltingPadJournalBearing":
        """Cast to another type.

        Returns:
            _Cast_TiltingPadJournalBearing
        """
        return _Cast_TiltingPadJournalBearing(self)
