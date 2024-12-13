"""InterferenceDetail"""

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
from mastapy._private.bearings.tolerances import _1956

_INTERFERENCE_DETAIL = python_net_import(
    "SMT.MastaAPI.Bearings.Tolerances", "InterferenceDetail"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings.tolerances import _1966, _1971, _1975
    from mastapy._private.materials import _282

    Self = TypeVar("Self", bound="InterferenceDetail")
    CastSelf = TypeVar("CastSelf", bound="InterferenceDetail._Cast_InterferenceDetail")


__docformat__ = "restructuredtext en"
__all__ = ("InterferenceDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterferenceDetail:
    """Special nested class for casting InterferenceDetail to subclasses."""

    __parent__: "InterferenceDetail"

    @property
    def bearing_connection_component(
        self: "CastSelf",
    ) -> "_1956.BearingConnectionComponent":
        return self.__parent__._cast(_1956.BearingConnectionComponent)

    @property
    def mounting_sleeve_diameter_detail(
        self: "CastSelf",
    ) -> "_1966.MountingSleeveDiameterDetail":
        from mastapy._private.bearings.tolerances import _1966

        return self.__parent__._cast(_1966.MountingSleeveDiameterDetail)

    @property
    def ring_detail(self: "CastSelf") -> "_1971.RingDetail":
        from mastapy._private.bearings.tolerances import _1971

        return self.__parent__._cast(_1971.RingDetail)

    @property
    def support_detail(self: "CastSelf") -> "_1975.SupportDetail":
        from mastapy._private.bearings.tolerances import _1975

        return self.__parent__._cast(_1975.SupportDetail)

    @property
    def interference_detail(self: "CastSelf") -> "InterferenceDetail":
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
class InterferenceDetail(_1956.BearingConnectionComponent):
    """InterferenceDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INTERFERENCE_DETAIL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def diameter_tolerance_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "DiameterToleranceFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @diameter_tolerance_factor.setter
    @enforce_parameter_types
    def diameter_tolerance_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DiameterToleranceFactor", value)

    @property
    def temperature(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Temperature")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @temperature.setter
    @enforce_parameter_types
    def temperature(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Temperature", value)

    @property
    def material(self: "Self") -> "_282.Material":
        """mastapy.materials.Material

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Material")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_InterferenceDetail":
        """Cast to another type.

        Returns:
            _Cast_InterferenceDetail
        """
        return _Cast_InterferenceDetail(self)
