"""ConnectionAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results import _2742

_CONNECTION_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults", "ConnectionAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7431,
        _7436,
        _7440,
        _7443,
        _7448,
        _7453,
        _7455,
        _7458,
        _7461,
        _7464,
        _7466,
        _7470,
        _7473,
        _7477,
        _7478,
        _7480,
        _7487,
        _7492,
        _7496,
        _7498,
        _7500,
        _7503,
        _7506,
        _7517,
        _7519,
        _7526,
        _7529,
        _7533,
        _7536,
        _7539,
        _7542,
        _7545,
        _7554,
        _7561,
        _7564,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7163,
        _7169,
        _7174,
        _7177,
        _7182,
        _7187,
        _7189,
        _7192,
        _7195,
        _7198,
        _7200,
        _7203,
        _7206,
        _7210,
        _7211,
        _7213,
        _7219,
        _7224,
        _7229,
        _7231,
        _7233,
        _7236,
        _7239,
        _7249,
        _7251,
        _7258,
        _7261,
        _7265,
        _7268,
        _7271,
        _7274,
        _7277,
        _7286,
        _7292,
        _7295,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7714,
        _7715,
        _7716,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6694,
        _6696,
        _6700,
        _6703,
        _6708,
        _6712,
        _6715,
        _6717,
        _6721,
        _6724,
        _6726,
        _6728,
        _6734,
        _6738,
        _6740,
        _6742,
        _6748,
        _6753,
        _6757,
        _6759,
        _6761,
        _6764,
        _6767,
        _6776,
        _6779,
        _6786,
        _6788,
        _6793,
        _6796,
        _6798,
        _6802,
        _6805,
        _6813,
        _6820,
        _6823,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6424,
        _6426,
        _6430,
        _6433,
        _6438,
        _6442,
        _6445,
        _6447,
        _6451,
        _6454,
        _6456,
        _6458,
        _6461,
        _6465,
        _6467,
        _6469,
        _6477,
        _6482,
        _6486,
        _6488,
        _6490,
        _6493,
        _6496,
        _6505,
        _6508,
        _6515,
        _6517,
        _6522,
        _6525,
        _6527,
        _6531,
        _6534,
        _6542,
        _6549,
        _6552,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5818,
        _5820,
        _5824,
        _5827,
        _5832,
        _5836,
        _5839,
        _5842,
        _5846,
        _5849,
        _5851,
        _5853,
        _5856,
        _5860,
        _5862,
        _5864,
        _5884,
        _5891,
        _5908,
        _5910,
        _5912,
        _5915,
        _5918,
        _5927,
        _5931,
        _5939,
        _5941,
        _5946,
        _5951,
        _5953,
        _5958,
        _5961,
        _5969,
        _5977,
        _5980,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6151,
        _6153,
        _6157,
        _6160,
        _6165,
        _6169,
        _6172,
        _6174,
        _6178,
        _6181,
        _6183,
        _6185,
        _6188,
        _6192,
        _6194,
        _6196,
        _6202,
        _6207,
        _6212,
        _6214,
        _6216,
        _6219,
        _6222,
        _6232,
        _6235,
        _6242,
        _6244,
        _6249,
        _6252,
        _6254,
        _6258,
        _6261,
        _6269,
        _6276,
        _6279,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5508,
        _5509,
        _5517,
        _5519,
        _5524,
        _5529,
        _5533,
        _5535,
        _5538,
        _5541,
        _5544,
        _5546,
        _5549,
        _5553,
        _5555,
        _5556,
        _5562,
        _5567,
        _5572,
        _5579,
        _5580,
        _5583,
        _5586,
        _5600,
        _5603,
        _5610,
        _5612,
        _5619,
        _5622,
        _5626,
        _5629,
        _5632,
        _5641,
        _5650,
        _5653,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4692,
        _4693,
        _4698,
        _4700,
        _4705,
        _4710,
        _4713,
        _4715,
        _4718,
        _4721,
        _4724,
        _4727,
        _4730,
        _4734,
        _4736,
        _4737,
        _4746,
        _4752,
        _4756,
        _4759,
        _4760,
        _4763,
        _4766,
        _4782,
        _4785,
        _4792,
        _4794,
        _4800,
        _4802,
        _4805,
        _4808,
        _4811,
        _4820,
        _4829,
        _4832,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5245,
        _5246,
        _5251,
        _5253,
        _5258,
        _5263,
        _5266,
        _5268,
        _5271,
        _5274,
        _5277,
        _5279,
        _5282,
        _5286,
        _5288,
        _5289,
        _5295,
        _5300,
        _5304,
        _5307,
        _5308,
        _5311,
        _5314,
        _5325,
        _5328,
        _5335,
        _5337,
        _5342,
        _5344,
        _5347,
        _5350,
        _5353,
        _5362,
        _5368,
        _5371,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _4981,
        _4982,
        _4987,
        _4989,
        _4994,
        _4999,
        _5002,
        _5004,
        _5007,
        _5010,
        _5013,
        _5015,
        _5018,
        _5022,
        _5024,
        _5025,
        _5032,
        _5037,
        _5041,
        _5044,
        _5045,
        _5048,
        _5051,
        _5062,
        _5065,
        _5072,
        _5074,
        _5079,
        _5081,
        _5084,
        _5087,
        _5090,
        _5099,
        _5105,
        _5108,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4412,
        _4413,
        _4418,
        _4420,
        _4425,
        _4430,
        _4433,
        _4435,
        _4438,
        _4441,
        _4444,
        _4446,
        _4449,
        _4453,
        _4455,
        _4456,
        _4469,
        _4474,
        _4478,
        _4481,
        _4482,
        _4485,
        _4488,
        _4509,
        _4512,
        _4519,
        _4521,
        _4526,
        _4528,
        _4531,
        _4534,
        _4537,
        _4546,
        _4552,
        _4555,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4144,
        _4145,
        _4150,
        _4152,
        _4157,
        _4162,
        _4165,
        _4167,
        _4170,
        _4173,
        _4176,
        _4178,
        _4181,
        _4185,
        _4186,
        _4189,
        _4195,
        _4202,
        _4206,
        _4209,
        _4210,
        _4213,
        _4216,
        _4226,
        _4229,
        _4238,
        _4240,
        _4245,
        _4247,
        _4250,
        _4253,
        _4256,
        _4266,
        _4272,
        _4275,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3871,
        _3872,
        _3877,
        _3879,
        _3884,
        _3889,
        _3892,
        _3894,
        _3897,
        _3900,
        _3903,
        _3905,
        _3909,
        _3913,
        _3914,
        _3916,
        _3923,
        _3928,
        _3932,
        _3935,
        _3936,
        _3939,
        _3942,
        _3952,
        _3955,
        _3962,
        _3964,
        _3969,
        _3971,
        _3974,
        _3980,
        _3983,
        _3992,
        _3998,
        _4001,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6962,
        _6967,
        _6973,
        _6976,
        _6981,
        _6985,
        _6989,
        _6991,
        _6995,
        _6999,
        _7002,
        _7004,
        _7007,
        _7011,
        _7013,
        _7016,
        _7038,
        _7045,
        _7059,
        _7064,
        _7066,
        _7069,
        _7072,
        _7084,
        _7087,
        _7099,
        _7101,
        _7106,
        _7109,
        _7111,
        _7115,
        _7118,
        _7127,
        _7138,
        _7141,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3079,
        _3080,
        _3085,
        _3087,
        _3092,
        _3097,
        _3100,
        _3102,
        _3105,
        _3108,
        _3111,
        _3113,
        _3116,
        _3120,
        _3121,
        _3123,
        _3130,
        _3135,
        _3139,
        _3142,
        _3143,
        _3146,
        _3149,
        _3159,
        _3162,
        _3169,
        _3171,
        _3176,
        _3178,
        _3181,
        _3187,
        _3190,
        _3199,
        _3205,
        _3208,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3608,
        _3609,
        _3614,
        _3616,
        _3621,
        _3626,
        _3629,
        _3631,
        _3634,
        _3637,
        _3640,
        _3642,
        _3645,
        _3649,
        _3650,
        _3652,
        _3658,
        _3663,
        _3667,
        _3670,
        _3671,
        _3674,
        _3677,
        _3687,
        _3690,
        _3697,
        _3699,
        _3704,
        _3706,
        _3709,
        _3713,
        _3716,
        _3725,
        _3731,
        _3734,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
        _3345,
        _3346,
        _3351,
        _3353,
        _3358,
        _3363,
        _3366,
        _3368,
        _3371,
        _3374,
        _3377,
        _3379,
        _3382,
        _3386,
        _3387,
        _3389,
        _3395,
        _3400,
        _3404,
        _3407,
        _3408,
        _3411,
        _3414,
        _3424,
        _3427,
        _3434,
        _3436,
        _3441,
        _3443,
        _3446,
        _3450,
        _3453,
        _3462,
        _3468,
        _3471,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2777,
        _2778,
        _2788,
        _2790,
        _2795,
        _2800,
        _2803,
        _2806,
        _2809,
        _2813,
        _2816,
        _2818,
        _2821,
        _2825,
        _2826,
        _2828,
        _2829,
        _2830,
        _2843,
        _2848,
        _2852,
        _2856,
        _2857,
        _2860,
        _2863,
        _2877,
        _2880,
        _2886,
        _2889,
        _2896,
        _2898,
        _2901,
        _2904,
        _2907,
        _2919,
        _2927,
        _2930,
    )

    Self = TypeVar("Self", bound="ConnectionAnalysis")
    CastSelf = TypeVar("CastSelf", bound="ConnectionAnalysis._Cast_ConnectionAnalysis")


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionAnalysis:
    """Special nested class for casting ConnectionAnalysis to subclasses."""

    __parent__: "ConnectionAnalysis"

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2742.DesignEntitySingleContextAnalysis":
        return self.__parent__._cast(_2742.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2740.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2740

        return self.__parent__._cast(_2740.DesignEntityAnalysis)

    @property
    def abstract_shaft_to_mountable_component_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2777.AbstractShaftToMountableComponentConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2777,
        )

        return self.__parent__._cast(
            _2777.AbstractShaftToMountableComponentConnectionSystemDeflection
        )

    @property
    def agma_gleason_conical_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2778.AGMAGleasonConicalGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2778,
        )

        return self.__parent__._cast(_2778.AGMAGleasonConicalGearMeshSystemDeflection)

    @property
    def belt_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2788.BeltConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2788,
        )

        return self.__parent__._cast(_2788.BeltConnectionSystemDeflection)

    @property
    def bevel_differential_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2790.BevelDifferentialGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2790,
        )

        return self.__parent__._cast(_2790.BevelDifferentialGearMeshSystemDeflection)

    @property
    def bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2795.BevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2795,
        )

        return self.__parent__._cast(_2795.BevelGearMeshSystemDeflection)

    @property
    def clutch_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2800.ClutchConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2800,
        )

        return self.__parent__._cast(_2800.ClutchConnectionSystemDeflection)

    @property
    def coaxial_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2803.CoaxialConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2803,
        )

        return self.__parent__._cast(_2803.CoaxialConnectionSystemDeflection)

    @property
    def concept_coupling_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2806.ConceptCouplingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2806,
        )

        return self.__parent__._cast(_2806.ConceptCouplingConnectionSystemDeflection)

    @property
    def concept_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2809.ConceptGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2809,
        )

        return self.__parent__._cast(_2809.ConceptGearMeshSystemDeflection)

    @property
    def conical_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2813.ConicalGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2813,
        )

        return self.__parent__._cast(_2813.ConicalGearMeshSystemDeflection)

    @property
    def connection_system_deflection(
        self: "CastSelf",
    ) -> "_2816.ConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2816,
        )

        return self.__parent__._cast(_2816.ConnectionSystemDeflection)

    @property
    def coupling_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2818.CouplingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2818,
        )

        return self.__parent__._cast(_2818.CouplingConnectionSystemDeflection)

    @property
    def cvt_belt_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2821.CVTBeltConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2821,
        )

        return self.__parent__._cast(_2821.CVTBeltConnectionSystemDeflection)

    @property
    def cycloidal_disc_central_bearing_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2825.CycloidalDiscCentralBearingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2825,
        )

        return self.__parent__._cast(
            _2825.CycloidalDiscCentralBearingConnectionSystemDeflection
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2826.CycloidalDiscPlanetaryBearingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2826,
        )

        return self.__parent__._cast(
            _2826.CycloidalDiscPlanetaryBearingConnectionSystemDeflection
        )

    @property
    def cylindrical_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2828.CylindricalGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2828,
        )

        return self.__parent__._cast(_2828.CylindricalGearMeshSystemDeflection)

    @property
    def cylindrical_gear_mesh_system_deflection_timestep(
        self: "CastSelf",
    ) -> "_2829.CylindricalGearMeshSystemDeflectionTimestep":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2829,
        )

        return self.__parent__._cast(_2829.CylindricalGearMeshSystemDeflectionTimestep)

    @property
    def cylindrical_gear_mesh_system_deflection_with_ltca_results(
        self: "CastSelf",
    ) -> "_2830.CylindricalGearMeshSystemDeflectionWithLTCAResults":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2830,
        )

        return self.__parent__._cast(
            _2830.CylindricalGearMeshSystemDeflectionWithLTCAResults
        )

    @property
    def face_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2843.FaceGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2843,
        )

        return self.__parent__._cast(_2843.FaceGearMeshSystemDeflection)

    @property
    def gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2848.GearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2848,
        )

        return self.__parent__._cast(_2848.GearMeshSystemDeflection)

    @property
    def hypoid_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2852.HypoidGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2852,
        )

        return self.__parent__._cast(_2852.HypoidGearMeshSystemDeflection)

    @property
    def inter_mountable_component_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2856.InterMountableComponentConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2856,
        )

        return self.__parent__._cast(
            _2856.InterMountableComponentConnectionSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2857.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2857,
        )

        return self.__parent__._cast(
            _2857.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2860.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2860,
        )

        return self.__parent__._cast(
            _2860.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2863.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2863,
        )

        return self.__parent__._cast(
            _2863.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection
        )

    @property
    def part_to_part_shear_coupling_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2877.PartToPartShearCouplingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2877,
        )

        return self.__parent__._cast(
            _2877.PartToPartShearCouplingConnectionSystemDeflection
        )

    @property
    def planetary_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2880.PlanetaryConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2880,
        )

        return self.__parent__._cast(_2880.PlanetaryConnectionSystemDeflection)

    @property
    def ring_pins_to_disc_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2886.RingPinsToDiscConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2886,
        )

        return self.__parent__._cast(_2886.RingPinsToDiscConnectionSystemDeflection)

    @property
    def rolling_ring_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2889.RollingRingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2889,
        )

        return self.__parent__._cast(_2889.RollingRingConnectionSystemDeflection)

    @property
    def shaft_to_mountable_component_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2896.ShaftToMountableComponentConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2896,
        )

        return self.__parent__._cast(
            _2896.ShaftToMountableComponentConnectionSystemDeflection
        )

    @property
    def spiral_bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2898.SpiralBevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2898,
        )

        return self.__parent__._cast(_2898.SpiralBevelGearMeshSystemDeflection)

    @property
    def spring_damper_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2901.SpringDamperConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2901,
        )

        return self.__parent__._cast(_2901.SpringDamperConnectionSystemDeflection)

    @property
    def straight_bevel_diff_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2904.StraightBevelDiffGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2904,
        )

        return self.__parent__._cast(_2904.StraightBevelDiffGearMeshSystemDeflection)

    @property
    def straight_bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2907.StraightBevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2907,
        )

        return self.__parent__._cast(_2907.StraightBevelGearMeshSystemDeflection)

    @property
    def torque_converter_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2919.TorqueConverterConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2919,
        )

        return self.__parent__._cast(_2919.TorqueConverterConnectionSystemDeflection)

    @property
    def worm_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2927.WormGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2927,
        )

        return self.__parent__._cast(_2927.WormGearMeshSystemDeflection)

    @property
    def zerol_bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2930.ZerolBevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2930,
        )

        return self.__parent__._cast(_2930.ZerolBevelGearMeshSystemDeflection)

    @property
    def abstract_shaft_to_mountable_component_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3079.AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3079,
        )

        return self.__parent__._cast(
            _3079.AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponse
        )

    @property
    def agma_gleason_conical_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3080.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3080,
        )

        return self.__parent__._cast(
            _3080.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponse
        )

    @property
    def belt_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3085.BeltConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3085,
        )

        return self.__parent__._cast(_3085.BeltConnectionSteadyStateSynchronousResponse)

    @property
    def bevel_differential_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3087.BevelDifferentialGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3087,
        )

        return self.__parent__._cast(
            _3087.BevelDifferentialGearMeshSteadyStateSynchronousResponse
        )

    @property
    def bevel_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3092.BevelGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3092,
        )

        return self.__parent__._cast(_3092.BevelGearMeshSteadyStateSynchronousResponse)

    @property
    def clutch_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3097.ClutchConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3097,
        )

        return self.__parent__._cast(
            _3097.ClutchConnectionSteadyStateSynchronousResponse
        )

    @property
    def coaxial_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3100.CoaxialConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3100,
        )

        return self.__parent__._cast(
            _3100.CoaxialConnectionSteadyStateSynchronousResponse
        )

    @property
    def concept_coupling_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3102.ConceptCouplingConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3102,
        )

        return self.__parent__._cast(
            _3102.ConceptCouplingConnectionSteadyStateSynchronousResponse
        )

    @property
    def concept_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3105.ConceptGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3105,
        )

        return self.__parent__._cast(
            _3105.ConceptGearMeshSteadyStateSynchronousResponse
        )

    @property
    def conical_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3108.ConicalGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3108,
        )

        return self.__parent__._cast(
            _3108.ConicalGearMeshSteadyStateSynchronousResponse
        )

    @property
    def connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3111.ConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3111,
        )

        return self.__parent__._cast(_3111.ConnectionSteadyStateSynchronousResponse)

    @property
    def coupling_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3113.CouplingConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3113,
        )

        return self.__parent__._cast(
            _3113.CouplingConnectionSteadyStateSynchronousResponse
        )

    @property
    def cvt_belt_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3116.CVTBeltConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3116,
        )

        return self.__parent__._cast(
            _3116.CVTBeltConnectionSteadyStateSynchronousResponse
        )

    @property
    def cycloidal_disc_central_bearing_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3120.CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3120,
        )

        return self.__parent__._cast(
            _3120.CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponse
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3121.CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3121,
        )

        return self.__parent__._cast(
            _3121.CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponse
        )

    @property
    def cylindrical_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3123.CylindricalGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3123,
        )

        return self.__parent__._cast(
            _3123.CylindricalGearMeshSteadyStateSynchronousResponse
        )

    @property
    def face_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3130.FaceGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3130,
        )

        return self.__parent__._cast(_3130.FaceGearMeshSteadyStateSynchronousResponse)

    @property
    def gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3135.GearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3135,
        )

        return self.__parent__._cast(_3135.GearMeshSteadyStateSynchronousResponse)

    @property
    def hypoid_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3139.HypoidGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3139,
        )

        return self.__parent__._cast(_3139.HypoidGearMeshSteadyStateSynchronousResponse)

    @property
    def inter_mountable_component_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3142.InterMountableComponentConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3142,
        )

        return self.__parent__._cast(
            _3142.InterMountableComponentConnectionSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3143.KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3143,
        )

        return self.__parent__._cast(
            _3143.KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3146.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3146,
        )

        return self.__parent__._cast(
            _3146.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3149.KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3149,
        )

        return self.__parent__._cast(
            _3149.KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponse
        )

    @property
    def part_to_part_shear_coupling_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3159.PartToPartShearCouplingConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3159,
        )

        return self.__parent__._cast(
            _3159.PartToPartShearCouplingConnectionSteadyStateSynchronousResponse
        )

    @property
    def planetary_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3162.PlanetaryConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3162,
        )

        return self.__parent__._cast(
            _3162.PlanetaryConnectionSteadyStateSynchronousResponse
        )

    @property
    def ring_pins_to_disc_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3169.RingPinsToDiscConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3169,
        )

        return self.__parent__._cast(
            _3169.RingPinsToDiscConnectionSteadyStateSynchronousResponse
        )

    @property
    def rolling_ring_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3171.RollingRingConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3171,
        )

        return self.__parent__._cast(
            _3171.RollingRingConnectionSteadyStateSynchronousResponse
        )

    @property
    def shaft_to_mountable_component_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3176.ShaftToMountableComponentConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3176,
        )

        return self.__parent__._cast(
            _3176.ShaftToMountableComponentConnectionSteadyStateSynchronousResponse
        )

    @property
    def spiral_bevel_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3178.SpiralBevelGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3178,
        )

        return self.__parent__._cast(
            _3178.SpiralBevelGearMeshSteadyStateSynchronousResponse
        )

    @property
    def spring_damper_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3181.SpringDamperConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3181,
        )

        return self.__parent__._cast(
            _3181.SpringDamperConnectionSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_diff_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3187.StraightBevelDiffGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3187,
        )

        return self.__parent__._cast(
            _3187.StraightBevelDiffGearMeshSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3190.StraightBevelGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3190,
        )

        return self.__parent__._cast(
            _3190.StraightBevelGearMeshSteadyStateSynchronousResponse
        )

    @property
    def torque_converter_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3199.TorqueConverterConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3199,
        )

        return self.__parent__._cast(
            _3199.TorqueConverterConnectionSteadyStateSynchronousResponse
        )

    @property
    def worm_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3205.WormGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3205,
        )

        return self.__parent__._cast(_3205.WormGearMeshSteadyStateSynchronousResponse)

    @property
    def zerol_bevel_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3208.ZerolBevelGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3208,
        )

        return self.__parent__._cast(
            _3208.ZerolBevelGearMeshSteadyStateSynchronousResponse
        )

    @property
    def abstract_shaft_to_mountable_component_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3345.AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3345,
        )

        return self.__parent__._cast(
            _3345.AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def agma_gleason_conical_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3346.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3346,
        )

        return self.__parent__._cast(
            _3346.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def belt_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3351.BeltConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3351,
        )

        return self.__parent__._cast(
            _3351.BeltConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_differential_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3353.BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3353,
        )

        return self.__parent__._cast(
            _3353.BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3358.BevelGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3358,
        )

        return self.__parent__._cast(
            _3358.BevelGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def clutch_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3363.ClutchConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3363,
        )

        return self.__parent__._cast(
            _3363.ClutchConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def coaxial_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3366.CoaxialConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3366,
        )

        return self.__parent__._cast(
            _3366.CoaxialConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def concept_coupling_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3368.ConceptCouplingConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3368,
        )

        return self.__parent__._cast(
            _3368.ConceptCouplingConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def concept_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3371.ConceptGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3371,
        )

        return self.__parent__._cast(
            _3371.ConceptGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def conical_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3374.ConicalGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3374,
        )

        return self.__parent__._cast(
            _3374.ConicalGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3377.ConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3377,
        )

        return self.__parent__._cast(
            _3377.ConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def coupling_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3379.CouplingConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3379,
        )

        return self.__parent__._cast(
            _3379.CouplingConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cvt_belt_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3382.CVTBeltConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3382,
        )

        return self.__parent__._cast(
            _3382.CVTBeltConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cycloidal_disc_central_bearing_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3386.CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3386,
        )

        return self.__parent__._cast(
            _3386.CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3387.CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3387,
        )

        return self.__parent__._cast(
            _3387.CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cylindrical_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3389.CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3389,
        )

        return self.__parent__._cast(
            _3389.CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def face_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3395.FaceGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3395,
        )

        return self.__parent__._cast(
            _3395.FaceGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3400.GearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3400,
        )

        return self.__parent__._cast(
            _3400.GearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def hypoid_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3404.HypoidGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3404,
        )

        return self.__parent__._cast(
            _3404.HypoidGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def inter_mountable_component_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> (
        "_3407.InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3407,
        )

        return self.__parent__._cast(
            _3407.InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3408.KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3408,
        )

        return self.__parent__._cast(
            _3408.KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3411.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3411,
        )

        return self.__parent__._cast(
            _3411.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3414.KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3414,
        )

        return self.__parent__._cast(
            _3414.KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def part_to_part_shear_coupling_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> (
        "_3424.PartToPartShearCouplingConnectionSteadyStateSynchronousResponseOnAShaft"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3424,
        )

        return self.__parent__._cast(
            _3424.PartToPartShearCouplingConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def planetary_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3427.PlanetaryConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3427,
        )

        return self.__parent__._cast(
            _3427.PlanetaryConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def ring_pins_to_disc_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3434.RingPinsToDiscConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3434,
        )

        return self.__parent__._cast(
            _3434.RingPinsToDiscConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def rolling_ring_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3436.RollingRingConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3436,
        )

        return self.__parent__._cast(
            _3436.RollingRingConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def shaft_to_mountable_component_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3441.ShaftToMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3441,
        )

        return self.__parent__._cast(
            _3441.ShaftToMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def spiral_bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3443.SpiralBevelGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3443,
        )

        return self.__parent__._cast(
            _3443.SpiralBevelGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def spring_damper_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3446.SpringDamperConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3446,
        )

        return self.__parent__._cast(
            _3446.SpringDamperConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_diff_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3450.StraightBevelDiffGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3450,
        )

        return self.__parent__._cast(
            _3450.StraightBevelDiffGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3453.StraightBevelGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3453,
        )

        return self.__parent__._cast(
            _3453.StraightBevelGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def torque_converter_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3462.TorqueConverterConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3462,
        )

        return self.__parent__._cast(
            _3462.TorqueConverterConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def worm_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3468.WormGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3468,
        )

        return self.__parent__._cast(
            _3468.WormGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def zerol_bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3471.ZerolBevelGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3471,
        )

        return self.__parent__._cast(
            _3471.ZerolBevelGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def abstract_shaft_to_mountable_component_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3608.AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3608,
        )

        return self.__parent__._cast(
            _3608.AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def agma_gleason_conical_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3609.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3609,
        )

        return self.__parent__._cast(
            _3609.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def belt_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3614.BeltConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3614,
        )

        return self.__parent__._cast(
            _3614.BeltConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_differential_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3616.BevelDifferentialGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3616,
        )

        return self.__parent__._cast(
            _3616.BevelDifferentialGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3621.BevelGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3621,
        )

        return self.__parent__._cast(
            _3621.BevelGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def clutch_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3626.ClutchConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3626,
        )

        return self.__parent__._cast(
            _3626.ClutchConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def coaxial_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3629.CoaxialConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3629,
        )

        return self.__parent__._cast(
            _3629.CoaxialConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def concept_coupling_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3631.ConceptCouplingConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3631,
        )

        return self.__parent__._cast(
            _3631.ConceptCouplingConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def concept_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3634.ConceptGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3634,
        )

        return self.__parent__._cast(
            _3634.ConceptGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def conical_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3637.ConicalGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3637,
        )

        return self.__parent__._cast(
            _3637.ConicalGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3640.ConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3640,
        )

        return self.__parent__._cast(
            _3640.ConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def coupling_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3642.CouplingConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3642,
        )

        return self.__parent__._cast(
            _3642.CouplingConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cvt_belt_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3645.CVTBeltConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3645,
        )

        return self.__parent__._cast(
            _3645.CVTBeltConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cycloidal_disc_central_bearing_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3649.CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3649,
        )

        return self.__parent__._cast(
            _3649.CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3650.CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3650,
        )

        return self.__parent__._cast(
            _3650.CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cylindrical_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3652.CylindricalGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3652,
        )

        return self.__parent__._cast(
            _3652.CylindricalGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def face_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3658.FaceGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3658,
        )

        return self.__parent__._cast(
            _3658.FaceGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3663.GearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3663,
        )

        return self.__parent__._cast(
            _3663.GearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def hypoid_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3667.HypoidGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3667,
        )

        return self.__parent__._cast(
            _3667.HypoidGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def inter_mountable_component_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_3670.InterMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3670,
        )

        return self.__parent__._cast(
            _3670.InterMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3671.KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3671,
        )

        return self.__parent__._cast(
            _3671.KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3674.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3674,
        )

        return self.__parent__._cast(
            _3674.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3677.KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3677,
        )

        return self.__parent__._cast(
            _3677.KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def part_to_part_shear_coupling_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_3687.PartToPartShearCouplingConnectionSteadyStateSynchronousResponseAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3687,
        )

        return self.__parent__._cast(
            _3687.PartToPartShearCouplingConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def planetary_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3690.PlanetaryConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3690,
        )

        return self.__parent__._cast(
            _3690.PlanetaryConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def ring_pins_to_disc_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3697.RingPinsToDiscConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3697,
        )

        return self.__parent__._cast(
            _3697.RingPinsToDiscConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def rolling_ring_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3699.RollingRingConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3699,
        )

        return self.__parent__._cast(
            _3699.RollingRingConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def shaft_to_mountable_component_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3704.ShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3704,
        )

        return self.__parent__._cast(
            _3704.ShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def spiral_bevel_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3706.SpiralBevelGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3706,
        )

        return self.__parent__._cast(
            _3706.SpiralBevelGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def spring_damper_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3709.SpringDamperConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3709,
        )

        return self.__parent__._cast(
            _3709.SpringDamperConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_diff_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3713.StraightBevelDiffGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3713,
        )

        return self.__parent__._cast(
            _3713.StraightBevelDiffGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3716.StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3716,
        )

        return self.__parent__._cast(
            _3716.StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def torque_converter_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3725.TorqueConverterConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3725,
        )

        return self.__parent__._cast(
            _3725.TorqueConverterConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def worm_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3731.WormGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3731,
        )

        return self.__parent__._cast(
            _3731.WormGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def zerol_bevel_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3734.ZerolBevelGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3734,
        )

        return self.__parent__._cast(
            _3734.ZerolBevelGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def abstract_shaft_to_mountable_component_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3871.AbstractShaftToMountableComponentConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3871,
        )

        return self.__parent__._cast(
            _3871.AbstractShaftToMountableComponentConnectionStabilityAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3872.AGMAGleasonConicalGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3872,
        )

        return self.__parent__._cast(_3872.AGMAGleasonConicalGearMeshStabilityAnalysis)

    @property
    def belt_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3877.BeltConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3877,
        )

        return self.__parent__._cast(_3877.BeltConnectionStabilityAnalysis)

    @property
    def bevel_differential_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3879.BevelDifferentialGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3879,
        )

        return self.__parent__._cast(_3879.BevelDifferentialGearMeshStabilityAnalysis)

    @property
    def bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3884.BevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3884,
        )

        return self.__parent__._cast(_3884.BevelGearMeshStabilityAnalysis)

    @property
    def clutch_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3889.ClutchConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3889,
        )

        return self.__parent__._cast(_3889.ClutchConnectionStabilityAnalysis)

    @property
    def coaxial_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3892.CoaxialConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3892,
        )

        return self.__parent__._cast(_3892.CoaxialConnectionStabilityAnalysis)

    @property
    def concept_coupling_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3894.ConceptCouplingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3894,
        )

        return self.__parent__._cast(_3894.ConceptCouplingConnectionStabilityAnalysis)

    @property
    def concept_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3897.ConceptGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3897,
        )

        return self.__parent__._cast(_3897.ConceptGearMeshStabilityAnalysis)

    @property
    def conical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3900.ConicalGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3900,
        )

        return self.__parent__._cast(_3900.ConicalGearMeshStabilityAnalysis)

    @property
    def connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3903.ConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3903,
        )

        return self.__parent__._cast(_3903.ConnectionStabilityAnalysis)

    @property
    def coupling_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3905.CouplingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3905,
        )

        return self.__parent__._cast(_3905.CouplingConnectionStabilityAnalysis)

    @property
    def cvt_belt_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3909.CVTBeltConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3909,
        )

        return self.__parent__._cast(_3909.CVTBeltConnectionStabilityAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3913.CycloidalDiscCentralBearingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3913,
        )

        return self.__parent__._cast(
            _3913.CycloidalDiscCentralBearingConnectionStabilityAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3914.CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3914,
        )

        return self.__parent__._cast(
            _3914.CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis
        )

    @property
    def cylindrical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3916.CylindricalGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3916,
        )

        return self.__parent__._cast(_3916.CylindricalGearMeshStabilityAnalysis)

    @property
    def face_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3923.FaceGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3923,
        )

        return self.__parent__._cast(_3923.FaceGearMeshStabilityAnalysis)

    @property
    def gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3928.GearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3928,
        )

        return self.__parent__._cast(_3928.GearMeshStabilityAnalysis)

    @property
    def hypoid_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3932.HypoidGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3932,
        )

        return self.__parent__._cast(_3932.HypoidGearMeshStabilityAnalysis)

    @property
    def inter_mountable_component_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3935.InterMountableComponentConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3935,
        )

        return self.__parent__._cast(
            _3935.InterMountableComponentConnectionStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3936.KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3936,
        )

        return self.__parent__._cast(
            _3936.KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3939.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3939,
        )

        return self.__parent__._cast(
            _3939.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3942.KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3942,
        )

        return self.__parent__._cast(
            _3942.KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3952.PartToPartShearCouplingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3952,
        )

        return self.__parent__._cast(
            _3952.PartToPartShearCouplingConnectionStabilityAnalysis
        )

    @property
    def planetary_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3955.PlanetaryConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3955,
        )

        return self.__parent__._cast(_3955.PlanetaryConnectionStabilityAnalysis)

    @property
    def ring_pins_to_disc_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3962.RingPinsToDiscConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3962,
        )

        return self.__parent__._cast(_3962.RingPinsToDiscConnectionStabilityAnalysis)

    @property
    def rolling_ring_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3964.RollingRingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3964,
        )

        return self.__parent__._cast(_3964.RollingRingConnectionStabilityAnalysis)

    @property
    def shaft_to_mountable_component_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3969.ShaftToMountableComponentConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3969,
        )

        return self.__parent__._cast(
            _3969.ShaftToMountableComponentConnectionStabilityAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3971.SpiralBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3971,
        )

        return self.__parent__._cast(_3971.SpiralBevelGearMeshStabilityAnalysis)

    @property
    def spring_damper_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3974.SpringDamperConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3974,
        )

        return self.__parent__._cast(_3974.SpringDamperConnectionStabilityAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3980.StraightBevelDiffGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3980,
        )

        return self.__parent__._cast(_3980.StraightBevelDiffGearMeshStabilityAnalysis)

    @property
    def straight_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3983.StraightBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3983,
        )

        return self.__parent__._cast(_3983.StraightBevelGearMeshStabilityAnalysis)

    @property
    def torque_converter_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3992.TorqueConverterConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3992,
        )

        return self.__parent__._cast(_3992.TorqueConverterConnectionStabilityAnalysis)

    @property
    def worm_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3998.WormGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3998,
        )

        return self.__parent__._cast(_3998.WormGearMeshStabilityAnalysis)

    @property
    def zerol_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4001.ZerolBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4001,
        )

        return self.__parent__._cast(_4001.ZerolBevelGearMeshStabilityAnalysis)

    @property
    def abstract_shaft_to_mountable_component_connection_power_flow(
        self: "CastSelf",
    ) -> "_4144.AbstractShaftToMountableComponentConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4144

        return self.__parent__._cast(
            _4144.AbstractShaftToMountableComponentConnectionPowerFlow
        )

    @property
    def agma_gleason_conical_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4145.AGMAGleasonConicalGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4145

        return self.__parent__._cast(_4145.AGMAGleasonConicalGearMeshPowerFlow)

    @property
    def belt_connection_power_flow(self: "CastSelf") -> "_4150.BeltConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4150

        return self.__parent__._cast(_4150.BeltConnectionPowerFlow)

    @property
    def bevel_differential_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4152.BevelDifferentialGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4152

        return self.__parent__._cast(_4152.BevelDifferentialGearMeshPowerFlow)

    @property
    def bevel_gear_mesh_power_flow(self: "CastSelf") -> "_4157.BevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4157

        return self.__parent__._cast(_4157.BevelGearMeshPowerFlow)

    @property
    def clutch_connection_power_flow(
        self: "CastSelf",
    ) -> "_4162.ClutchConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4162

        return self.__parent__._cast(_4162.ClutchConnectionPowerFlow)

    @property
    def coaxial_connection_power_flow(
        self: "CastSelf",
    ) -> "_4165.CoaxialConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4165

        return self.__parent__._cast(_4165.CoaxialConnectionPowerFlow)

    @property
    def concept_coupling_connection_power_flow(
        self: "CastSelf",
    ) -> "_4167.ConceptCouplingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4167

        return self.__parent__._cast(_4167.ConceptCouplingConnectionPowerFlow)

    @property
    def concept_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4170.ConceptGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4170

        return self.__parent__._cast(_4170.ConceptGearMeshPowerFlow)

    @property
    def conical_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4173.ConicalGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4173

        return self.__parent__._cast(_4173.ConicalGearMeshPowerFlow)

    @property
    def connection_power_flow(self: "CastSelf") -> "_4176.ConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4176

        return self.__parent__._cast(_4176.ConnectionPowerFlow)

    @property
    def coupling_connection_power_flow(
        self: "CastSelf",
    ) -> "_4178.CouplingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4178

        return self.__parent__._cast(_4178.CouplingConnectionPowerFlow)

    @property
    def cvt_belt_connection_power_flow(
        self: "CastSelf",
    ) -> "_4181.CVTBeltConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4181

        return self.__parent__._cast(_4181.CVTBeltConnectionPowerFlow)

    @property
    def cycloidal_disc_central_bearing_connection_power_flow(
        self: "CastSelf",
    ) -> "_4185.CycloidalDiscCentralBearingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4185

        return self.__parent__._cast(
            _4185.CycloidalDiscCentralBearingConnectionPowerFlow
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_power_flow(
        self: "CastSelf",
    ) -> "_4186.CycloidalDiscPlanetaryBearingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4186

        return self.__parent__._cast(
            _4186.CycloidalDiscPlanetaryBearingConnectionPowerFlow
        )

    @property
    def cylindrical_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4189.CylindricalGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4189

        return self.__parent__._cast(_4189.CylindricalGearMeshPowerFlow)

    @property
    def face_gear_mesh_power_flow(self: "CastSelf") -> "_4195.FaceGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4195

        return self.__parent__._cast(_4195.FaceGearMeshPowerFlow)

    @property
    def gear_mesh_power_flow(self: "CastSelf") -> "_4202.GearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4202

        return self.__parent__._cast(_4202.GearMeshPowerFlow)

    @property
    def hypoid_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4206.HypoidGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4206

        return self.__parent__._cast(_4206.HypoidGearMeshPowerFlow)

    @property
    def inter_mountable_component_connection_power_flow(
        self: "CastSelf",
    ) -> "_4209.InterMountableComponentConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4209

        return self.__parent__._cast(_4209.InterMountableComponentConnectionPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4210.KlingelnbergCycloPalloidConicalGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4210

        return self.__parent__._cast(
            _4210.KlingelnbergCycloPalloidConicalGearMeshPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4213.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4213

        return self.__parent__._cast(
            _4213.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4216.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4216

        return self.__parent__._cast(
            _4216.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow
        )

    @property
    def part_to_part_shear_coupling_connection_power_flow(
        self: "CastSelf",
    ) -> "_4226.PartToPartShearCouplingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4226

        return self.__parent__._cast(_4226.PartToPartShearCouplingConnectionPowerFlow)

    @property
    def planetary_connection_power_flow(
        self: "CastSelf",
    ) -> "_4229.PlanetaryConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4229

        return self.__parent__._cast(_4229.PlanetaryConnectionPowerFlow)

    @property
    def ring_pins_to_disc_connection_power_flow(
        self: "CastSelf",
    ) -> "_4238.RingPinsToDiscConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4238

        return self.__parent__._cast(_4238.RingPinsToDiscConnectionPowerFlow)

    @property
    def rolling_ring_connection_power_flow(
        self: "CastSelf",
    ) -> "_4240.RollingRingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4240

        return self.__parent__._cast(_4240.RollingRingConnectionPowerFlow)

    @property
    def shaft_to_mountable_component_connection_power_flow(
        self: "CastSelf",
    ) -> "_4245.ShaftToMountableComponentConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4245

        return self.__parent__._cast(_4245.ShaftToMountableComponentConnectionPowerFlow)

    @property
    def spiral_bevel_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4247.SpiralBevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4247

        return self.__parent__._cast(_4247.SpiralBevelGearMeshPowerFlow)

    @property
    def spring_damper_connection_power_flow(
        self: "CastSelf",
    ) -> "_4250.SpringDamperConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4250

        return self.__parent__._cast(_4250.SpringDamperConnectionPowerFlow)

    @property
    def straight_bevel_diff_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4253.StraightBevelDiffGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4253

        return self.__parent__._cast(_4253.StraightBevelDiffGearMeshPowerFlow)

    @property
    def straight_bevel_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4256.StraightBevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4256

        return self.__parent__._cast(_4256.StraightBevelGearMeshPowerFlow)

    @property
    def torque_converter_connection_power_flow(
        self: "CastSelf",
    ) -> "_4266.TorqueConverterConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4266

        return self.__parent__._cast(_4266.TorqueConverterConnectionPowerFlow)

    @property
    def worm_gear_mesh_power_flow(self: "CastSelf") -> "_4272.WormGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4272

        return self.__parent__._cast(_4272.WormGearMeshPowerFlow)

    @property
    def zerol_bevel_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4275.ZerolBevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4275

        return self.__parent__._cast(_4275.ZerolBevelGearMeshPowerFlow)

    @property
    def abstract_shaft_to_mountable_component_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4412.AbstractShaftToMountableComponentConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4412,
        )

        return self.__parent__._cast(
            _4412.AbstractShaftToMountableComponentConnectionParametricStudyTool
        )

    @property
    def agma_gleason_conical_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4413.AGMAGleasonConicalGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4413,
        )

        return self.__parent__._cast(
            _4413.AGMAGleasonConicalGearMeshParametricStudyTool
        )

    @property
    def belt_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4418.BeltConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4418,
        )

        return self.__parent__._cast(_4418.BeltConnectionParametricStudyTool)

    @property
    def bevel_differential_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4420.BevelDifferentialGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4420,
        )

        return self.__parent__._cast(_4420.BevelDifferentialGearMeshParametricStudyTool)

    @property
    def bevel_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4425.BevelGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4425,
        )

        return self.__parent__._cast(_4425.BevelGearMeshParametricStudyTool)

    @property
    def clutch_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4430.ClutchConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4430,
        )

        return self.__parent__._cast(_4430.ClutchConnectionParametricStudyTool)

    @property
    def coaxial_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4433.CoaxialConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4433,
        )

        return self.__parent__._cast(_4433.CoaxialConnectionParametricStudyTool)

    @property
    def concept_coupling_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4435.ConceptCouplingConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4435,
        )

        return self.__parent__._cast(_4435.ConceptCouplingConnectionParametricStudyTool)

    @property
    def concept_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4438.ConceptGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4438,
        )

        return self.__parent__._cast(_4438.ConceptGearMeshParametricStudyTool)

    @property
    def conical_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4441.ConicalGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4441,
        )

        return self.__parent__._cast(_4441.ConicalGearMeshParametricStudyTool)

    @property
    def connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4444.ConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4444,
        )

        return self.__parent__._cast(_4444.ConnectionParametricStudyTool)

    @property
    def coupling_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4446.CouplingConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4446,
        )

        return self.__parent__._cast(_4446.CouplingConnectionParametricStudyTool)

    @property
    def cvt_belt_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4449.CVTBeltConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4449,
        )

        return self.__parent__._cast(_4449.CVTBeltConnectionParametricStudyTool)

    @property
    def cycloidal_disc_central_bearing_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4453.CycloidalDiscCentralBearingConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4453,
        )

        return self.__parent__._cast(
            _4453.CycloidalDiscCentralBearingConnectionParametricStudyTool
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4455.CycloidalDiscPlanetaryBearingConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4455,
        )

        return self.__parent__._cast(
            _4455.CycloidalDiscPlanetaryBearingConnectionParametricStudyTool
        )

    @property
    def cylindrical_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4456.CylindricalGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4456,
        )

        return self.__parent__._cast(_4456.CylindricalGearMeshParametricStudyTool)

    @property
    def face_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4469.FaceGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4469,
        )

        return self.__parent__._cast(_4469.FaceGearMeshParametricStudyTool)

    @property
    def gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4474.GearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4474,
        )

        return self.__parent__._cast(_4474.GearMeshParametricStudyTool)

    @property
    def hypoid_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4478.HypoidGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4478,
        )

        return self.__parent__._cast(_4478.HypoidGearMeshParametricStudyTool)

    @property
    def inter_mountable_component_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4481.InterMountableComponentConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4481,
        )

        return self.__parent__._cast(
            _4481.InterMountableComponentConnectionParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4482.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4482,
        )

        return self.__parent__._cast(
            _4482.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4485.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4485,
        )

        return self.__parent__._cast(
            _4485.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4488.KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4488,
        )

        return self.__parent__._cast(
            _4488.KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool
        )

    @property
    def part_to_part_shear_coupling_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4509.PartToPartShearCouplingConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4509,
        )

        return self.__parent__._cast(
            _4509.PartToPartShearCouplingConnectionParametricStudyTool
        )

    @property
    def planetary_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4512.PlanetaryConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4512,
        )

        return self.__parent__._cast(_4512.PlanetaryConnectionParametricStudyTool)

    @property
    def ring_pins_to_disc_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4519.RingPinsToDiscConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4519,
        )

        return self.__parent__._cast(_4519.RingPinsToDiscConnectionParametricStudyTool)

    @property
    def rolling_ring_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4521.RollingRingConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4521,
        )

        return self.__parent__._cast(_4521.RollingRingConnectionParametricStudyTool)

    @property
    def shaft_to_mountable_component_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4526.ShaftToMountableComponentConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4526,
        )

        return self.__parent__._cast(
            _4526.ShaftToMountableComponentConnectionParametricStudyTool
        )

    @property
    def spiral_bevel_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4528.SpiralBevelGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4528,
        )

        return self.__parent__._cast(_4528.SpiralBevelGearMeshParametricStudyTool)

    @property
    def spring_damper_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4531.SpringDamperConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4531,
        )

        return self.__parent__._cast(_4531.SpringDamperConnectionParametricStudyTool)

    @property
    def straight_bevel_diff_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4534.StraightBevelDiffGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4534,
        )

        return self.__parent__._cast(_4534.StraightBevelDiffGearMeshParametricStudyTool)

    @property
    def straight_bevel_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4537.StraightBevelGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4537,
        )

        return self.__parent__._cast(_4537.StraightBevelGearMeshParametricStudyTool)

    @property
    def torque_converter_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4546.TorqueConverterConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4546,
        )

        return self.__parent__._cast(_4546.TorqueConverterConnectionParametricStudyTool)

    @property
    def worm_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4552.WormGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4552,
        )

        return self.__parent__._cast(_4552.WormGearMeshParametricStudyTool)

    @property
    def zerol_bevel_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4555.ZerolBevelGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4555,
        )

        return self.__parent__._cast(_4555.ZerolBevelGearMeshParametricStudyTool)

    @property
    def abstract_shaft_to_mountable_component_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4692.AbstractShaftToMountableComponentConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4692,
        )

        return self.__parent__._cast(
            _4692.AbstractShaftToMountableComponentConnectionModalAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4693.AGMAGleasonConicalGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4693,
        )

        return self.__parent__._cast(_4693.AGMAGleasonConicalGearMeshModalAnalysis)

    @property
    def belt_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4698.BeltConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4698,
        )

        return self.__parent__._cast(_4698.BeltConnectionModalAnalysis)

    @property
    def bevel_differential_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4700.BevelDifferentialGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4700,
        )

        return self.__parent__._cast(_4700.BevelDifferentialGearMeshModalAnalysis)

    @property
    def bevel_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4705.BevelGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4705,
        )

        return self.__parent__._cast(_4705.BevelGearMeshModalAnalysis)

    @property
    def clutch_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4710.ClutchConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4710,
        )

        return self.__parent__._cast(_4710.ClutchConnectionModalAnalysis)

    @property
    def coaxial_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4713.CoaxialConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4713,
        )

        return self.__parent__._cast(_4713.CoaxialConnectionModalAnalysis)

    @property
    def concept_coupling_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4715.ConceptCouplingConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4715,
        )

        return self.__parent__._cast(_4715.ConceptCouplingConnectionModalAnalysis)

    @property
    def concept_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4718.ConceptGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4718,
        )

        return self.__parent__._cast(_4718.ConceptGearMeshModalAnalysis)

    @property
    def conical_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4721.ConicalGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4721,
        )

        return self.__parent__._cast(_4721.ConicalGearMeshModalAnalysis)

    @property
    def connection_modal_analysis(self: "CastSelf") -> "_4724.ConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4724,
        )

        return self.__parent__._cast(_4724.ConnectionModalAnalysis)

    @property
    def coupling_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4727.CouplingConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4727,
        )

        return self.__parent__._cast(_4727.CouplingConnectionModalAnalysis)

    @property
    def cvt_belt_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4730.CVTBeltConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4730,
        )

        return self.__parent__._cast(_4730.CVTBeltConnectionModalAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4734.CycloidalDiscCentralBearingConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4734,
        )

        return self.__parent__._cast(
            _4734.CycloidalDiscCentralBearingConnectionModalAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4736.CycloidalDiscPlanetaryBearingConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4736,
        )

        return self.__parent__._cast(
            _4736.CycloidalDiscPlanetaryBearingConnectionModalAnalysis
        )

    @property
    def cylindrical_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4737.CylindricalGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4737,
        )

        return self.__parent__._cast(_4737.CylindricalGearMeshModalAnalysis)

    @property
    def face_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4746.FaceGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4746,
        )

        return self.__parent__._cast(_4746.FaceGearMeshModalAnalysis)

    @property
    def gear_mesh_modal_analysis(self: "CastSelf") -> "_4752.GearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4752,
        )

        return self.__parent__._cast(_4752.GearMeshModalAnalysis)

    @property
    def hypoid_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4756.HypoidGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4756,
        )

        return self.__parent__._cast(_4756.HypoidGearMeshModalAnalysis)

    @property
    def inter_mountable_component_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4759.InterMountableComponentConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4759,
        )

        return self.__parent__._cast(
            _4759.InterMountableComponentConnectionModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4760.KlingelnbergCycloPalloidConicalGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4760,
        )

        return self.__parent__._cast(
            _4760.KlingelnbergCycloPalloidConicalGearMeshModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4763.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4763,
        )

        return self.__parent__._cast(
            _4763.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4766.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4766,
        )

        return self.__parent__._cast(
            _4766.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4782.PartToPartShearCouplingConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4782,
        )

        return self.__parent__._cast(
            _4782.PartToPartShearCouplingConnectionModalAnalysis
        )

    @property
    def planetary_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4785.PlanetaryConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4785,
        )

        return self.__parent__._cast(_4785.PlanetaryConnectionModalAnalysis)

    @property
    def ring_pins_to_disc_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4792.RingPinsToDiscConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4792,
        )

        return self.__parent__._cast(_4792.RingPinsToDiscConnectionModalAnalysis)

    @property
    def rolling_ring_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4794.RollingRingConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4794,
        )

        return self.__parent__._cast(_4794.RollingRingConnectionModalAnalysis)

    @property
    def shaft_to_mountable_component_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4800.ShaftToMountableComponentConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4800,
        )

        return self.__parent__._cast(
            _4800.ShaftToMountableComponentConnectionModalAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4802.SpiralBevelGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4802,
        )

        return self.__parent__._cast(_4802.SpiralBevelGearMeshModalAnalysis)

    @property
    def spring_damper_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4805.SpringDamperConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4805,
        )

        return self.__parent__._cast(_4805.SpringDamperConnectionModalAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4808.StraightBevelDiffGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4808,
        )

        return self.__parent__._cast(_4808.StraightBevelDiffGearMeshModalAnalysis)

    @property
    def straight_bevel_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4811.StraightBevelGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4811,
        )

        return self.__parent__._cast(_4811.StraightBevelGearMeshModalAnalysis)

    @property
    def torque_converter_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4820.TorqueConverterConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4820,
        )

        return self.__parent__._cast(_4820.TorqueConverterConnectionModalAnalysis)

    @property
    def worm_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4829.WormGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4829,
        )

        return self.__parent__._cast(_4829.WormGearMeshModalAnalysis)

    @property
    def zerol_bevel_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4832.ZerolBevelGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4832,
        )

        return self.__parent__._cast(_4832.ZerolBevelGearMeshModalAnalysis)

    @property
    def abstract_shaft_to_mountable_component_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4981.AbstractShaftToMountableComponentConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4981,
        )

        return self.__parent__._cast(
            _4981.AbstractShaftToMountableComponentConnectionModalAnalysisAtAStiffness
        )

    @property
    def agma_gleason_conical_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4982.AGMAGleasonConicalGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4982,
        )

        return self.__parent__._cast(
            _4982.AGMAGleasonConicalGearMeshModalAnalysisAtAStiffness
        )

    @property
    def belt_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4987.BeltConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4987,
        )

        return self.__parent__._cast(_4987.BeltConnectionModalAnalysisAtAStiffness)

    @property
    def bevel_differential_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4989.BevelDifferentialGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4989,
        )

        return self.__parent__._cast(
            _4989.BevelDifferentialGearMeshModalAnalysisAtAStiffness
        )

    @property
    def bevel_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4994.BevelGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4994,
        )

        return self.__parent__._cast(_4994.BevelGearMeshModalAnalysisAtAStiffness)

    @property
    def clutch_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4999.ClutchConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4999,
        )

        return self.__parent__._cast(_4999.ClutchConnectionModalAnalysisAtAStiffness)

    @property
    def coaxial_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5002.CoaxialConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5002,
        )

        return self.__parent__._cast(_5002.CoaxialConnectionModalAnalysisAtAStiffness)

    @property
    def concept_coupling_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5004.ConceptCouplingConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5004,
        )

        return self.__parent__._cast(
            _5004.ConceptCouplingConnectionModalAnalysisAtAStiffness
        )

    @property
    def concept_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5007.ConceptGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5007,
        )

        return self.__parent__._cast(_5007.ConceptGearMeshModalAnalysisAtAStiffness)

    @property
    def conical_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5010.ConicalGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5010,
        )

        return self.__parent__._cast(_5010.ConicalGearMeshModalAnalysisAtAStiffness)

    @property
    def connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5013.ConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5013,
        )

        return self.__parent__._cast(_5013.ConnectionModalAnalysisAtAStiffness)

    @property
    def coupling_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5015.CouplingConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5015,
        )

        return self.__parent__._cast(_5015.CouplingConnectionModalAnalysisAtAStiffness)

    @property
    def cvt_belt_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5018.CVTBeltConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5018,
        )

        return self.__parent__._cast(_5018.CVTBeltConnectionModalAnalysisAtAStiffness)

    @property
    def cycloidal_disc_central_bearing_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5022.CycloidalDiscCentralBearingConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5022,
        )

        return self.__parent__._cast(
            _5022.CycloidalDiscCentralBearingConnectionModalAnalysisAtAStiffness
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5024.CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5024,
        )

        return self.__parent__._cast(
            _5024.CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtAStiffness
        )

    @property
    def cylindrical_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5025.CylindricalGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5025,
        )

        return self.__parent__._cast(_5025.CylindricalGearMeshModalAnalysisAtAStiffness)

    @property
    def face_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5032.FaceGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5032,
        )

        return self.__parent__._cast(_5032.FaceGearMeshModalAnalysisAtAStiffness)

    @property
    def gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5037.GearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5037,
        )

        return self.__parent__._cast(_5037.GearMeshModalAnalysisAtAStiffness)

    @property
    def hypoid_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5041.HypoidGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5041,
        )

        return self.__parent__._cast(_5041.HypoidGearMeshModalAnalysisAtAStiffness)

    @property
    def inter_mountable_component_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5044.InterMountableComponentConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5044,
        )

        return self.__parent__._cast(
            _5044.InterMountableComponentConnectionModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5045.KlingelnbergCycloPalloidConicalGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5045,
        )

        return self.__parent__._cast(
            _5045.KlingelnbergCycloPalloidConicalGearMeshModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5048.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5048,
        )

        return self.__parent__._cast(
            _5048.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5051.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5051,
        )

        return self.__parent__._cast(
            _5051.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysisAtAStiffness
        )

    @property
    def part_to_part_shear_coupling_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5062.PartToPartShearCouplingConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5062,
        )

        return self.__parent__._cast(
            _5062.PartToPartShearCouplingConnectionModalAnalysisAtAStiffness
        )

    @property
    def planetary_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5065.PlanetaryConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5065,
        )

        return self.__parent__._cast(_5065.PlanetaryConnectionModalAnalysisAtAStiffness)

    @property
    def ring_pins_to_disc_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5072.RingPinsToDiscConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5072,
        )

        return self.__parent__._cast(
            _5072.RingPinsToDiscConnectionModalAnalysisAtAStiffness
        )

    @property
    def rolling_ring_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5074.RollingRingConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5074,
        )

        return self.__parent__._cast(
            _5074.RollingRingConnectionModalAnalysisAtAStiffness
        )

    @property
    def shaft_to_mountable_component_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5079.ShaftToMountableComponentConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5079,
        )

        return self.__parent__._cast(
            _5079.ShaftToMountableComponentConnectionModalAnalysisAtAStiffness
        )

    @property
    def spiral_bevel_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5081.SpiralBevelGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5081,
        )

        return self.__parent__._cast(_5081.SpiralBevelGearMeshModalAnalysisAtAStiffness)

    @property
    def spring_damper_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5084.SpringDamperConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5084,
        )

        return self.__parent__._cast(
            _5084.SpringDamperConnectionModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_diff_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5087.StraightBevelDiffGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5087,
        )

        return self.__parent__._cast(
            _5087.StraightBevelDiffGearMeshModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5090.StraightBevelGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5090,
        )

        return self.__parent__._cast(
            _5090.StraightBevelGearMeshModalAnalysisAtAStiffness
        )

    @property
    def torque_converter_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5099.TorqueConverterConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5099,
        )

        return self.__parent__._cast(
            _5099.TorqueConverterConnectionModalAnalysisAtAStiffness
        )

    @property
    def worm_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5105.WormGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5105,
        )

        return self.__parent__._cast(_5105.WormGearMeshModalAnalysisAtAStiffness)

    @property
    def zerol_bevel_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5108.ZerolBevelGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5108,
        )

        return self.__parent__._cast(_5108.ZerolBevelGearMeshModalAnalysisAtAStiffness)

    @property
    def abstract_shaft_to_mountable_component_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5245.AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5245,
        )

        return self.__parent__._cast(
            _5245.AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed
        )

    @property
    def agma_gleason_conical_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5246.AGMAGleasonConicalGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5246,
        )

        return self.__parent__._cast(
            _5246.AGMAGleasonConicalGearMeshModalAnalysisAtASpeed
        )

    @property
    def belt_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5251.BeltConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5251,
        )

        return self.__parent__._cast(_5251.BeltConnectionModalAnalysisAtASpeed)

    @property
    def bevel_differential_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5253.BevelDifferentialGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5253,
        )

        return self.__parent__._cast(
            _5253.BevelDifferentialGearMeshModalAnalysisAtASpeed
        )

    @property
    def bevel_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5258.BevelGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5258,
        )

        return self.__parent__._cast(_5258.BevelGearMeshModalAnalysisAtASpeed)

    @property
    def clutch_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5263.ClutchConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5263,
        )

        return self.__parent__._cast(_5263.ClutchConnectionModalAnalysisAtASpeed)

    @property
    def coaxial_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5266.CoaxialConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5266,
        )

        return self.__parent__._cast(_5266.CoaxialConnectionModalAnalysisAtASpeed)

    @property
    def concept_coupling_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5268.ConceptCouplingConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5268,
        )

        return self.__parent__._cast(
            _5268.ConceptCouplingConnectionModalAnalysisAtASpeed
        )

    @property
    def concept_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5271.ConceptGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5271,
        )

        return self.__parent__._cast(_5271.ConceptGearMeshModalAnalysisAtASpeed)

    @property
    def conical_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5274.ConicalGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5274,
        )

        return self.__parent__._cast(_5274.ConicalGearMeshModalAnalysisAtASpeed)

    @property
    def connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5277.ConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5277,
        )

        return self.__parent__._cast(_5277.ConnectionModalAnalysisAtASpeed)

    @property
    def coupling_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5279.CouplingConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5279,
        )

        return self.__parent__._cast(_5279.CouplingConnectionModalAnalysisAtASpeed)

    @property
    def cvt_belt_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5282.CVTBeltConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5282,
        )

        return self.__parent__._cast(_5282.CVTBeltConnectionModalAnalysisAtASpeed)

    @property
    def cycloidal_disc_central_bearing_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5286.CycloidalDiscCentralBearingConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5286,
        )

        return self.__parent__._cast(
            _5286.CycloidalDiscCentralBearingConnectionModalAnalysisAtASpeed
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5288.CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5288,
        )

        return self.__parent__._cast(
            _5288.CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtASpeed
        )

    @property
    def cylindrical_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5289.CylindricalGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5289,
        )

        return self.__parent__._cast(_5289.CylindricalGearMeshModalAnalysisAtASpeed)

    @property
    def face_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5295.FaceGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5295,
        )

        return self.__parent__._cast(_5295.FaceGearMeshModalAnalysisAtASpeed)

    @property
    def gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5300.GearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5300,
        )

        return self.__parent__._cast(_5300.GearMeshModalAnalysisAtASpeed)

    @property
    def hypoid_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5304.HypoidGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5304,
        )

        return self.__parent__._cast(_5304.HypoidGearMeshModalAnalysisAtASpeed)

    @property
    def inter_mountable_component_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5307.InterMountableComponentConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5307,
        )

        return self.__parent__._cast(
            _5307.InterMountableComponentConnectionModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5308.KlingelnbergCycloPalloidConicalGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5308,
        )

        return self.__parent__._cast(
            _5308.KlingelnbergCycloPalloidConicalGearMeshModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5311.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5311,
        )

        return self.__parent__._cast(
            _5311.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5314.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5314,
        )

        return self.__parent__._cast(
            _5314.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysisAtASpeed
        )

    @property
    def part_to_part_shear_coupling_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5325.PartToPartShearCouplingConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5325,
        )

        return self.__parent__._cast(
            _5325.PartToPartShearCouplingConnectionModalAnalysisAtASpeed
        )

    @property
    def planetary_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5328.PlanetaryConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5328,
        )

        return self.__parent__._cast(_5328.PlanetaryConnectionModalAnalysisAtASpeed)

    @property
    def ring_pins_to_disc_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5335.RingPinsToDiscConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5335,
        )

        return self.__parent__._cast(
            _5335.RingPinsToDiscConnectionModalAnalysisAtASpeed
        )

    @property
    def rolling_ring_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5337.RollingRingConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5337,
        )

        return self.__parent__._cast(_5337.RollingRingConnectionModalAnalysisAtASpeed)

    @property
    def shaft_to_mountable_component_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5342.ShaftToMountableComponentConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5342,
        )

        return self.__parent__._cast(
            _5342.ShaftToMountableComponentConnectionModalAnalysisAtASpeed
        )

    @property
    def spiral_bevel_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5344.SpiralBevelGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5344,
        )

        return self.__parent__._cast(_5344.SpiralBevelGearMeshModalAnalysisAtASpeed)

    @property
    def spring_damper_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5347.SpringDamperConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5347,
        )

        return self.__parent__._cast(_5347.SpringDamperConnectionModalAnalysisAtASpeed)

    @property
    def straight_bevel_diff_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5350.StraightBevelDiffGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5350,
        )

        return self.__parent__._cast(
            _5350.StraightBevelDiffGearMeshModalAnalysisAtASpeed
        )

    @property
    def straight_bevel_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5353.StraightBevelGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5353,
        )

        return self.__parent__._cast(_5353.StraightBevelGearMeshModalAnalysisAtASpeed)

    @property
    def torque_converter_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5362.TorqueConverterConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5362,
        )

        return self.__parent__._cast(
            _5362.TorqueConverterConnectionModalAnalysisAtASpeed
        )

    @property
    def worm_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5368.WormGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5368,
        )

        return self.__parent__._cast(_5368.WormGearMeshModalAnalysisAtASpeed)

    @property
    def zerol_bevel_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5371.ZerolBevelGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5371,
        )

        return self.__parent__._cast(_5371.ZerolBevelGearMeshModalAnalysisAtASpeed)

    @property
    def abstract_shaft_to_mountable_component_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5508.AbstractShaftToMountableComponentConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5508,
        )

        return self.__parent__._cast(
            _5508.AbstractShaftToMountableComponentConnectionMultibodyDynamicsAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5509.AGMAGleasonConicalGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5509,
        )

        return self.__parent__._cast(
            _5509.AGMAGleasonConicalGearMeshMultibodyDynamicsAnalysis
        )

    @property
    def belt_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5517.BeltConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5517,
        )

        return self.__parent__._cast(_5517.BeltConnectionMultibodyDynamicsAnalysis)

    @property
    def bevel_differential_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5519.BevelDifferentialGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5519,
        )

        return self.__parent__._cast(
            _5519.BevelDifferentialGearMeshMultibodyDynamicsAnalysis
        )

    @property
    def bevel_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5524.BevelGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5524,
        )

        return self.__parent__._cast(_5524.BevelGearMeshMultibodyDynamicsAnalysis)

    @property
    def clutch_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5529.ClutchConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5529,
        )

        return self.__parent__._cast(_5529.ClutchConnectionMultibodyDynamicsAnalysis)

    @property
    def coaxial_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5533.CoaxialConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5533,
        )

        return self.__parent__._cast(_5533.CoaxialConnectionMultibodyDynamicsAnalysis)

    @property
    def concept_coupling_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5535.ConceptCouplingConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5535,
        )

        return self.__parent__._cast(
            _5535.ConceptCouplingConnectionMultibodyDynamicsAnalysis
        )

    @property
    def concept_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5538.ConceptGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5538,
        )

        return self.__parent__._cast(_5538.ConceptGearMeshMultibodyDynamicsAnalysis)

    @property
    def conical_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5541.ConicalGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5541,
        )

        return self.__parent__._cast(_5541.ConicalGearMeshMultibodyDynamicsAnalysis)

    @property
    def connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5544.ConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5544,
        )

        return self.__parent__._cast(_5544.ConnectionMultibodyDynamicsAnalysis)

    @property
    def coupling_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5546.CouplingConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5546,
        )

        return self.__parent__._cast(_5546.CouplingConnectionMultibodyDynamicsAnalysis)

    @property
    def cvt_belt_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5549.CVTBeltConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5549,
        )

        return self.__parent__._cast(_5549.CVTBeltConnectionMultibodyDynamicsAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5553.CycloidalDiscCentralBearingConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5553,
        )

        return self.__parent__._cast(
            _5553.CycloidalDiscCentralBearingConnectionMultibodyDynamicsAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5555.CycloidalDiscPlanetaryBearingConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5555,
        )

        return self.__parent__._cast(
            _5555.CycloidalDiscPlanetaryBearingConnectionMultibodyDynamicsAnalysis
        )

    @property
    def cylindrical_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5556.CylindricalGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5556,
        )

        return self.__parent__._cast(_5556.CylindricalGearMeshMultibodyDynamicsAnalysis)

    @property
    def face_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5562.FaceGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5562,
        )

        return self.__parent__._cast(_5562.FaceGearMeshMultibodyDynamicsAnalysis)

    @property
    def gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5567.GearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5567,
        )

        return self.__parent__._cast(_5567.GearMeshMultibodyDynamicsAnalysis)

    @property
    def hypoid_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5572.HypoidGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5572,
        )

        return self.__parent__._cast(_5572.HypoidGearMeshMultibodyDynamicsAnalysis)

    @property
    def inter_mountable_component_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5579.InterMountableComponentConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5579,
        )

        return self.__parent__._cast(
            _5579.InterMountableComponentConnectionMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5580.KlingelnbergCycloPalloidConicalGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5580,
        )

        return self.__parent__._cast(
            _5580.KlingelnbergCycloPalloidConicalGearMeshMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5583.KlingelnbergCycloPalloidHypoidGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5583,
        )

        return self.__parent__._cast(
            _5583.KlingelnbergCycloPalloidHypoidGearMeshMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5586.KlingelnbergCycloPalloidSpiralBevelGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5586,
        )

        return self.__parent__._cast(
            _5586.KlingelnbergCycloPalloidSpiralBevelGearMeshMultibodyDynamicsAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5600.PartToPartShearCouplingConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5600,
        )

        return self.__parent__._cast(
            _5600.PartToPartShearCouplingConnectionMultibodyDynamicsAnalysis
        )

    @property
    def planetary_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5603.PlanetaryConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5603,
        )

        return self.__parent__._cast(_5603.PlanetaryConnectionMultibodyDynamicsAnalysis)

    @property
    def ring_pins_to_disc_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5610.RingPinsToDiscConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5610,
        )

        return self.__parent__._cast(
            _5610.RingPinsToDiscConnectionMultibodyDynamicsAnalysis
        )

    @property
    def rolling_ring_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5612.RollingRingConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5612,
        )

        return self.__parent__._cast(
            _5612.RollingRingConnectionMultibodyDynamicsAnalysis
        )

    @property
    def shaft_to_mountable_component_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5619.ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5619,
        )

        return self.__parent__._cast(
            _5619.ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5622.SpiralBevelGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5622,
        )

        return self.__parent__._cast(_5622.SpiralBevelGearMeshMultibodyDynamicsAnalysis)

    @property
    def spring_damper_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5626.SpringDamperConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5626,
        )

        return self.__parent__._cast(
            _5626.SpringDamperConnectionMultibodyDynamicsAnalysis
        )

    @property
    def straight_bevel_diff_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5629.StraightBevelDiffGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5629,
        )

        return self.__parent__._cast(
            _5629.StraightBevelDiffGearMeshMultibodyDynamicsAnalysis
        )

    @property
    def straight_bevel_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5632.StraightBevelGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5632,
        )

        return self.__parent__._cast(
            _5632.StraightBevelGearMeshMultibodyDynamicsAnalysis
        )

    @property
    def torque_converter_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5641.TorqueConverterConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5641,
        )

        return self.__parent__._cast(
            _5641.TorqueConverterConnectionMultibodyDynamicsAnalysis
        )

    @property
    def worm_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5650.WormGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5650,
        )

        return self.__parent__._cast(_5650.WormGearMeshMultibodyDynamicsAnalysis)

    @property
    def zerol_bevel_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5653.ZerolBevelGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5653,
        )

        return self.__parent__._cast(_5653.ZerolBevelGearMeshMultibodyDynamicsAnalysis)

    @property
    def abstract_shaft_to_mountable_component_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5818.AbstractShaftToMountableComponentConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5818,
        )

        return self.__parent__._cast(
            _5818.AbstractShaftToMountableComponentConnectionHarmonicAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5820.AGMAGleasonConicalGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5820,
        )

        return self.__parent__._cast(_5820.AGMAGleasonConicalGearMeshHarmonicAnalysis)

    @property
    def belt_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5824.BeltConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5824,
        )

        return self.__parent__._cast(_5824.BeltConnectionHarmonicAnalysis)

    @property
    def bevel_differential_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5827.BevelDifferentialGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5827,
        )

        return self.__parent__._cast(_5827.BevelDifferentialGearMeshHarmonicAnalysis)

    @property
    def bevel_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5832.BevelGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5832,
        )

        return self.__parent__._cast(_5832.BevelGearMeshHarmonicAnalysis)

    @property
    def clutch_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5836.ClutchConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5836,
        )

        return self.__parent__._cast(_5836.ClutchConnectionHarmonicAnalysis)

    @property
    def coaxial_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5839.CoaxialConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5839,
        )

        return self.__parent__._cast(_5839.CoaxialConnectionHarmonicAnalysis)

    @property
    def concept_coupling_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5842.ConceptCouplingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5842,
        )

        return self.__parent__._cast(_5842.ConceptCouplingConnectionHarmonicAnalysis)

    @property
    def concept_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5846.ConceptGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5846,
        )

        return self.__parent__._cast(_5846.ConceptGearMeshHarmonicAnalysis)

    @property
    def conical_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5849.ConicalGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5849,
        )

        return self.__parent__._cast(_5849.ConicalGearMeshHarmonicAnalysis)

    @property
    def connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5851.ConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5851,
        )

        return self.__parent__._cast(_5851.ConnectionHarmonicAnalysis)

    @property
    def coupling_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5853.CouplingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5853,
        )

        return self.__parent__._cast(_5853.CouplingConnectionHarmonicAnalysis)

    @property
    def cvt_belt_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5856.CVTBeltConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5856,
        )

        return self.__parent__._cast(_5856.CVTBeltConnectionHarmonicAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5860.CycloidalDiscCentralBearingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5860,
        )

        return self.__parent__._cast(
            _5860.CycloidalDiscCentralBearingConnectionHarmonicAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5862.CycloidalDiscPlanetaryBearingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5862,
        )

        return self.__parent__._cast(
            _5862.CycloidalDiscPlanetaryBearingConnectionHarmonicAnalysis
        )

    @property
    def cylindrical_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5864.CylindricalGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5864,
        )

        return self.__parent__._cast(_5864.CylindricalGearMeshHarmonicAnalysis)

    @property
    def face_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5884.FaceGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5884,
        )

        return self.__parent__._cast(_5884.FaceGearMeshHarmonicAnalysis)

    @property
    def gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5891.GearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5891,
        )

        return self.__parent__._cast(_5891.GearMeshHarmonicAnalysis)

    @property
    def hypoid_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5908.HypoidGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5908,
        )

        return self.__parent__._cast(_5908.HypoidGearMeshHarmonicAnalysis)

    @property
    def inter_mountable_component_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5910.InterMountableComponentConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5910,
        )

        return self.__parent__._cast(
            _5910.InterMountableComponentConnectionHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5912.KlingelnbergCycloPalloidConicalGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5912,
        )

        return self.__parent__._cast(
            _5912.KlingelnbergCycloPalloidConicalGearMeshHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5915.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5915,
        )

        return self.__parent__._cast(
            _5915.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5918.KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5918,
        )

        return self.__parent__._cast(
            _5918.KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5927.PartToPartShearCouplingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5927,
        )

        return self.__parent__._cast(
            _5927.PartToPartShearCouplingConnectionHarmonicAnalysis
        )

    @property
    def planetary_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5931.PlanetaryConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5931,
        )

        return self.__parent__._cast(_5931.PlanetaryConnectionHarmonicAnalysis)

    @property
    def ring_pins_to_disc_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5939.RingPinsToDiscConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5939,
        )

        return self.__parent__._cast(_5939.RingPinsToDiscConnectionHarmonicAnalysis)

    @property
    def rolling_ring_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5941.RollingRingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5941,
        )

        return self.__parent__._cast(_5941.RollingRingConnectionHarmonicAnalysis)

    @property
    def shaft_to_mountable_component_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5946.ShaftToMountableComponentConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5946,
        )

        return self.__parent__._cast(
            _5946.ShaftToMountableComponentConnectionHarmonicAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5951.SpiralBevelGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5951,
        )

        return self.__parent__._cast(_5951.SpiralBevelGearMeshHarmonicAnalysis)

    @property
    def spring_damper_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5953.SpringDamperConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5953,
        )

        return self.__parent__._cast(_5953.SpringDamperConnectionHarmonicAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5958.StraightBevelDiffGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5958,
        )

        return self.__parent__._cast(_5958.StraightBevelDiffGearMeshHarmonicAnalysis)

    @property
    def straight_bevel_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5961.StraightBevelGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5961,
        )

        return self.__parent__._cast(_5961.StraightBevelGearMeshHarmonicAnalysis)

    @property
    def torque_converter_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5969.TorqueConverterConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5969,
        )

        return self.__parent__._cast(_5969.TorqueConverterConnectionHarmonicAnalysis)

    @property
    def worm_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5977.WormGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5977,
        )

        return self.__parent__._cast(_5977.WormGearMeshHarmonicAnalysis)

    @property
    def zerol_bevel_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5980.ZerolBevelGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5980,
        )

        return self.__parent__._cast(_5980.ZerolBevelGearMeshHarmonicAnalysis)

    @property
    def abstract_shaft_to_mountable_component_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6151.AbstractShaftToMountableComponentConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6151,
        )

        return self.__parent__._cast(
            _6151.AbstractShaftToMountableComponentConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def agma_gleason_conical_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6153.AGMAGleasonConicalGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6153,
        )

        return self.__parent__._cast(
            _6153.AGMAGleasonConicalGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def belt_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6157.BeltConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6157,
        )

        return self.__parent__._cast(
            _6157.BeltConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_differential_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6160.BevelDifferentialGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6160,
        )

        return self.__parent__._cast(
            _6160.BevelDifferentialGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6165.BevelGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6165,
        )

        return self.__parent__._cast(
            _6165.BevelGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def clutch_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6169.ClutchConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6169,
        )

        return self.__parent__._cast(
            _6169.ClutchConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def coaxial_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6172.CoaxialConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6172,
        )

        return self.__parent__._cast(
            _6172.CoaxialConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def concept_coupling_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6174.ConceptCouplingConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6174,
        )

        return self.__parent__._cast(
            _6174.ConceptCouplingConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def concept_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6178.ConceptGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6178,
        )

        return self.__parent__._cast(
            _6178.ConceptGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def conical_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6181.ConicalGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6181,
        )

        return self.__parent__._cast(
            _6181.ConicalGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6183.ConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6183,
        )

        return self.__parent__._cast(_6183.ConnectionHarmonicAnalysisOfSingleExcitation)

    @property
    def coupling_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6185.CouplingConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6185,
        )

        return self.__parent__._cast(
            _6185.CouplingConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cvt_belt_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6188.CVTBeltConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6188,
        )

        return self.__parent__._cast(
            _6188.CVTBeltConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cycloidal_disc_central_bearing_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> (
        "_6192.CycloidalDiscCentralBearingConnectionHarmonicAnalysisOfSingleExcitation"
    ):
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6192,
        )

        return self.__parent__._cast(
            _6192.CycloidalDiscCentralBearingConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6194.CycloidalDiscPlanetaryBearingConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6194,
        )

        return self.__parent__._cast(
            _6194.CycloidalDiscPlanetaryBearingConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cylindrical_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6196.CylindricalGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6196,
        )

        return self.__parent__._cast(
            _6196.CylindricalGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def face_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6202.FaceGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6202,
        )

        return self.__parent__._cast(
            _6202.FaceGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6207.GearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6207,
        )

        return self.__parent__._cast(_6207.GearMeshHarmonicAnalysisOfSingleExcitation)

    @property
    def hypoid_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6212.HypoidGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6212,
        )

        return self.__parent__._cast(
            _6212.HypoidGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def inter_mountable_component_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6214.InterMountableComponentConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6214,
        )

        return self.__parent__._cast(
            _6214.InterMountableComponentConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6216.KlingelnbergCycloPalloidConicalGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6216,
        )

        return self.__parent__._cast(
            _6216.KlingelnbergCycloPalloidConicalGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> (
        "_6219.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysisOfSingleExcitation"
    ):
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6219,
        )

        return self.__parent__._cast(
            _6219.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6222.KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6222,
        )

        return self.__parent__._cast(
            _6222.KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def part_to_part_shear_coupling_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6232.PartToPartShearCouplingConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6232,
        )

        return self.__parent__._cast(
            _6232.PartToPartShearCouplingConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def planetary_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6235.PlanetaryConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6235,
        )

        return self.__parent__._cast(
            _6235.PlanetaryConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def ring_pins_to_disc_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6242.RingPinsToDiscConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6242,
        )

        return self.__parent__._cast(
            _6242.RingPinsToDiscConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def rolling_ring_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6244.RollingRingConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6244,
        )

        return self.__parent__._cast(
            _6244.RollingRingConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def shaft_to_mountable_component_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6249.ShaftToMountableComponentConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6249,
        )

        return self.__parent__._cast(
            _6249.ShaftToMountableComponentConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spiral_bevel_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6252.SpiralBevelGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6252,
        )

        return self.__parent__._cast(
            _6252.SpiralBevelGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spring_damper_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6254.SpringDamperConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6254,
        )

        return self.__parent__._cast(
            _6254.SpringDamperConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_diff_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6258.StraightBevelDiffGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6258,
        )

        return self.__parent__._cast(
            _6258.StraightBevelDiffGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6261.StraightBevelGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6261,
        )

        return self.__parent__._cast(
            _6261.StraightBevelGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def torque_converter_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6269.TorqueConverterConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6269,
        )

        return self.__parent__._cast(
            _6269.TorqueConverterConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def worm_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6276.WormGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6276,
        )

        return self.__parent__._cast(
            _6276.WormGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def zerol_bevel_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6279.ZerolBevelGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6279,
        )

        return self.__parent__._cast(
            _6279.ZerolBevelGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def abstract_shaft_to_mountable_component_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6424.AbstractShaftToMountableComponentConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6424,
        )

        return self.__parent__._cast(
            _6424.AbstractShaftToMountableComponentConnectionDynamicAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6426.AGMAGleasonConicalGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6426,
        )

        return self.__parent__._cast(_6426.AGMAGleasonConicalGearMeshDynamicAnalysis)

    @property
    def belt_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6430.BeltConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6430,
        )

        return self.__parent__._cast(_6430.BeltConnectionDynamicAnalysis)

    @property
    def bevel_differential_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6433.BevelDifferentialGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6433,
        )

        return self.__parent__._cast(_6433.BevelDifferentialGearMeshDynamicAnalysis)

    @property
    def bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6438.BevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6438,
        )

        return self.__parent__._cast(_6438.BevelGearMeshDynamicAnalysis)

    @property
    def clutch_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6442.ClutchConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6442,
        )

        return self.__parent__._cast(_6442.ClutchConnectionDynamicAnalysis)

    @property
    def coaxial_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6445.CoaxialConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6445,
        )

        return self.__parent__._cast(_6445.CoaxialConnectionDynamicAnalysis)

    @property
    def concept_coupling_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6447.ConceptCouplingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6447,
        )

        return self.__parent__._cast(_6447.ConceptCouplingConnectionDynamicAnalysis)

    @property
    def concept_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6451.ConceptGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6451,
        )

        return self.__parent__._cast(_6451.ConceptGearMeshDynamicAnalysis)

    @property
    def conical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6454.ConicalGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6454,
        )

        return self.__parent__._cast(_6454.ConicalGearMeshDynamicAnalysis)

    @property
    def connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6456.ConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6456,
        )

        return self.__parent__._cast(_6456.ConnectionDynamicAnalysis)

    @property
    def coupling_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6458.CouplingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6458,
        )

        return self.__parent__._cast(_6458.CouplingConnectionDynamicAnalysis)

    @property
    def cvt_belt_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6461.CVTBeltConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6461,
        )

        return self.__parent__._cast(_6461.CVTBeltConnectionDynamicAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6465.CycloidalDiscCentralBearingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6465,
        )

        return self.__parent__._cast(
            _6465.CycloidalDiscCentralBearingConnectionDynamicAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6467.CycloidalDiscPlanetaryBearingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6467,
        )

        return self.__parent__._cast(
            _6467.CycloidalDiscPlanetaryBearingConnectionDynamicAnalysis
        )

    @property
    def cylindrical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6469.CylindricalGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6469,
        )

        return self.__parent__._cast(_6469.CylindricalGearMeshDynamicAnalysis)

    @property
    def face_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6477.FaceGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6477,
        )

        return self.__parent__._cast(_6477.FaceGearMeshDynamicAnalysis)

    @property
    def gear_mesh_dynamic_analysis(self: "CastSelf") -> "_6482.GearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6482,
        )

        return self.__parent__._cast(_6482.GearMeshDynamicAnalysis)

    @property
    def hypoid_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6486.HypoidGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6486,
        )

        return self.__parent__._cast(_6486.HypoidGearMeshDynamicAnalysis)

    @property
    def inter_mountable_component_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6488.InterMountableComponentConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6488,
        )

        return self.__parent__._cast(
            _6488.InterMountableComponentConnectionDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6490.KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6490,
        )

        return self.__parent__._cast(
            _6490.KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6493.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6493,
        )

        return self.__parent__._cast(
            _6493.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6496.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6496,
        )

        return self.__parent__._cast(
            _6496.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6505.PartToPartShearCouplingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6505,
        )

        return self.__parent__._cast(
            _6505.PartToPartShearCouplingConnectionDynamicAnalysis
        )

    @property
    def planetary_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6508.PlanetaryConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6508,
        )

        return self.__parent__._cast(_6508.PlanetaryConnectionDynamicAnalysis)

    @property
    def ring_pins_to_disc_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6515.RingPinsToDiscConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6515,
        )

        return self.__parent__._cast(_6515.RingPinsToDiscConnectionDynamicAnalysis)

    @property
    def rolling_ring_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6517.RollingRingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6517,
        )

        return self.__parent__._cast(_6517.RollingRingConnectionDynamicAnalysis)

    @property
    def shaft_to_mountable_component_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6522.ShaftToMountableComponentConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6522,
        )

        return self.__parent__._cast(
            _6522.ShaftToMountableComponentConnectionDynamicAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6525.SpiralBevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6525,
        )

        return self.__parent__._cast(_6525.SpiralBevelGearMeshDynamicAnalysis)

    @property
    def spring_damper_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6527.SpringDamperConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6527,
        )

        return self.__parent__._cast(_6527.SpringDamperConnectionDynamicAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6531.StraightBevelDiffGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6531,
        )

        return self.__parent__._cast(_6531.StraightBevelDiffGearMeshDynamicAnalysis)

    @property
    def straight_bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6534.StraightBevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6534,
        )

        return self.__parent__._cast(_6534.StraightBevelGearMeshDynamicAnalysis)

    @property
    def torque_converter_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6542.TorqueConverterConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6542,
        )

        return self.__parent__._cast(_6542.TorqueConverterConnectionDynamicAnalysis)

    @property
    def worm_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6549.WormGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6549,
        )

        return self.__parent__._cast(_6549.WormGearMeshDynamicAnalysis)

    @property
    def zerol_bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6552.ZerolBevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6552,
        )

        return self.__parent__._cast(_6552.ZerolBevelGearMeshDynamicAnalysis)

    @property
    def abstract_shaft_to_mountable_component_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6694.AbstractShaftToMountableComponentConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6694,
        )

        return self.__parent__._cast(
            _6694.AbstractShaftToMountableComponentConnectionCriticalSpeedAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6696.AGMAGleasonConicalGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6696,
        )

        return self.__parent__._cast(
            _6696.AGMAGleasonConicalGearMeshCriticalSpeedAnalysis
        )

    @property
    def belt_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6700.BeltConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6700,
        )

        return self.__parent__._cast(_6700.BeltConnectionCriticalSpeedAnalysis)

    @property
    def bevel_differential_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6703.BevelDifferentialGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6703,
        )

        return self.__parent__._cast(
            _6703.BevelDifferentialGearMeshCriticalSpeedAnalysis
        )

    @property
    def bevel_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6708.BevelGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6708,
        )

        return self.__parent__._cast(_6708.BevelGearMeshCriticalSpeedAnalysis)

    @property
    def clutch_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6712.ClutchConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6712,
        )

        return self.__parent__._cast(_6712.ClutchConnectionCriticalSpeedAnalysis)

    @property
    def coaxial_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6715.CoaxialConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6715,
        )

        return self.__parent__._cast(_6715.CoaxialConnectionCriticalSpeedAnalysis)

    @property
    def concept_coupling_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6717.ConceptCouplingConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6717,
        )

        return self.__parent__._cast(
            _6717.ConceptCouplingConnectionCriticalSpeedAnalysis
        )

    @property
    def concept_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6721.ConceptGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6721,
        )

        return self.__parent__._cast(_6721.ConceptGearMeshCriticalSpeedAnalysis)

    @property
    def conical_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6724.ConicalGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6724,
        )

        return self.__parent__._cast(_6724.ConicalGearMeshCriticalSpeedAnalysis)

    @property
    def connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6726.ConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6726,
        )

        return self.__parent__._cast(_6726.ConnectionCriticalSpeedAnalysis)

    @property
    def coupling_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6728.CouplingConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6728,
        )

        return self.__parent__._cast(_6728.CouplingConnectionCriticalSpeedAnalysis)

    @property
    def cvt_belt_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6734.CVTBeltConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6734,
        )

        return self.__parent__._cast(_6734.CVTBeltConnectionCriticalSpeedAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6738.CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6738,
        )

        return self.__parent__._cast(
            _6738.CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6740.CycloidalDiscPlanetaryBearingConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6740,
        )

        return self.__parent__._cast(
            _6740.CycloidalDiscPlanetaryBearingConnectionCriticalSpeedAnalysis
        )

    @property
    def cylindrical_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6742.CylindricalGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6742,
        )

        return self.__parent__._cast(_6742.CylindricalGearMeshCriticalSpeedAnalysis)

    @property
    def face_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6748.FaceGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6748,
        )

        return self.__parent__._cast(_6748.FaceGearMeshCriticalSpeedAnalysis)

    @property
    def gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6753.GearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6753,
        )

        return self.__parent__._cast(_6753.GearMeshCriticalSpeedAnalysis)

    @property
    def hypoid_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6757.HypoidGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6757,
        )

        return self.__parent__._cast(_6757.HypoidGearMeshCriticalSpeedAnalysis)

    @property
    def inter_mountable_component_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6759.InterMountableComponentConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6759,
        )

        return self.__parent__._cast(
            _6759.InterMountableComponentConnectionCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6761.KlingelnbergCycloPalloidConicalGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6761,
        )

        return self.__parent__._cast(
            _6761.KlingelnbergCycloPalloidConicalGearMeshCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6764.KlingelnbergCycloPalloidHypoidGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6764,
        )

        return self.__parent__._cast(
            _6764.KlingelnbergCycloPalloidHypoidGearMeshCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6767.KlingelnbergCycloPalloidSpiralBevelGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6767,
        )

        return self.__parent__._cast(
            _6767.KlingelnbergCycloPalloidSpiralBevelGearMeshCriticalSpeedAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6776.PartToPartShearCouplingConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6776,
        )

        return self.__parent__._cast(
            _6776.PartToPartShearCouplingConnectionCriticalSpeedAnalysis
        )

    @property
    def planetary_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6779.PlanetaryConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6779,
        )

        return self.__parent__._cast(_6779.PlanetaryConnectionCriticalSpeedAnalysis)

    @property
    def ring_pins_to_disc_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6786.RingPinsToDiscConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6786,
        )

        return self.__parent__._cast(
            _6786.RingPinsToDiscConnectionCriticalSpeedAnalysis
        )

    @property
    def rolling_ring_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6788.RollingRingConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6788,
        )

        return self.__parent__._cast(_6788.RollingRingConnectionCriticalSpeedAnalysis)

    @property
    def shaft_to_mountable_component_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6793.ShaftToMountableComponentConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6793,
        )

        return self.__parent__._cast(
            _6793.ShaftToMountableComponentConnectionCriticalSpeedAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6796.SpiralBevelGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6796,
        )

        return self.__parent__._cast(_6796.SpiralBevelGearMeshCriticalSpeedAnalysis)

    @property
    def spring_damper_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6798.SpringDamperConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6798,
        )

        return self.__parent__._cast(_6798.SpringDamperConnectionCriticalSpeedAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6802.StraightBevelDiffGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6802,
        )

        return self.__parent__._cast(
            _6802.StraightBevelDiffGearMeshCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6805.StraightBevelGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6805,
        )

        return self.__parent__._cast(_6805.StraightBevelGearMeshCriticalSpeedAnalysis)

    @property
    def torque_converter_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6813.TorqueConverterConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6813,
        )

        return self.__parent__._cast(
            _6813.TorqueConverterConnectionCriticalSpeedAnalysis
        )

    @property
    def worm_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6820.WormGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6820,
        )

        return self.__parent__._cast(_6820.WormGearMeshCriticalSpeedAnalysis)

    @property
    def zerol_bevel_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6823.ZerolBevelGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6823,
        )

        return self.__parent__._cast(_6823.ZerolBevelGearMeshCriticalSpeedAnalysis)

    @property
    def abstract_shaft_to_mountable_component_connection_load_case(
        self: "CastSelf",
    ) -> "_6962.AbstractShaftToMountableComponentConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6962,
        )

        return self.__parent__._cast(
            _6962.AbstractShaftToMountableComponentConnectionLoadCase
        )

    @property
    def agma_gleason_conical_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_6967.AGMAGleasonConicalGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6967,
        )

        return self.__parent__._cast(_6967.AGMAGleasonConicalGearMeshLoadCase)

    @property
    def belt_connection_load_case(self: "CastSelf") -> "_6973.BeltConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6973,
        )

        return self.__parent__._cast(_6973.BeltConnectionLoadCase)

    @property
    def bevel_differential_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_6976.BevelDifferentialGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6976,
        )

        return self.__parent__._cast(_6976.BevelDifferentialGearMeshLoadCase)

    @property
    def bevel_gear_mesh_load_case(self: "CastSelf") -> "_6981.BevelGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6981,
        )

        return self.__parent__._cast(_6981.BevelGearMeshLoadCase)

    @property
    def clutch_connection_load_case(
        self: "CastSelf",
    ) -> "_6985.ClutchConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6985,
        )

        return self.__parent__._cast(_6985.ClutchConnectionLoadCase)

    @property
    def coaxial_connection_load_case(
        self: "CastSelf",
    ) -> "_6989.CoaxialConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6989,
        )

        return self.__parent__._cast(_6989.CoaxialConnectionLoadCase)

    @property
    def concept_coupling_connection_load_case(
        self: "CastSelf",
    ) -> "_6991.ConceptCouplingConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6991,
        )

        return self.__parent__._cast(_6991.ConceptCouplingConnectionLoadCase)

    @property
    def concept_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_6995.ConceptGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6995,
        )

        return self.__parent__._cast(_6995.ConceptGearMeshLoadCase)

    @property
    def conical_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_6999.ConicalGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6999,
        )

        return self.__parent__._cast(_6999.ConicalGearMeshLoadCase)

    @property
    def connection_load_case(self: "CastSelf") -> "_7002.ConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7002,
        )

        return self.__parent__._cast(_7002.ConnectionLoadCase)

    @property
    def coupling_connection_load_case(
        self: "CastSelf",
    ) -> "_7004.CouplingConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7004,
        )

        return self.__parent__._cast(_7004.CouplingConnectionLoadCase)

    @property
    def cvt_belt_connection_load_case(
        self: "CastSelf",
    ) -> "_7007.CVTBeltConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7007,
        )

        return self.__parent__._cast(_7007.CVTBeltConnectionLoadCase)

    @property
    def cycloidal_disc_central_bearing_connection_load_case(
        self: "CastSelf",
    ) -> "_7011.CycloidalDiscCentralBearingConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7011,
        )

        return self.__parent__._cast(
            _7011.CycloidalDiscCentralBearingConnectionLoadCase
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_load_case(
        self: "CastSelf",
    ) -> "_7013.CycloidalDiscPlanetaryBearingConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7013,
        )

        return self.__parent__._cast(
            _7013.CycloidalDiscPlanetaryBearingConnectionLoadCase
        )

    @property
    def cylindrical_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7016.CylindricalGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7016,
        )

        return self.__parent__._cast(_7016.CylindricalGearMeshLoadCase)

    @property
    def face_gear_mesh_load_case(self: "CastSelf") -> "_7038.FaceGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7038,
        )

        return self.__parent__._cast(_7038.FaceGearMeshLoadCase)

    @property
    def gear_mesh_load_case(self: "CastSelf") -> "_7045.GearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7045,
        )

        return self.__parent__._cast(_7045.GearMeshLoadCase)

    @property
    def hypoid_gear_mesh_load_case(self: "CastSelf") -> "_7059.HypoidGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7059,
        )

        return self.__parent__._cast(_7059.HypoidGearMeshLoadCase)

    @property
    def inter_mountable_component_connection_load_case(
        self: "CastSelf",
    ) -> "_7064.InterMountableComponentConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7064,
        )

        return self.__parent__._cast(_7064.InterMountableComponentConnectionLoadCase)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7066.KlingelnbergCycloPalloidConicalGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7066,
        )

        return self.__parent__._cast(
            _7066.KlingelnbergCycloPalloidConicalGearMeshLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7069.KlingelnbergCycloPalloidHypoidGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7069,
        )

        return self.__parent__._cast(
            _7069.KlingelnbergCycloPalloidHypoidGearMeshLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7072.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7072,
        )

        return self.__parent__._cast(
            _7072.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase
        )

    @property
    def part_to_part_shear_coupling_connection_load_case(
        self: "CastSelf",
    ) -> "_7084.PartToPartShearCouplingConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7084,
        )

        return self.__parent__._cast(_7084.PartToPartShearCouplingConnectionLoadCase)

    @property
    def planetary_connection_load_case(
        self: "CastSelf",
    ) -> "_7087.PlanetaryConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7087,
        )

        return self.__parent__._cast(_7087.PlanetaryConnectionLoadCase)

    @property
    def ring_pins_to_disc_connection_load_case(
        self: "CastSelf",
    ) -> "_7099.RingPinsToDiscConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7099,
        )

        return self.__parent__._cast(_7099.RingPinsToDiscConnectionLoadCase)

    @property
    def rolling_ring_connection_load_case(
        self: "CastSelf",
    ) -> "_7101.RollingRingConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7101,
        )

        return self.__parent__._cast(_7101.RollingRingConnectionLoadCase)

    @property
    def shaft_to_mountable_component_connection_load_case(
        self: "CastSelf",
    ) -> "_7106.ShaftToMountableComponentConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7106,
        )

        return self.__parent__._cast(_7106.ShaftToMountableComponentConnectionLoadCase)

    @property
    def spiral_bevel_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7109.SpiralBevelGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7109,
        )

        return self.__parent__._cast(_7109.SpiralBevelGearMeshLoadCase)

    @property
    def spring_damper_connection_load_case(
        self: "CastSelf",
    ) -> "_7111.SpringDamperConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7111,
        )

        return self.__parent__._cast(_7111.SpringDamperConnectionLoadCase)

    @property
    def straight_bevel_diff_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7115.StraightBevelDiffGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7115,
        )

        return self.__parent__._cast(_7115.StraightBevelDiffGearMeshLoadCase)

    @property
    def straight_bevel_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7118.StraightBevelGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7118,
        )

        return self.__parent__._cast(_7118.StraightBevelGearMeshLoadCase)

    @property
    def torque_converter_connection_load_case(
        self: "CastSelf",
    ) -> "_7127.TorqueConverterConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7127,
        )

        return self.__parent__._cast(_7127.TorqueConverterConnectionLoadCase)

    @property
    def worm_gear_mesh_load_case(self: "CastSelf") -> "_7138.WormGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7138,
        )

        return self.__parent__._cast(_7138.WormGearMeshLoadCase)

    @property
    def zerol_bevel_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7141.ZerolBevelGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7141,
        )

        return self.__parent__._cast(_7141.ZerolBevelGearMeshLoadCase)

    @property
    def abstract_shaft_to_mountable_component_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7163.AbstractShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7163,
        )

        return self.__parent__._cast(
            _7163.AbstractShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def agma_gleason_conical_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7169.AGMAGleasonConicalGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7169,
        )

        return self.__parent__._cast(
            _7169.AGMAGleasonConicalGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def belt_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7174.BeltConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7174,
        )

        return self.__parent__._cast(
            _7174.BeltConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_differential_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7177.BevelDifferentialGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7177,
        )

        return self.__parent__._cast(
            _7177.BevelDifferentialGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7182.BevelGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7182,
        )

        return self.__parent__._cast(
            _7182.BevelGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def clutch_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7187.ClutchConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7187,
        )

        return self.__parent__._cast(
            _7187.ClutchConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def coaxial_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7189.CoaxialConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7189,
        )

        return self.__parent__._cast(
            _7189.CoaxialConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def concept_coupling_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7192.ConceptCouplingConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7192,
        )

        return self.__parent__._cast(
            _7192.ConceptCouplingConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def concept_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7195.ConceptGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7195,
        )

        return self.__parent__._cast(
            _7195.ConceptGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def conical_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7198.ConicalGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7198,
        )

        return self.__parent__._cast(
            _7198.ConicalGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7200.ConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7200,
        )

        return self.__parent__._cast(
            _7200.ConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def coupling_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7203.CouplingConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7203,
        )

        return self.__parent__._cast(
            _7203.CouplingConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cvt_belt_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7206.CVTBeltConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7206,
        )

        return self.__parent__._cast(
            _7206.CVTBeltConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cycloidal_disc_central_bearing_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7210.CycloidalDiscCentralBearingConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7210,
        )

        return self.__parent__._cast(
            _7210.CycloidalDiscCentralBearingConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7211.CycloidalDiscPlanetaryBearingConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7211,
        )

        return self.__parent__._cast(
            _7211.CycloidalDiscPlanetaryBearingConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cylindrical_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7213.CylindricalGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7213,
        )

        return self.__parent__._cast(
            _7213.CylindricalGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def face_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7219.FaceGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7219,
        )

        return self.__parent__._cast(
            _7219.FaceGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7224.GearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7224,
        )

        return self.__parent__._cast(
            _7224.GearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def hypoid_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7229.HypoidGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7229,
        )

        return self.__parent__._cast(
            _7229.HypoidGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def inter_mountable_component_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7231.InterMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7231,
        )

        return self.__parent__._cast(
            _7231.InterMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7233.KlingelnbergCycloPalloidConicalGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7233,
        )

        return self.__parent__._cast(
            _7233.KlingelnbergCycloPalloidConicalGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7236.KlingelnbergCycloPalloidHypoidGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7236,
        )

        return self.__parent__._cast(
            _7236.KlingelnbergCycloPalloidHypoidGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7239.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7239,
        )

        return self.__parent__._cast(
            _7239.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_to_part_shear_coupling_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7249.PartToPartShearCouplingConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7249,
        )

        return self.__parent__._cast(
            _7249.PartToPartShearCouplingConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def planetary_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7251.PlanetaryConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7251,
        )

        return self.__parent__._cast(
            _7251.PlanetaryConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def ring_pins_to_disc_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7258.RingPinsToDiscConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7258,
        )

        return self.__parent__._cast(
            _7258.RingPinsToDiscConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def rolling_ring_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7261.RollingRingConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7261,
        )

        return self.__parent__._cast(
            _7261.RollingRingConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def shaft_to_mountable_component_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7265.ShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7265,
        )

        return self.__parent__._cast(
            _7265.ShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spiral_bevel_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7268.SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7268,
        )

        return self.__parent__._cast(
            _7268.SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spring_damper_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7271.SpringDamperConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7271,
        )

        return self.__parent__._cast(
            _7271.SpringDamperConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_diff_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7274.StraightBevelDiffGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7274,
        )

        return self.__parent__._cast(
            _7274.StraightBevelDiffGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7277.StraightBevelGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7277,
        )

        return self.__parent__._cast(
            _7277.StraightBevelGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def torque_converter_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7286.TorqueConverterConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7286,
        )

        return self.__parent__._cast(
            _7286.TorqueConverterConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def worm_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7292.WormGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7292,
        )

        return self.__parent__._cast(
            _7292.WormGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def zerol_bevel_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7295.ZerolBevelGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7295,
        )

        return self.__parent__._cast(
            _7295.ZerolBevelGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def abstract_shaft_to_mountable_component_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7431.AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7431,
        )

        return self.__parent__._cast(
            _7431.AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection
        )

    @property
    def agma_gleason_conical_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7436.AGMAGleasonConicalGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7436,
        )

        return self.__parent__._cast(
            _7436.AGMAGleasonConicalGearMeshAdvancedSystemDeflection
        )

    @property
    def belt_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7440.BeltConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7440,
        )

        return self.__parent__._cast(_7440.BeltConnectionAdvancedSystemDeflection)

    @property
    def bevel_differential_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7443.BevelDifferentialGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7443,
        )

        return self.__parent__._cast(
            _7443.BevelDifferentialGearMeshAdvancedSystemDeflection
        )

    @property
    def bevel_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7448.BevelGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7448,
        )

        return self.__parent__._cast(_7448.BevelGearMeshAdvancedSystemDeflection)

    @property
    def clutch_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7453.ClutchConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7453,
        )

        return self.__parent__._cast(_7453.ClutchConnectionAdvancedSystemDeflection)

    @property
    def coaxial_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7455.CoaxialConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7455,
        )

        return self.__parent__._cast(_7455.CoaxialConnectionAdvancedSystemDeflection)

    @property
    def concept_coupling_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7458.ConceptCouplingConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7458,
        )

        return self.__parent__._cast(
            _7458.ConceptCouplingConnectionAdvancedSystemDeflection
        )

    @property
    def concept_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7461.ConceptGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7461,
        )

        return self.__parent__._cast(_7461.ConceptGearMeshAdvancedSystemDeflection)

    @property
    def conical_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7464.ConicalGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7464,
        )

        return self.__parent__._cast(_7464.ConicalGearMeshAdvancedSystemDeflection)

    @property
    def connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7466.ConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7466,
        )

        return self.__parent__._cast(_7466.ConnectionAdvancedSystemDeflection)

    @property
    def coupling_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7470.CouplingConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7470,
        )

        return self.__parent__._cast(_7470.CouplingConnectionAdvancedSystemDeflection)

    @property
    def cvt_belt_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7473.CVTBeltConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7473,
        )

        return self.__parent__._cast(_7473.CVTBeltConnectionAdvancedSystemDeflection)

    @property
    def cycloidal_disc_central_bearing_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7477.CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7477,
        )

        return self.__parent__._cast(
            _7477.CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7478.CycloidalDiscPlanetaryBearingConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7478,
        )

        return self.__parent__._cast(
            _7478.CycloidalDiscPlanetaryBearingConnectionAdvancedSystemDeflection
        )

    @property
    def cylindrical_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7480.CylindricalGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7480,
        )

        return self.__parent__._cast(_7480.CylindricalGearMeshAdvancedSystemDeflection)

    @property
    def face_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7487.FaceGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7487,
        )

        return self.__parent__._cast(_7487.FaceGearMeshAdvancedSystemDeflection)

    @property
    def gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7492.GearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7492,
        )

        return self.__parent__._cast(_7492.GearMeshAdvancedSystemDeflection)

    @property
    def hypoid_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7496.HypoidGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7496,
        )

        return self.__parent__._cast(_7496.HypoidGearMeshAdvancedSystemDeflection)

    @property
    def inter_mountable_component_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7498.InterMountableComponentConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7498,
        )

        return self.__parent__._cast(
            _7498.InterMountableComponentConnectionAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7500.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7500,
        )

        return self.__parent__._cast(
            _7500.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7503.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7503,
        )

        return self.__parent__._cast(
            _7503.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7506.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7506,
        )

        return self.__parent__._cast(
            _7506.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection
        )

    @property
    def part_to_part_shear_coupling_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7517.PartToPartShearCouplingConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7517,
        )

        return self.__parent__._cast(
            _7517.PartToPartShearCouplingConnectionAdvancedSystemDeflection
        )

    @property
    def planetary_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7519.PlanetaryConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7519,
        )

        return self.__parent__._cast(_7519.PlanetaryConnectionAdvancedSystemDeflection)

    @property
    def ring_pins_to_disc_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7526.RingPinsToDiscConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7526,
        )

        return self.__parent__._cast(
            _7526.RingPinsToDiscConnectionAdvancedSystemDeflection
        )

    @property
    def rolling_ring_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7529.RollingRingConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7529,
        )

        return self.__parent__._cast(
            _7529.RollingRingConnectionAdvancedSystemDeflection
        )

    @property
    def shaft_to_mountable_component_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7533.ShaftToMountableComponentConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7533,
        )

        return self.__parent__._cast(
            _7533.ShaftToMountableComponentConnectionAdvancedSystemDeflection
        )

    @property
    def spiral_bevel_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7536.SpiralBevelGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7536,
        )

        return self.__parent__._cast(_7536.SpiralBevelGearMeshAdvancedSystemDeflection)

    @property
    def spring_damper_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7539.SpringDamperConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7539,
        )

        return self.__parent__._cast(
            _7539.SpringDamperConnectionAdvancedSystemDeflection
        )

    @property
    def straight_bevel_diff_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7542.StraightBevelDiffGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7542,
        )

        return self.__parent__._cast(
            _7542.StraightBevelDiffGearMeshAdvancedSystemDeflection
        )

    @property
    def straight_bevel_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7545.StraightBevelGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7545,
        )

        return self.__parent__._cast(
            _7545.StraightBevelGearMeshAdvancedSystemDeflection
        )

    @property
    def torque_converter_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7554.TorqueConverterConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7554,
        )

        return self.__parent__._cast(
            _7554.TorqueConverterConnectionAdvancedSystemDeflection
        )

    @property
    def worm_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7561.WormGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7561,
        )

        return self.__parent__._cast(_7561.WormGearMeshAdvancedSystemDeflection)

    @property
    def zerol_bevel_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7564.ZerolBevelGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7564,
        )

        return self.__parent__._cast(_7564.ZerolBevelGearMeshAdvancedSystemDeflection)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7712.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7712,
        )

        return self.__parent__._cast(_7712.ConnectionAnalysisCase)

    @property
    def connection_fe_analysis(self: "CastSelf") -> "_7714.ConnectionFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7714,
        )

        return self.__parent__._cast(_7714.ConnectionFEAnalysis)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7715.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7715,
        )

        return self.__parent__._cast(_7715.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_time_series_load_analysis_case(
        self: "CastSelf",
    ) -> "_7716.ConnectionTimeSeriesLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7716,
        )

        return self.__parent__._cast(_7716.ConnectionTimeSeriesLoadAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "ConnectionAnalysis":
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
class ConnectionAnalysis(_2742.DesignEntitySingleContextAnalysis):
    """ConnectionAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def short_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShortName")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ConnectionAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConnectionAnalysis
        """
        return _Cast_ConnectionAnalysis(self)
