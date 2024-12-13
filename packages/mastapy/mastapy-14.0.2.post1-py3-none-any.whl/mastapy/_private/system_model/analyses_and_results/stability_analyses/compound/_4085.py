"""PartCompoundStabilityAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7720

_PART_COMPOUND_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
    "PartCompoundStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7717
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3951,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
        _4004,
        _4005,
        _4006,
        _4008,
        _4010,
        _4011,
        _4012,
        _4014,
        _4015,
        _4017,
        _4018,
        _4019,
        _4020,
        _4022,
        _4023,
        _4024,
        _4025,
        _4027,
        _4029,
        _4030,
        _4032,
        _4033,
        _4035,
        _4036,
        _4038,
        _4040,
        _4041,
        _4043,
        _4045,
        _4046,
        _4047,
        _4049,
        _4051,
        _4053,
        _4054,
        _4055,
        _4056,
        _4057,
        _4059,
        _4060,
        _4061,
        _4062,
        _4064,
        _4065,
        _4066,
        _4068,
        _4070,
        _4072,
        _4073,
        _4075,
        _4076,
        _4078,
        _4079,
        _4080,
        _4081,
        _4082,
        _4083,
        _4084,
        _4086,
        _4088,
        _4090,
        _4091,
        _4092,
        _4093,
        _4094,
        _4095,
        _4097,
        _4098,
        _4100,
        _4101,
        _4102,
        _4104,
        _4105,
        _4107,
        _4108,
        _4110,
        _4111,
        _4113,
        _4114,
        _4116,
        _4117,
        _4118,
        _4119,
        _4120,
        _4121,
        _4122,
        _4123,
        _4125,
        _4126,
        _4127,
        _4128,
        _4129,
        _4131,
        _4132,
        _4134,
    )

    Self = TypeVar("Self", bound="PartCompoundStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PartCompoundStabilityAnalysis._Cast_PartCompoundStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartCompoundStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartCompoundStabilityAnalysis:
    """Special nested class for casting PartCompoundStabilityAnalysis to subclasses."""

    __parent__: "PartCompoundStabilityAnalysis"

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7720.PartCompoundAnalysis":
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
    def abstract_assembly_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4004.AbstractAssemblyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4004,
        )

        return self.__parent__._cast(_4004.AbstractAssemblyCompoundStabilityAnalysis)

    @property
    def abstract_shaft_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4005.AbstractShaftCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4005,
        )

        return self.__parent__._cast(_4005.AbstractShaftCompoundStabilityAnalysis)

    @property
    def abstract_shaft_or_housing_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4006.AbstractShaftOrHousingCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4006,
        )

        return self.__parent__._cast(
            _4006.AbstractShaftOrHousingCompoundStabilityAnalysis
        )

    @property
    def agma_gleason_conical_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4008.AGMAGleasonConicalGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4008,
        )

        return self.__parent__._cast(
            _4008.AGMAGleasonConicalGearCompoundStabilityAnalysis
        )

    @property
    def agma_gleason_conical_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4010.AGMAGleasonConicalGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4010,
        )

        return self.__parent__._cast(
            _4010.AGMAGleasonConicalGearSetCompoundStabilityAnalysis
        )

    @property
    def assembly_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4011.AssemblyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4011,
        )

        return self.__parent__._cast(_4011.AssemblyCompoundStabilityAnalysis)

    @property
    def bearing_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4012.BearingCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4012,
        )

        return self.__parent__._cast(_4012.BearingCompoundStabilityAnalysis)

    @property
    def belt_drive_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4014.BeltDriveCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4014,
        )

        return self.__parent__._cast(_4014.BeltDriveCompoundStabilityAnalysis)

    @property
    def bevel_differential_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4015.BevelDifferentialGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4015,
        )

        return self.__parent__._cast(
            _4015.BevelDifferentialGearCompoundStabilityAnalysis
        )

    @property
    def bevel_differential_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4017.BevelDifferentialGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4017,
        )

        return self.__parent__._cast(
            _4017.BevelDifferentialGearSetCompoundStabilityAnalysis
        )

    @property
    def bevel_differential_planet_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4018.BevelDifferentialPlanetGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4018,
        )

        return self.__parent__._cast(
            _4018.BevelDifferentialPlanetGearCompoundStabilityAnalysis
        )

    @property
    def bevel_differential_sun_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4019.BevelDifferentialSunGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4019,
        )

        return self.__parent__._cast(
            _4019.BevelDifferentialSunGearCompoundStabilityAnalysis
        )

    @property
    def bevel_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4020.BevelGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4020,
        )

        return self.__parent__._cast(_4020.BevelGearCompoundStabilityAnalysis)

    @property
    def bevel_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4022.BevelGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4022,
        )

        return self.__parent__._cast(_4022.BevelGearSetCompoundStabilityAnalysis)

    @property
    def bolt_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4023.BoltCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4023,
        )

        return self.__parent__._cast(_4023.BoltCompoundStabilityAnalysis)

    @property
    def bolted_joint_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4024.BoltedJointCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4024,
        )

        return self.__parent__._cast(_4024.BoltedJointCompoundStabilityAnalysis)

    @property
    def clutch_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4025.ClutchCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4025,
        )

        return self.__parent__._cast(_4025.ClutchCompoundStabilityAnalysis)

    @property
    def clutch_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4027.ClutchHalfCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4027,
        )

        return self.__parent__._cast(_4027.ClutchHalfCompoundStabilityAnalysis)

    @property
    def component_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4029.ComponentCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4029,
        )

        return self.__parent__._cast(_4029.ComponentCompoundStabilityAnalysis)

    @property
    def concept_coupling_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4030.ConceptCouplingCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4030,
        )

        return self.__parent__._cast(_4030.ConceptCouplingCompoundStabilityAnalysis)

    @property
    def concept_coupling_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4032.ConceptCouplingHalfCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4032,
        )

        return self.__parent__._cast(_4032.ConceptCouplingHalfCompoundStabilityAnalysis)

    @property
    def concept_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4033.ConceptGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4033,
        )

        return self.__parent__._cast(_4033.ConceptGearCompoundStabilityAnalysis)

    @property
    def concept_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4035.ConceptGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4035,
        )

        return self.__parent__._cast(_4035.ConceptGearSetCompoundStabilityAnalysis)

    @property
    def conical_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4036.ConicalGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4036,
        )

        return self.__parent__._cast(_4036.ConicalGearCompoundStabilityAnalysis)

    @property
    def conical_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4038.ConicalGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4038,
        )

        return self.__parent__._cast(_4038.ConicalGearSetCompoundStabilityAnalysis)

    @property
    def connector_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4040.ConnectorCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4040,
        )

        return self.__parent__._cast(_4040.ConnectorCompoundStabilityAnalysis)

    @property
    def coupling_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4041.CouplingCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4041,
        )

        return self.__parent__._cast(_4041.CouplingCompoundStabilityAnalysis)

    @property
    def coupling_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4043.CouplingHalfCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4043,
        )

        return self.__parent__._cast(_4043.CouplingHalfCompoundStabilityAnalysis)

    @property
    def cvt_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4045.CVTCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4045,
        )

        return self.__parent__._cast(_4045.CVTCompoundStabilityAnalysis)

    @property
    def cvt_pulley_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4046.CVTPulleyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4046,
        )

        return self.__parent__._cast(_4046.CVTPulleyCompoundStabilityAnalysis)

    @property
    def cycloidal_assembly_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4047.CycloidalAssemblyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4047,
        )

        return self.__parent__._cast(_4047.CycloidalAssemblyCompoundStabilityAnalysis)

    @property
    def cycloidal_disc_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4049.CycloidalDiscCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4049,
        )

        return self.__parent__._cast(_4049.CycloidalDiscCompoundStabilityAnalysis)

    @property
    def cylindrical_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4051.CylindricalGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4051,
        )

        return self.__parent__._cast(_4051.CylindricalGearCompoundStabilityAnalysis)

    @property
    def cylindrical_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4053.CylindricalGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4053,
        )

        return self.__parent__._cast(_4053.CylindricalGearSetCompoundStabilityAnalysis)

    @property
    def cylindrical_planet_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4054.CylindricalPlanetGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4054,
        )

        return self.__parent__._cast(
            _4054.CylindricalPlanetGearCompoundStabilityAnalysis
        )

    @property
    def datum_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4055.DatumCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4055,
        )

        return self.__parent__._cast(_4055.DatumCompoundStabilityAnalysis)

    @property
    def external_cad_model_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4056.ExternalCADModelCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4056,
        )

        return self.__parent__._cast(_4056.ExternalCADModelCompoundStabilityAnalysis)

    @property
    def face_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4057.FaceGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4057,
        )

        return self.__parent__._cast(_4057.FaceGearCompoundStabilityAnalysis)

    @property
    def face_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4059.FaceGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4059,
        )

        return self.__parent__._cast(_4059.FaceGearSetCompoundStabilityAnalysis)

    @property
    def fe_part_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4060.FEPartCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4060,
        )

        return self.__parent__._cast(_4060.FEPartCompoundStabilityAnalysis)

    @property
    def flexible_pin_assembly_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4061.FlexiblePinAssemblyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4061,
        )

        return self.__parent__._cast(_4061.FlexiblePinAssemblyCompoundStabilityAnalysis)

    @property
    def gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4062.GearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4062,
        )

        return self.__parent__._cast(_4062.GearCompoundStabilityAnalysis)

    @property
    def gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4064.GearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4064,
        )

        return self.__parent__._cast(_4064.GearSetCompoundStabilityAnalysis)

    @property
    def guide_dxf_model_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4065.GuideDxfModelCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4065,
        )

        return self.__parent__._cast(_4065.GuideDxfModelCompoundStabilityAnalysis)

    @property
    def hypoid_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4066.HypoidGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4066,
        )

        return self.__parent__._cast(_4066.HypoidGearCompoundStabilityAnalysis)

    @property
    def hypoid_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4068.HypoidGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4068,
        )

        return self.__parent__._cast(_4068.HypoidGearSetCompoundStabilityAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4070.KlingelnbergCycloPalloidConicalGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4070,
        )

        return self.__parent__._cast(
            _4070.KlingelnbergCycloPalloidConicalGearCompoundStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4072.KlingelnbergCycloPalloidConicalGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4072,
        )

        return self.__parent__._cast(
            _4072.KlingelnbergCycloPalloidConicalGearSetCompoundStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4073.KlingelnbergCycloPalloidHypoidGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4073,
        )

        return self.__parent__._cast(
            _4073.KlingelnbergCycloPalloidHypoidGearCompoundStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4075.KlingelnbergCycloPalloidHypoidGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4075,
        )

        return self.__parent__._cast(
            _4075.KlingelnbergCycloPalloidHypoidGearSetCompoundStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4076.KlingelnbergCycloPalloidSpiralBevelGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4076,
        )

        return self.__parent__._cast(
            _4076.KlingelnbergCycloPalloidSpiralBevelGearCompoundStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4078.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4078,
        )

        return self.__parent__._cast(
            _4078.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundStabilityAnalysis
        )

    @property
    def mass_disc_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4079.MassDiscCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4079,
        )

        return self.__parent__._cast(_4079.MassDiscCompoundStabilityAnalysis)

    @property
    def measurement_component_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4080.MeasurementComponentCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4080,
        )

        return self.__parent__._cast(
            _4080.MeasurementComponentCompoundStabilityAnalysis
        )

    @property
    def microphone_array_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4081.MicrophoneArrayCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4081,
        )

        return self.__parent__._cast(_4081.MicrophoneArrayCompoundStabilityAnalysis)

    @property
    def microphone_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4082.MicrophoneCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4082,
        )

        return self.__parent__._cast(_4082.MicrophoneCompoundStabilityAnalysis)

    @property
    def mountable_component_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4083.MountableComponentCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4083,
        )

        return self.__parent__._cast(_4083.MountableComponentCompoundStabilityAnalysis)

    @property
    def oil_seal_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4084.OilSealCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4084,
        )

        return self.__parent__._cast(_4084.OilSealCompoundStabilityAnalysis)

    @property
    def part_to_part_shear_coupling_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4086.PartToPartShearCouplingCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4086,
        )

        return self.__parent__._cast(
            _4086.PartToPartShearCouplingCompoundStabilityAnalysis
        )

    @property
    def part_to_part_shear_coupling_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4088.PartToPartShearCouplingHalfCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4088,
        )

        return self.__parent__._cast(
            _4088.PartToPartShearCouplingHalfCompoundStabilityAnalysis
        )

    @property
    def planetary_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4090.PlanetaryGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4090,
        )

        return self.__parent__._cast(_4090.PlanetaryGearSetCompoundStabilityAnalysis)

    @property
    def planet_carrier_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4091.PlanetCarrierCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4091,
        )

        return self.__parent__._cast(_4091.PlanetCarrierCompoundStabilityAnalysis)

    @property
    def point_load_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4092.PointLoadCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4092,
        )

        return self.__parent__._cast(_4092.PointLoadCompoundStabilityAnalysis)

    @property
    def power_load_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4093.PowerLoadCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4093,
        )

        return self.__parent__._cast(_4093.PowerLoadCompoundStabilityAnalysis)

    @property
    def pulley_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4094.PulleyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4094,
        )

        return self.__parent__._cast(_4094.PulleyCompoundStabilityAnalysis)

    @property
    def ring_pins_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4095.RingPinsCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4095,
        )

        return self.__parent__._cast(_4095.RingPinsCompoundStabilityAnalysis)

    @property
    def rolling_ring_assembly_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4097.RollingRingAssemblyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4097,
        )

        return self.__parent__._cast(_4097.RollingRingAssemblyCompoundStabilityAnalysis)

    @property
    def rolling_ring_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4098.RollingRingCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4098,
        )

        return self.__parent__._cast(_4098.RollingRingCompoundStabilityAnalysis)

    @property
    def root_assembly_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4100.RootAssemblyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4100,
        )

        return self.__parent__._cast(_4100.RootAssemblyCompoundStabilityAnalysis)

    @property
    def shaft_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4101.ShaftCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4101,
        )

        return self.__parent__._cast(_4101.ShaftCompoundStabilityAnalysis)

    @property
    def shaft_hub_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4102.ShaftHubConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4102,
        )

        return self.__parent__._cast(_4102.ShaftHubConnectionCompoundStabilityAnalysis)

    @property
    def specialised_assembly_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4104.SpecialisedAssemblyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4104,
        )

        return self.__parent__._cast(_4104.SpecialisedAssemblyCompoundStabilityAnalysis)

    @property
    def spiral_bevel_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4105.SpiralBevelGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4105,
        )

        return self.__parent__._cast(_4105.SpiralBevelGearCompoundStabilityAnalysis)

    @property
    def spiral_bevel_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4107.SpiralBevelGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4107,
        )

        return self.__parent__._cast(_4107.SpiralBevelGearSetCompoundStabilityAnalysis)

    @property
    def spring_damper_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4108.SpringDamperCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4108,
        )

        return self.__parent__._cast(_4108.SpringDamperCompoundStabilityAnalysis)

    @property
    def spring_damper_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4110.SpringDamperHalfCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4110,
        )

        return self.__parent__._cast(_4110.SpringDamperHalfCompoundStabilityAnalysis)

    @property
    def straight_bevel_diff_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4111.StraightBevelDiffGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4111,
        )

        return self.__parent__._cast(
            _4111.StraightBevelDiffGearCompoundStabilityAnalysis
        )

    @property
    def straight_bevel_diff_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4113.StraightBevelDiffGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4113,
        )

        return self.__parent__._cast(
            _4113.StraightBevelDiffGearSetCompoundStabilityAnalysis
        )

    @property
    def straight_bevel_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4114.StraightBevelGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4114,
        )

        return self.__parent__._cast(_4114.StraightBevelGearCompoundStabilityAnalysis)

    @property
    def straight_bevel_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4116.StraightBevelGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4116,
        )

        return self.__parent__._cast(
            _4116.StraightBevelGearSetCompoundStabilityAnalysis
        )

    @property
    def straight_bevel_planet_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4117.StraightBevelPlanetGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4117,
        )

        return self.__parent__._cast(
            _4117.StraightBevelPlanetGearCompoundStabilityAnalysis
        )

    @property
    def straight_bevel_sun_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4118.StraightBevelSunGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4118,
        )

        return self.__parent__._cast(
            _4118.StraightBevelSunGearCompoundStabilityAnalysis
        )

    @property
    def synchroniser_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4119.SynchroniserCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4119,
        )

        return self.__parent__._cast(_4119.SynchroniserCompoundStabilityAnalysis)

    @property
    def synchroniser_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4120.SynchroniserHalfCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4120,
        )

        return self.__parent__._cast(_4120.SynchroniserHalfCompoundStabilityAnalysis)

    @property
    def synchroniser_part_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4121.SynchroniserPartCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4121,
        )

        return self.__parent__._cast(_4121.SynchroniserPartCompoundStabilityAnalysis)

    @property
    def synchroniser_sleeve_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4122.SynchroniserSleeveCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4122,
        )

        return self.__parent__._cast(_4122.SynchroniserSleeveCompoundStabilityAnalysis)

    @property
    def torque_converter_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4123.TorqueConverterCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4123,
        )

        return self.__parent__._cast(_4123.TorqueConverterCompoundStabilityAnalysis)

    @property
    def torque_converter_pump_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4125.TorqueConverterPumpCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4125,
        )

        return self.__parent__._cast(_4125.TorqueConverterPumpCompoundStabilityAnalysis)

    @property
    def torque_converter_turbine_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4126.TorqueConverterTurbineCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4126,
        )

        return self.__parent__._cast(
            _4126.TorqueConverterTurbineCompoundStabilityAnalysis
        )

    @property
    def unbalanced_mass_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4127.UnbalancedMassCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4127,
        )

        return self.__parent__._cast(_4127.UnbalancedMassCompoundStabilityAnalysis)

    @property
    def virtual_component_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4128.VirtualComponentCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4128,
        )

        return self.__parent__._cast(_4128.VirtualComponentCompoundStabilityAnalysis)

    @property
    def worm_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4129.WormGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4129,
        )

        return self.__parent__._cast(_4129.WormGearCompoundStabilityAnalysis)

    @property
    def worm_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4131.WormGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4131,
        )

        return self.__parent__._cast(_4131.WormGearSetCompoundStabilityAnalysis)

    @property
    def zerol_bevel_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4132.ZerolBevelGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4132,
        )

        return self.__parent__._cast(_4132.ZerolBevelGearCompoundStabilityAnalysis)

    @property
    def zerol_bevel_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4134.ZerolBevelGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4134,
        )

        return self.__parent__._cast(_4134.ZerolBevelGearSetCompoundStabilityAnalysis)

    @property
    def part_compound_stability_analysis(
        self: "CastSelf",
    ) -> "PartCompoundStabilityAnalysis":
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
class PartCompoundStabilityAnalysis(_7720.PartCompoundAnalysis):
    """PartCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_COMPOUND_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(self: "Self") -> "List[_3951.PartStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.PartStabilityAnalysis]

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
    ) -> "List[_3951.PartStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.PartStabilityAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_PartCompoundStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_PartCompoundStabilityAnalysis
        """
        return _Cast_PartCompoundStabilityAnalysis(self)
