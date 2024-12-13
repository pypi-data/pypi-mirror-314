"""RelativeMeasurementViewModel"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import

_RELATIVE_MEASUREMENT_VIEW_MODEL = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "RelativeMeasurementViewModel"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.gears.gear_designs.cylindrical import _1069, _1072, _1117
    from mastapy._private.gears.gear_designs.cylindrical.thickness_stock_and_backlash import (
        _1125,
        _1126,
    )

    Self = TypeVar("Self", bound="RelativeMeasurementViewModel")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RelativeMeasurementViewModel._Cast_RelativeMeasurementViewModel",
    )

T = TypeVar("T")

__docformat__ = "restructuredtext en"
__all__ = ("RelativeMeasurementViewModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RelativeMeasurementViewModel:
    """Special nested class for casting RelativeMeasurementViewModel to subclasses."""

    __parent__: "RelativeMeasurementViewModel"

    @property
    def cylindrical_mesh_angular_backlash(
        self: "CastSelf",
    ) -> "_1069.CylindricalMeshAngularBacklash":
        from mastapy._private.gears.gear_designs.cylindrical import _1069

        return self.__parent__._cast(_1069.CylindricalMeshAngularBacklash)

    @property
    def cylindrical_mesh_linear_backlash_specification(
        self: "CastSelf",
    ) -> "_1072.CylindricalMeshLinearBacklashSpecification":
        from mastapy._private.gears.gear_designs.cylindrical import _1072

        return self.__parent__._cast(_1072.CylindricalMeshLinearBacklashSpecification)

    @property
    def toleranced_value_specification(
        self: "CastSelf",
    ) -> "_1117.TolerancedValueSpecification":
        from mastapy._private.gears.gear_designs.cylindrical import _1117

        return self.__parent__._cast(_1117.TolerancedValueSpecification)

    @property
    def nominal_value_specification(
        self: "CastSelf",
    ) -> "_1125.NominalValueSpecification":
        from mastapy._private.gears.gear_designs.cylindrical.thickness_stock_and_backlash import (
            _1125,
        )

        return self.__parent__._cast(_1125.NominalValueSpecification)

    @property
    def no_value_specification(self: "CastSelf") -> "_1126.NoValueSpecification":
        from mastapy._private.gears.gear_designs.cylindrical.thickness_stock_and_backlash import (
            _1126,
        )

        return self.__parent__._cast(_1126.NoValueSpecification)

    @property
    def relative_measurement_view_model(
        self: "CastSelf",
    ) -> "RelativeMeasurementViewModel":
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
class RelativeMeasurementViewModel(_0.APIBase, Generic[T]):
    """RelativeMeasurementViewModel

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _RELATIVE_MEASUREMENT_VIEW_MODEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_RelativeMeasurementViewModel":
        """Cast to another type.

        Returns:
            _Cast_RelativeMeasurementViewModel
        """
        return _Cast_RelativeMeasurementViewModel(self)
