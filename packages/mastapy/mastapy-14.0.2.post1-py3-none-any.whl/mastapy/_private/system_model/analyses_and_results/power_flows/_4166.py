"""ComponentPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows import _4225

_COMPONENT_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "ComponentPowerFlow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740, _2742, _2746
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7719,
        _7722,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4142,
        _4143,
        _4146,
        _4149,
        _4153,
        _4155,
        _4156,
        _4158,
        _4161,
        _4163,
        _4168,
        _4171,
        _4174,
        _4177,
        _4179,
        _4183,
        _4187,
        _4190,
        _4192,
        _4193,
        _4194,
        _4196,
        _4200,
        _4203,
        _4205,
        _4207,
        _4211,
        _4214,
        _4217,
        _4219,
        _4220,
        _4222,
        _4223,
        _4224,
        _4227,
        _4231,
        _4232,
        _4235,
        _4236,
        _4237,
        _4241,
        _4243,
        _4244,
        _4248,
        _4251,
        _4254,
        _4257,
        _4259,
        _4260,
        _4261,
        _4262,
        _4264,
        _4268,
        _4269,
        _4270,
        _4271,
        _4273,
        _4276,
    )
    from mastapy._private.system_model.part_model import _2502

    Self = TypeVar("Self", bound="ComponentPowerFlow")
    CastSelf = TypeVar("CastSelf", bound="ComponentPowerFlow._Cast_ComponentPowerFlow")


__docformat__ = "restructuredtext en"
__all__ = ("ComponentPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentPowerFlow:
    """Special nested class for casting ComponentPowerFlow to subclasses."""

    __parent__: "ComponentPowerFlow"

    @property
    def part_power_flow(self: "CastSelf") -> "_4225.PartPowerFlow":
        return self.__parent__._cast(_4225.PartPowerFlow)

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
    def abstract_shaft_or_housing_power_flow(
        self: "CastSelf",
    ) -> "_4142.AbstractShaftOrHousingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4142

        return self.__parent__._cast(_4142.AbstractShaftOrHousingPowerFlow)

    @property
    def abstract_shaft_power_flow(self: "CastSelf") -> "_4143.AbstractShaftPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4143

        return self.__parent__._cast(_4143.AbstractShaftPowerFlow)

    @property
    def agma_gleason_conical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4146.AGMAGleasonConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4146

        return self.__parent__._cast(_4146.AGMAGleasonConicalGearPowerFlow)

    @property
    def bearing_power_flow(self: "CastSelf") -> "_4149.BearingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4149

        return self.__parent__._cast(_4149.BearingPowerFlow)

    @property
    def bevel_differential_gear_power_flow(
        self: "CastSelf",
    ) -> "_4153.BevelDifferentialGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4153

        return self.__parent__._cast(_4153.BevelDifferentialGearPowerFlow)

    @property
    def bevel_differential_planet_gear_power_flow(
        self: "CastSelf",
    ) -> "_4155.BevelDifferentialPlanetGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4155

        return self.__parent__._cast(_4155.BevelDifferentialPlanetGearPowerFlow)

    @property
    def bevel_differential_sun_gear_power_flow(
        self: "CastSelf",
    ) -> "_4156.BevelDifferentialSunGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4156

        return self.__parent__._cast(_4156.BevelDifferentialSunGearPowerFlow)

    @property
    def bevel_gear_power_flow(self: "CastSelf") -> "_4158.BevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4158

        return self.__parent__._cast(_4158.BevelGearPowerFlow)

    @property
    def bolt_power_flow(self: "CastSelf") -> "_4161.BoltPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4161

        return self.__parent__._cast(_4161.BoltPowerFlow)

    @property
    def clutch_half_power_flow(self: "CastSelf") -> "_4163.ClutchHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4163

        return self.__parent__._cast(_4163.ClutchHalfPowerFlow)

    @property
    def concept_coupling_half_power_flow(
        self: "CastSelf",
    ) -> "_4168.ConceptCouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4168

        return self.__parent__._cast(_4168.ConceptCouplingHalfPowerFlow)

    @property
    def concept_gear_power_flow(self: "CastSelf") -> "_4171.ConceptGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4171

        return self.__parent__._cast(_4171.ConceptGearPowerFlow)

    @property
    def conical_gear_power_flow(self: "CastSelf") -> "_4174.ConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4174

        return self.__parent__._cast(_4174.ConicalGearPowerFlow)

    @property
    def connector_power_flow(self: "CastSelf") -> "_4177.ConnectorPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4177

        return self.__parent__._cast(_4177.ConnectorPowerFlow)

    @property
    def coupling_half_power_flow(self: "CastSelf") -> "_4179.CouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4179

        return self.__parent__._cast(_4179.CouplingHalfPowerFlow)

    @property
    def cvt_pulley_power_flow(self: "CastSelf") -> "_4183.CVTPulleyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4183

        return self.__parent__._cast(_4183.CVTPulleyPowerFlow)

    @property
    def cycloidal_disc_power_flow(self: "CastSelf") -> "_4187.CycloidalDiscPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4187

        return self.__parent__._cast(_4187.CycloidalDiscPowerFlow)

    @property
    def cylindrical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4190.CylindricalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4190

        return self.__parent__._cast(_4190.CylindricalGearPowerFlow)

    @property
    def cylindrical_planet_gear_power_flow(
        self: "CastSelf",
    ) -> "_4192.CylindricalPlanetGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4192

        return self.__parent__._cast(_4192.CylindricalPlanetGearPowerFlow)

    @property
    def datum_power_flow(self: "CastSelf") -> "_4193.DatumPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4193

        return self.__parent__._cast(_4193.DatumPowerFlow)

    @property
    def external_cad_model_power_flow(
        self: "CastSelf",
    ) -> "_4194.ExternalCADModelPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4194

        return self.__parent__._cast(_4194.ExternalCADModelPowerFlow)

    @property
    def face_gear_power_flow(self: "CastSelf") -> "_4196.FaceGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4196

        return self.__parent__._cast(_4196.FaceGearPowerFlow)

    @property
    def fe_part_power_flow(self: "CastSelf") -> "_4200.FEPartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4200

        return self.__parent__._cast(_4200.FEPartPowerFlow)

    @property
    def gear_power_flow(self: "CastSelf") -> "_4203.GearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4203

        return self.__parent__._cast(_4203.GearPowerFlow)

    @property
    def guide_dxf_model_power_flow(self: "CastSelf") -> "_4205.GuideDxfModelPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4205

        return self.__parent__._cast(_4205.GuideDxfModelPowerFlow)

    @property
    def hypoid_gear_power_flow(self: "CastSelf") -> "_4207.HypoidGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4207

        return self.__parent__._cast(_4207.HypoidGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4211.KlingelnbergCycloPalloidConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4211

        return self.__parent__._cast(_4211.KlingelnbergCycloPalloidConicalGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_power_flow(
        self: "CastSelf",
    ) -> "_4214.KlingelnbergCycloPalloidHypoidGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4214

        return self.__parent__._cast(_4214.KlingelnbergCycloPalloidHypoidGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4217.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4217

        return self.__parent__._cast(
            _4217.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow
        )

    @property
    def mass_disc_power_flow(self: "CastSelf") -> "_4219.MassDiscPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4219

        return self.__parent__._cast(_4219.MassDiscPowerFlow)

    @property
    def measurement_component_power_flow(
        self: "CastSelf",
    ) -> "_4220.MeasurementComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4220

        return self.__parent__._cast(_4220.MeasurementComponentPowerFlow)

    @property
    def microphone_power_flow(self: "CastSelf") -> "_4222.MicrophonePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4222

        return self.__parent__._cast(_4222.MicrophonePowerFlow)

    @property
    def mountable_component_power_flow(
        self: "CastSelf",
    ) -> "_4223.MountableComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4223

        return self.__parent__._cast(_4223.MountableComponentPowerFlow)

    @property
    def oil_seal_power_flow(self: "CastSelf") -> "_4224.OilSealPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4224

        return self.__parent__._cast(_4224.OilSealPowerFlow)

    @property
    def part_to_part_shear_coupling_half_power_flow(
        self: "CastSelf",
    ) -> "_4227.PartToPartShearCouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4227

        return self.__parent__._cast(_4227.PartToPartShearCouplingHalfPowerFlow)

    @property
    def planet_carrier_power_flow(self: "CastSelf") -> "_4231.PlanetCarrierPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4231

        return self.__parent__._cast(_4231.PlanetCarrierPowerFlow)

    @property
    def point_load_power_flow(self: "CastSelf") -> "_4232.PointLoadPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4232

        return self.__parent__._cast(_4232.PointLoadPowerFlow)

    @property
    def power_load_power_flow(self: "CastSelf") -> "_4235.PowerLoadPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4235

        return self.__parent__._cast(_4235.PowerLoadPowerFlow)

    @property
    def pulley_power_flow(self: "CastSelf") -> "_4236.PulleyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4236

        return self.__parent__._cast(_4236.PulleyPowerFlow)

    @property
    def ring_pins_power_flow(self: "CastSelf") -> "_4237.RingPinsPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4237

        return self.__parent__._cast(_4237.RingPinsPowerFlow)

    @property
    def rolling_ring_power_flow(self: "CastSelf") -> "_4241.RollingRingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4241

        return self.__parent__._cast(_4241.RollingRingPowerFlow)

    @property
    def shaft_hub_connection_power_flow(
        self: "CastSelf",
    ) -> "_4243.ShaftHubConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4243

        return self.__parent__._cast(_4243.ShaftHubConnectionPowerFlow)

    @property
    def shaft_power_flow(self: "CastSelf") -> "_4244.ShaftPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4244

        return self.__parent__._cast(_4244.ShaftPowerFlow)

    @property
    def spiral_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4248.SpiralBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4248

        return self.__parent__._cast(_4248.SpiralBevelGearPowerFlow)

    @property
    def spring_damper_half_power_flow(
        self: "CastSelf",
    ) -> "_4251.SpringDamperHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4251

        return self.__parent__._cast(_4251.SpringDamperHalfPowerFlow)

    @property
    def straight_bevel_diff_gear_power_flow(
        self: "CastSelf",
    ) -> "_4254.StraightBevelDiffGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4254

        return self.__parent__._cast(_4254.StraightBevelDiffGearPowerFlow)

    @property
    def straight_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4257.StraightBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4257

        return self.__parent__._cast(_4257.StraightBevelGearPowerFlow)

    @property
    def straight_bevel_planet_gear_power_flow(
        self: "CastSelf",
    ) -> "_4259.StraightBevelPlanetGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4259

        return self.__parent__._cast(_4259.StraightBevelPlanetGearPowerFlow)

    @property
    def straight_bevel_sun_gear_power_flow(
        self: "CastSelf",
    ) -> "_4260.StraightBevelSunGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4260

        return self.__parent__._cast(_4260.StraightBevelSunGearPowerFlow)

    @property
    def synchroniser_half_power_flow(
        self: "CastSelf",
    ) -> "_4261.SynchroniserHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4261

        return self.__parent__._cast(_4261.SynchroniserHalfPowerFlow)

    @property
    def synchroniser_part_power_flow(
        self: "CastSelf",
    ) -> "_4262.SynchroniserPartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4262

        return self.__parent__._cast(_4262.SynchroniserPartPowerFlow)

    @property
    def synchroniser_sleeve_power_flow(
        self: "CastSelf",
    ) -> "_4264.SynchroniserSleevePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4264

        return self.__parent__._cast(_4264.SynchroniserSleevePowerFlow)

    @property
    def torque_converter_pump_power_flow(
        self: "CastSelf",
    ) -> "_4268.TorqueConverterPumpPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4268

        return self.__parent__._cast(_4268.TorqueConverterPumpPowerFlow)

    @property
    def torque_converter_turbine_power_flow(
        self: "CastSelf",
    ) -> "_4269.TorqueConverterTurbinePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4269

        return self.__parent__._cast(_4269.TorqueConverterTurbinePowerFlow)

    @property
    def unbalanced_mass_power_flow(self: "CastSelf") -> "_4270.UnbalancedMassPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4270

        return self.__parent__._cast(_4270.UnbalancedMassPowerFlow)

    @property
    def virtual_component_power_flow(
        self: "CastSelf",
    ) -> "_4271.VirtualComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4271

        return self.__parent__._cast(_4271.VirtualComponentPowerFlow)

    @property
    def worm_gear_power_flow(self: "CastSelf") -> "_4273.WormGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4273

        return self.__parent__._cast(_4273.WormGearPowerFlow)

    @property
    def zerol_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4276.ZerolBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4276

        return self.__parent__._cast(_4276.ZerolBevelGearPowerFlow)

    @property
    def component_power_flow(self: "CastSelf") -> "ComponentPowerFlow":
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
class ComponentPowerFlow(_4225.PartPowerFlow):
    """ComponentPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Speed")

        if temp is None:
            return 0.0

        return temp

    @property
    def component_design(self: "Self") -> "_2502.Component":
        """mastapy.system_model.part_model.Component

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ComponentPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_ComponentPowerFlow
        """
        return _Cast_ComponentPowerFlow(self)
