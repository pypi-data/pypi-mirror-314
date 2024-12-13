"""AGMA20151A01AccuracyGrader"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
    _1177,
)

_AGMA20151A01_ACCURACY_GRADER = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.AccuracyAndTolerances",
    "AGMA20151A01AccuracyGrader",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
        _1176,
        _1185,
    )

    Self = TypeVar("Self", bound="AGMA20151A01AccuracyGrader")
    CastSelf = TypeVar(
        "CastSelf", bound="AGMA20151A01AccuracyGrader._Cast_AGMA20151A01AccuracyGrader"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMA20151A01AccuracyGrader",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMA20151A01AccuracyGrader:
    """Special nested class for casting AGMA20151A01AccuracyGrader to subclasses."""

    __parent__: "AGMA20151A01AccuracyGrader"

    @property
    def cylindrical_accuracy_grader_with_profile_form_and_slope(
        self: "CastSelf",
    ) -> "_1177.CylindricalAccuracyGraderWithProfileFormAndSlope":
        return self.__parent__._cast(
            _1177.CylindricalAccuracyGraderWithProfileFormAndSlope
        )

    @property
    def cylindrical_accuracy_grader(
        self: "CastSelf",
    ) -> "_1176.CylindricalAccuracyGrader":
        from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
            _1176,
        )

        return self.__parent__._cast(_1176.CylindricalAccuracyGrader)

    @property
    def agma20151a01_accuracy_grader(self: "CastSelf") -> "AGMA20151A01AccuracyGrader":
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
class AGMA20151A01AccuracyGrader(
    _1177.CylindricalAccuracyGraderWithProfileFormAndSlope
):
    """AGMA20151A01AccuracyGrader

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA20151A01_ACCURACY_GRADER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def helix_form_tolerance(self: "Self") -> "_1185.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HelixFormTolerance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def helix_slope_tolerance(self: "Self") -> "_1185.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HelixSlopeTolerance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def profile_form_tolerance(self: "Self") -> "_1185.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileFormTolerance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def profile_slope_tolerance(self: "Self") -> "_1185.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileSlopeTolerance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def runout_tolerance(self: "Self") -> "_1185.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RunoutTolerance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def sector_pitch_deviation_tolerance(self: "Self") -> "_1185.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SectorPitchDeviationTolerance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def single_flank_toothto_tooth_composite_tolerance(
        self: "Self",
    ) -> "_1185.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SingleFlankToothtoToothCompositeTolerance"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def single_flank_total_composite_tolerance(
        self: "Self",
    ) -> "_1185.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SingleFlankTotalCompositeTolerance"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def single_pitch_deviation_tolerance(self: "Self") -> "_1185.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SinglePitchDeviationTolerance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def toothto_tooth_radial_composite_tolerance(
        self: "Self",
    ) -> "_1185.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ToothtoToothRadialCompositeTolerance"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def total_cumulative_pitch_deviation_tolerance(
        self: "Self",
    ) -> "_1185.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalCumulativePitchDeviationTolerance"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def total_helix_tolerance(self: "Self") -> "_1185.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalHelixTolerance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def total_profile_tolerance(self: "Self") -> "_1185.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalProfileTolerance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def total_radial_composite_tolerance(self: "Self") -> "_1185.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalRadialCompositeTolerance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_AGMA20151A01AccuracyGrader":
        """Cast to another type.

        Returns:
            _Cast_AGMA20151A01AccuracyGrader
        """
        return _Cast_AGMA20151A01AccuracyGrader(self)
