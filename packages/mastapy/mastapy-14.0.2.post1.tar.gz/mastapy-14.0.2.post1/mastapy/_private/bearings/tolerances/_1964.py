"""InterferenceTolerance"""

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
from mastapy._private.bearings.tolerances import _1956

_INTERFERENCE_TOLERANCE = python_net_import(
    "SMT.MastaAPI.Bearings.Tolerances", "InterferenceTolerance"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings import _1943
    from mastapy._private.bearings.tolerances import (
        _1959,
        _1961,
        _1962,
        _1967,
        _1968,
        _1972,
        _1977,
    )

    Self = TypeVar("Self", bound="InterferenceTolerance")
    CastSelf = TypeVar(
        "CastSelf", bound="InterferenceTolerance._Cast_InterferenceTolerance"
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterferenceTolerance",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterferenceTolerance:
    """Special nested class for casting InterferenceTolerance to subclasses."""

    __parent__: "InterferenceTolerance"

    @property
    def bearing_connection_component(
        self: "CastSelf",
    ) -> "_1956.BearingConnectionComponent":
        return self.__parent__._cast(_1956.BearingConnectionComponent)

    @property
    def inner_ring_tolerance(self: "CastSelf") -> "_1961.InnerRingTolerance":
        from mastapy._private.bearings.tolerances import _1961

        return self.__parent__._cast(_1961.InnerRingTolerance)

    @property
    def inner_support_tolerance(self: "CastSelf") -> "_1962.InnerSupportTolerance":
        from mastapy._private.bearings.tolerances import _1962

        return self.__parent__._cast(_1962.InnerSupportTolerance)

    @property
    def outer_ring_tolerance(self: "CastSelf") -> "_1967.OuterRingTolerance":
        from mastapy._private.bearings.tolerances import _1967

        return self.__parent__._cast(_1967.OuterRingTolerance)

    @property
    def outer_support_tolerance(self: "CastSelf") -> "_1968.OuterSupportTolerance":
        from mastapy._private.bearings.tolerances import _1968

        return self.__parent__._cast(_1968.OuterSupportTolerance)

    @property
    def ring_tolerance(self: "CastSelf") -> "_1972.RingTolerance":
        from mastapy._private.bearings.tolerances import _1972

        return self.__parent__._cast(_1972.RingTolerance)

    @property
    def support_tolerance(self: "CastSelf") -> "_1977.SupportTolerance":
        from mastapy._private.bearings.tolerances import _1977

        return self.__parent__._cast(_1977.SupportTolerance)

    @property
    def interference_tolerance(self: "CastSelf") -> "InterferenceTolerance":
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
class InterferenceTolerance(_1956.BearingConnectionComponent):
    """InterferenceTolerance

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INTERFERENCE_TOLERANCE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def definition_option(self: "Self") -> "_1959.BearingToleranceDefinitionOptions":
        """mastapy.bearings.tolerances.BearingToleranceDefinitionOptions"""
        temp = pythonnet_property_get(self.wrapped, "DefinitionOption")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.Tolerances.BearingToleranceDefinitionOptions"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.tolerances._1959",
            "BearingToleranceDefinitionOptions",
        )(value)

    @definition_option.setter
    @enforce_parameter_types
    def definition_option(
        self: "Self", value: "_1959.BearingToleranceDefinitionOptions"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.Tolerances.BearingToleranceDefinitionOptions"
        )
        pythonnet_property_set(self.wrapped, "DefinitionOption", value)

    @property
    def mounting_point_surface_finish(
        self: "Self",
    ) -> "_1943.MountingPointSurfaceFinishes":
        """mastapy.bearings.MountingPointSurfaceFinishes"""
        temp = pythonnet_property_get(self.wrapped, "MountingPointSurfaceFinish")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.MountingPointSurfaceFinishes"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._1943", "MountingPointSurfaceFinishes"
        )(value)

    @mounting_point_surface_finish.setter
    @enforce_parameter_types
    def mounting_point_surface_finish(
        self: "Self", value: "_1943.MountingPointSurfaceFinishes"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.MountingPointSurfaceFinishes"
        )
        pythonnet_property_set(self.wrapped, "MountingPointSurfaceFinish", value)

    @property
    def non_contacting_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "NonContactingDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @non_contacting_diameter.setter
    @enforce_parameter_types
    def non_contacting_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NonContactingDiameter", value)

    @property
    def surface_fitting_reduction(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SurfaceFittingReduction")

        if temp is None:
            return 0.0

        return temp

    @surface_fitting_reduction.setter
    @enforce_parameter_types
    def surface_fitting_reduction(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SurfaceFittingReduction",
            float(value) if value is not None else 0.0,
        )

    @property
    def tolerance_lower_limit(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ToleranceLowerLimit")

        if temp is None:
            return 0.0

        return temp

    @tolerance_lower_limit.setter
    @enforce_parameter_types
    def tolerance_lower_limit(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ToleranceLowerLimit",
            float(value) if value is not None else 0.0,
        )

    @property
    def tolerance_upper_limit(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ToleranceUpperLimit")

        if temp is None:
            return 0.0

        return temp

    @tolerance_upper_limit.setter
    @enforce_parameter_types
    def tolerance_upper_limit(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ToleranceUpperLimit",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_InterferenceTolerance":
        """Cast to another type.

        Returns:
            _Cast_InterferenceTolerance
        """
        return _Cast_InterferenceTolerance(self)
