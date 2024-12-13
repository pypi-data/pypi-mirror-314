"""HobbingProcessProfileCalculation"""

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
from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
    _691,
)

_HOBBING_PROCESS_PROFILE_CALCULATION = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew",
    "HobbingProcessProfileCalculation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1058
    from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
        _687,
        _705,
    )
    from mastapy._private.utility_gui.charts import _1922

    Self = TypeVar("Self", bound="HobbingProcessProfileCalculation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HobbingProcessProfileCalculation._Cast_HobbingProcessProfileCalculation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HobbingProcessProfileCalculation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HobbingProcessProfileCalculation:
    """Special nested class for casting HobbingProcessProfileCalculation to subclasses."""

    __parent__: "HobbingProcessProfileCalculation"

    @property
    def hobbing_process_calculation(
        self: "CastSelf",
    ) -> "_691.HobbingProcessCalculation":
        return self.__parent__._cast(_691.HobbingProcessCalculation)

    @property
    def process_calculation(self: "CastSelf") -> "_705.ProcessCalculation":
        from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
            _705,
        )

        return self.__parent__._cast(_705.ProcessCalculation)

    @property
    def hobbing_process_profile_calculation(
        self: "CastSelf",
    ) -> "HobbingProcessProfileCalculation":
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
class HobbingProcessProfileCalculation(_691.HobbingProcessCalculation):
    """HobbingProcessProfileCalculation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HOBBING_PROCESS_PROFILE_CALCULATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def chart_display_method(
        self: "Self",
    ) -> "_1058.CylindricalGearProfileMeasurementType":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurementType"""
        temp = pythonnet_property_get(self.wrapped, "ChartDisplayMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.CylindricalGearProfileMeasurementType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1058",
            "CylindricalGearProfileMeasurementType",
        )(value)

    @chart_display_method.setter
    @enforce_parameter_types
    def chart_display_method(
        self: "Self", value: "_1058.CylindricalGearProfileMeasurementType"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.CylindricalGearProfileMeasurementType",
        )
        pythonnet_property_set(self.wrapped, "ChartDisplayMethod", value)

    @property
    def left_flank_profile_modification_chart(
        self: "Self",
    ) -> "_1922.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftFlankProfileModificationChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def number_of_profile_bands(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfProfileBands")

        if temp is None:
            return 0

        return temp

    @number_of_profile_bands.setter
    @enforce_parameter_types
    def number_of_profile_bands(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfProfileBands", int(value) if value is not None else 0
        )

    @property
    def result_z_plane(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ResultZPlane")

        if temp is None:
            return 0.0

        return temp

    @result_z_plane.setter
    @enforce_parameter_types
    def result_z_plane(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ResultZPlane", float(value) if value is not None else 0.0
        )

    @property
    def right_flank_profile_modification_chart(
        self: "Self",
    ) -> "_1922.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RightFlankProfileModificationChart"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def left_flank(self: "Self") -> "_687.CalculateProfileDeviationAccuracy":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.CalculateProfileDeviationAccuracy

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def right_flank(self: "Self") -> "_687.CalculateProfileDeviationAccuracy":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.CalculateProfileDeviationAccuracy

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_HobbingProcessProfileCalculation":
        """Cast to another type.

        Returns:
            _Cast_HobbingProcessProfileCalculation
        """
        return _Cast_HobbingProcessProfileCalculation(self)
