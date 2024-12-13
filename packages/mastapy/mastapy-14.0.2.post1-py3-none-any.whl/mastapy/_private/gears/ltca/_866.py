"""GearMeshLoadDistributionAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call_overload,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.analysis import _1263

_GEAR_LOAD_DISTRIBUTION_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.LTCA", "GearLoadDistributionAnalysis"
)
_GEAR_MESH_LOAD_DISTRIBUTION_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.LTCA", "GearMeshLoadDistributionAnalysis"
)
_GEAR_FLANKS = python_net_import("SMT.MastaAPI.Gears", "GearFlanks")
_STRESS_RESULTS_TYPE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "StressResultsType"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears import _338
    from mastapy._private.gears.analysis import _1256, _1262
    from mastapy._private.gears.ltca import _865, _867
    from mastapy._private.gears.ltca.conical import _895
    from mastapy._private.gears.ltca.cylindrical import _882
    from mastapy._private.math_utility import _1563
    from mastapy._private.nodal_analysis import _90

    Self = TypeVar("Self", bound="GearMeshLoadDistributionAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearMeshLoadDistributionAnalysis._Cast_GearMeshLoadDistributionAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshLoadDistributionAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshLoadDistributionAnalysis:
    """Special nested class for casting GearMeshLoadDistributionAnalysis to subclasses."""

    __parent__: "GearMeshLoadDistributionAnalysis"

    @property
    def gear_mesh_implementation_analysis(
        self: "CastSelf",
    ) -> "_1263.GearMeshImplementationAnalysis":
        return self.__parent__._cast(_1263.GearMeshImplementationAnalysis)

    @property
    def gear_mesh_design_analysis(self: "CastSelf") -> "_1262.GearMeshDesignAnalysis":
        from mastapy._private.gears.analysis import _1262

        return self.__parent__._cast(_1262.GearMeshDesignAnalysis)

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1256.AbstractGearMeshAnalysis":
        from mastapy._private.gears.analysis import _1256

        return self.__parent__._cast(_1256.AbstractGearMeshAnalysis)

    @property
    def cylindrical_gear_mesh_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_882.CylindricalGearMeshLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.cylindrical import _882

        return self.__parent__._cast(_882.CylindricalGearMeshLoadDistributionAnalysis)

    @property
    def conical_mesh_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_895.ConicalMeshLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.conical import _895

        return self.__parent__._cast(_895.ConicalMeshLoadDistributionAnalysis)

    @property
    def gear_mesh_load_distribution_analysis(
        self: "CastSelf",
    ) -> "GearMeshLoadDistributionAnalysis":
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
class GearMeshLoadDistributionAnalysis(_1263.GearMeshImplementationAnalysis):
    """GearMeshLoadDistributionAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_LOAD_DISTRIBUTION_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def actual_total_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActualTotalContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    def analysis_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AnalysisName")

        if temp is None:
            return ""

        return temp

    @property
    def index_of_roll_angle_with_maximum_contact_stress(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "IndexOfRollAngleWithMaximumContactStress"
        )

        if temp is None:
            return 0

        return temp

    @property
    def is_advanced_ltca(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsAdvancedLTCA")

        if temp is None:
            return False

        return temp

    @is_advanced_ltca.setter
    @enforce_parameter_types
    def is_advanced_ltca(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IsAdvancedLTCA", bool(value) if value is not None else False
        )

    @property
    def load_case_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCaseName")

        if temp is None:
            return ""

        return temp

    @property
    def maximum_contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumContactStress")

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_force_per_unit_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumForcePerUnitLength")

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
    def minimum_force_per_unit_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumForcePerUnitLength")

        if temp is None:
            return 0.0

        return temp

    @property
    def number_of_roll_angles(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfRollAngles")

        if temp is None:
            return 0

        return temp

    @property
    def peakto_peak_moment_about_centre(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PeaktoPeakMomentAboutCentre")

        if temp is None:
            return 0.0

        return temp

    @property
    def moment_about_centre_fourier_series(self: "Self") -> "_1563.FourierSeries":
        """mastapy.math_utility.FourierSeries

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MomentAboutCentreFourierSeries")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def transmission_error_fourier_series(self: "Self") -> "_1563.FourierSeries":
        """mastapy.math_utility.FourierSeries

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransmissionErrorFourierSeries")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def load_distribution_analyses_at_single_rotation(
        self: "Self",
    ) -> "List[_867.GearMeshLoadDistributionAtRotation]":
        """List[mastapy.gears.ltca.GearMeshLoadDistributionAtRotation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LoadDistributionAnalysesAtSingleRotation"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @enforce_parameter_types
    def maximum_root_stress_with_flanks(
        self: "Self",
        gear: "_865.GearLoadDistributionAnalysis",
        flank: "_338.GearFlanks",
        stress_type: "_90.StressResultsType",
    ) -> "float":
        """float

        Args:
            gear (mastapy.gears.ltca.GearLoadDistributionAnalysis)
            flank (mastapy.gears.GearFlanks)
            stress_type (mastapy.nodal_analysis.StressResultsType)
        """
        flank = conversion.mp_to_pn_enum(flank, "SMT.MastaAPI.Gears.GearFlanks")
        stress_type = conversion.mp_to_pn_enum(
            stress_type, "SMT.MastaAPI.NodalAnalysis.StressResultsType"
        )
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "MaximumRootStress",
            [_GEAR_LOAD_DISTRIBUTION_ANALYSIS, _GEAR_FLANKS, _STRESS_RESULTS_TYPE],
            gear.wrapped if gear else None,
            flank,
            stress_type,
        )
        return method_result

    @enforce_parameter_types
    def maximum_root_stress(
        self: "Self",
        gear: "_865.GearLoadDistributionAnalysis",
        stress_type: "_90.StressResultsType",
    ) -> "float":
        """float

        Args:
            gear (mastapy.gears.ltca.GearLoadDistributionAnalysis)
            stress_type (mastapy.nodal_analysis.StressResultsType)
        """
        stress_type = conversion.mp_to_pn_enum(
            stress_type, "SMT.MastaAPI.NodalAnalysis.StressResultsType"
        )
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "MaximumRootStress",
            [_GEAR_LOAD_DISTRIBUTION_ANALYSIS, _STRESS_RESULTS_TYPE],
            gear.wrapped if gear else None,
            stress_type,
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshLoadDistributionAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearMeshLoadDistributionAnalysis
        """
        return _Cast_GearMeshLoadDistributionAnalysis(self)
