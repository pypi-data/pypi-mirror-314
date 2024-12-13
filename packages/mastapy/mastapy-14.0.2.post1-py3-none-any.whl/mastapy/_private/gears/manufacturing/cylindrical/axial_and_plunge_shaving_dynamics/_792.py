"""ShavingDynamicsCalculationForDesignedGears"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.cylindrical import _1057
from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
    _791,
)

_REPORTING_OVERRIDABLE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "ReportingOverridable"
)
_SHAVING_DYNAMICS_CALCULATION_FOR_DESIGNED_GEARS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics",
    "ShavingDynamicsCalculationForDesignedGears",
)

if TYPE_CHECKING:
    from typing import Any, List, Type

    from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
        _777,
        _783,
        _786,
        _789,
        _790,
    )
    from mastapy._private.utility_gui.charts import _1922

    Self = TypeVar("Self", bound="ShavingDynamicsCalculationForDesignedGears")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShavingDynamicsCalculationForDesignedGears._Cast_ShavingDynamicsCalculationForDesignedGears",
    )

T = TypeVar("T", bound="_790.ShavingDynamics")

__docformat__ = "restructuredtext en"
__all__ = ("ShavingDynamicsCalculationForDesignedGears",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShavingDynamicsCalculationForDesignedGears:
    """Special nested class for casting ShavingDynamicsCalculationForDesignedGears to subclasses."""

    __parent__: "ShavingDynamicsCalculationForDesignedGears"

    @property
    def shaving_dynamics_calculation(
        self: "CastSelf",
    ) -> "_791.ShavingDynamicsCalculation":
        return self.__parent__._cast(_791.ShavingDynamicsCalculation)

    @property
    def conventional_shaving_dynamics_calculation_for_designed_gears(
        self: "CastSelf",
    ) -> "_777.ConventionalShavingDynamicsCalculationForDesignedGears":
        from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
            _777,
        )

        return self.__parent__._cast(
            _777.ConventionalShavingDynamicsCalculationForDesignedGears
        )

    @property
    def plunge_shaving_dynamics_calculation_for_designed_gears(
        self: "CastSelf",
    ) -> "_783.PlungeShavingDynamicsCalculationForDesignedGears":
        from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
            _783,
        )

        return self.__parent__._cast(
            _783.PlungeShavingDynamicsCalculationForDesignedGears
        )

    @property
    def shaving_dynamics_calculation_for_designed_gears(
        self: "CastSelf",
    ) -> "ShavingDynamicsCalculationForDesignedGears":
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
class ShavingDynamicsCalculationForDesignedGears(_791.ShavingDynamicsCalculation[T]):
    """ShavingDynamicsCalculationForDesignedGears

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _SHAVING_DYNAMICS_CALCULATION_FOR_DESIGNED_GEARS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def redressing_chart(self: "Self") -> "_1922.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RedressingChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def selected_redressing(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_T":
        """ListWithSelectedItem[T]"""
        temp = pythonnet_property_get(self.wrapped, "SelectedRedressing")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_T",
        )(temp)

    @selected_redressing.setter
    @enforce_parameter_types
    def selected_redressing(self: "Self", value: "T") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_T.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_T.implicit_type()
        value = wrapper_type[enclosed_type](value if value is not None else None)
        pythonnet_property_set(self.wrapped, "SelectedRedressing", value)

    @property
    def end_of_shaving_profile(
        self: "Self",
    ) -> "_1057.CylindricalGearProfileMeasurement":
        """mastapy.mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get_with_method(
            self.wrapped, "EndOfShavingProfile", "Value"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def redressing(self: "Self") -> "_789.ShaverRedressing[T]":
        """mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics.ShaverRedressing[T]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Redressing")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[T](temp)

    @property
    def start_of_shaving_profile(
        self: "Self",
    ) -> "_1057.CylindricalGearProfileMeasurement":
        """mastapy.mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get_with_method(
            self.wrapped, "StartOfShavingProfile", "Value"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def redressing_settings(self: "Self") -> "List[_786.RedressingSettings[T]]":
        """List[mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics.RedressingSettings[T]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RedressingSettings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ShavingDynamicsCalculationForDesignedGears":
        """Cast to another type.

        Returns:
            _Cast_ShavingDynamicsCalculationForDesignedGears
        """
        return _Cast_ShavingDynamicsCalculationForDesignedGears(self)
