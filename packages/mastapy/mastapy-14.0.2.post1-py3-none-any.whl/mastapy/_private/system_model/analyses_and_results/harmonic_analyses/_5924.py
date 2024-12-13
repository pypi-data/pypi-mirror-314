"""MountableComponentHarmonicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _5841

_MOUNTABLE_COMPONENT_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "MountableComponentHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740, _2742, _2746
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7719,
        _7722,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5819,
        _5823,
        _5826,
        _5829,
        _5830,
        _5831,
        _5837,
        _5843,
        _5845,
        _5848,
        _5852,
        _5854,
        _5858,
        _5863,
        _5866,
        _5883,
        _5889,
        _5907,
        _5911,
        _5914,
        _5917,
        _5920,
        _5921,
        _5925,
        _5926,
        _5928,
        _5933,
        _5934,
        _5935,
        _5936,
        _5938,
        _5942,
        _5945,
        _5950,
        _5954,
        _5957,
        _5960,
        _5963,
        _5964,
        _5965,
        _5967,
        _5968,
        _5971,
        _5972,
        _5974,
        _5975,
        _5976,
        _5979,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4777
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2873,
    )
    from mastapy._private.system_model.part_model import _2524

    Self = TypeVar("Self", bound="MountableComponentHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MountableComponentHarmonicAnalysis._Cast_MountableComponentHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountableComponentHarmonicAnalysis:
    """Special nested class for casting MountableComponentHarmonicAnalysis to subclasses."""

    __parent__: "MountableComponentHarmonicAnalysis"

    @property
    def component_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5841.ComponentHarmonicAnalysis":
        return self.__parent__._cast(_5841.ComponentHarmonicAnalysis)

    @property
    def part_harmonic_analysis(self: "CastSelf") -> "_5926.PartHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5926,
        )

        return self.__parent__._cast(_5926.PartHarmonicAnalysis)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7722.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7722,
        )

        return self.__parent__._cast(_7722.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7719.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7719,
        )

        return self.__parent__._cast(_7719.PartAnalysisCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2746.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2746

        return self.__parent__._cast(_2746.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2742.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2742

        return self.__parent__._cast(_2742.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2740.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2740

        return self.__parent__._cast(_2740.DesignEntityAnalysis)

    @property
    def agma_gleason_conical_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5819.AGMAGleasonConicalGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5819,
        )

        return self.__parent__._cast(_5819.AGMAGleasonConicalGearHarmonicAnalysis)

    @property
    def bearing_harmonic_analysis(self: "CastSelf") -> "_5823.BearingHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5823,
        )

        return self.__parent__._cast(_5823.BearingHarmonicAnalysis)

    @property
    def bevel_differential_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5826.BevelDifferentialGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5826,
        )

        return self.__parent__._cast(_5826.BevelDifferentialGearHarmonicAnalysis)

    @property
    def bevel_differential_planet_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5829.BevelDifferentialPlanetGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5829,
        )

        return self.__parent__._cast(_5829.BevelDifferentialPlanetGearHarmonicAnalysis)

    @property
    def bevel_differential_sun_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5830.BevelDifferentialSunGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5830,
        )

        return self.__parent__._cast(_5830.BevelDifferentialSunGearHarmonicAnalysis)

    @property
    def bevel_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5831.BevelGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5831,
        )

        return self.__parent__._cast(_5831.BevelGearHarmonicAnalysis)

    @property
    def clutch_half_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5837.ClutchHalfHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5837,
        )

        return self.__parent__._cast(_5837.ClutchHalfHarmonicAnalysis)

    @property
    def concept_coupling_half_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5843.ConceptCouplingHalfHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5843,
        )

        return self.__parent__._cast(_5843.ConceptCouplingHalfHarmonicAnalysis)

    @property
    def concept_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5845.ConceptGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5845,
        )

        return self.__parent__._cast(_5845.ConceptGearHarmonicAnalysis)

    @property
    def conical_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5848.ConicalGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5848,
        )

        return self.__parent__._cast(_5848.ConicalGearHarmonicAnalysis)

    @property
    def connector_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5852.ConnectorHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5852,
        )

        return self.__parent__._cast(_5852.ConnectorHarmonicAnalysis)

    @property
    def coupling_half_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5854.CouplingHalfHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5854,
        )

        return self.__parent__._cast(_5854.CouplingHalfHarmonicAnalysis)

    @property
    def cvt_pulley_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5858.CVTPulleyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5858,
        )

        return self.__parent__._cast(_5858.CVTPulleyHarmonicAnalysis)

    @property
    def cylindrical_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5863.CylindricalGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5863,
        )

        return self.__parent__._cast(_5863.CylindricalGearHarmonicAnalysis)

    @property
    def cylindrical_planet_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5866.CylindricalPlanetGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5866,
        )

        return self.__parent__._cast(_5866.CylindricalPlanetGearHarmonicAnalysis)

    @property
    def face_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5883.FaceGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5883,
        )

        return self.__parent__._cast(_5883.FaceGearHarmonicAnalysis)

    @property
    def gear_harmonic_analysis(self: "CastSelf") -> "_5889.GearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5889,
        )

        return self.__parent__._cast(_5889.GearHarmonicAnalysis)

    @property
    def hypoid_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5907.HypoidGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5907,
        )

        return self.__parent__._cast(_5907.HypoidGearHarmonicAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5911.KlingelnbergCycloPalloidConicalGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5911,
        )

        return self.__parent__._cast(
            _5911.KlingelnbergCycloPalloidConicalGearHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5914.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5914,
        )

        return self.__parent__._cast(
            _5914.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5917.KlingelnbergCycloPalloidSpiralBevelGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5917,
        )

        return self.__parent__._cast(
            _5917.KlingelnbergCycloPalloidSpiralBevelGearHarmonicAnalysis
        )

    @property
    def mass_disc_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5920.MassDiscHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5920,
        )

        return self.__parent__._cast(_5920.MassDiscHarmonicAnalysis)

    @property
    def measurement_component_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5921.MeasurementComponentHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5921,
        )

        return self.__parent__._cast(_5921.MeasurementComponentHarmonicAnalysis)

    @property
    def oil_seal_harmonic_analysis(self: "CastSelf") -> "_5925.OilSealHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5925,
        )

        return self.__parent__._cast(_5925.OilSealHarmonicAnalysis)

    @property
    def part_to_part_shear_coupling_half_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5928.PartToPartShearCouplingHalfHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5928,
        )

        return self.__parent__._cast(_5928.PartToPartShearCouplingHalfHarmonicAnalysis)

    @property
    def planet_carrier_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5933.PlanetCarrierHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5933,
        )

        return self.__parent__._cast(_5933.PlanetCarrierHarmonicAnalysis)

    @property
    def point_load_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5934.PointLoadHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5934,
        )

        return self.__parent__._cast(_5934.PointLoadHarmonicAnalysis)

    @property
    def power_load_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5935.PowerLoadHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5935,
        )

        return self.__parent__._cast(_5935.PowerLoadHarmonicAnalysis)

    @property
    def pulley_harmonic_analysis(self: "CastSelf") -> "_5936.PulleyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5936,
        )

        return self.__parent__._cast(_5936.PulleyHarmonicAnalysis)

    @property
    def ring_pins_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5938.RingPinsHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5938,
        )

        return self.__parent__._cast(_5938.RingPinsHarmonicAnalysis)

    @property
    def rolling_ring_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5942.RollingRingHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5942,
        )

        return self.__parent__._cast(_5942.RollingRingHarmonicAnalysis)

    @property
    def shaft_hub_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5945.ShaftHubConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5945,
        )

        return self.__parent__._cast(_5945.ShaftHubConnectionHarmonicAnalysis)

    @property
    def spiral_bevel_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5950.SpiralBevelGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5950,
        )

        return self.__parent__._cast(_5950.SpiralBevelGearHarmonicAnalysis)

    @property
    def spring_damper_half_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5954.SpringDamperHalfHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5954,
        )

        return self.__parent__._cast(_5954.SpringDamperHalfHarmonicAnalysis)

    @property
    def straight_bevel_diff_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5957.StraightBevelDiffGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5957,
        )

        return self.__parent__._cast(_5957.StraightBevelDiffGearHarmonicAnalysis)

    @property
    def straight_bevel_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5960.StraightBevelGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5960,
        )

        return self.__parent__._cast(_5960.StraightBevelGearHarmonicAnalysis)

    @property
    def straight_bevel_planet_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5963.StraightBevelPlanetGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5963,
        )

        return self.__parent__._cast(_5963.StraightBevelPlanetGearHarmonicAnalysis)

    @property
    def straight_bevel_sun_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5964.StraightBevelSunGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5964,
        )

        return self.__parent__._cast(_5964.StraightBevelSunGearHarmonicAnalysis)

    @property
    def synchroniser_half_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5965.SynchroniserHalfHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5965,
        )

        return self.__parent__._cast(_5965.SynchroniserHalfHarmonicAnalysis)

    @property
    def synchroniser_part_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5967.SynchroniserPartHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5967,
        )

        return self.__parent__._cast(_5967.SynchroniserPartHarmonicAnalysis)

    @property
    def synchroniser_sleeve_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5968.SynchroniserSleeveHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5968,
        )

        return self.__parent__._cast(_5968.SynchroniserSleeveHarmonicAnalysis)

    @property
    def torque_converter_pump_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5971.TorqueConverterPumpHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5971,
        )

        return self.__parent__._cast(_5971.TorqueConverterPumpHarmonicAnalysis)

    @property
    def torque_converter_turbine_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5972.TorqueConverterTurbineHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5972,
        )

        return self.__parent__._cast(_5972.TorqueConverterTurbineHarmonicAnalysis)

    @property
    def unbalanced_mass_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5974.UnbalancedMassHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5974,
        )

        return self.__parent__._cast(_5974.UnbalancedMassHarmonicAnalysis)

    @property
    def virtual_component_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5975.VirtualComponentHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5975,
        )

        return self.__parent__._cast(_5975.VirtualComponentHarmonicAnalysis)

    @property
    def worm_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5976.WormGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5976,
        )

        return self.__parent__._cast(_5976.WormGearHarmonicAnalysis)

    @property
    def zerol_bevel_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5979.ZerolBevelGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5979,
        )

        return self.__parent__._cast(_5979.ZerolBevelGearHarmonicAnalysis)

    @property
    def mountable_component_harmonic_analysis(
        self: "CastSelf",
    ) -> "MountableComponentHarmonicAnalysis":
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
class MountableComponentHarmonicAnalysis(_5841.ComponentHarmonicAnalysis):
    """MountableComponentHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUNTABLE_COMPONENT_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2524.MountableComponent":
        """mastapy.system_model.part_model.MountableComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def coupled_modal_analysis(self: "Self") -> "_4777.MountableComponentModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.MountableComponentModalAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CoupledModalAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(
        self: "Self",
    ) -> "_2873.MountableComponentSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.MountableComponentSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_MountableComponentHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_MountableComponentHarmonicAnalysis
        """
        return _Cast_MountableComponentHarmonicAnalysis(self)
