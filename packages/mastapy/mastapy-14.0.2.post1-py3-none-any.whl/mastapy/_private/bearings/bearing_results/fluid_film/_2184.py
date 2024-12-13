"""LoadedTiltingPadThrustBearingResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.bearing_results.fluid_film import _2177

_LOADED_TILTING_PAD_THRUST_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.FluidFilm",
    "LoadedTiltingPadThrustBearingResults",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _1930
    from mastapy._private.bearings.bearing_results import _2005, _2010, _2013
    from mastapy._private.bearings.bearing_results.fluid_film import _2175

    Self = TypeVar("Self", bound="LoadedTiltingPadThrustBearingResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedTiltingPadThrustBearingResults._Cast_LoadedTiltingPadThrustBearingResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedTiltingPadThrustBearingResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedTiltingPadThrustBearingResults:
    """Special nested class for casting LoadedTiltingPadThrustBearingResults to subclasses."""

    __parent__: "LoadedTiltingPadThrustBearingResults"

    @property
    def loaded_pad_fluid_film_bearing_results(
        self: "CastSelf",
    ) -> "_2177.LoadedPadFluidFilmBearingResults":
        return self.__parent__._cast(_2177.LoadedPadFluidFilmBearingResults)

    @property
    def loaded_fluid_film_bearing_results(
        self: "CastSelf",
    ) -> "_2175.LoadedFluidFilmBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2175

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
    def loaded_tilting_pad_thrust_bearing_results(
        self: "CastSelf",
    ) -> "LoadedTiltingPadThrustBearingResults":
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
class LoadedTiltingPadThrustBearingResults(_2177.LoadedPadFluidFilmBearingResults):
    """LoadedTiltingPadThrustBearingResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_TILTING_PAD_THRUST_BEARING_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def average_pad_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AveragePadLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    def axial_internal_clearance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AxialInternalClearance")

        if temp is None:
            return 0.0

        return temp

    @axial_internal_clearance.setter
    @enforce_parameter_types
    def axial_internal_clearance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AxialInternalClearance",
            float(value) if value is not None else 0.0,
        )

    @property
    def maximum_bearing_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumBearingTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_pad_film_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumPadFilmTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_pad_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumPadLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_pad_specific_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumPadSpecificLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_pressure_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumPressureVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_reynolds_number(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumReynoldsNumber")

        if temp is None:
            return 0.0

        return temp

    @property
    def mean_reynolds_number(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanReynoldsNumber")

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_film_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumFilmThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_flow_rate(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumFlowRate")

        if temp is None:
            return 0.0

        return temp

    @property
    def oil_exit_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OilExitTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedTiltingPadThrustBearingResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedTiltingPadThrustBearingResults
        """
        return _Cast_LoadedTiltingPadThrustBearingResults(self)
