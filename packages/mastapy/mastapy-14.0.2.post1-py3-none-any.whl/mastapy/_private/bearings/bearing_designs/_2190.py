"""NonLinearBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_designs import _2186

_NON_LINEAR_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns", "NonLinearBearing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_designs import _2187
    from mastapy._private.bearings.bearing_designs.concept import _2254, _2255, _2256
    from mastapy._private.bearings.bearing_designs.fluid_film import (
        _2244,
        _2246,
        _2248,
        _2250,
        _2251,
        _2252,
    )
    from mastapy._private.bearings.bearing_designs.rolling import (
        _2191,
        _2192,
        _2193,
        _2194,
        _2195,
        _2196,
        _2198,
        _2204,
        _2205,
        _2206,
        _2210,
        _2215,
        _2216,
        _2217,
        _2218,
        _2221,
        _2223,
        _2226,
        _2227,
        _2228,
        _2229,
        _2230,
        _2231,
    )

    Self = TypeVar("Self", bound="NonLinearBearing")
    CastSelf = TypeVar("CastSelf", bound="NonLinearBearing._Cast_NonLinearBearing")


__docformat__ = "restructuredtext en"
__all__ = ("NonLinearBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NonLinearBearing:
    """Special nested class for casting NonLinearBearing to subclasses."""

    __parent__: "NonLinearBearing"

    @property
    def bearing_design(self: "CastSelf") -> "_2186.BearingDesign":
        return self.__parent__._cast(_2186.BearingDesign)

    @property
    def detailed_bearing(self: "CastSelf") -> "_2187.DetailedBearing":
        from mastapy._private.bearings.bearing_designs import _2187

        return self.__parent__._cast(_2187.DetailedBearing)

    @property
    def angular_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2191.AngularContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2191

        return self.__parent__._cast(_2191.AngularContactBallBearing)

    @property
    def angular_contact_thrust_ball_bearing(
        self: "CastSelf",
    ) -> "_2192.AngularContactThrustBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2192

        return self.__parent__._cast(_2192.AngularContactThrustBallBearing)

    @property
    def asymmetric_spherical_roller_bearing(
        self: "CastSelf",
    ) -> "_2193.AsymmetricSphericalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2193

        return self.__parent__._cast(_2193.AsymmetricSphericalRollerBearing)

    @property
    def axial_thrust_cylindrical_roller_bearing(
        self: "CastSelf",
    ) -> "_2194.AxialThrustCylindricalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2194

        return self.__parent__._cast(_2194.AxialThrustCylindricalRollerBearing)

    @property
    def axial_thrust_needle_roller_bearing(
        self: "CastSelf",
    ) -> "_2195.AxialThrustNeedleRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2195

        return self.__parent__._cast(_2195.AxialThrustNeedleRollerBearing)

    @property
    def ball_bearing(self: "CastSelf") -> "_2196.BallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2196

        return self.__parent__._cast(_2196.BallBearing)

    @property
    def barrel_roller_bearing(self: "CastSelf") -> "_2198.BarrelRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2198

        return self.__parent__._cast(_2198.BarrelRollerBearing)

    @property
    def crossed_roller_bearing(self: "CastSelf") -> "_2204.CrossedRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2204

        return self.__parent__._cast(_2204.CrossedRollerBearing)

    @property
    def cylindrical_roller_bearing(
        self: "CastSelf",
    ) -> "_2205.CylindricalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2205

        return self.__parent__._cast(_2205.CylindricalRollerBearing)

    @property
    def deep_groove_ball_bearing(self: "CastSelf") -> "_2206.DeepGrooveBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2206

        return self.__parent__._cast(_2206.DeepGrooveBallBearing)

    @property
    def four_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2210.FourPointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2210

        return self.__parent__._cast(_2210.FourPointContactBallBearing)

    @property
    def multi_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2215.MultiPointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2215

        return self.__parent__._cast(_2215.MultiPointContactBallBearing)

    @property
    def needle_roller_bearing(self: "CastSelf") -> "_2216.NeedleRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2216

        return self.__parent__._cast(_2216.NeedleRollerBearing)

    @property
    def non_barrel_roller_bearing(self: "CastSelf") -> "_2217.NonBarrelRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2217

        return self.__parent__._cast(_2217.NonBarrelRollerBearing)

    @property
    def roller_bearing(self: "CastSelf") -> "_2218.RollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2218

        return self.__parent__._cast(_2218.RollerBearing)

    @property
    def rolling_bearing(self: "CastSelf") -> "_2221.RollingBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2221

        return self.__parent__._cast(_2221.RollingBearing)

    @property
    def self_aligning_ball_bearing(self: "CastSelf") -> "_2223.SelfAligningBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2223

        return self.__parent__._cast(_2223.SelfAligningBallBearing)

    @property
    def spherical_roller_bearing(self: "CastSelf") -> "_2226.SphericalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2226

        return self.__parent__._cast(_2226.SphericalRollerBearing)

    @property
    def spherical_roller_thrust_bearing(
        self: "CastSelf",
    ) -> "_2227.SphericalRollerThrustBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2227

        return self.__parent__._cast(_2227.SphericalRollerThrustBearing)

    @property
    def taper_roller_bearing(self: "CastSelf") -> "_2228.TaperRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2228

        return self.__parent__._cast(_2228.TaperRollerBearing)

    @property
    def three_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2229.ThreePointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2229

        return self.__parent__._cast(_2229.ThreePointContactBallBearing)

    @property
    def thrust_ball_bearing(self: "CastSelf") -> "_2230.ThrustBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2230

        return self.__parent__._cast(_2230.ThrustBallBearing)

    @property
    def toroidal_roller_bearing(self: "CastSelf") -> "_2231.ToroidalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2231

        return self.__parent__._cast(_2231.ToroidalRollerBearing)

    @property
    def pad_fluid_film_bearing(self: "CastSelf") -> "_2244.PadFluidFilmBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2244

        return self.__parent__._cast(_2244.PadFluidFilmBearing)

    @property
    def plain_grease_filled_journal_bearing(
        self: "CastSelf",
    ) -> "_2246.PlainGreaseFilledJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2246

        return self.__parent__._cast(_2246.PlainGreaseFilledJournalBearing)

    @property
    def plain_journal_bearing(self: "CastSelf") -> "_2248.PlainJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2248

        return self.__parent__._cast(_2248.PlainJournalBearing)

    @property
    def plain_oil_fed_journal_bearing(
        self: "CastSelf",
    ) -> "_2250.PlainOilFedJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2250

        return self.__parent__._cast(_2250.PlainOilFedJournalBearing)

    @property
    def tilting_pad_journal_bearing(
        self: "CastSelf",
    ) -> "_2251.TiltingPadJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2251

        return self.__parent__._cast(_2251.TiltingPadJournalBearing)

    @property
    def tilting_pad_thrust_bearing(self: "CastSelf") -> "_2252.TiltingPadThrustBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2252

        return self.__parent__._cast(_2252.TiltingPadThrustBearing)

    @property
    def concept_axial_clearance_bearing(
        self: "CastSelf",
    ) -> "_2254.ConceptAxialClearanceBearing":
        from mastapy._private.bearings.bearing_designs.concept import _2254

        return self.__parent__._cast(_2254.ConceptAxialClearanceBearing)

    @property
    def concept_clearance_bearing(self: "CastSelf") -> "_2255.ConceptClearanceBearing":
        from mastapy._private.bearings.bearing_designs.concept import _2255

        return self.__parent__._cast(_2255.ConceptClearanceBearing)

    @property
    def concept_radial_clearance_bearing(
        self: "CastSelf",
    ) -> "_2256.ConceptRadialClearanceBearing":
        from mastapy._private.bearings.bearing_designs.concept import _2256

        return self.__parent__._cast(_2256.ConceptRadialClearanceBearing)

    @property
    def non_linear_bearing(self: "CastSelf") -> "NonLinearBearing":
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
class NonLinearBearing(_2186.BearingDesign):
    """NonLinearBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NON_LINEAR_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_NonLinearBearing":
        """Cast to another type.

        Returns:
            _Cast_NonLinearBearing
        """
        return _Cast_NonLinearBearing(self)
