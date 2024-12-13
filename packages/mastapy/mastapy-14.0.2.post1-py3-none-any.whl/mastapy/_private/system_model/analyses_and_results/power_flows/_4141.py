"""AbstractAssemblyPowerFlow"""

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

_ABSTRACT_ASSEMBLY_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows",
    "AbstractAssemblyPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740, _2742, _2746
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7719,
        _7722,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4147,
        _4148,
        _4151,
        _4154,
        _4159,
        _4160,
        _4164,
        _4169,
        _4172,
        _4175,
        _4180,
        _4182,
        _4184,
        _4191,
        _4197,
        _4201,
        _4204,
        _4208,
        _4212,
        _4215,
        _4218,
        _4221,
        _4228,
        _4230,
        _4239,
        _4242,
        _4246,
        _4249,
        _4252,
        _4255,
        _4258,
        _4263,
        _4267,
        _4274,
        _4277,
    )
    from mastapy._private.system_model.part_model import _2492

    Self = TypeVar("Self", bound="AbstractAssemblyPowerFlow")
    CastSelf = TypeVar(
        "CastSelf", bound="AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractAssemblyPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractAssemblyPowerFlow:
    """Special nested class for casting AbstractAssemblyPowerFlow to subclasses."""

    __parent__: "AbstractAssemblyPowerFlow"

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
    def belt_drive_power_flow(self: "CastSelf") -> "_4151.BeltDrivePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4151

        return self.__parent__._cast(_4151.BeltDrivePowerFlow)

    @property
    def bevel_differential_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4154.BevelDifferentialGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4154

        return self.__parent__._cast(_4154.BevelDifferentialGearSetPowerFlow)

    @property
    def bevel_gear_set_power_flow(self: "CastSelf") -> "_4159.BevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4159

        return self.__parent__._cast(_4159.BevelGearSetPowerFlow)

    @property
    def bolted_joint_power_flow(self: "CastSelf") -> "_4160.BoltedJointPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4160

        return self.__parent__._cast(_4160.BoltedJointPowerFlow)

    @property
    def clutch_power_flow(self: "CastSelf") -> "_4164.ClutchPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4164

        return self.__parent__._cast(_4164.ClutchPowerFlow)

    @property
    def concept_coupling_power_flow(
        self: "CastSelf",
    ) -> "_4169.ConceptCouplingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4169

        return self.__parent__._cast(_4169.ConceptCouplingPowerFlow)

    @property
    def concept_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4172.ConceptGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4172

        return self.__parent__._cast(_4172.ConceptGearSetPowerFlow)

    @property
    def conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4175.ConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4175

        return self.__parent__._cast(_4175.ConicalGearSetPowerFlow)

    @property
    def coupling_power_flow(self: "CastSelf") -> "_4180.CouplingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4180

        return self.__parent__._cast(_4180.CouplingPowerFlow)

    @property
    def cvt_power_flow(self: "CastSelf") -> "_4182.CVTPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4182

        return self.__parent__._cast(_4182.CVTPowerFlow)

    @property
    def cycloidal_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4184.CycloidalAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4184

        return self.__parent__._cast(_4184.CycloidalAssemblyPowerFlow)

    @property
    def cylindrical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4191.CylindricalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4191

        return self.__parent__._cast(_4191.CylindricalGearSetPowerFlow)

    @property
    def face_gear_set_power_flow(self: "CastSelf") -> "_4197.FaceGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4197

        return self.__parent__._cast(_4197.FaceGearSetPowerFlow)

    @property
    def flexible_pin_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4201.FlexiblePinAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4201

        return self.__parent__._cast(_4201.FlexiblePinAssemblyPowerFlow)

    @property
    def gear_set_power_flow(self: "CastSelf") -> "_4204.GearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4204

        return self.__parent__._cast(_4204.GearSetPowerFlow)

    @property
    def hypoid_gear_set_power_flow(self: "CastSelf") -> "_4208.HypoidGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4208

        return self.__parent__._cast(_4208.HypoidGearSetPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4212.KlingelnbergCycloPalloidConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4212

        return self.__parent__._cast(
            _4212.KlingelnbergCycloPalloidConicalGearSetPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4215.KlingelnbergCycloPalloidHypoidGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4215

        return self.__parent__._cast(
            _4215.KlingelnbergCycloPalloidHypoidGearSetPowerFlow
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
    def microphone_array_power_flow(
        self: "CastSelf",
    ) -> "_4221.MicrophoneArrayPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4221

        return self.__parent__._cast(_4221.MicrophoneArrayPowerFlow)

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
    def rolling_ring_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4239.RollingRingAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4239

        return self.__parent__._cast(_4239.RollingRingAssemblyPowerFlow)

    @property
    def root_assembly_power_flow(self: "CastSelf") -> "_4242.RootAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4242

        return self.__parent__._cast(_4242.RootAssemblyPowerFlow)

    @property
    def specialised_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4246.SpecialisedAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4246

        return self.__parent__._cast(_4246.SpecialisedAssemblyPowerFlow)

    @property
    def spiral_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4249.SpiralBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4249

        return self.__parent__._cast(_4249.SpiralBevelGearSetPowerFlow)

    @property
    def spring_damper_power_flow(self: "CastSelf") -> "_4252.SpringDamperPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4252

        return self.__parent__._cast(_4252.SpringDamperPowerFlow)

    @property
    def straight_bevel_diff_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4255.StraightBevelDiffGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4255

        return self.__parent__._cast(_4255.StraightBevelDiffGearSetPowerFlow)

    @property
    def straight_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4258.StraightBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4258

        return self.__parent__._cast(_4258.StraightBevelGearSetPowerFlow)

    @property
    def synchroniser_power_flow(self: "CastSelf") -> "_4263.SynchroniserPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4263

        return self.__parent__._cast(_4263.SynchroniserPowerFlow)

    @property
    def torque_converter_power_flow(
        self: "CastSelf",
    ) -> "_4267.TorqueConverterPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4267

        return self.__parent__._cast(_4267.TorqueConverterPowerFlow)

    @property
    def worm_gear_set_power_flow(self: "CastSelf") -> "_4274.WormGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4274

        return self.__parent__._cast(_4274.WormGearSetPowerFlow)

    @property
    def zerol_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4277.ZerolBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4277

        return self.__parent__._cast(_4277.ZerolBevelGearSetPowerFlow)

    @property
    def abstract_assembly_power_flow(self: "CastSelf") -> "AbstractAssemblyPowerFlow":
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
class AbstractAssemblyPowerFlow(_4225.PartPowerFlow):
    """AbstractAssemblyPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_ASSEMBLY_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2492.AbstractAssembly":
        """mastapy.system_model.part_model.AbstractAssembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_design(self: "Self") -> "_2492.AbstractAssembly":
        """mastapy.system_model.part_model.AbstractAssembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractAssemblyPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_AbstractAssemblyPowerFlow
        """
        return _Cast_AbstractAssemblyPowerFlow(self)
