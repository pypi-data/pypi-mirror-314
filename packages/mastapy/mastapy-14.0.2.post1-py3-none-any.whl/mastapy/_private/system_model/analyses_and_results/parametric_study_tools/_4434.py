"""ComponentParametricStudyTool"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
    _4508,
)

_COMPONENT_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "ComponentParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740, _2742, _2746
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7719
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4410,
        _4411,
        _4414,
        _4417,
        _4421,
        _4423,
        _4424,
        _4426,
        _4429,
        _4431,
        _4436,
        _4439,
        _4442,
        _4445,
        _4447,
        _4451,
        _4454,
        _4457,
        _4459,
        _4460,
        _4468,
        _4470,
        _4472,
        _4475,
        _4477,
        _4479,
        _4483,
        _4486,
        _4489,
        _4491,
        _4492,
        _4494,
        _4496,
        _4497,
        _4510,
        _4514,
        _4515,
        _4516,
        _4517,
        _4518,
        _4522,
        _4524,
        _4525,
        _4529,
        _4532,
        _4535,
        _4538,
        _4540,
        _4541,
        _4542,
        _4544,
        _4545,
        _4548,
        _4549,
        _4550,
        _4551,
        _4553,
        _4556,
    )
    from mastapy._private.system_model.part_model import _2502

    Self = TypeVar("Self", bound="ComponentParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ComponentParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentParametricStudyTool:
    """Special nested class for casting ComponentParametricStudyTool to subclasses."""

    __parent__: "ComponentParametricStudyTool"

    @property
    def part_parametric_study_tool(self: "CastSelf") -> "_4508.PartParametricStudyTool":
        return self.__parent__._cast(_4508.PartParametricStudyTool)

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
    def abstract_shaft_or_housing_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4410.AbstractShaftOrHousingParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4410,
        )

        return self.__parent__._cast(_4410.AbstractShaftOrHousingParametricStudyTool)

    @property
    def abstract_shaft_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4411.AbstractShaftParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4411,
        )

        return self.__parent__._cast(_4411.AbstractShaftParametricStudyTool)

    @property
    def agma_gleason_conical_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4414.AGMAGleasonConicalGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4414,
        )

        return self.__parent__._cast(_4414.AGMAGleasonConicalGearParametricStudyTool)

    @property
    def bearing_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4417.BearingParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4417,
        )

        return self.__parent__._cast(_4417.BearingParametricStudyTool)

    @property
    def bevel_differential_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4421.BevelDifferentialGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4421,
        )

        return self.__parent__._cast(_4421.BevelDifferentialGearParametricStudyTool)

    @property
    def bevel_differential_planet_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4423.BevelDifferentialPlanetGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4423,
        )

        return self.__parent__._cast(
            _4423.BevelDifferentialPlanetGearParametricStudyTool
        )

    @property
    def bevel_differential_sun_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4424.BevelDifferentialSunGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4424,
        )

        return self.__parent__._cast(_4424.BevelDifferentialSunGearParametricStudyTool)

    @property
    def bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4426.BevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4426,
        )

        return self.__parent__._cast(_4426.BevelGearParametricStudyTool)

    @property
    def bolt_parametric_study_tool(self: "CastSelf") -> "_4429.BoltParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4429,
        )

        return self.__parent__._cast(_4429.BoltParametricStudyTool)

    @property
    def clutch_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4431.ClutchHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4431,
        )

        return self.__parent__._cast(_4431.ClutchHalfParametricStudyTool)

    @property
    def concept_coupling_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4436.ConceptCouplingHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4436,
        )

        return self.__parent__._cast(_4436.ConceptCouplingHalfParametricStudyTool)

    @property
    def concept_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4439.ConceptGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4439,
        )

        return self.__parent__._cast(_4439.ConceptGearParametricStudyTool)

    @property
    def conical_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4442.ConicalGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4442,
        )

        return self.__parent__._cast(_4442.ConicalGearParametricStudyTool)

    @property
    def connector_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4445.ConnectorParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4445,
        )

        return self.__parent__._cast(_4445.ConnectorParametricStudyTool)

    @property
    def coupling_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4447.CouplingHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4447,
        )

        return self.__parent__._cast(_4447.CouplingHalfParametricStudyTool)

    @property
    def cvt_pulley_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4451.CVTPulleyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4451,
        )

        return self.__parent__._cast(_4451.CVTPulleyParametricStudyTool)

    @property
    def cycloidal_disc_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4454.CycloidalDiscParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4454,
        )

        return self.__parent__._cast(_4454.CycloidalDiscParametricStudyTool)

    @property
    def cylindrical_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4457.CylindricalGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4457,
        )

        return self.__parent__._cast(_4457.CylindricalGearParametricStudyTool)

    @property
    def cylindrical_planet_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4459.CylindricalPlanetGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4459,
        )

        return self.__parent__._cast(_4459.CylindricalPlanetGearParametricStudyTool)

    @property
    def datum_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4460.DatumParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4460,
        )

        return self.__parent__._cast(_4460.DatumParametricStudyTool)

    @property
    def external_cad_model_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4468.ExternalCADModelParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4468,
        )

        return self.__parent__._cast(_4468.ExternalCADModelParametricStudyTool)

    @property
    def face_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4470.FaceGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4470,
        )

        return self.__parent__._cast(_4470.FaceGearParametricStudyTool)

    @property
    def fe_part_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4472.FEPartParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4472,
        )

        return self.__parent__._cast(_4472.FEPartParametricStudyTool)

    @property
    def gear_parametric_study_tool(self: "CastSelf") -> "_4475.GearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4475,
        )

        return self.__parent__._cast(_4475.GearParametricStudyTool)

    @property
    def guide_dxf_model_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4477.GuideDxfModelParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4477,
        )

        return self.__parent__._cast(_4477.GuideDxfModelParametricStudyTool)

    @property
    def hypoid_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4479.HypoidGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4479,
        )

        return self.__parent__._cast(_4479.HypoidGearParametricStudyTool)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4483.KlingelnbergCycloPalloidConicalGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4483,
        )

        return self.__parent__._cast(
            _4483.KlingelnbergCycloPalloidConicalGearParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4486.KlingelnbergCycloPalloidHypoidGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4486,
        )

        return self.__parent__._cast(
            _4486.KlingelnbergCycloPalloidHypoidGearParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4489.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4489,
        )

        return self.__parent__._cast(
            _4489.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool
        )

    @property
    def mass_disc_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4491.MassDiscParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4491,
        )

        return self.__parent__._cast(_4491.MassDiscParametricStudyTool)

    @property
    def measurement_component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4492.MeasurementComponentParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4492,
        )

        return self.__parent__._cast(_4492.MeasurementComponentParametricStudyTool)

    @property
    def microphone_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4494.MicrophoneParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4494,
        )

        return self.__parent__._cast(_4494.MicrophoneParametricStudyTool)

    @property
    def mountable_component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4496.MountableComponentParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4496,
        )

        return self.__parent__._cast(_4496.MountableComponentParametricStudyTool)

    @property
    def oil_seal_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4497.OilSealParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4497,
        )

        return self.__parent__._cast(_4497.OilSealParametricStudyTool)

    @property
    def part_to_part_shear_coupling_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4510.PartToPartShearCouplingHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4510,
        )

        return self.__parent__._cast(
            _4510.PartToPartShearCouplingHalfParametricStudyTool
        )

    @property
    def planet_carrier_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4514.PlanetCarrierParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4514,
        )

        return self.__parent__._cast(_4514.PlanetCarrierParametricStudyTool)

    @property
    def point_load_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4515.PointLoadParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4515,
        )

        return self.__parent__._cast(_4515.PointLoadParametricStudyTool)

    @property
    def power_load_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4516.PowerLoadParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4516,
        )

        return self.__parent__._cast(_4516.PowerLoadParametricStudyTool)

    @property
    def pulley_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4517.PulleyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4517,
        )

        return self.__parent__._cast(_4517.PulleyParametricStudyTool)

    @property
    def ring_pins_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4518.RingPinsParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4518,
        )

        return self.__parent__._cast(_4518.RingPinsParametricStudyTool)

    @property
    def rolling_ring_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4522.RollingRingParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4522,
        )

        return self.__parent__._cast(_4522.RollingRingParametricStudyTool)

    @property
    def shaft_hub_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4524.ShaftHubConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4524,
        )

        return self.__parent__._cast(_4524.ShaftHubConnectionParametricStudyTool)

    @property
    def shaft_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4525.ShaftParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4525,
        )

        return self.__parent__._cast(_4525.ShaftParametricStudyTool)

    @property
    def spiral_bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4529.SpiralBevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4529,
        )

        return self.__parent__._cast(_4529.SpiralBevelGearParametricStudyTool)

    @property
    def spring_damper_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4532.SpringDamperHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4532,
        )

        return self.__parent__._cast(_4532.SpringDamperHalfParametricStudyTool)

    @property
    def straight_bevel_diff_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4535.StraightBevelDiffGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4535,
        )

        return self.__parent__._cast(_4535.StraightBevelDiffGearParametricStudyTool)

    @property
    def straight_bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4538.StraightBevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4538,
        )

        return self.__parent__._cast(_4538.StraightBevelGearParametricStudyTool)

    @property
    def straight_bevel_planet_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4540.StraightBevelPlanetGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4540,
        )

        return self.__parent__._cast(_4540.StraightBevelPlanetGearParametricStudyTool)

    @property
    def straight_bevel_sun_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4541.StraightBevelSunGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4541,
        )

        return self.__parent__._cast(_4541.StraightBevelSunGearParametricStudyTool)

    @property
    def synchroniser_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4542.SynchroniserHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4542,
        )

        return self.__parent__._cast(_4542.SynchroniserHalfParametricStudyTool)

    @property
    def synchroniser_part_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4544.SynchroniserPartParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4544,
        )

        return self.__parent__._cast(_4544.SynchroniserPartParametricStudyTool)

    @property
    def synchroniser_sleeve_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4545.SynchroniserSleeveParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4545,
        )

        return self.__parent__._cast(_4545.SynchroniserSleeveParametricStudyTool)

    @property
    def torque_converter_pump_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4548.TorqueConverterPumpParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4548,
        )

        return self.__parent__._cast(_4548.TorqueConverterPumpParametricStudyTool)

    @property
    def torque_converter_turbine_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4549.TorqueConverterTurbineParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4549,
        )

        return self.__parent__._cast(_4549.TorqueConverterTurbineParametricStudyTool)

    @property
    def unbalanced_mass_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4550.UnbalancedMassParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4550,
        )

        return self.__parent__._cast(_4550.UnbalancedMassParametricStudyTool)

    @property
    def virtual_component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4551.VirtualComponentParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4551,
        )

        return self.__parent__._cast(_4551.VirtualComponentParametricStudyTool)

    @property
    def worm_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4553.WormGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4553,
        )

        return self.__parent__._cast(_4553.WormGearParametricStudyTool)

    @property
    def zerol_bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4556.ZerolBevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4556,
        )

        return self.__parent__._cast(_4556.ZerolBevelGearParametricStudyTool)

    @property
    def component_parametric_study_tool(
        self: "CastSelf",
    ) -> "ComponentParametricStudyTool":
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
class ComponentParametricStudyTool(_4508.PartParametricStudyTool):
    """ComponentParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def cast_to(self: "Self") -> "_Cast_ComponentParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_ComponentParametricStudyTool
        """
        return _Cast_ComponentParametricStudyTool(self)
