"""AssemblyCompoundSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
    _2942,
)

_ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "AssemblyCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1267
    from mastapy._private.nodal_analysis import _50
    from mastapy._private.shafts import _40
    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2781,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _2950,
        _2952,
        _2955,
        _2961,
        _2962,
        _2963,
        _2968,
        _2973,
        _2983,
        _2985,
        _2987,
        _2991,
        _2998,
        _2999,
        _3000,
        _3007,
        _3014,
        _3017,
        _3018,
        _3019,
        _3021,
        _3023,
        _3024,
        _3025,
        _3030,
        _3031,
        _3032,
        _3034,
        _3036,
        _3039,
        _3040,
        _3042,
        _3047,
        _3048,
        _3053,
        _3056,
        _3059,
        _3063,
        _3067,
        _3071,
        _3074,
    )
    from mastapy._private.system_model.part_model import _2491

    Self = TypeVar("Self", bound="AssemblyCompoundSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AssemblyCompoundSystemDeflection._Cast_AssemblyCompoundSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AssemblyCompoundSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AssemblyCompoundSystemDeflection:
    """Special nested class for casting AssemblyCompoundSystemDeflection to subclasses."""

    __parent__: "AssemblyCompoundSystemDeflection"

    @property
    def abstract_assembly_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2942.AbstractAssemblyCompoundSystemDeflection":
        return self.__parent__._cast(_2942.AbstractAssemblyCompoundSystemDeflection)

    @property
    def part_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3024.PartCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3024,
        )

        return self.__parent__._cast(_3024.PartCompoundSystemDeflection)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7720.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7720,
        )

        return self.__parent__._cast(_7720.PartCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7717.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7717,
        )

        return self.__parent__._cast(_7717.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2740.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2740

        return self.__parent__._cast(_2740.DesignEntityAnalysis)

    @property
    def root_assembly_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3039.RootAssemblyCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3039,
        )

        return self.__parent__._cast(_3039.RootAssemblyCompoundSystemDeflection)

    @property
    def assembly_compound_system_deflection(
        self: "CastSelf",
    ) -> "AssemblyCompoundSystemDeflection":
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
class AssemblyCompoundSystemDeflection(_2942.AbstractAssemblyCompoundSystemDeflection):
    """AssemblyCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def overall_duty_cycle_bearing_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "OverallDutyCycleBearingReliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def overall_duty_cycle_gear_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverallDutyCycleGearReliability")

        if temp is None:
            return 0.0

        return temp

    @property
    def overall_duty_cycle_shaft_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverallDutyCycleShaftReliability")

        if temp is None:
            return 0.0

        return temp

    @property
    def overall_oil_seal_duty_cycle_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "OverallOilSealDutyCycleReliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def overall_system_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverallSystemReliability")

        if temp is None:
            return 0.0

        return temp

    @property
    def analysis_settings(self: "Self") -> "_50.AnalysisSettingsItem":
        """mastapy.nodal_analysis.AnalysisSettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AnalysisSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_design(self: "Self") -> "_2491.Assembly":
        """mastapy.system_model.part_model.Assembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_design(self: "Self") -> "_2491.Assembly":
        """mastapy.system_model.part_model.Assembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def rating_for_all_gear_sets(self: "Self") -> "_1267.GearSetGroupDutyCycle":
        """mastapy.gears.analysis.GearSetGroupDutyCycle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatingForAllGearSets")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def shaft_settings(self: "Self") -> "_40.ShaftSettingsItem":
        """mastapy.shafts.ShaftSettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_2781.AssemblySystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.AssemblySystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bearings(self: "Self") -> "List[_2950.BearingCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.BearingCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Bearings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def belt_drives(self: "Self") -> "List[_2952.BeltDriveCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.BeltDriveCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BeltDrives")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bevel_differential_gear_sets(
        self: "Self",
    ) -> "List[_2955.BevelDifferentialGearSetCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.BevelDifferentialGearSetCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelDifferentialGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bolted_joints(
        self: "Self",
    ) -> "List[_2962.BoltedJointCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.BoltedJointCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BoltedJoints")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bolts(self: "Self") -> "List[_2961.BoltCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.BoltCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Bolts")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cv_ts(self: "Self") -> "List[_2983.CVTCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.CVTCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CVTs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def clutches(self: "Self") -> "List[_2963.ClutchCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.ClutchCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Clutches")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def concept_couplings(
        self: "Self",
    ) -> "List[_2968.ConceptCouplingCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.ConceptCouplingCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConceptCouplings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def concept_gear_sets(
        self: "Self",
    ) -> "List[_2973.ConceptGearSetCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.ConceptGearSetCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConceptGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cycloidal_assemblies(
        self: "Self",
    ) -> "List[_2985.CycloidalAssemblyCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.CycloidalAssemblyCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CycloidalAssemblies")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cycloidal_discs(
        self: "Self",
    ) -> "List[_2987.CycloidalDiscCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.CycloidalDiscCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CycloidalDiscs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cylindrical_gear_sets(
        self: "Self",
    ) -> "List[_2991.CylindricalGearSetCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.CylindricalGearSetCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def fe_parts(self: "Self") -> "List[_2999.FEPartCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.FEPartCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FEParts")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def face_gear_sets(
        self: "Self",
    ) -> "List[_2998.FaceGearSetCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.FaceGearSetCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def flexible_pin_assemblies(
        self: "Self",
    ) -> "List[_3000.FlexiblePinAssemblyCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.FlexiblePinAssemblyCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FlexiblePinAssemblies")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def hypoid_gear_sets(
        self: "Self",
    ) -> "List[_3007.HypoidGearSetCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.HypoidGearSetCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HypoidGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(
        self: "Self",
    ) -> "List[_3014.KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidHypoidGearSets"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(
        self: "Self",
    ) -> (
        "List[_3017.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSystemDeflection]"
    ):
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidSpiralBevelGearSets"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def mass_discs(self: "Self") -> "List[_3018.MassDiscCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.MassDiscCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MassDiscs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def measurement_components(
        self: "Self",
    ) -> "List[_3019.MeasurementComponentCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.MeasurementComponentCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeasurementComponents")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def microphones(self: "Self") -> "List[_3021.MicrophoneCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.MicrophoneCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Microphones")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def oil_seals(self: "Self") -> "List[_3023.OilSealCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.OilSealCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OilSeals")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def part_to_part_shear_couplings(
        self: "Self",
    ) -> "List[_3025.PartToPartShearCouplingCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.PartToPartShearCouplingCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PartToPartShearCouplings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def planet_carriers(
        self: "Self",
    ) -> "List[_3030.PlanetCarrierCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.PlanetCarrierCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlanetCarriers")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def point_loads(self: "Self") -> "List[_3031.PointLoadCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.PointLoadCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PointLoads")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def power_loads(self: "Self") -> "List[_3032.PowerLoadCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.PowerLoadCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerLoads")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def ring_pins(self: "Self") -> "List[_3034.RingPinsCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.RingPinsCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RingPins")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def rolling_bearings(self: "Self") -> "List[_2950.BearingCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.BearingCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollingBearings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def rolling_ring_assemblies(
        self: "Self",
    ) -> "List[_3036.RollingRingAssemblyCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.RollingRingAssemblyCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollingRingAssemblies")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def shaft_hub_connections(
        self: "Self",
    ) -> "List[_3042.ShaftHubConnectionCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.ShaftHubConnectionCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftHubConnections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def shafts(self: "Self") -> "List[_3040.ShaftCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.ShaftCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Shafts")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def spiral_bevel_gear_sets(
        self: "Self",
    ) -> "List[_3047.SpiralBevelGearSetCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.SpiralBevelGearSetCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpiralBevelGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def spring_dampers(
        self: "Self",
    ) -> "List[_3048.SpringDamperCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.SpringDamperCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpringDampers")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def straight_bevel_diff_gear_sets(
        self: "Self",
    ) -> "List[_3053.StraightBevelDiffGearSetCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.StraightBevelDiffGearSetCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelDiffGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def straight_bevel_gear_sets(
        self: "Self",
    ) -> "List[_3056.StraightBevelGearSetCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.StraightBevelGearSetCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def synchronisers(
        self: "Self",
    ) -> "List[_3059.SynchroniserCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.SynchroniserCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Synchronisers")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def torque_converters(
        self: "Self",
    ) -> "List[_3063.TorqueConverterCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.TorqueConverterCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueConverters")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def unbalanced_masses(
        self: "Self",
    ) -> "List[_3067.UnbalancedMassCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.UnbalancedMassCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UnbalancedMasses")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def worm_gear_sets(
        self: "Self",
    ) -> "List[_3071.WormGearSetCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.WormGearSetCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def zerol_bevel_gear_sets(
        self: "Self",
    ) -> "List[_3074.ZerolBevelGearSetCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.ZerolBevelGearSetCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZerolBevelGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases(self: "Self") -> "List[_2781.AssemblySystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.AssemblySystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_AssemblyCompoundSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_AssemblyCompoundSystemDeflection
        """
        return _Cast_AssemblyCompoundSystemDeflection(self)
