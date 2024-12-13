"""LoadedPlainOilFedJournalBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results.fluid_film import _2178

_LOADED_PLAIN_OIL_FED_JOURNAL_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.FluidFilm", "LoadedPlainOilFedJournalBearing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _1930
    from mastapy._private.bearings.bearing_results import _2005, _2010, _2013
    from mastapy._private.bearings.bearing_results.fluid_film import _2175

    Self = TypeVar("Self", bound="LoadedPlainOilFedJournalBearing")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedPlainOilFedJournalBearing._Cast_LoadedPlainOilFedJournalBearing",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedPlainOilFedJournalBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedPlainOilFedJournalBearing:
    """Special nested class for casting LoadedPlainOilFedJournalBearing to subclasses."""

    __parent__: "LoadedPlainOilFedJournalBearing"

    @property
    def loaded_plain_journal_bearing_results(
        self: "CastSelf",
    ) -> "_2178.LoadedPlainJournalBearingResults":
        return self.__parent__._cast(_2178.LoadedPlainJournalBearingResults)

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
    def loaded_plain_oil_fed_journal_bearing(
        self: "CastSelf",
    ) -> "LoadedPlainOilFedJournalBearing":
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
class LoadedPlainOilFedJournalBearing(_2178.LoadedPlainJournalBearingResults):
    """LoadedPlainOilFedJournalBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_PLAIN_OIL_FED_JOURNAL_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def angle_between_oil_feed_inlet_and_minimum_film_thickness(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AngleBetweenOilFeedInletAndMinimumFilmThickness"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def angle_between_oil_feed_inlet_and_point_of_loading(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AngleBetweenOilFeedInletAndPointOfLoading"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def combined_flow_rate(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CombinedFlowRate")

        if temp is None:
            return 0.0

        return temp

    @property
    def current_oil_inlet_angular_position_from_the_x_axis(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CurrentOilInletAngularPositionFromTheXAxis"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def feed_pressure(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FeedPressure")

        if temp is None:
            return 0.0

        return temp

    @property
    def ideal_oil_inlet_angular_position_from_the_x_axis(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "IdealOilInletAngularPositionFromTheXAxis"
        )

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
    def pressure_flow_rate(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PressureFlowRate")

        if temp is None:
            return 0.0

        return temp

    @property
    def side_flow_rate(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SideFlowRate")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedPlainOilFedJournalBearing":
        """Cast to another type.

        Returns:
            _Cast_LoadedPlainOilFedJournalBearing
        """
        return _Cast_LoadedPlainOilFedJournalBearing(self)
