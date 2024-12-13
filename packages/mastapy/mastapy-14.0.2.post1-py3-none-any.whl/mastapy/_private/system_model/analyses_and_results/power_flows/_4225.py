"""PartPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7722

_PART_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "PartPowerFlow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740, _2742, _2746
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7719
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4141,
        _4142,
        _4143,
        _4146,
        _4147,
        _4148,
        _4149,
        _4151,
        _4153,
        _4154,
        _4155,
        _4156,
        _4158,
        _4159,
        _4160,
        _4161,
        _4163,
        _4164,
        _4166,
        _4168,
        _4169,
        _4171,
        _4172,
        _4174,
        _4175,
        _4177,
        _4179,
        _4180,
        _4182,
        _4183,
        _4184,
        _4187,
        _4190,
        _4191,
        _4192,
        _4193,
        _4194,
        _4196,
        _4197,
        _4200,
        _4201,
        _4203,
        _4204,
        _4205,
        _4207,
        _4208,
        _4211,
        _4212,
        _4214,
        _4215,
        _4217,
        _4218,
        _4219,
        _4220,
        _4221,
        _4222,
        _4223,
        _4224,
        _4227,
        _4228,
        _4230,
        _4231,
        _4232,
        _4233,
        _4235,
        _4236,
        _4237,
        _4239,
        _4241,
        _4242,
        _4243,
        _4244,
        _4246,
        _4248,
        _4249,
        _4251,
        _4252,
        _4254,
        _4255,
        _4257,
        _4258,
        _4259,
        _4260,
        _4261,
        _4262,
        _4263,
        _4264,
        _4267,
        _4268,
        _4269,
        _4270,
        _4271,
        _4273,
        _4274,
        _4276,
        _4277,
    )
    from mastapy._private.system_model.drawing import _2311
    from mastapy._private.system_model.part_model import _2528

    Self = TypeVar("Self", bound="PartPowerFlow")
    CastSelf = TypeVar("CastSelf", bound="PartPowerFlow._Cast_PartPowerFlow")


__docformat__ = "restructuredtext en"
__all__ = ("PartPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartPowerFlow:
    """Special nested class for casting PartPowerFlow to subclasses."""

    __parent__: "PartPowerFlow"

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7722.PartStaticLoadAnalysisCase":
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
    def abstract_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4141.AbstractAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4141

        return self.__parent__._cast(_4141.AbstractAssemblyPowerFlow)

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
    def agma_gleason_conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4147.AGMAGleasonConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4147

        return self.__parent__._cast(_4147.AGMAGleasonConicalGearSetPowerFlow)

    @property
    def assembly_power_flow(self: "CastSelf") -> "_4148.AssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4148

        return self.__parent__._cast(_4148.AssemblyPowerFlow)

    @property
    def bearing_power_flow(self: "CastSelf") -> "_4149.BearingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4149

        return self.__parent__._cast(_4149.BearingPowerFlow)

    @property
    def belt_drive_power_flow(self: "CastSelf") -> "_4151.BeltDrivePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4151

        return self.__parent__._cast(_4151.BeltDrivePowerFlow)

    @property
    def bevel_differential_gear_power_flow(
        self: "CastSelf",
    ) -> "_4153.BevelDifferentialGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4153

        return self.__parent__._cast(_4153.BevelDifferentialGearPowerFlow)

    @property
    def bevel_differential_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4154.BevelDifferentialGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4154

        return self.__parent__._cast(_4154.BevelDifferentialGearSetPowerFlow)

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
    def bevel_gear_set_power_flow(self: "CastSelf") -> "_4159.BevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4159

        return self.__parent__._cast(_4159.BevelGearSetPowerFlow)

    @property
    def bolted_joint_power_flow(self: "CastSelf") -> "_4160.BoltedJointPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4160

        return self.__parent__._cast(_4160.BoltedJointPowerFlow)

    @property
    def bolt_power_flow(self: "CastSelf") -> "_4161.BoltPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4161

        return self.__parent__._cast(_4161.BoltPowerFlow)

    @property
    def clutch_half_power_flow(self: "CastSelf") -> "_4163.ClutchHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4163

        return self.__parent__._cast(_4163.ClutchHalfPowerFlow)

    @property
    def clutch_power_flow(self: "CastSelf") -> "_4164.ClutchPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4164

        return self.__parent__._cast(_4164.ClutchPowerFlow)

    @property
    def component_power_flow(self: "CastSelf") -> "_4166.ComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4166

        return self.__parent__._cast(_4166.ComponentPowerFlow)

    @property
    def concept_coupling_half_power_flow(
        self: "CastSelf",
    ) -> "_4168.ConceptCouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4168

        return self.__parent__._cast(_4168.ConceptCouplingHalfPowerFlow)

    @property
    def concept_coupling_power_flow(
        self: "CastSelf",
    ) -> "_4169.ConceptCouplingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4169

        return self.__parent__._cast(_4169.ConceptCouplingPowerFlow)

    @property
    def concept_gear_power_flow(self: "CastSelf") -> "_4171.ConceptGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4171

        return self.__parent__._cast(_4171.ConceptGearPowerFlow)

    @property
    def concept_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4172.ConceptGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4172

        return self.__parent__._cast(_4172.ConceptGearSetPowerFlow)

    @property
    def conical_gear_power_flow(self: "CastSelf") -> "_4174.ConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4174

        return self.__parent__._cast(_4174.ConicalGearPowerFlow)

    @property
    def conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4175.ConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4175

        return self.__parent__._cast(_4175.ConicalGearSetPowerFlow)

    @property
    def connector_power_flow(self: "CastSelf") -> "_4177.ConnectorPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4177

        return self.__parent__._cast(_4177.ConnectorPowerFlow)

    @property
    def coupling_half_power_flow(self: "CastSelf") -> "_4179.CouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4179

        return self.__parent__._cast(_4179.CouplingHalfPowerFlow)

    @property
    def coupling_power_flow(self: "CastSelf") -> "_4180.CouplingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4180

        return self.__parent__._cast(_4180.CouplingPowerFlow)

    @property
    def cvt_power_flow(self: "CastSelf") -> "_4182.CVTPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4182

        return self.__parent__._cast(_4182.CVTPowerFlow)

    @property
    def cvt_pulley_power_flow(self: "CastSelf") -> "_4183.CVTPulleyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4183

        return self.__parent__._cast(_4183.CVTPulleyPowerFlow)

    @property
    def cycloidal_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4184.CycloidalAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4184

        return self.__parent__._cast(_4184.CycloidalAssemblyPowerFlow)

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
    def cylindrical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4191.CylindricalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4191

        return self.__parent__._cast(_4191.CylindricalGearSetPowerFlow)

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
    def face_gear_set_power_flow(self: "CastSelf") -> "_4197.FaceGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4197

        return self.__parent__._cast(_4197.FaceGearSetPowerFlow)

    @property
    def fe_part_power_flow(self: "CastSelf") -> "_4200.FEPartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4200

        return self.__parent__._cast(_4200.FEPartPowerFlow)

    @property
    def flexible_pin_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4201.FlexiblePinAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4201

        return self.__parent__._cast(_4201.FlexiblePinAssemblyPowerFlow)

    @property
    def gear_power_flow(self: "CastSelf") -> "_4203.GearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4203

        return self.__parent__._cast(_4203.GearPowerFlow)

    @property
    def gear_set_power_flow(self: "CastSelf") -> "_4204.GearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4204

        return self.__parent__._cast(_4204.GearSetPowerFlow)

    @property
    def guide_dxf_model_power_flow(self: "CastSelf") -> "_4205.GuideDxfModelPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4205

        return self.__parent__._cast(_4205.GuideDxfModelPowerFlow)

    @property
    def hypoid_gear_power_flow(self: "CastSelf") -> "_4207.HypoidGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4207

        return self.__parent__._cast(_4207.HypoidGearPowerFlow)

    @property
    def hypoid_gear_set_power_flow(self: "CastSelf") -> "_4208.HypoidGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4208

        return self.__parent__._cast(_4208.HypoidGearSetPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4211.KlingelnbergCycloPalloidConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4211

        return self.__parent__._cast(_4211.KlingelnbergCycloPalloidConicalGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4212.KlingelnbergCycloPalloidConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4212

        return self.__parent__._cast(
            _4212.KlingelnbergCycloPalloidConicalGearSetPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_power_flow(
        self: "CastSelf",
    ) -> "_4214.KlingelnbergCycloPalloidHypoidGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4214

        return self.__parent__._cast(_4214.KlingelnbergCycloPalloidHypoidGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4215.KlingelnbergCycloPalloidHypoidGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4215

        return self.__parent__._cast(
            _4215.KlingelnbergCycloPalloidHypoidGearSetPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4217.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4217

        return self.__parent__._cast(
            _4217.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4218.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4218

        return self.__parent__._cast(
            _4218.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow
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
    def microphone_array_power_flow(
        self: "CastSelf",
    ) -> "_4221.MicrophoneArrayPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4221

        return self.__parent__._cast(_4221.MicrophoneArrayPowerFlow)

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
    def part_to_part_shear_coupling_power_flow(
        self: "CastSelf",
    ) -> "_4228.PartToPartShearCouplingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4228

        return self.__parent__._cast(_4228.PartToPartShearCouplingPowerFlow)

    @property
    def planetary_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4230.PlanetaryGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4230

        return self.__parent__._cast(_4230.PlanetaryGearSetPowerFlow)

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
    def rolling_ring_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4239.RollingRingAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4239

        return self.__parent__._cast(_4239.RollingRingAssemblyPowerFlow)

    @property
    def rolling_ring_power_flow(self: "CastSelf") -> "_4241.RollingRingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4241

        return self.__parent__._cast(_4241.RollingRingPowerFlow)

    @property
    def root_assembly_power_flow(self: "CastSelf") -> "_4242.RootAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4242

        return self.__parent__._cast(_4242.RootAssemblyPowerFlow)

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
    def specialised_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4246.SpecialisedAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4246

        return self.__parent__._cast(_4246.SpecialisedAssemblyPowerFlow)

    @property
    def spiral_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4248.SpiralBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4248

        return self.__parent__._cast(_4248.SpiralBevelGearPowerFlow)

    @property
    def spiral_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4249.SpiralBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4249

        return self.__parent__._cast(_4249.SpiralBevelGearSetPowerFlow)

    @property
    def spring_damper_half_power_flow(
        self: "CastSelf",
    ) -> "_4251.SpringDamperHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4251

        return self.__parent__._cast(_4251.SpringDamperHalfPowerFlow)

    @property
    def spring_damper_power_flow(self: "CastSelf") -> "_4252.SpringDamperPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4252

        return self.__parent__._cast(_4252.SpringDamperPowerFlow)

    @property
    def straight_bevel_diff_gear_power_flow(
        self: "CastSelf",
    ) -> "_4254.StraightBevelDiffGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4254

        return self.__parent__._cast(_4254.StraightBevelDiffGearPowerFlow)

    @property
    def straight_bevel_diff_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4255.StraightBevelDiffGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4255

        return self.__parent__._cast(_4255.StraightBevelDiffGearSetPowerFlow)

    @property
    def straight_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4257.StraightBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4257

        return self.__parent__._cast(_4257.StraightBevelGearPowerFlow)

    @property
    def straight_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4258.StraightBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4258

        return self.__parent__._cast(_4258.StraightBevelGearSetPowerFlow)

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
    def synchroniser_power_flow(self: "CastSelf") -> "_4263.SynchroniserPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4263

        return self.__parent__._cast(_4263.SynchroniserPowerFlow)

    @property
    def synchroniser_sleeve_power_flow(
        self: "CastSelf",
    ) -> "_4264.SynchroniserSleevePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4264

        return self.__parent__._cast(_4264.SynchroniserSleevePowerFlow)

    @property
    def torque_converter_power_flow(
        self: "CastSelf",
    ) -> "_4267.TorqueConverterPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4267

        return self.__parent__._cast(_4267.TorqueConverterPowerFlow)

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
    def worm_gear_set_power_flow(self: "CastSelf") -> "_4274.WormGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4274

        return self.__parent__._cast(_4274.WormGearSetPowerFlow)

    @property
    def zerol_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4276.ZerolBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4276

        return self.__parent__._cast(_4276.ZerolBevelGearPowerFlow)

    @property
    def zerol_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4277.ZerolBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4277

        return self.__parent__._cast(_4277.ZerolBevelGearSetPowerFlow)

    @property
    def part_power_flow(self: "CastSelf") -> "PartPowerFlow":
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
class PartPowerFlow(_7722.PartStaticLoadAnalysisCase):
    """PartPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def two_d_drawing_showing_power_flow(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TwoDDrawingShowingPowerFlow")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def component_design(self: "Self") -> "_2528.Part":
        """mastapy.system_model.part_model.Part

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def power_flow(self: "Self") -> "_4233.PowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.PowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlow")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    def create_viewable(self: "Self") -> "_2311.PowerFlowViewable":
        """mastapy.system_model.drawing.PowerFlowViewable"""
        method_result = pythonnet_method_call(self.wrapped, "CreateViewable")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PartPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_PartPowerFlow
        """
        return _Cast_PartPowerFlow(self)
