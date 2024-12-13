"""LoadedPlainJournalBearingResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.bearing_results.fluid_film import _2175

_LOADED_PLAIN_JOURNAL_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.FluidFilm", "LoadedPlainJournalBearingResults"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings import _1930
    from mastapy._private.bearings.bearing_results import _2005, _2010, _2013
    from mastapy._private.bearings.bearing_results.fluid_film import _2176, _2179, _2180

    Self = TypeVar("Self", bound="LoadedPlainJournalBearingResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedPlainJournalBearingResults._Cast_LoadedPlainJournalBearingResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedPlainJournalBearingResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedPlainJournalBearingResults:
    """Special nested class for casting LoadedPlainJournalBearingResults to subclasses."""

    __parent__: "LoadedPlainJournalBearingResults"

    @property
    def loaded_fluid_film_bearing_results(
        self: "CastSelf",
    ) -> "_2175.LoadedFluidFilmBearingResults":
        return self.__parent__._cast(_2175.LoadedFluidFilmBearingResults)

    @property
    def loaded_detailed_bearing_results(
        self: "CastSelf",
    ) -> "_2010.LoadedDetailedBearingResults":
        from mastapy._private.bearings.bearing_results import _2010

        return self.__parent__._cast(_2010.LoadedDetailedBearingResults)

    @property
    def loaded_non_linear_bearing_results(
        self: "CastSelf",
    ) -> "_2013.LoadedNonLinearBearingResults":
        from mastapy._private.bearings.bearing_results import _2013

        return self.__parent__._cast(_2013.LoadedNonLinearBearingResults)

    @property
    def loaded_bearing_results(self: "CastSelf") -> "_2005.LoadedBearingResults":
        from mastapy._private.bearings.bearing_results import _2005

        return self.__parent__._cast(_2005.LoadedBearingResults)

    @property
    def bearing_load_case_results_lightweight(
        self: "CastSelf",
    ) -> "_1930.BearingLoadCaseResultsLightweight":
        from mastapy._private.bearings import _1930

        return self.__parent__._cast(_1930.BearingLoadCaseResultsLightweight)

    @property
    def loaded_grease_filled_journal_bearing_results(
        self: "CastSelf",
    ) -> "_2176.LoadedGreaseFilledJournalBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2176

        return self.__parent__._cast(_2176.LoadedGreaseFilledJournalBearingResults)

    @property
    def loaded_plain_oil_fed_journal_bearing(
        self: "CastSelf",
    ) -> "_2180.LoadedPlainOilFedJournalBearing":
        from mastapy._private.bearings.bearing_results.fluid_film import _2180

        return self.__parent__._cast(_2180.LoadedPlainOilFedJournalBearing)

    @property
    def loaded_plain_journal_bearing_results(
        self: "CastSelf",
    ) -> "LoadedPlainJournalBearingResults":
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
class LoadedPlainJournalBearingResults(_2175.LoadedFluidFilmBearingResults):
    """LoadedPlainJournalBearingResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_PLAIN_JOURNAL_BEARING_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def angular_position_of_the_minimum_film_thickness_from_the_x_axis(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AngularPositionOfTheMinimumFilmThicknessFromTheXAxis"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def attitude_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AttitudeAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def attitude_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AttitudeForce")

        if temp is None:
            return 0.0

        return temp

    @property
    def diametrical_clearance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DiametricalClearance")

        if temp is None:
            return 0.0

        return temp

    @property
    def eccentricity_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EccentricityRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    def kinematic_viscosity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KinematicViscosity")

        if temp is None:
            return 0.0

        return temp

    @property
    def lubricant_density(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricantDensity")

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_central_film_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumCentralFilmThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    def non_dimensional_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NonDimensionalLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    def non_dimensional_power_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NonDimensionalPowerLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    def operating_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OperatingTemperature")

        if temp is None:
            return 0.0

        return temp

    @operating_temperature.setter
    @enforce_parameter_types
    def operating_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OperatingTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    def pressure_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PressureVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    def radial_load_per_unit_of_projected_area(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadialLoadPerUnitOfProjectedArea")

        if temp is None:
            return 0.0

        return temp

    @property
    def shaft_relative_rotation_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftRelativeRotationSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    def journal_bearing_rows(
        self: "Self",
    ) -> "List[_2179.LoadedPlainJournalBearingRow]":
        """List[mastapy.bearings.bearing_results.fluid_film.LoadedPlainJournalBearingRow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "JournalBearingRows")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedPlainJournalBearingResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedPlainJournalBearingResults
        """
        return _Cast_LoadedPlainJournalBearingResults(self)
