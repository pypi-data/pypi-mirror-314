"""MountableComponentCompoundCriticalSpeedAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
    _6850,
)

_MOUNTABLE_COMPONENT_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound",
    "MountableComponentCompoundCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6773,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
        _6829,
        _6833,
        _6836,
        _6839,
        _6840,
        _6841,
        _6848,
        _6853,
        _6854,
        _6857,
        _6861,
        _6864,
        _6867,
        _6872,
        _6875,
        _6878,
        _6883,
        _6887,
        _6891,
        _6894,
        _6897,
        _6900,
        _6901,
        _6905,
        _6906,
        _6909,
        _6912,
        _6913,
        _6914,
        _6915,
        _6916,
        _6919,
        _6923,
        _6926,
        _6931,
        _6932,
        _6935,
        _6938,
        _6939,
        _6941,
        _6942,
        _6943,
        _6946,
        _6947,
        _6948,
        _6949,
        _6950,
        _6953,
    )

    Self = TypeVar("Self", bound="MountableComponentCompoundCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MountableComponentCompoundCriticalSpeedAnalysis._Cast_MountableComponentCompoundCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentCompoundCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountableComponentCompoundCriticalSpeedAnalysis:
    """Special nested class for casting MountableComponentCompoundCriticalSpeedAnalysis to subclasses."""

    __parent__: "MountableComponentCompoundCriticalSpeedAnalysis"

    @property
    def component_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6850.ComponentCompoundCriticalSpeedAnalysis":
        return self.__parent__._cast(_6850.ComponentCompoundCriticalSpeedAnalysis)

    @property
    def part_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6906.PartCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6906,
        )

        return self.__parent__._cast(_6906.PartCompoundCriticalSpeedAnalysis)

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
    def agma_gleason_conical_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6829.AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6829,
        )

        return self.__parent__._cast(
            _6829.AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis
        )

    @property
    def bearing_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6833.BearingCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6833,
        )

        return self.__parent__._cast(_6833.BearingCompoundCriticalSpeedAnalysis)

    @property
    def bevel_differential_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6836.BevelDifferentialGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6836,
        )

        return self.__parent__._cast(
            _6836.BevelDifferentialGearCompoundCriticalSpeedAnalysis
        )

    @property
    def bevel_differential_planet_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6839.BevelDifferentialPlanetGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6839,
        )

        return self.__parent__._cast(
            _6839.BevelDifferentialPlanetGearCompoundCriticalSpeedAnalysis
        )

    @property
    def bevel_differential_sun_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6840.BevelDifferentialSunGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6840,
        )

        return self.__parent__._cast(
            _6840.BevelDifferentialSunGearCompoundCriticalSpeedAnalysis
        )

    @property
    def bevel_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6841.BevelGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6841,
        )

        return self.__parent__._cast(_6841.BevelGearCompoundCriticalSpeedAnalysis)

    @property
    def clutch_half_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6848.ClutchHalfCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6848,
        )

        return self.__parent__._cast(_6848.ClutchHalfCompoundCriticalSpeedAnalysis)

    @property
    def concept_coupling_half_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6853.ConceptCouplingHalfCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6853,
        )

        return self.__parent__._cast(
            _6853.ConceptCouplingHalfCompoundCriticalSpeedAnalysis
        )

    @property
    def concept_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6854.ConceptGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6854,
        )

        return self.__parent__._cast(_6854.ConceptGearCompoundCriticalSpeedAnalysis)

    @property
    def conical_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6857.ConicalGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6857,
        )

        return self.__parent__._cast(_6857.ConicalGearCompoundCriticalSpeedAnalysis)

    @property
    def connector_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6861.ConnectorCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6861,
        )

        return self.__parent__._cast(_6861.ConnectorCompoundCriticalSpeedAnalysis)

    @property
    def coupling_half_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6864.CouplingHalfCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6864,
        )

        return self.__parent__._cast(_6864.CouplingHalfCompoundCriticalSpeedAnalysis)

    @property
    def cvt_pulley_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6867.CVTPulleyCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6867,
        )

        return self.__parent__._cast(_6867.CVTPulleyCompoundCriticalSpeedAnalysis)

    @property
    def cylindrical_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6872.CylindricalGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6872,
        )

        return self.__parent__._cast(_6872.CylindricalGearCompoundCriticalSpeedAnalysis)

    @property
    def cylindrical_planet_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6875.CylindricalPlanetGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6875,
        )

        return self.__parent__._cast(
            _6875.CylindricalPlanetGearCompoundCriticalSpeedAnalysis
        )

    @property
    def face_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6878.FaceGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6878,
        )

        return self.__parent__._cast(_6878.FaceGearCompoundCriticalSpeedAnalysis)

    @property
    def gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6883.GearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6883,
        )

        return self.__parent__._cast(_6883.GearCompoundCriticalSpeedAnalysis)

    @property
    def hypoid_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6887.HypoidGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6887,
        )

        return self.__parent__._cast(_6887.HypoidGearCompoundCriticalSpeedAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6891.KlingelnbergCycloPalloidConicalGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6891,
        )

        return self.__parent__._cast(
            _6891.KlingelnbergCycloPalloidConicalGearCompoundCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6894.KlingelnbergCycloPalloidHypoidGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6894,
        )

        return self.__parent__._cast(
            _6894.KlingelnbergCycloPalloidHypoidGearCompoundCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6897.KlingelnbergCycloPalloidSpiralBevelGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6897,
        )

        return self.__parent__._cast(
            _6897.KlingelnbergCycloPalloidSpiralBevelGearCompoundCriticalSpeedAnalysis
        )

    @property
    def mass_disc_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6900.MassDiscCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6900,
        )

        return self.__parent__._cast(_6900.MassDiscCompoundCriticalSpeedAnalysis)

    @property
    def measurement_component_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6901.MeasurementComponentCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6901,
        )

        return self.__parent__._cast(
            _6901.MeasurementComponentCompoundCriticalSpeedAnalysis
        )

    @property
    def oil_seal_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6905.OilSealCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6905,
        )

        return self.__parent__._cast(_6905.OilSealCompoundCriticalSpeedAnalysis)

    @property
    def part_to_part_shear_coupling_half_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6909.PartToPartShearCouplingHalfCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6909,
        )

        return self.__parent__._cast(
            _6909.PartToPartShearCouplingHalfCompoundCriticalSpeedAnalysis
        )

    @property
    def planet_carrier_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6912.PlanetCarrierCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6912,
        )

        return self.__parent__._cast(_6912.PlanetCarrierCompoundCriticalSpeedAnalysis)

    @property
    def point_load_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6913.PointLoadCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6913,
        )

        return self.__parent__._cast(_6913.PointLoadCompoundCriticalSpeedAnalysis)

    @property
    def power_load_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6914.PowerLoadCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6914,
        )

        return self.__parent__._cast(_6914.PowerLoadCompoundCriticalSpeedAnalysis)

    @property
    def pulley_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6915.PulleyCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6915,
        )

        return self.__parent__._cast(_6915.PulleyCompoundCriticalSpeedAnalysis)

    @property
    def ring_pins_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6916.RingPinsCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6916,
        )

        return self.__parent__._cast(_6916.RingPinsCompoundCriticalSpeedAnalysis)

    @property
    def rolling_ring_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6919.RollingRingCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6919,
        )

        return self.__parent__._cast(_6919.RollingRingCompoundCriticalSpeedAnalysis)

    @property
    def shaft_hub_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6923.ShaftHubConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6923,
        )

        return self.__parent__._cast(
            _6923.ShaftHubConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def spiral_bevel_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6926.SpiralBevelGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6926,
        )

        return self.__parent__._cast(_6926.SpiralBevelGearCompoundCriticalSpeedAnalysis)

    @property
    def spring_damper_half_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6931.SpringDamperHalfCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6931,
        )

        return self.__parent__._cast(
            _6931.SpringDamperHalfCompoundCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_diff_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6932.StraightBevelDiffGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6932,
        )

        return self.__parent__._cast(
            _6932.StraightBevelDiffGearCompoundCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6935.StraightBevelGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6935,
        )

        return self.__parent__._cast(
            _6935.StraightBevelGearCompoundCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_planet_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6938.StraightBevelPlanetGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6938,
        )

        return self.__parent__._cast(
            _6938.StraightBevelPlanetGearCompoundCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_sun_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6939.StraightBevelSunGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6939,
        )

        return self.__parent__._cast(
            _6939.StraightBevelSunGearCompoundCriticalSpeedAnalysis
        )

    @property
    def synchroniser_half_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6941.SynchroniserHalfCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6941,
        )

        return self.__parent__._cast(
            _6941.SynchroniserHalfCompoundCriticalSpeedAnalysis
        )

    @property
    def synchroniser_part_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6942.SynchroniserPartCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6942,
        )

        return self.__parent__._cast(
            _6942.SynchroniserPartCompoundCriticalSpeedAnalysis
        )

    @property
    def synchroniser_sleeve_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6943.SynchroniserSleeveCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6943,
        )

        return self.__parent__._cast(
            _6943.SynchroniserSleeveCompoundCriticalSpeedAnalysis
        )

    @property
    def torque_converter_pump_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6946.TorqueConverterPumpCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6946,
        )

        return self.__parent__._cast(
            _6946.TorqueConverterPumpCompoundCriticalSpeedAnalysis
        )

    @property
    def torque_converter_turbine_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6947.TorqueConverterTurbineCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6947,
        )

        return self.__parent__._cast(
            _6947.TorqueConverterTurbineCompoundCriticalSpeedAnalysis
        )

    @property
    def unbalanced_mass_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6948.UnbalancedMassCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6948,
        )

        return self.__parent__._cast(_6948.UnbalancedMassCompoundCriticalSpeedAnalysis)

    @property
    def virtual_component_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6949.VirtualComponentCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6949,
        )

        return self.__parent__._cast(
            _6949.VirtualComponentCompoundCriticalSpeedAnalysis
        )

    @property
    def worm_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6950.WormGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6950,
        )

        return self.__parent__._cast(_6950.WormGearCompoundCriticalSpeedAnalysis)

    @property
    def zerol_bevel_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6953.ZerolBevelGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6953,
        )

        return self.__parent__._cast(_6953.ZerolBevelGearCompoundCriticalSpeedAnalysis)

    @property
    def mountable_component_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "MountableComponentCompoundCriticalSpeedAnalysis":
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
class MountableComponentCompoundCriticalSpeedAnalysis(
    _6850.ComponentCompoundCriticalSpeedAnalysis
):
    """MountableComponentCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUNTABLE_COMPONENT_COMPOUND_CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_6773.MountableComponentCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.MountableComponentCriticalSpeedAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6773.MountableComponentCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.MountableComponentCriticalSpeedAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_MountableComponentCompoundCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_MountableComponentCompoundCriticalSpeedAnalysis
        """
        return _Cast_MountableComponentCompoundCriticalSpeedAnalysis(self)
