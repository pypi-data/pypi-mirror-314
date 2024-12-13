"""LoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    overridable_enum_runtime,
    utility,
)
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import enum_with_selected_value, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.bearing_results.rolling import _2028
from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import _2165
from mastapy._private.gears import _349
from mastapy._private.nodal_analysis.nodal_entities import _131
from mastapy._private.system_model import _2271
from mastapy._private.system_model.analyses_and_results import _2739

_COUPLING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings", "CouplingConnection"
)
_SPRING_DAMPER_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings", "SpringDamperConnection"
)
_TORQUE_CONVERTER_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings",
    "TorqueConverterConnection",
)
_PART_TO_PART_SHEAR_COUPLING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings",
    "PartToPartShearCouplingConnection",
)
_CLUTCH_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings", "ClutchConnection"
)
_CONCEPT_COUPLING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings",
    "ConceptCouplingConnection",
)
_ABSTRACT_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "AbstractShaft"
)
_MICROPHONE = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Microphone")
_MICROPHONE_ARRAY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MicrophoneArray"
)
_ABSTRACT_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "AbstractAssembly"
)
_ABSTRACT_SHAFT_OR_HOUSING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "AbstractShaftOrHousing"
)
_BEARING = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Bearing")
_BOLT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Bolt")
_BOLTED_JOINT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "BoltedJoint")
_COMPONENT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Component")
_CONNECTOR = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Connector")
_DATUM = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Datum")
_EXTERNAL_CAD_MODEL = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "ExternalCADModel"
)
_FE_PART = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "FEPart")
_FLEXIBLE_PIN_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "FlexiblePinAssembly"
)
_ASSEMBLY = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Assembly")
_GUIDE_DXF_MODEL = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "GuideDxfModel"
)
_MASS_DISC = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "MassDisc")
_MEASUREMENT_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MeasurementComponent"
)
_MOUNTABLE_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MountableComponent"
)
_OIL_SEAL = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "OilSeal")
_PART = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Part")
_PLANET_CARRIER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "PlanetCarrier"
)
_POINT_LOAD = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "PointLoad")
_POWER_LOAD = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "PowerLoad")
_ROOT_ASSEMBLY = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "RootAssembly")
_SPECIALISED_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "SpecialisedAssembly"
)
_UNBALANCED_MASS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "UnbalancedMass"
)
_VIRTUAL_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "VirtualComponent"
)
_SHAFT = python_net_import("SMT.MastaAPI.SystemModel.PartModel.ShaftModel", "Shaft")
_CONCEPT_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConceptGear"
)
_CONCEPT_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConceptGearSet"
)
_FACE_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "FaceGear")
_FACE_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "FaceGearSet"
)
_AGMA_GLEASON_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGear"
)
_AGMA_GLEASON_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGearSet"
)
_BEVEL_DIFFERENTIAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialGear"
)
_BEVEL_DIFFERENTIAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialGearSet"
)
_BEVEL_DIFFERENTIAL_PLANET_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialPlanetGear"
)
_BEVEL_DIFFERENTIAL_SUN_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialSunGear"
)
_BEVEL_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelGear")
_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelGearSet"
)
_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGear"
)
_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGearSet"
)
_CYLINDRICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalGear"
)
_CYLINDRICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalGearSet"
)
_CYLINDRICAL_PLANET_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalPlanetGear"
)
_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "Gear")
_GEAR_SET = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "GearSet")
_HYPOID_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "HypoidGear"
)
_HYPOID_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "HypoidGearSet"
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidConicalGear"
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidConicalGearSet"
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidHypoidGear"
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidHypoidGearSet"
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears",
    "KlingelnbergCycloPalloidSpiralBevelGear",
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears",
    "KlingelnbergCycloPalloidSpiralBevelGearSet",
)
_PLANETARY_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "PlanetaryGearSet"
)
_SPIRAL_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "SpiralBevelGear"
)
_SPIRAL_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "SpiralBevelGearSet"
)
_STRAIGHT_BEVEL_DIFF_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelDiffGear"
)
_STRAIGHT_BEVEL_DIFF_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelDiffGearSet"
)
_STRAIGHT_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelGear"
)
_STRAIGHT_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelGearSet"
)
_STRAIGHT_BEVEL_PLANET_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelPlanetGear"
)
_STRAIGHT_BEVEL_SUN_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelSunGear"
)
_WORM_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "WormGear")
_WORM_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "WormGearSet"
)
_ZEROL_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ZerolBevelGear"
)
_ZEROL_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ZerolBevelGearSet"
)
_CYCLOIDAL_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "CycloidalAssembly"
)
_CYCLOIDAL_DISC = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "CycloidalDisc"
)
_RING_PINS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "RingPins"
)
_PART_TO_PART_SHEAR_COUPLING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "PartToPartShearCoupling"
)
_PART_TO_PART_SHEAR_COUPLING_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "PartToPartShearCouplingHalf"
)
_BELT_DRIVE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "BeltDrive"
)
_CLUTCH = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Couplings", "Clutch")
_CLUTCH_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ClutchHalf"
)
_CONCEPT_COUPLING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ConceptCoupling"
)
_CONCEPT_COUPLING_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ConceptCouplingHalf"
)
_COUPLING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Coupling"
)
_COUPLING_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CouplingHalf"
)
_CVT = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Couplings", "CVT")
_CVT_PULLEY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CVTPulley"
)
_PULLEY = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Couplings", "Pulley")
_SHAFT_HUB_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ShaftHubConnection"
)
_ROLLING_RING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "RollingRing"
)
_ROLLING_RING_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "RollingRingAssembly"
)
_SPRING_DAMPER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SpringDamper"
)
_SPRING_DAMPER_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SpringDamperHalf"
)
_SYNCHRONISER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Synchroniser"
)
_SYNCHRONISER_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserHalf"
)
_SYNCHRONISER_PART = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserPart"
)
_SYNCHRONISER_SLEEVE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserSleeve"
)
_TORQUE_CONVERTER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverter"
)
_TORQUE_CONVERTER_PUMP = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverterPump"
)
_TORQUE_CONVERTER_TURBINE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverterTurbine"
)
_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets",
    "ShaftToMountableComponentConnection",
)
_CVT_BELT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "CVTBeltConnection"
)
_BELT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "BeltConnection"
)
_COAXIAL_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "CoaxialConnection"
)
_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "Connection"
)
_INTER_MOUNTABLE_COMPONENT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets",
    "InterMountableComponentConnection",
)
_PLANETARY_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "PlanetaryConnection"
)
_ROLLING_RING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "RollingRingConnection"
)
_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets",
    "AbstractShaftToMountableComponentConnection",
)
_BEVEL_DIFFERENTIAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "BevelDifferentialGearMesh"
)
_CONCEPT_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "ConceptGearMesh"
)
_FACE_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "FaceGearMesh"
)
_STRAIGHT_BEVEL_DIFF_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "StraightBevelDiffGearMesh"
)
_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "BevelGearMesh"
)
_CONICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "ConicalGearMesh"
)
_AGMA_GLEASON_CONICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "AGMAGleasonConicalGearMesh"
)
_CYLINDRICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "CylindricalGearMesh"
)
_HYPOID_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "HypoidGearMesh"
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears",
    "KlingelnbergCycloPalloidConicalGearMesh",
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears",
    "KlingelnbergCycloPalloidHypoidGearMesh",
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears",
    "KlingelnbergCycloPalloidSpiralBevelGearMesh",
)
_SPIRAL_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "SpiralBevelGearMesh"
)
_STRAIGHT_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "StraightBevelGearMesh"
)
_WORM_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "WormGearMesh"
)
_ZEROL_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "ZerolBevelGearMesh"
)
_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "GearMesh"
)
_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal",
    "CycloidalDiscCentralBearingConnection",
)
_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal",
    "CycloidalDiscPlanetaryBearingConnection",
)
_RING_PINS_TO_DISC_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal",
    "RingPinsToDiscConnection",
)
_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "LoadCase"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings.bearing_results.rolling import _2023, _2125
    from mastapy._private.system_model import _2266, _2281
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5906,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5514
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4502,
        _4504,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6957,
        _6958,
        _6959,
        _6960,
        _6961,
        _6962,
        _6963,
        _6964,
        _6966,
        _6967,
        _6968,
        _6971,
        _6972,
        _6973,
        _6974,
        _6975,
        _6976,
        _6977,
        _6978,
        _6979,
        _6980,
        _6981,
        _6982,
        _6983,
        _6984,
        _6985,
        _6986,
        _6987,
        _6989,
        _6990,
        _6991,
        _6992,
        _6993,
        _6994,
        _6995,
        _6996,
        _6997,
        _6999,
        _7001,
        _7002,
        _7003,
        _7004,
        _7005,
        _7006,
        _7007,
        _7008,
        _7009,
        _7010,
        _7011,
        _7012,
        _7013,
        _7014,
        _7016,
        _7018,
        _7019,
        _7022,
        _7036,
        _7037,
        _7038,
        _7039,
        _7040,
        _7041,
        _7043,
        _7045,
        _7048,
        _7049,
        _7058,
        _7059,
        _7060,
        _7064,
        _7065,
        _7066,
        _7067,
        _7068,
        _7069,
        _7070,
        _7071,
        _7072,
        _7073,
        _7074,
        _7075,
        _7077,
        _7078,
        _7079,
        _7081,
        _7083,
        _7084,
        _7085,
        _7086,
        _7087,
        _7088,
        _7090,
        _7093,
        _7094,
        _7095,
        _7098,
        _7099,
        _7100,
        _7101,
        _7102,
        _7103,
        _7104,
        _7105,
        _7106,
        _7107,
        _7108,
        _7109,
        _7110,
        _7111,
        _7112,
        _7113,
        _7114,
        _7115,
        _7116,
        _7117,
        _7118,
        _7119,
        _7120,
        _7121,
        _7122,
        _7123,
        _7124,
        _7125,
        _7127,
        _7128,
        _7129,
        _7130,
        _7133,
        _7135,
        _7136,
        _7137,
        _7138,
        _7139,
        _7140,
        _7141,
        _7142,
    )
    from mastapy._private.system_model.connections_and_sockets import (
        _2322,
        _2325,
        _2326,
        _2329,
        _2330,
        _2338,
        _2344,
        _2349,
        _2352,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import (
        _2399,
        _2401,
        _2403,
        _2405,
        _2407,
        _2409,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2392,
        _2395,
        _2398,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2356,
        _2358,
        _2360,
        _2362,
        _2364,
        _2366,
        _2368,
        _2370,
        _2372,
        _2375,
        _2376,
        _2377,
        _2380,
        _2382,
        _2384,
        _2386,
        _2388,
    )
    from mastapy._private.system_model.part_model import (
        _2491,
        _2492,
        _2493,
        _2494,
        _2497,
        _2500,
        _2501,
        _2502,
        _2505,
        _2506,
        _2510,
        _2511,
        _2512,
        _2513,
        _2520,
        _2521,
        _2522,
        _2523,
        _2524,
        _2526,
        _2528,
        _2529,
        _2531,
        _2532,
        _2535,
        _2537,
        _2538,
        _2540,
    )
    from mastapy._private.system_model.part_model.couplings import (
        _2638,
        _2640,
        _2641,
        _2643,
        _2644,
        _2646,
        _2647,
        _2649,
        _2650,
        _2651,
        _2652,
        _2654,
        _2660,
        _2661,
        _2662,
        _2667,
        _2668,
        _2669,
        _2671,
        _2672,
        _2673,
        _2674,
        _2675,
        _2677,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2629, _2630, _2631
    from mastapy._private.system_model.part_model.gears import (
        _2574,
        _2575,
        _2576,
        _2577,
        _2578,
        _2579,
        _2580,
        _2581,
        _2582,
        _2583,
        _2584,
        _2585,
        _2586,
        _2587,
        _2588,
        _2589,
        _2590,
        _2591,
        _2593,
        _2595,
        _2596,
        _2597,
        _2598,
        _2599,
        _2600,
        _2601,
        _2602,
        _2603,
        _2604,
        _2605,
        _2606,
        _2607,
        _2608,
        _2609,
        _2610,
        _2611,
        _2612,
        _2613,
        _2614,
        _2615,
    )
    from mastapy._private.system_model.part_model.shaft_model import _2543

    Self = TypeVar("Self", bound="LoadCase")
    CastSelf = TypeVar("CastSelf", bound="LoadCase._Cast_LoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("LoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadCase:
    """Special nested class for casting LoadCase to subclasses."""

    __parent__: "LoadCase"

    @property
    def context(self: "CastSelf") -> "_2739.Context":
        return self.__parent__._cast(_2739.Context)

    @property
    def parametric_study_static_load(
        self: "CastSelf",
    ) -> "_4502.ParametricStudyStaticLoad":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4502,
        )

        return self.__parent__._cast(_4502.ParametricStudyStaticLoad)

    @property
    def harmonic_analysis_with_varying_stiffness_static_load_case(
        self: "CastSelf",
    ) -> "_5906.HarmonicAnalysisWithVaryingStiffnessStaticLoadCase":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5906,
        )

        return self.__parent__._cast(
            _5906.HarmonicAnalysisWithVaryingStiffnessStaticLoadCase
        )

    @property
    def static_load_case(self: "CastSelf") -> "_6957.StaticLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6957,
        )

        return self.__parent__._cast(_6957.StaticLoadCase)

    @property
    def time_series_load_case(self: "CastSelf") -> "_6958.TimeSeriesLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6958,
        )

        return self.__parent__._cast(_6958.TimeSeriesLoadCase)

    @property
    def advanced_time_stepping_analysis_for_modulation_static_load_case(
        self: "CastSelf",
    ) -> "_6964.AdvancedTimeSteppingAnalysisForModulationStaticLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6964,
        )

        return self.__parent__._cast(
            _6964.AdvancedTimeSteppingAnalysisForModulationStaticLoadCase
        )

    @property
    def load_case(self: "CastSelf") -> "LoadCase":
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
class LoadCase(_2739.Context):
    """LoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def air_density(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "AirDensity")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @air_density.setter
    @enforce_parameter_types
    def air_density(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AirDensity", value)

    @property
    def ball_bearing_contact_calculation(
        self: "Self",
    ) -> "_2023.BallBearingContactCalculation":
        """mastapy.bearings.bearing_results.rolling.BallBearingContactCalculation"""
        temp = pythonnet_property_get(self.wrapped, "BallBearingContactCalculation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Bearings.BearingResults.Rolling.BallBearingContactCalculation",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.bearing_results.rolling._2023",
            "BallBearingContactCalculation",
        )(value)

    @ball_bearing_contact_calculation.setter
    @enforce_parameter_types
    def ball_bearing_contact_calculation(
        self: "Self", value: "_2023.BallBearingContactCalculation"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Bearings.BearingResults.Rolling.BallBearingContactCalculation",
        )
        pythonnet_property_set(self.wrapped, "BallBearingContactCalculation", value)

    @property
    def ball_bearing_friction_model_for_gyroscopic_moment(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_FrictionModelForGyroscopicMoment":
        """EnumWithSelectedValue[mastapy.bearings.bearing_results.rolling.FrictionModelForGyroscopicMoment]"""
        temp = pythonnet_property_get(
            self.wrapped, "BallBearingFrictionModelForGyroscopicMoment"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_FrictionModelForGyroscopicMoment.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @ball_bearing_friction_model_for_gyroscopic_moment.setter
    @enforce_parameter_types
    def ball_bearing_friction_model_for_gyroscopic_moment(
        self: "Self", value: "_2028.FrictionModelForGyroscopicMoment"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FrictionModelForGyroscopicMoment.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped, "BallBearingFrictionModelForGyroscopicMoment", value
        )

    @property
    def bearing_element_orbit_model(self: "Self") -> "_5514.BearingElementOrbitModel":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BearingElementOrbitModel"""
        temp = pythonnet_property_get(self.wrapped, "BearingElementOrbitModel")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.BearingElementOrbitModel",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.mbd_analyses._5514",
            "BearingElementOrbitModel",
        )(value)

    @bearing_element_orbit_model.setter
    @enforce_parameter_types
    def bearing_element_orbit_model(
        self: "Self", value: "_5514.BearingElementOrbitModel"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.BearingElementOrbitModel",
        )
        pythonnet_property_set(self.wrapped, "BearingElementOrbitModel", value)

    @property
    def characteristic_specific_acoustic_impedance(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "CharacteristicSpecificAcousticImpedance"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @characteristic_specific_acoustic_impedance.setter
    @enforce_parameter_types
    def characteristic_specific_acoustic_impedance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "CharacteristicSpecificAcousticImpedance", value
        )

    @property
    def energy_convergence_absolute_tolerance(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "EnergyConvergenceAbsoluteTolerance"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @energy_convergence_absolute_tolerance.setter
    @enforce_parameter_types
    def energy_convergence_absolute_tolerance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "EnergyConvergenceAbsoluteTolerance", value
        )

    @property
    def expand_grounded_nodes_for_thermal_effects(
        self: "Self",
    ) -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(
            self.wrapped, "ExpandGroundedNodesForThermalEffects"
        )

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @expand_grounded_nodes_for_thermal_effects.setter
    @enforce_parameter_types
    def expand_grounded_nodes_for_thermal_effects(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "ExpandGroundedNodesForThermalEffects", value
        )

    @property
    def force_multiple_mesh_nodes_for_unloaded_cylindrical_gear_meshes(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "ForceMultipleMeshNodesForUnloadedCylindricalGearMeshes"
        )

        if temp is None:
            return False

        return temp

    @force_multiple_mesh_nodes_for_unloaded_cylindrical_gear_meshes.setter
    @enforce_parameter_types
    def force_multiple_mesh_nodes_for_unloaded_cylindrical_gear_meshes(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ForceMultipleMeshNodesForUnloadedCylindricalGearMeshes",
            bool(value) if value is not None else False,
        )

    @property
    def gear_mesh_nodes_per_unit_length_to_diameter_ratio(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "GearMeshNodesPerUnitLengthToDiameterRatio"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @gear_mesh_nodes_per_unit_length_to_diameter_ratio.setter
    @enforce_parameter_types
    def gear_mesh_nodes_per_unit_length_to_diameter_ratio(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "GearMeshNodesPerUnitLengthToDiameterRatio", value
        )

    @property
    def grid_refinement_factor_contact_width(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "GridRefinementFactorContactWidth")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @grid_refinement_factor_contact_width.setter
    @enforce_parameter_types
    def grid_refinement_factor_contact_width(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "GridRefinementFactorContactWidth", value)

    @property
    def grid_refinement_factor_rib_height(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "GridRefinementFactorRibHeight")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @grid_refinement_factor_rib_height.setter
    @enforce_parameter_types
    def grid_refinement_factor_rib_height(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "GridRefinementFactorRibHeight", value)

    @property
    def hypoid_gear_wind_up_removal_method_for_misalignments(
        self: "Self",
    ) -> "_2266.HypoidWindUpRemovalMethod":
        """mastapy.system_model.HypoidWindUpRemovalMethod"""
        temp = pythonnet_property_get(
            self.wrapped, "HypoidGearWindUpRemovalMethodForMisalignments"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.SystemModel.HypoidWindUpRemovalMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model._2266", "HypoidWindUpRemovalMethod"
        )(value)

    @hypoid_gear_wind_up_removal_method_for_misalignments.setter
    @enforce_parameter_types
    def hypoid_gear_wind_up_removal_method_for_misalignments(
        self: "Self", value: "_2266.HypoidWindUpRemovalMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.SystemModel.HypoidWindUpRemovalMethod"
        )
        pythonnet_property_set(
            self.wrapped, "HypoidGearWindUpRemovalMethodForMisalignments", value
        )

    @property
    def include_bearing_centrifugal_ring_expansion(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "IncludeBearingCentrifugalRingExpansion"
        )

        if temp is None:
            return False

        return temp

    @include_bearing_centrifugal_ring_expansion.setter
    @enforce_parameter_types
    def include_bearing_centrifugal_ring_expansion(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeBearingCentrifugalRingExpansion",
            bool(value) if value is not None else False,
        )

    @property
    def include_bearing_centrifugal(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeBearingCentrifugal")

        if temp is None:
            return False

        return temp

    @include_bearing_centrifugal.setter
    @enforce_parameter_types
    def include_bearing_centrifugal(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeBearingCentrifugal",
            bool(value) if value is not None else False,
        )

    @property
    def include_fitting_effects(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeFittingEffects")

        if temp is None:
            return False

        return temp

    @include_fitting_effects.setter
    @enforce_parameter_types
    def include_fitting_effects(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeFittingEffects",
            bool(value) if value is not None else False,
        )

    @property
    def include_gear_blank_elastic_distortion(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeGearBlankElasticDistortion")

        if temp is None:
            return False

        return temp

    @include_gear_blank_elastic_distortion.setter
    @enforce_parameter_types
    def include_gear_blank_elastic_distortion(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeGearBlankElasticDistortion",
            bool(value) if value is not None else False,
        )

    @property
    def include_gravity(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeGravity")

        if temp is None:
            return False

        return temp

    @include_gravity.setter
    @enforce_parameter_types
    def include_gravity(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IncludeGravity", bool(value) if value is not None else False
        )

    @property
    def include_inner_race_distortion_for_flexible_pin_spindle(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "IncludeInnerRaceDistortionForFlexiblePinSpindle"
        )

        if temp is None:
            return False

        return temp

    @include_inner_race_distortion_for_flexible_pin_spindle.setter
    @enforce_parameter_types
    def include_inner_race_distortion_for_flexible_pin_spindle(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeInnerRaceDistortionForFlexiblePinSpindle",
            bool(value) if value is not None else False,
        )

    @property
    def include_planetary_centrifugal(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludePlanetaryCentrifugal")

        if temp is None:
            return False

        return temp

    @include_planetary_centrifugal.setter
    @enforce_parameter_types
    def include_planetary_centrifugal(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludePlanetaryCentrifugal",
            bool(value) if value is not None else False,
        )

    @property
    def include_profile_modifications_and_manufacturing_errors_during_cycloidal_analysis(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "IncludeProfileModificationsAndManufacturingErrorsDuringCycloidalAnalysis",
        )

        if temp is None:
            return False

        return temp

    @include_profile_modifications_and_manufacturing_errors_during_cycloidal_analysis.setter
    @enforce_parameter_types
    def include_profile_modifications_and_manufacturing_errors_during_cycloidal_analysis(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeProfileModificationsAndManufacturingErrorsDuringCycloidalAnalysis",
            bool(value) if value is not None else False,
        )

    @property
    def include_rib_contact_analysis(self: "Self") -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(self.wrapped, "IncludeRibContactAnalysis")

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @include_rib_contact_analysis.setter
    @enforce_parameter_types
    def include_rib_contact_analysis(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(self.wrapped, "IncludeRibContactAnalysis", value)

    @property
    def include_ring_ovality(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeRingOvality")

        if temp is None:
            return False

        return temp

    @include_ring_ovality.setter
    @enforce_parameter_types
    def include_ring_ovality(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeRingOvality",
            bool(value) if value is not None else False,
        )

    @property
    def include_thermal_expansion_effects(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeThermalExpansionEffects")

        if temp is None:
            return False

        return temp

    @include_thermal_expansion_effects.setter
    @enforce_parameter_types
    def include_thermal_expansion_effects(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeThermalExpansionEffects",
            bool(value) if value is not None else False,
        )

    @property
    def include_tilt_stiffness_for_bevel_hypoid_gears(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "IncludeTiltStiffnessForBevelHypoidGears"
        )

        if temp is None:
            return False

        return temp

    @include_tilt_stiffness_for_bevel_hypoid_gears.setter
    @enforce_parameter_types
    def include_tilt_stiffness_for_bevel_hypoid_gears(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeTiltStiffnessForBevelHypoidGears",
            bool(value) if value is not None else False,
        )

    @property
    def maximum_shaft_section_cross_sectional_area_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumShaftSectionCrossSectionalAreaRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @maximum_shaft_section_cross_sectional_area_ratio.setter
    @enforce_parameter_types
    def maximum_shaft_section_cross_sectional_area_ratio(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumShaftSectionCrossSectionalAreaRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    def maximum_shaft_section_length_to_diameter_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumShaftSectionLengthToDiameterRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @maximum_shaft_section_length_to_diameter_ratio.setter
    @enforce_parameter_types
    def maximum_shaft_section_length_to_diameter_ratio(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumShaftSectionLengthToDiameterRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    def maximum_shaft_section_polar_area_moment_of_inertia_ratio(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumShaftSectionPolarAreaMomentOfInertiaRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @maximum_shaft_section_polar_area_moment_of_inertia_ratio.setter
    @enforce_parameter_types
    def maximum_shaft_section_polar_area_moment_of_inertia_ratio(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumShaftSectionPolarAreaMomentOfInertiaRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    def maximum_translation_per_solver_step(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MaximumTranslationPerSolverStep")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_translation_per_solver_step.setter
    @enforce_parameter_types
    def maximum_translation_per_solver_step(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaximumTranslationPerSolverStep", value)

    @property
    def mesh_stiffness_model(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel":
        """EnumWithSelectedValue[mastapy.system_model.MeshStiffnessModel]"""
        temp = pythonnet_property_get(self.wrapped, "MeshStiffnessModel")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @mesh_stiffness_model.setter
    @enforce_parameter_types
    def mesh_stiffness_model(self: "Self", value: "_2271.MeshStiffnessModel") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "MeshStiffnessModel", value)

    @property
    def micro_geometry_model_in_system_deflection(
        self: "Self",
    ) -> "overridable.Overridable_MicroGeometryModel":
        """Overridable[mastapy.gears.MicroGeometryModel]"""
        temp = pythonnet_property_get(
            self.wrapped, "MicroGeometryModelInSystemDeflection"
        )

        if temp is None:
            return None

        value = overridable.Overridable_MicroGeometryModel.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @micro_geometry_model_in_system_deflection.setter
    @enforce_parameter_types
    def micro_geometry_model_in_system_deflection(
        self: "Self",
        value: "Union[_349.MicroGeometryModel, Tuple[_349.MicroGeometryModel, bool]]",
    ) -> None:
        wrapper_type = overridable.Overridable_MicroGeometryModel.wrapper_type()
        enclosed_type = overridable.Overridable_MicroGeometryModel.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MicroGeometryModelInSystemDeflection", value
        )

    @property
    def minimum_force_for_bearing_to_be_considered_loaded(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumForceForBearingToBeConsideredLoaded"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_force_for_bearing_to_be_considered_loaded.setter
    @enforce_parameter_types
    def minimum_force_for_bearing_to_be_considered_loaded(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MinimumForceForBearingToBeConsideredLoaded", value
        )

    @property
    def minimum_moment_for_bearing_to_be_considered_loaded(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumMomentForBearingToBeConsideredLoaded"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_moment_for_bearing_to_be_considered_loaded.setter
    @enforce_parameter_types
    def minimum_moment_for_bearing_to_be_considered_loaded(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MinimumMomentForBearingToBeConsideredLoaded", value
        )

    @property
    def minimum_number_of_gear_mesh_nodes(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "MinimumNumberOfGearMeshNodes")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @minimum_number_of_gear_mesh_nodes.setter
    @enforce_parameter_types
    def minimum_number_of_gear_mesh_nodes(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MinimumNumberOfGearMeshNodes", value)

    @property
    def minimum_power_for_gear_mesh_to_be_loaded(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MinimumPowerForGearMeshToBeLoaded")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_power_for_gear_mesh_to_be_loaded.setter
    @enforce_parameter_types
    def minimum_power_for_gear_mesh_to_be_loaded(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MinimumPowerForGearMeshToBeLoaded", value)

    @property
    def minimum_torque_for_gear_mesh_to_be_loaded(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumTorqueForGearMeshToBeLoaded"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_torque_for_gear_mesh_to_be_loaded.setter
    @enforce_parameter_types
    def minimum_torque_for_gear_mesh_to_be_loaded(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MinimumTorqueForGearMeshToBeLoaded", value
        )

    @property
    def model_bearing_mounting_clearances_automatically(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "ModelBearingMountingClearancesAutomatically"
        )

        if temp is None:
            return False

        return temp

    @model_bearing_mounting_clearances_automatically.setter
    @enforce_parameter_types
    def model_bearing_mounting_clearances_automatically(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ModelBearingMountingClearancesAutomatically",
            bool(value) if value is not None else False,
        )

    @property
    def number_of_grid_points_across_rib_contact_width(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfGridPointsAcrossRibContactWidth"
        )

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_grid_points_across_rib_contact_width.setter
    @enforce_parameter_types
    def number_of_grid_points_across_rib_contact_width(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "NumberOfGridPointsAcrossRibContactWidth", value
        )

    @property
    def number_of_grid_points_across_rib_height(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfGridPointsAcrossRibHeight")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_grid_points_across_rib_height.setter
    @enforce_parameter_types
    def number_of_grid_points_across_rib_height(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NumberOfGridPointsAcrossRibHeight", value)

    @property
    def number_of_strips_for_roller_calculation(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfStripsForRollerCalculation"
        )

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_strips_for_roller_calculation.setter
    @enforce_parameter_types
    def number_of_strips_for_roller_calculation(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "NumberOfStripsForRollerCalculation", value
        )

    @property
    def peak_load_factor_for_shafts(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PeakLoadFactorForShafts")

        if temp is None:
            return 0.0

        return temp

    @peak_load_factor_for_shafts.setter
    @enforce_parameter_types
    def peak_load_factor_for_shafts(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PeakLoadFactorForShafts",
            float(value) if value is not None else 0.0,
        )

    @property
    def refine_grid_around_contact_point(
        self: "Self",
    ) -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(self.wrapped, "RefineGridAroundContactPoint")

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @refine_grid_around_contact_point.setter
    @enforce_parameter_types
    def refine_grid_around_contact_point(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RefineGridAroundContactPoint", value)

    @property
    def relative_tolerance_for_convergence(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RelativeToleranceForConvergence")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @relative_tolerance_for_convergence.setter
    @enforce_parameter_types
    def relative_tolerance_for_convergence(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RelativeToleranceForConvergence", value)

    @property
    def ring_ovality_scaling(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RingOvalityScaling")

        if temp is None:
            return 0.0

        return temp

    @ring_ovality_scaling.setter
    @enforce_parameter_types
    def ring_ovality_scaling(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RingOvalityScaling",
            float(value) if value is not None else 0.0,
        )

    @property
    def roller_analysis_method(self: "Self") -> "_2125.RollerAnalysisMethod":
        """mastapy.bearings.bearing_results.rolling.RollerAnalysisMethod"""
        temp = pythonnet_property_get(self.wrapped, "RollerAnalysisMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.BearingResults.Rolling.RollerAnalysisMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.bearing_results.rolling._2125",
            "RollerAnalysisMethod",
        )(value)

    @roller_analysis_method.setter
    @enforce_parameter_types
    def roller_analysis_method(
        self: "Self", value: "_2125.RollerAnalysisMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.BearingResults.Rolling.RollerAnalysisMethod"
        )
        pythonnet_property_set(self.wrapped, "RollerAnalysisMethod", value)

    @property
    def set_first_element_angle_to_load_direction(
        self: "Self",
    ) -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(
            self.wrapped, "SetFirstElementAngleToLoadDirection"
        )

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @set_first_element_angle_to_load_direction.setter
    @enforce_parameter_types
    def set_first_element_angle_to_load_direction(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "SetFirstElementAngleToLoadDirection", value
        )

    @property
    def shear_area_factor_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ShearAreaFactorMethod":
        """EnumWithSelectedValue[mastapy.nodal_analysis.nodal_entities.ShearAreaFactorMethod]"""
        temp = pythonnet_property_get(self.wrapped, "ShearAreaFactorMethod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ShearAreaFactorMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @shear_area_factor_method.setter
    @enforce_parameter_types
    def shear_area_factor_method(
        self: "Self", value: "_131.ShearAreaFactorMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ShearAreaFactorMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ShearAreaFactorMethod", value)

    @property
    def speed_of_sound(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "SpeedOfSound")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @speed_of_sound.setter
    @enforce_parameter_types
    def speed_of_sound(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "SpeedOfSound", value)

    @property
    def spline_rigid_bond_detailed_connection_nodes_per_unit_length_to_diameter_ratio(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped,
            "SplineRigidBondDetailedConnectionNodesPerUnitLengthToDiameterRatio",
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @spline_rigid_bond_detailed_connection_nodes_per_unit_length_to_diameter_ratio.setter
    @enforce_parameter_types
    def spline_rigid_bond_detailed_connection_nodes_per_unit_length_to_diameter_ratio(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped,
            "SplineRigidBondDetailedConnectionNodesPerUnitLengthToDiameterRatio",
            value,
        )

    @property
    def stress_concentration_method_for_rating(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod":
        """EnumWithSelectedValue[mastapy.bearings.bearing_results.rolling.iso_rating_results.StressConcentrationMethod]"""
        temp = pythonnet_property_get(
            self.wrapped, "StressConcentrationMethodForRating"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @stress_concentration_method_for_rating.setter
    @enforce_parameter_types
    def stress_concentration_method_for_rating(
        self: "Self", value: "_2165.StressConcentrationMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped, "StressConcentrationMethodForRating", value
        )

    @property
    def tolerance_factor_for_axial_internal_clearances(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ToleranceFactorForAxialInternalClearances"
        )

        if temp is None:
            return 0.0

        return temp

    @tolerance_factor_for_axial_internal_clearances.setter
    @enforce_parameter_types
    def tolerance_factor_for_axial_internal_clearances(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ToleranceFactorForAxialInternalClearances",
            float(value) if value is not None else 0.0,
        )

    @property
    def tolerance_factor_for_inner_fit(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ToleranceFactorForInnerFit")

        if temp is None:
            return 0.0

        return temp

    @tolerance_factor_for_inner_fit.setter
    @enforce_parameter_types
    def tolerance_factor_for_inner_fit(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ToleranceFactorForInnerFit",
            float(value) if value is not None else 0.0,
        )

    @property
    def tolerance_factor_for_inner_mounting_sleeve_bore(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "ToleranceFactorForInnerMountingSleeveBore"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @tolerance_factor_for_inner_mounting_sleeve_bore.setter
    @enforce_parameter_types
    def tolerance_factor_for_inner_mounting_sleeve_bore(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "ToleranceFactorForInnerMountingSleeveBore", value
        )

    @property
    def tolerance_factor_for_inner_mounting_sleeve_outer_diameter(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "ToleranceFactorForInnerMountingSleeveOuterDiameter"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @tolerance_factor_for_inner_mounting_sleeve_outer_diameter.setter
    @enforce_parameter_types
    def tolerance_factor_for_inner_mounting_sleeve_outer_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "ToleranceFactorForInnerMountingSleeveOuterDiameter", value
        )

    @property
    def tolerance_factor_for_inner_ring(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ToleranceFactorForInnerRing")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @tolerance_factor_for_inner_ring.setter
    @enforce_parameter_types
    def tolerance_factor_for_inner_ring(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ToleranceFactorForInnerRing", value)

    @property
    def tolerance_factor_for_inner_support(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ToleranceFactorForInnerSupport")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @tolerance_factor_for_inner_support.setter
    @enforce_parameter_types
    def tolerance_factor_for_inner_support(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ToleranceFactorForInnerSupport", value)

    @property
    def tolerance_factor_for_outer_fit(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ToleranceFactorForOuterFit")

        if temp is None:
            return 0.0

        return temp

    @tolerance_factor_for_outer_fit.setter
    @enforce_parameter_types
    def tolerance_factor_for_outer_fit(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ToleranceFactorForOuterFit",
            float(value) if value is not None else 0.0,
        )

    @property
    def tolerance_factor_for_outer_mounting_sleeve_bore(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "ToleranceFactorForOuterMountingSleeveBore"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @tolerance_factor_for_outer_mounting_sleeve_bore.setter
    @enforce_parameter_types
    def tolerance_factor_for_outer_mounting_sleeve_bore(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "ToleranceFactorForOuterMountingSleeveBore", value
        )

    @property
    def tolerance_factor_for_outer_mounting_sleeve_outer_diameter(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "ToleranceFactorForOuterMountingSleeveOuterDiameter"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @tolerance_factor_for_outer_mounting_sleeve_outer_diameter.setter
    @enforce_parameter_types
    def tolerance_factor_for_outer_mounting_sleeve_outer_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "ToleranceFactorForOuterMountingSleeveOuterDiameter", value
        )

    @property
    def tolerance_factor_for_outer_ring(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ToleranceFactorForOuterRing")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @tolerance_factor_for_outer_ring.setter
    @enforce_parameter_types
    def tolerance_factor_for_outer_ring(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ToleranceFactorForOuterRing", value)

    @property
    def tolerance_factor_for_outer_support(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ToleranceFactorForOuterSupport")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @tolerance_factor_for_outer_support.setter
    @enforce_parameter_types
    def tolerance_factor_for_outer_support(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ToleranceFactorForOuterSupport", value)

    @property
    def tolerance_factor_for_radial_internal_clearances(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ToleranceFactorForRadialInternalClearances"
        )

        if temp is None:
            return 0.0

        return temp

    @tolerance_factor_for_radial_internal_clearances.setter
    @enforce_parameter_types
    def tolerance_factor_for_radial_internal_clearances(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ToleranceFactorForRadialInternalClearances",
            float(value) if value is not None else 0.0,
        )

    @property
    def use_default_temperatures(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseDefaultTemperatures")

        if temp is None:
            return False

        return temp

    @use_default_temperatures.setter
    @enforce_parameter_types
    def use_default_temperatures(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseDefaultTemperatures",
            bool(value) if value is not None else False,
        )

    @property
    def use_node_per_bearing_row_inner(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseNodePerBearingRowInner")

        if temp is None:
            return False

        return temp

    @use_node_per_bearing_row_inner.setter
    @enforce_parameter_types
    def use_node_per_bearing_row_inner(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseNodePerBearingRowInner",
            bool(value) if value is not None else False,
        )

    @property
    def use_node_per_bearing_row_outer(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseNodePerBearingRowOuter")

        if temp is None:
            return False

        return temp

    @use_node_per_bearing_row_outer.setter
    @enforce_parameter_types
    def use_node_per_bearing_row_outer(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseNodePerBearingRowOuter",
            bool(value) if value is not None else False,
        )

    @property
    def use_single_node_for_cylindrical_gear_meshes(
        self: "Self",
    ) -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(
            self.wrapped, "UseSingleNodeForCylindricalGearMeshes"
        )

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @use_single_node_for_cylindrical_gear_meshes.setter
    @enforce_parameter_types
    def use_single_node_for_cylindrical_gear_meshes(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "UseSingleNodeForCylindricalGearMeshes", value
        )

    @property
    def use_single_node_for_spline_rigid_bond_detailed_connection_connections(
        self: "Self",
    ) -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(
            self.wrapped, "UseSingleNodeForSplineRigidBondDetailedConnectionConnections"
        )

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @use_single_node_for_spline_rigid_bond_detailed_connection_connections.setter
    @enforce_parameter_types
    def use_single_node_for_spline_rigid_bond_detailed_connection_connections(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(
            self.wrapped,
            "UseSingleNodeForSplineRigidBondDetailedConnectionConnections",
            value,
        )

    @property
    def additional_acceleration(self: "Self") -> "_6963.AdditionalAccelerationOptions":
        """mastapy.system_model.analyses_and_results.static_loads.AdditionalAccelerationOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AdditionalAcceleration")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def input_power_load(self: "Self") -> "_7094.PowerLoadLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InputPowerLoad")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def output_power_load(self: "Self") -> "_7094.PowerLoadLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OutputPowerLoad")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def parametric_study_tool_options(
        self: "Self",
    ) -> "_4504.ParametricStudyToolOptions":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ParametricStudyToolOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ParametricStudyToolOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def temperatures(self: "Self") -> "_2281.TransmissionTemperatureSet":
        """mastapy.system_model.TransmissionTemperatureSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Temperatures")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def transmission_efficiency_settings(
        self: "Self",
    ) -> "_7133.TransmissionEfficiencySettings":
        """mastapy.system_model.analyses_and_results.static_loads.TransmissionEfficiencySettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransmissionEfficiencySettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def power_loads(self: "Self") -> "List[_7094.PowerLoadLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase]

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

    def delete(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Delete")

    @enforce_parameter_types
    def inputs_for_coupling_connection(
        self: "Self", design_entity: "_2403.CouplingConnection"
    ) -> "_7004.CouplingConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_COUPLING_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_spring_damper_connection(
        self: "Self", design_entity: "_2407.SpringDamperConnection"
    ) -> "_7111.SpringDamperConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_SPRING_DAMPER_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_torque_converter_connection(
        self: "Self", design_entity: "_2409.TorqueConverterConnection"
    ) -> "_7127.TorqueConverterConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_TORQUE_CONVERTER_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_abstract_shaft(
        self: "Self", design_entity: "_2493.AbstractShaft"
    ) -> "_6960.AbstractShaftLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.AbstractShaftLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaft)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_ABSTRACT_SHAFT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_microphone(
        self: "Self", design_entity: "_2522.Microphone"
    ) -> "_7078.MicrophoneLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.MicrophoneLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.Microphone)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_MICROPHONE],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_microphone_array(
        self: "Self", design_entity: "_2523.MicrophoneArray"
    ) -> "_7077.MicrophoneArrayLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.MicrophoneArrayLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.MicrophoneArray)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_MICROPHONE_ARRAY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_abstract_assembly(
        self: "Self", design_entity: "_2492.AbstractAssembly"
    ) -> "_6959.AbstractAssemblyLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_ABSTRACT_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_abstract_shaft_or_housing(
        self: "Self", design_entity: "_2494.AbstractShaftOrHousing"
    ) -> "_6961.AbstractShaftOrHousingLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_ABSTRACT_SHAFT_OR_HOUSING],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_bearing(
        self: "Self", design_entity: "_2497.Bearing"
    ) -> "_6972.BearingLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_BEARING],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_bolt(
        self: "Self", design_entity: "_2500.Bolt"
    ) -> "_6984.BoltLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_BOLT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_bolted_joint(
        self: "Self", design_entity: "_2501.BoltedJoint"
    ) -> "_6983.BoltedJointLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_BOLTED_JOINT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_component(
        self: "Self", design_entity: "_2502.Component"
    ) -> "_6990.ComponentLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_COMPONENT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_connector(
        self: "Self", design_entity: "_2505.Connector"
    ) -> "_7003.ConnectorLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.Connector)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_CONNECTOR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_datum(
        self: "Self", design_entity: "_2506.Datum"
    ) -> "_7022.DatumLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.Datum)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_DATUM],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_external_cad_model(
        self: "Self", design_entity: "_2510.ExternalCADModel"
    ) -> "_7036.ExternalCADModelLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_EXTERNAL_CAD_MODEL],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_fe_part(
        self: "Self", design_entity: "_2511.FEPart"
    ) -> "_7040.FEPartLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.FEPartLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.FEPart)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_FE_PART],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_flexible_pin_assembly(
        self: "Self", design_entity: "_2512.FlexiblePinAssembly"
    ) -> "_7041.FlexiblePinAssemblyLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_FLEXIBLE_PIN_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_assembly(
        self: "Self", design_entity: "_2491.Assembly"
    ) -> "_6971.AssemblyLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_guide_dxf_model(
        self: "Self", design_entity: "_2513.GuideDxfModel"
    ) -> "_7049.GuideDxfModelLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_GUIDE_DXF_MODEL],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_mass_disc(
        self: "Self", design_entity: "_2520.MassDisc"
    ) -> "_7074.MassDiscLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_MASS_DISC],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_measurement_component(
        self: "Self", design_entity: "_2521.MeasurementComponent"
    ) -> "_7075.MeasurementComponentLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_MEASUREMENT_COMPONENT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_mountable_component(
        self: "Self", design_entity: "_2524.MountableComponent"
    ) -> "_7079.MountableComponentLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_MOUNTABLE_COMPONENT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_oil_seal(
        self: "Self", design_entity: "_2526.OilSeal"
    ) -> "_7081.OilSealLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_OIL_SEAL],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_part(
        self: "Self", design_entity: "_2528.Part"
    ) -> "_7083.PartLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PartLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.Part)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_PART],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_planet_carrier(
        self: "Self", design_entity: "_2529.PlanetCarrier"
    ) -> "_7090.PlanetCarrierLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_PLANET_CARRIER],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_point_load(
        self: "Self", design_entity: "_2531.PointLoad"
    ) -> "_7093.PointLoadLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_POINT_LOAD],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_power_load(
        self: "Self", design_entity: "_2532.PowerLoad"
    ) -> "_7094.PowerLoadLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_POWER_LOAD],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_root_assembly(
        self: "Self", design_entity: "_2535.RootAssembly"
    ) -> "_7103.RootAssemblyLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_ROOT_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_specialised_assembly(
        self: "Self", design_entity: "_2537.SpecialisedAssembly"
    ) -> "_7107.SpecialisedAssemblyLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_SPECIALISED_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_unbalanced_mass(
        self: "Self", design_entity: "_2538.UnbalancedMass"
    ) -> "_7135.UnbalancedMassLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_UNBALANCED_MASS],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_virtual_component(
        self: "Self", design_entity: "_2540.VirtualComponent"
    ) -> "_7136.VirtualComponentLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_VIRTUAL_COMPONENT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_shaft(
        self: "Self", design_entity: "_2543.Shaft"
    ) -> "_7105.ShaftLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_SHAFT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_concept_gear(
        self: "Self", design_entity: "_2582.ConceptGear"
    ) -> "_6994.ConceptGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_CONCEPT_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_concept_gear_set(
        self: "Self", design_entity: "_2583.ConceptGearSet"
    ) -> "_6996.ConceptGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_CONCEPT_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_face_gear(
        self: "Self", design_entity: "_2589.FaceGear"
    ) -> "_7037.FaceGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_FACE_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_face_gear_set(
        self: "Self", design_entity: "_2590.FaceGearSet"
    ) -> "_7039.FaceGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_FACE_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_agma_gleason_conical_gear(
        self: "Self", design_entity: "_2574.AGMAGleasonConicalGear"
    ) -> "_6966.AGMAGleasonConicalGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_AGMA_GLEASON_CONICAL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_agma_gleason_conical_gear_set(
        self: "Self", design_entity: "_2575.AGMAGleasonConicalGearSet"
    ) -> "_6968.AGMAGleasonConicalGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_AGMA_GLEASON_CONICAL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_bevel_differential_gear(
        self: "Self", design_entity: "_2576.BevelDifferentialGear"
    ) -> "_6975.BevelDifferentialGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_BEVEL_DIFFERENTIAL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_bevel_differential_gear_set(
        self: "Self", design_entity: "_2577.BevelDifferentialGearSet"
    ) -> "_6977.BevelDifferentialGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_BEVEL_DIFFERENTIAL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_bevel_differential_planet_gear(
        self: "Self", design_entity: "_2578.BevelDifferentialPlanetGear"
    ) -> "_6978.BevelDifferentialPlanetGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_BEVEL_DIFFERENTIAL_PLANET_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_bevel_differential_sun_gear(
        self: "Self", design_entity: "_2579.BevelDifferentialSunGear"
    ) -> "_6979.BevelDifferentialSunGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_BEVEL_DIFFERENTIAL_SUN_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_bevel_gear(
        self: "Self", design_entity: "_2580.BevelGear"
    ) -> "_6980.BevelGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_BEVEL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_bevel_gear_set(
        self: "Self", design_entity: "_2581.BevelGearSet"
    ) -> "_6982.BevelGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_BEVEL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_conical_gear(
        self: "Self", design_entity: "_2584.ConicalGear"
    ) -> "_6997.ConicalGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_CONICAL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_conical_gear_set(
        self: "Self", design_entity: "_2585.ConicalGearSet"
    ) -> "_7001.ConicalGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_CONICAL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_cylindrical_gear(
        self: "Self", design_entity: "_2586.CylindricalGear"
    ) -> "_7014.CylindricalGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_CYLINDRICAL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_cylindrical_gear_set(
        self: "Self", design_entity: "_2587.CylindricalGearSet"
    ) -> "_7018.CylindricalGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_CYLINDRICAL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_cylindrical_planet_gear(
        self: "Self", design_entity: "_2588.CylindricalPlanetGear"
    ) -> "_7019.CylindricalPlanetGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_CYLINDRICAL_PLANET_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_gear(
        self: "Self", design_entity: "_2591.Gear"
    ) -> "_7043.GearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.GearLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_gear_set(
        self: "Self", design_entity: "_2593.GearSet"
    ) -> "_7048.GearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_hypoid_gear(
        self: "Self", design_entity: "_2595.HypoidGear"
    ) -> "_7058.HypoidGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_HYPOID_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_hypoid_gear_set(
        self: "Self", design_entity: "_2596.HypoidGearSet"
    ) -> "_7060.HypoidGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_HYPOID_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_klingelnberg_cyclo_palloid_conical_gear(
        self: "Self", design_entity: "_2597.KlingelnbergCycloPalloidConicalGear"
    ) -> "_7065.KlingelnbergCycloPalloidConicalGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_klingelnberg_cyclo_palloid_conical_gear_set(
        self: "Self", design_entity: "_2598.KlingelnbergCycloPalloidConicalGearSet"
    ) -> "_7067.KlingelnbergCycloPalloidConicalGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_klingelnberg_cyclo_palloid_hypoid_gear(
        self: "Self", design_entity: "_2599.KlingelnbergCycloPalloidHypoidGear"
    ) -> "_7068.KlingelnbergCycloPalloidHypoidGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "Self", design_entity: "_2600.KlingelnbergCycloPalloidHypoidGearSet"
    ) -> "_7070.KlingelnbergCycloPalloidHypoidGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "Self", design_entity: "_2601.KlingelnbergCycloPalloidSpiralBevelGear"
    ) -> "_7071.KlingelnbergCycloPalloidSpiralBevelGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
        self: "Self", design_entity: "_2602.KlingelnbergCycloPalloidSpiralBevelGearSet"
    ) -> "_7073.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_planetary_gear_set(
        self: "Self", design_entity: "_2603.PlanetaryGearSet"
    ) -> "_7088.PlanetaryGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_PLANETARY_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_spiral_bevel_gear(
        self: "Self", design_entity: "_2604.SpiralBevelGear"
    ) -> "_7108.SpiralBevelGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_SPIRAL_BEVEL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_spiral_bevel_gear_set(
        self: "Self", design_entity: "_2605.SpiralBevelGearSet"
    ) -> "_7110.SpiralBevelGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_SPIRAL_BEVEL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_straight_bevel_diff_gear(
        self: "Self", design_entity: "_2606.StraightBevelDiffGear"
    ) -> "_7114.StraightBevelDiffGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_STRAIGHT_BEVEL_DIFF_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_straight_bevel_diff_gear_set(
        self: "Self", design_entity: "_2607.StraightBevelDiffGearSet"
    ) -> "_7116.StraightBevelDiffGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_STRAIGHT_BEVEL_DIFF_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_straight_bevel_gear(
        self: "Self", design_entity: "_2608.StraightBevelGear"
    ) -> "_7117.StraightBevelGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_STRAIGHT_BEVEL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_straight_bevel_gear_set(
        self: "Self", design_entity: "_2609.StraightBevelGearSet"
    ) -> "_7119.StraightBevelGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_STRAIGHT_BEVEL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_straight_bevel_planet_gear(
        self: "Self", design_entity: "_2610.StraightBevelPlanetGear"
    ) -> "_7120.StraightBevelPlanetGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_STRAIGHT_BEVEL_PLANET_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_straight_bevel_sun_gear(
        self: "Self", design_entity: "_2611.StraightBevelSunGear"
    ) -> "_7121.StraightBevelSunGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_STRAIGHT_BEVEL_SUN_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_worm_gear(
        self: "Self", design_entity: "_2612.WormGear"
    ) -> "_7137.WormGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_WORM_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_worm_gear_set(
        self: "Self", design_entity: "_2613.WormGearSet"
    ) -> "_7139.WormGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_WORM_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_zerol_bevel_gear(
        self: "Self", design_entity: "_2614.ZerolBevelGear"
    ) -> "_7140.ZerolBevelGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_ZEROL_BEVEL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_zerol_bevel_gear_set(
        self: "Self", design_entity: "_2615.ZerolBevelGearSet"
    ) -> "_7142.ZerolBevelGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_ZEROL_BEVEL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_cycloidal_assembly(
        self: "Self", design_entity: "_2629.CycloidalAssembly"
    ) -> "_7010.CycloidalAssemblyLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CycloidalAssemblyLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.CycloidalAssembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_CYCLOIDAL_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_cycloidal_disc(
        self: "Self", design_entity: "_2630.CycloidalDisc"
    ) -> "_7012.CycloidalDiscLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.CycloidalDisc)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_CYCLOIDAL_DISC],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_ring_pins(
        self: "Self", design_entity: "_2631.RingPins"
    ) -> "_7098.RingPinsLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.RingPinsLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.RingPins)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_RING_PINS],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_part_to_part_shear_coupling(
        self: "Self", design_entity: "_2651.PartToPartShearCoupling"
    ) -> "_7086.PartToPartShearCouplingLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_PART_TO_PART_SHEAR_COUPLING],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_part_to_part_shear_coupling_half(
        self: "Self", design_entity: "_2652.PartToPartShearCouplingHalf"
    ) -> "_7085.PartToPartShearCouplingHalfLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingHalfLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_PART_TO_PART_SHEAR_COUPLING_HALF],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_belt_drive(
        self: "Self", design_entity: "_2638.BeltDrive"
    ) -> "_6974.BeltDriveLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_BELT_DRIVE],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_clutch(
        self: "Self", design_entity: "_2640.Clutch"
    ) -> "_6987.ClutchLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_CLUTCH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_clutch_half(
        self: "Self", design_entity: "_2641.ClutchHalf"
    ) -> "_6986.ClutchHalfLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_CLUTCH_HALF],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_concept_coupling(
        self: "Self", design_entity: "_2643.ConceptCoupling"
    ) -> "_6993.ConceptCouplingLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_CONCEPT_COUPLING],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_concept_coupling_half(
        self: "Self", design_entity: "_2644.ConceptCouplingHalf"
    ) -> "_6992.ConceptCouplingHalfLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_CONCEPT_COUPLING_HALF],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_coupling(
        self: "Self", design_entity: "_2646.Coupling"
    ) -> "_7006.CouplingLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_COUPLING],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_coupling_half(
        self: "Self", design_entity: "_2647.CouplingHalf"
    ) -> "_7005.CouplingHalfLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_COUPLING_HALF],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_cvt(self: "Self", design_entity: "_2649.CVT") -> "_7008.CVTLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_CVT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_cvt_pulley(
        self: "Self", design_entity: "_2650.CVTPulley"
    ) -> "_7009.CVTPulleyLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_CVT_PULLEY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_pulley(
        self: "Self", design_entity: "_2654.Pulley"
    ) -> "_7095.PulleyLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_PULLEY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_shaft_hub_connection(
        self: "Self", design_entity: "_2662.ShaftHubConnection"
    ) -> "_7104.ShaftHubConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_SHAFT_HUB_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_rolling_ring(
        self: "Self", design_entity: "_2660.RollingRing"
    ) -> "_7102.RollingRingLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_ROLLING_RING],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_rolling_ring_assembly(
        self: "Self", design_entity: "_2661.RollingRingAssembly"
    ) -> "_7100.RollingRingAssemblyLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_ROLLING_RING_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_spring_damper(
        self: "Self", design_entity: "_2667.SpringDamper"
    ) -> "_7113.SpringDamperLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_SPRING_DAMPER],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_spring_damper_half(
        self: "Self", design_entity: "_2668.SpringDamperHalf"
    ) -> "_7112.SpringDamperHalfLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_SPRING_DAMPER_HALF],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_synchroniser(
        self: "Self", design_entity: "_2669.Synchroniser"
    ) -> "_7123.SynchroniserLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_SYNCHRONISER],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_synchroniser_half(
        self: "Self", design_entity: "_2671.SynchroniserHalf"
    ) -> "_7122.SynchroniserHalfLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_SYNCHRONISER_HALF],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_synchroniser_part(
        self: "Self", design_entity: "_2672.SynchroniserPart"
    ) -> "_7124.SynchroniserPartLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_SYNCHRONISER_PART],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_synchroniser_sleeve(
        self: "Self", design_entity: "_2673.SynchroniserSleeve"
    ) -> "_7125.SynchroniserSleeveLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_SYNCHRONISER_SLEEVE],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_torque_converter(
        self: "Self", design_entity: "_2674.TorqueConverter"
    ) -> "_7128.TorqueConverterLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_TORQUE_CONVERTER],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_torque_converter_pump(
        self: "Self", design_entity: "_2675.TorqueConverterPump"
    ) -> "_7129.TorqueConverterPumpLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_TORQUE_CONVERTER_PUMP],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_torque_converter_turbine(
        self: "Self", design_entity: "_2677.TorqueConverterTurbine"
    ) -> "_7130.TorqueConverterTurbineLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_TORQUE_CONVERTER_TURBINE],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_shaft_to_mountable_component_connection(
        self: "Self", design_entity: "_2352.ShaftToMountableComponentConnection"
    ) -> "_7106.ShaftToMountableComponentConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_cvt_belt_connection(
        self: "Self", design_entity: "_2330.CVTBeltConnection"
    ) -> "_7007.CVTBeltConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_CVT_BELT_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_belt_connection(
        self: "Self", design_entity: "_2325.BeltConnection"
    ) -> "_6973.BeltConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_BELT_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_coaxial_connection(
        self: "Self", design_entity: "_2326.CoaxialConnection"
    ) -> "_6989.CoaxialConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_COAXIAL_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_connection(
        self: "Self", design_entity: "_2329.Connection"
    ) -> "_7002.ConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_inter_mountable_component_connection(
        self: "Self", design_entity: "_2338.InterMountableComponentConnection"
    ) -> "_7064.InterMountableComponentConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_INTER_MOUNTABLE_COMPONENT_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_planetary_connection(
        self: "Self", design_entity: "_2344.PlanetaryConnection"
    ) -> "_7087.PlanetaryConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_PLANETARY_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_rolling_ring_connection(
        self: "Self", design_entity: "_2349.RollingRingConnection"
    ) -> "_7101.RollingRingConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_ROLLING_RING_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_abstract_shaft_to_mountable_component_connection(
        self: "Self", design_entity: "_2322.AbstractShaftToMountableComponentConnection"
    ) -> "_6962.AbstractShaftToMountableComponentConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.AbstractShaftToMountableComponentConnectionLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.AbstractShaftToMountableComponentConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_bevel_differential_gear_mesh(
        self: "Self", design_entity: "_2358.BevelDifferentialGearMesh"
    ) -> "_6976.BevelDifferentialGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_BEVEL_DIFFERENTIAL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_concept_gear_mesh(
        self: "Self", design_entity: "_2362.ConceptGearMesh"
    ) -> "_6995.ConceptGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_CONCEPT_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_face_gear_mesh(
        self: "Self", design_entity: "_2368.FaceGearMesh"
    ) -> "_7038.FaceGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_FACE_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_straight_bevel_diff_gear_mesh(
        self: "Self", design_entity: "_2382.StraightBevelDiffGearMesh"
    ) -> "_7115.StraightBevelDiffGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_STRAIGHT_BEVEL_DIFF_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_bevel_gear_mesh(
        self: "Self", design_entity: "_2360.BevelGearMesh"
    ) -> "_6981.BevelGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_BEVEL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_conical_gear_mesh(
        self: "Self", design_entity: "_2364.ConicalGearMesh"
    ) -> "_6999.ConicalGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_CONICAL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_agma_gleason_conical_gear_mesh(
        self: "Self", design_entity: "_2356.AGMAGleasonConicalGearMesh"
    ) -> "_6967.AGMAGleasonConicalGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_AGMA_GLEASON_CONICAL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_cylindrical_gear_mesh(
        self: "Self", design_entity: "_2366.CylindricalGearMesh"
    ) -> "_7016.CylindricalGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_CYLINDRICAL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_hypoid_gear_mesh(
        self: "Self", design_entity: "_2372.HypoidGearMesh"
    ) -> "_7059.HypoidGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_HYPOID_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_klingelnberg_cyclo_palloid_conical_gear_mesh(
        self: "Self", design_entity: "_2375.KlingelnbergCycloPalloidConicalGearMesh"
    ) -> "_7066.KlingelnbergCycloPalloidConicalGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(
        self: "Self", design_entity: "_2376.KlingelnbergCycloPalloidHypoidGearMesh"
    ) -> "_7069.KlingelnbergCycloPalloidHypoidGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(
        self: "Self", design_entity: "_2377.KlingelnbergCycloPalloidSpiralBevelGearMesh"
    ) -> "_7072.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_spiral_bevel_gear_mesh(
        self: "Self", design_entity: "_2380.SpiralBevelGearMesh"
    ) -> "_7109.SpiralBevelGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_SPIRAL_BEVEL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_straight_bevel_gear_mesh(
        self: "Self", design_entity: "_2384.StraightBevelGearMesh"
    ) -> "_7118.StraightBevelGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_STRAIGHT_BEVEL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_worm_gear_mesh(
        self: "Self", design_entity: "_2386.WormGearMesh"
    ) -> "_7138.WormGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_WORM_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_zerol_bevel_gear_mesh(
        self: "Self", design_entity: "_2388.ZerolBevelGearMesh"
    ) -> "_7141.ZerolBevelGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_ZEROL_BEVEL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_gear_mesh(
        self: "Self", design_entity: "_2370.GearMesh"
    ) -> "_7045.GearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_cycloidal_disc_central_bearing_connection(
        self: "Self", design_entity: "_2392.CycloidalDiscCentralBearingConnection"
    ) -> "_7011.CycloidalDiscCentralBearingConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscCentralBearingConnectionLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscCentralBearingConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_cycloidal_disc_planetary_bearing_connection(
        self: "Self", design_entity: "_2395.CycloidalDiscPlanetaryBearingConnection"
    ) -> "_7013.CycloidalDiscPlanetaryBearingConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscPlanetaryBearingConnectionLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscPlanetaryBearingConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_ring_pins_to_disc_connection(
        self: "Self", design_entity: "_2398.RingPinsToDiscConnection"
    ) -> "_7099.RingPinsToDiscConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.RingPinsToDiscConnectionLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.RingPinsToDiscConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_RING_PINS_TO_DISC_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_part_to_part_shear_coupling_connection(
        self: "Self", design_entity: "_2405.PartToPartShearCouplingConnection"
    ) -> "_7084.PartToPartShearCouplingConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingConnectionLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_PART_TO_PART_SHEAR_COUPLING_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_clutch_connection(
        self: "Self", design_entity: "_2399.ClutchConnection"
    ) -> "_6985.ClutchConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_CLUTCH_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def inputs_for_concept_coupling_connection(
        self: "Self", design_entity: "_2401.ConceptCouplingConnection"
    ) -> "_6991.ConceptCouplingConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "InputsFor",
            [_CONCEPT_COUPLING_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_LoadCase":
        """Cast to another type.

        Returns:
            _Cast_LoadCase
        """
        return _Cast_LoadCase(self)
