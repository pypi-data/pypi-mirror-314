"""LoadedDetailedBearingResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.bearing_results import _2013

_LOADED_DETAILED_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults", "LoadedDetailedBearingResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _1930
    from mastapy._private.bearings.bearing_results import _2005
    from mastapy._private.bearings.bearing_results.fluid_film import (
        _2175,
        _2176,
        _2177,
        _2178,
        _2180,
        _2183,
        _2184,
    )
    from mastapy._private.bearings.bearing_results.rolling import (
        _2039,
        _2042,
        _2045,
        _2050,
        _2053,
        _2058,
        _2061,
        _2065,
        _2068,
        _2073,
        _2077,
        _2080,
        _2085,
        _2089,
        _2092,
        _2096,
        _2099,
        _2104,
        _2107,
        _2110,
        _2113,
    )
    from mastapy._private.materials import _280

    Self = TypeVar("Self", bound="LoadedDetailedBearingResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedDetailedBearingResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedDetailedBearingResults:
    """Special nested class for casting LoadedDetailedBearingResults to subclasses."""

    __parent__: "LoadedDetailedBearingResults"

    @property
    def loaded_non_linear_bearing_results(
        self: "CastSelf",
    ) -> "_2013.LoadedNonLinearBearingResults":
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
    def loaded_angular_contact_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2039.LoadedAngularContactBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2039

        return self.__parent__._cast(_2039.LoadedAngularContactBallBearingResults)

    @property
    def loaded_angular_contact_thrust_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2042.LoadedAngularContactThrustBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2042

        return self.__parent__._cast(_2042.LoadedAngularContactThrustBallBearingResults)

    @property
    def loaded_asymmetric_spherical_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2045.LoadedAsymmetricSphericalRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2045

        return self.__parent__._cast(
            _2045.LoadedAsymmetricSphericalRollerBearingResults
        )

    @property
    def loaded_axial_thrust_cylindrical_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2050.LoadedAxialThrustCylindricalRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2050

        return self.__parent__._cast(
            _2050.LoadedAxialThrustCylindricalRollerBearingResults
        )

    @property
    def loaded_axial_thrust_needle_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2053.LoadedAxialThrustNeedleRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2053

        return self.__parent__._cast(_2053.LoadedAxialThrustNeedleRollerBearingResults)

    @property
    def loaded_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2058.LoadedBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2058

        return self.__parent__._cast(_2058.LoadedBallBearingResults)

    @property
    def loaded_crossed_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2061.LoadedCrossedRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2061

        return self.__parent__._cast(_2061.LoadedCrossedRollerBearingResults)

    @property
    def loaded_cylindrical_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2065.LoadedCylindricalRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2065

        return self.__parent__._cast(_2065.LoadedCylindricalRollerBearingResults)

    @property
    def loaded_deep_groove_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2068.LoadedDeepGrooveBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2068

        return self.__parent__._cast(_2068.LoadedDeepGrooveBallBearingResults)

    @property
    def loaded_four_point_contact_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2073.LoadedFourPointContactBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2073

        return self.__parent__._cast(_2073.LoadedFourPointContactBallBearingResults)

    @property
    def loaded_needle_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2077.LoadedNeedleRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2077

        return self.__parent__._cast(_2077.LoadedNeedleRollerBearingResults)

    @property
    def loaded_non_barrel_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2080.LoadedNonBarrelRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2080

        return self.__parent__._cast(_2080.LoadedNonBarrelRollerBearingResults)

    @property
    def loaded_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2085.LoadedRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2085

        return self.__parent__._cast(_2085.LoadedRollerBearingResults)

    @property
    def loaded_rolling_bearing_results(
        self: "CastSelf",
    ) -> "_2089.LoadedRollingBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2089

        return self.__parent__._cast(_2089.LoadedRollingBearingResults)

    @property
    def loaded_self_aligning_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2092.LoadedSelfAligningBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2092

        return self.__parent__._cast(_2092.LoadedSelfAligningBallBearingResults)

    @property
    def loaded_spherical_roller_radial_bearing_results(
        self: "CastSelf",
    ) -> "_2096.LoadedSphericalRollerRadialBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2096

        return self.__parent__._cast(_2096.LoadedSphericalRollerRadialBearingResults)

    @property
    def loaded_spherical_roller_thrust_bearing_results(
        self: "CastSelf",
    ) -> "_2099.LoadedSphericalRollerThrustBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2099

        return self.__parent__._cast(_2099.LoadedSphericalRollerThrustBearingResults)

    @property
    def loaded_taper_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2104.LoadedTaperRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2104

        return self.__parent__._cast(_2104.LoadedTaperRollerBearingResults)

    @property
    def loaded_three_point_contact_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2107.LoadedThreePointContactBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2107

        return self.__parent__._cast(_2107.LoadedThreePointContactBallBearingResults)

    @property
    def loaded_thrust_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2110.LoadedThrustBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2110

        return self.__parent__._cast(_2110.LoadedThrustBallBearingResults)

    @property
    def loaded_toroidal_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2113.LoadedToroidalRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2113

        return self.__parent__._cast(_2113.LoadedToroidalRollerBearingResults)

    @property
    def loaded_fluid_film_bearing_results(
        self: "CastSelf",
    ) -> "_2175.LoadedFluidFilmBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2175

        return self.__parent__._cast(_2175.LoadedFluidFilmBearingResults)

    @property
    def loaded_grease_filled_journal_bearing_results(
        self: "CastSelf",
    ) -> "_2176.LoadedGreaseFilledJournalBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2176

        return self.__parent__._cast(_2176.LoadedGreaseFilledJournalBearingResults)

    @property
    def loaded_pad_fluid_film_bearing_results(
        self: "CastSelf",
    ) -> "_2177.LoadedPadFluidFilmBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2177

        return self.__parent__._cast(_2177.LoadedPadFluidFilmBearingResults)

    @property
    def loaded_plain_journal_bearing_results(
        self: "CastSelf",
    ) -> "_2178.LoadedPlainJournalBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2178

        return self.__parent__._cast(_2178.LoadedPlainJournalBearingResults)

    @property
    def loaded_plain_oil_fed_journal_bearing(
        self: "CastSelf",
    ) -> "_2180.LoadedPlainOilFedJournalBearing":
        from mastapy._private.bearings.bearing_results.fluid_film import _2180

        return self.__parent__._cast(_2180.LoadedPlainOilFedJournalBearing)

    @property
    def loaded_tilting_pad_journal_bearing_results(
        self: "CastSelf",
    ) -> "_2183.LoadedTiltingPadJournalBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2183

        return self.__parent__._cast(_2183.LoadedTiltingPadJournalBearingResults)

    @property
    def loaded_tilting_pad_thrust_bearing_results(
        self: "CastSelf",
    ) -> "_2184.LoadedTiltingPadThrustBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2184

        return self.__parent__._cast(_2184.LoadedTiltingPadThrustBearingResults)

    @property
    def loaded_detailed_bearing_results(
        self: "CastSelf",
    ) -> "LoadedDetailedBearingResults":
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
class LoadedDetailedBearingResults(_2013.LoadedNonLinearBearingResults):
    """LoadedDetailedBearingResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_DETAILED_BEARING_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def lubricant_flow_rate(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LubricantFlowRate")

        if temp is None:
            return 0.0

        return temp

    @lubricant_flow_rate.setter
    @enforce_parameter_types
    def lubricant_flow_rate(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LubricantFlowRate",
            float(value) if value is not None else 0.0,
        )

    @property
    def oil_sump_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OilSumpTemperature")

        if temp is None:
            return 0.0

        return temp

    @oil_sump_temperature.setter
    @enforce_parameter_types
    def oil_sump_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OilSumpTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    def operating_air_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OperatingAirTemperature")

        if temp is None:
            return 0.0

        return temp

    @operating_air_temperature.setter
    @enforce_parameter_types
    def operating_air_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OperatingAirTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    def temperature_when_assembled(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TemperatureWhenAssembled")

        if temp is None:
            return 0.0

        return temp

    @temperature_when_assembled.setter
    @enforce_parameter_types
    def temperature_when_assembled(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TemperatureWhenAssembled",
            float(value) if value is not None else 0.0,
        )

    @property
    def lubrication(self: "Self") -> "_280.LubricationDetail":
        """mastapy.materials.LubricationDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Lubrication")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedDetailedBearingResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedDetailedBearingResults
        """
        return _Cast_LoadedDetailedBearingResults(self)
