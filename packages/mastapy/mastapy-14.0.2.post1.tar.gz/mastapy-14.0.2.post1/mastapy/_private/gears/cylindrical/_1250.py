"""CylindricalGearWorstLTCAContactChartDataAsTextFile"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_CYLINDRICAL_GEAR_WORST_LTCA_CONTACT_CHART_DATA_AS_TEXT_FILE = python_net_import(
    "SMT.MastaAPI.Gears.Cylindrical",
    "CylindricalGearWorstLTCAContactChartDataAsTextFile",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalGearWorstLTCAContactChartDataAsTextFile")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearWorstLTCAContactChartDataAsTextFile._Cast_CylindricalGearWorstLTCAContactChartDataAsTextFile",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearWorstLTCAContactChartDataAsTextFile",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearWorstLTCAContactChartDataAsTextFile:
    """Special nested class for casting CylindricalGearWorstLTCAContactChartDataAsTextFile to subclasses."""

    __parent__: "CylindricalGearWorstLTCAContactChartDataAsTextFile"

    @property
    def cylindrical_gear_worst_ltca_contact_chart_data_as_text_file(
        self: "CastSelf",
    ) -> "CylindricalGearWorstLTCAContactChartDataAsTextFile":
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
class CylindricalGearWorstLTCAContactChartDataAsTextFile(_0.APIBase):
    """CylindricalGearWorstLTCAContactChartDataAsTextFile

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _CYLINDRICAL_GEAR_WORST_LTCA_CONTACT_CHART_DATA_AS_TEXT_FILE
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def coefficient_of_friction(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CoefficientOfFriction")

        if temp is None:
            return ""

        return temp

    @property
    def depth_of_max_shear_stress(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DepthOfMaxShearStress")

        if temp is None:
            return ""

        return temp

    @property
    def force_per_unit_length(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForcePerUnitLength")

        if temp is None:
            return ""

        return temp

    @property
    def gap_between_loaded_flanks_transverse(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GapBetweenLoadedFlanksTransverse")

        if temp is None:
            return ""

        return temp

    @property
    def gap_between_unloaded_flanks_transverse(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GapBetweenUnloadedFlanksTransverse"
        )

        if temp is None:
            return ""

        return temp

    @property
    def gear_a_depth_of_maximum_material_exposure_iso633642019(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearADepthOfMaximumMaterialExposureISO633642019"
        )

        if temp is None:
            return ""

        return temp

    @property
    def gear_a_maximum_material_exposure_iso633642019(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearAMaximumMaterialExposureISO633642019"
        )

        if temp is None:
            return ""

        return temp

    @property
    def gear_b_depth_of_maximum_material_exposure_iso633642019(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearBDepthOfMaximumMaterialExposureISO633642019"
        )

        if temp is None:
            return ""

        return temp

    @property
    def gear_b_maximum_material_exposure_iso633642019(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearBMaximumMaterialExposureISO633642019"
        )

        if temp is None:
            return ""

        return temp

    @property
    def hertzian_contact_half_width(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HertzianContactHalfWidth")

        if temp is None:
            return ""

        return temp

    @property
    def lubrication_state_d_value(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricationStateDValue")

        if temp is None:
            return ""

        return temp

    @property
    def max_pressure(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaxPressure")

        if temp is None:
            return ""

        return temp

    @property
    def max_shear_stress(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaxShearStress")

        if temp is None:
            return ""

        return temp

    @property
    def micropitting_contact_temperature_isotr1514412010(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MicropittingContactTemperatureISOTR1514412010"
        )

        if temp is None:
            return ""

        return temp

    @property
    def micropitting_contact_temperature_isotr1514412014(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MicropittingContactTemperatureISOTR1514412014"
        )

        if temp is None:
            return ""

        return temp

    @property
    def micropitting_contact_temperature_isots6336222018(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MicropittingContactTemperatureISOTS6336222018"
        )

        if temp is None:
            return ""

        return temp

    @property
    def micropitting_flash_temperature_isotr1514412010(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MicropittingFlashTemperatureISOTR1514412010"
        )

        if temp is None:
            return ""

        return temp

    @property
    def micropitting_flash_temperature_isotr1514412014(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MicropittingFlashTemperatureISOTR1514412014"
        )

        if temp is None:
            return ""

        return temp

    @property
    def micropitting_flash_temperature_isots6336222018(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MicropittingFlashTemperatureISOTS6336222018"
        )

        if temp is None:
            return ""

        return temp

    @property
    def micropitting_safety_factor_isotr1514412010(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MicropittingSafetyFactorISOTR1514412010"
        )

        if temp is None:
            return ""

        return temp

    @property
    def micropitting_safety_factor_isotr1514412014(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MicropittingSafetyFactorISOTR1514412014"
        )

        if temp is None:
            return ""

        return temp

    @property
    def micropitting_safety_factor_isots6336222018(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MicropittingSafetyFactorISOTS6336222018"
        )

        if temp is None:
            return ""

        return temp

    @property
    def minimum_lubricant_film_thickness_dowson(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumLubricantFilmThicknessDowson"
        )

        if temp is None:
            return ""

        return temp

    @property
    def minimum_lubricant_film_thickness_isotr1514412010(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumLubricantFilmThicknessISOTR1514412010"
        )

        if temp is None:
            return ""

        return temp

    @property
    def minimum_lubricant_film_thickness_isotr1514412014(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumLubricantFilmThicknessISOTR1514412014"
        )

        if temp is None:
            return ""

        return temp

    @property
    def minimum_lubricant_film_thickness_isots6336222018(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumLubricantFilmThicknessISOTS6336222018"
        )

        if temp is None:
            return ""

        return temp

    @property
    def pressure_velocity_pv(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PressureVelocityPV")

        if temp is None:
            return ""

        return temp

    @property
    def scuffing_contact_temperature_agma925a03(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingContactTemperatureAGMA925A03"
        )

        if temp is None:
            return ""

        return temp

    @property
    def scuffing_contact_temperature_agma925b22(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingContactTemperatureAGMA925B22"
        )

        if temp is None:
            return ""

        return temp

    @property
    def scuffing_contact_temperature_din399041987(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingContactTemperatureDIN399041987"
        )

        if temp is None:
            return ""

        return temp

    @property
    def scuffing_contact_temperature_isotr1398912000(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingContactTemperatureISOTR1398912000"
        )

        if temp is None:
            return ""

        return temp

    @property
    def scuffing_contact_temperature_isots6336202017(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingContactTemperatureISOTS6336202017"
        )

        if temp is None:
            return ""

        return temp

    @property
    def scuffing_contact_temperature_isots6336202022(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingContactTemperatureISOTS6336202022"
        )

        if temp is None:
            return ""

        return temp

    @property
    def scuffing_flash_temperature_agma925a03(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingFlashTemperatureAGMA925A03"
        )

        if temp is None:
            return ""

        return temp

    @property
    def scuffing_flash_temperature_agma925b22(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingFlashTemperatureAGMA925B22"
        )

        if temp is None:
            return ""

        return temp

    @property
    def scuffing_flash_temperature_din399041987(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingFlashTemperatureDIN399041987"
        )

        if temp is None:
            return ""

        return temp

    @property
    def scuffing_flash_temperature_isotr1398912000(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingFlashTemperatureISOTR1398912000"
        )

        if temp is None:
            return ""

        return temp

    @property
    def scuffing_flash_temperature_isots6336202017(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingFlashTemperatureISOTS6336202017"
        )

        if temp is None:
            return ""

        return temp

    @property
    def scuffing_flash_temperature_isots6336202022(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingFlashTemperatureISOTS6336202022"
        )

        if temp is None:
            return ""

        return temp

    @property
    def scuffing_safety_factor_agma925a03(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ScuffingSafetyFactorAGMA925A03")

        if temp is None:
            return ""

        return temp

    @property
    def scuffing_safety_factor_agma925b22(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ScuffingSafetyFactorAGMA925B22")

        if temp is None:
            return ""

        return temp

    @property
    def scuffing_safety_factor_din399041987(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ScuffingSafetyFactorDIN399041987")

        if temp is None:
            return ""

        return temp

    @property
    def scuffing_safety_factor_isotr1398912000(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingSafetyFactorISOTR1398912000"
        )

        if temp is None:
            return ""

        return temp

    @property
    def scuffing_safety_factor_isots6336202017(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingSafetyFactorISOTS6336202017"
        )

        if temp is None:
            return ""

        return temp

    @property
    def scuffing_safety_factor_isots6336202022(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingSafetyFactorISOTS6336202022"
        )

        if temp is None:
            return ""

        return temp

    @property
    def sliding_power_loss(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlidingPowerLoss")

        if temp is None:
            return ""

        return temp

    @property
    def sliding_velocity(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlidingVelocity")

        if temp is None:
            return ""

        return temp

    @property
    def specific_lubricant_film_thickness_isotr1514412010(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SpecificLubricantFilmThicknessISOTR1514412010"
        )

        if temp is None:
            return ""

        return temp

    @property
    def specific_lubricant_film_thickness_isotr1514412014(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SpecificLubricantFilmThicknessISOTR1514412014"
        )

        if temp is None:
            return ""

        return temp

    @property
    def specific_lubricant_film_thickness_isots6336222018(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SpecificLubricantFilmThicknessISOTS6336222018"
        )

        if temp is None:
            return ""

        return temp

    @property
    def total_deflection_for_mesh(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalDeflectionForMesh")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_CylindricalGearWorstLTCAContactChartDataAsTextFile":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearWorstLTCAContactChartDataAsTextFile
        """
        return _Cast_CylindricalGearWorstLTCAContactChartDataAsTextFile(self)
