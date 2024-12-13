"""DesignEntity"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_DESIGN_ENTITY = python_net_import("SMT.MastaAPI.SystemModel", "DesignEntity")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model import _2257
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
    from mastapy._private.utility.model_validation import _1846, _1847
    from mastapy._private.utility.scripting import _1794

    Self = TypeVar("Self", bound="DesignEntity")
    CastSelf = TypeVar("CastSelf", bound="DesignEntity._Cast_DesignEntity")


__docformat__ = "restructuredtext en"
__all__ = ("DesignEntity",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DesignEntity:
    """Special nested class for casting DesignEntity to subclasses."""

    __parent__: "DesignEntity"

    @property
    def abstract_shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2322.AbstractShaftToMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2322

        return self.__parent__._cast(_2322.AbstractShaftToMountableComponentConnection)

    @property
    def belt_connection(self: "CastSelf") -> "_2325.BeltConnection":
        from mastapy._private.system_model.connections_and_sockets import _2325

        return self.__parent__._cast(_2325.BeltConnection)

    @property
    def coaxial_connection(self: "CastSelf") -> "_2326.CoaxialConnection":
        from mastapy._private.system_model.connections_and_sockets import _2326

        return self.__parent__._cast(_2326.CoaxialConnection)

    @property
    def connection(self: "CastSelf") -> "_2329.Connection":
        from mastapy._private.system_model.connections_and_sockets import _2329

        return self.__parent__._cast(_2329.Connection)

    @property
    def cvt_belt_connection(self: "CastSelf") -> "_2330.CVTBeltConnection":
        from mastapy._private.system_model.connections_and_sockets import _2330

        return self.__parent__._cast(_2330.CVTBeltConnection)

    @property
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2338.InterMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2338

        return self.__parent__._cast(_2338.InterMountableComponentConnection)

    @property
    def planetary_connection(self: "CastSelf") -> "_2344.PlanetaryConnection":
        from mastapy._private.system_model.connections_and_sockets import _2344

        return self.__parent__._cast(_2344.PlanetaryConnection)

    @property
    def rolling_ring_connection(self: "CastSelf") -> "_2349.RollingRingConnection":
        from mastapy._private.system_model.connections_and_sockets import _2349

        return self.__parent__._cast(_2349.RollingRingConnection)

    @property
    def shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2352.ShaftToMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2352

        return self.__parent__._cast(_2352.ShaftToMountableComponentConnection)

    @property
    def agma_gleason_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2356.AGMAGleasonConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2356

        return self.__parent__._cast(_2356.AGMAGleasonConicalGearMesh)

    @property
    def bevel_differential_gear_mesh(
        self: "CastSelf",
    ) -> "_2358.BevelDifferentialGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2358

        return self.__parent__._cast(_2358.BevelDifferentialGearMesh)

    @property
    def bevel_gear_mesh(self: "CastSelf") -> "_2360.BevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2360

        return self.__parent__._cast(_2360.BevelGearMesh)

    @property
    def concept_gear_mesh(self: "CastSelf") -> "_2362.ConceptGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2362

        return self.__parent__._cast(_2362.ConceptGearMesh)

    @property
    def conical_gear_mesh(self: "CastSelf") -> "_2364.ConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2364

        return self.__parent__._cast(_2364.ConicalGearMesh)

    @property
    def cylindrical_gear_mesh(self: "CastSelf") -> "_2366.CylindricalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2366

        return self.__parent__._cast(_2366.CylindricalGearMesh)

    @property
    def face_gear_mesh(self: "CastSelf") -> "_2368.FaceGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2368

        return self.__parent__._cast(_2368.FaceGearMesh)

    @property
    def gear_mesh(self: "CastSelf") -> "_2370.GearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2370

        return self.__parent__._cast(_2370.GearMesh)

    @property
    def hypoid_gear_mesh(self: "CastSelf") -> "_2372.HypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2372

        return self.__parent__._cast(_2372.HypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2375.KlingelnbergCycloPalloidConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2375

        return self.__parent__._cast(_2375.KlingelnbergCycloPalloidConicalGearMesh)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh(
        self: "CastSelf",
    ) -> "_2376.KlingelnbergCycloPalloidHypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2376

        return self.__parent__._cast(_2376.KlingelnbergCycloPalloidHypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(
        self: "CastSelf",
    ) -> "_2377.KlingelnbergCycloPalloidSpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2377

        return self.__parent__._cast(_2377.KlingelnbergCycloPalloidSpiralBevelGearMesh)

    @property
    def spiral_bevel_gear_mesh(self: "CastSelf") -> "_2380.SpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2380

        return self.__parent__._cast(_2380.SpiralBevelGearMesh)

    @property
    def straight_bevel_diff_gear_mesh(
        self: "CastSelf",
    ) -> "_2382.StraightBevelDiffGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2382

        return self.__parent__._cast(_2382.StraightBevelDiffGearMesh)

    @property
    def straight_bevel_gear_mesh(self: "CastSelf") -> "_2384.StraightBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2384

        return self.__parent__._cast(_2384.StraightBevelGearMesh)

    @property
    def worm_gear_mesh(self: "CastSelf") -> "_2386.WormGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2386

        return self.__parent__._cast(_2386.WormGearMesh)

    @property
    def zerol_bevel_gear_mesh(self: "CastSelf") -> "_2388.ZerolBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2388

        return self.__parent__._cast(_2388.ZerolBevelGearMesh)

    @property
    def cycloidal_disc_central_bearing_connection(
        self: "CastSelf",
    ) -> "_2392.CycloidalDiscCentralBearingConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2392,
        )

        return self.__parent__._cast(_2392.CycloidalDiscCentralBearingConnection)

    @property
    def cycloidal_disc_planetary_bearing_connection(
        self: "CastSelf",
    ) -> "_2395.CycloidalDiscPlanetaryBearingConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2395,
        )

        return self.__parent__._cast(_2395.CycloidalDiscPlanetaryBearingConnection)

    @property
    def ring_pins_to_disc_connection(
        self: "CastSelf",
    ) -> "_2398.RingPinsToDiscConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2398,
        )

        return self.__parent__._cast(_2398.RingPinsToDiscConnection)

    @property
    def clutch_connection(self: "CastSelf") -> "_2399.ClutchConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2399,
        )

        return self.__parent__._cast(_2399.ClutchConnection)

    @property
    def concept_coupling_connection(
        self: "CastSelf",
    ) -> "_2401.ConceptCouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2401,
        )

        return self.__parent__._cast(_2401.ConceptCouplingConnection)

    @property
    def coupling_connection(self: "CastSelf") -> "_2403.CouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2403,
        )

        return self.__parent__._cast(_2403.CouplingConnection)

    @property
    def part_to_part_shear_coupling_connection(
        self: "CastSelf",
    ) -> "_2405.PartToPartShearCouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2405,
        )

        return self.__parent__._cast(_2405.PartToPartShearCouplingConnection)

    @property
    def spring_damper_connection(self: "CastSelf") -> "_2407.SpringDamperConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2407,
        )

        return self.__parent__._cast(_2407.SpringDamperConnection)

    @property
    def torque_converter_connection(
        self: "CastSelf",
    ) -> "_2409.TorqueConverterConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2409,
        )

        return self.__parent__._cast(_2409.TorqueConverterConnection)

    @property
    def assembly(self: "CastSelf") -> "_2491.Assembly":
        from mastapy._private.system_model.part_model import _2491

        return self.__parent__._cast(_2491.Assembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2492.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2492

        return self.__parent__._cast(_2492.AbstractAssembly)

    @property
    def abstract_shaft(self: "CastSelf") -> "_2493.AbstractShaft":
        from mastapy._private.system_model.part_model import _2493

        return self.__parent__._cast(_2493.AbstractShaft)

    @property
    def abstract_shaft_or_housing(self: "CastSelf") -> "_2494.AbstractShaftOrHousing":
        from mastapy._private.system_model.part_model import _2494

        return self.__parent__._cast(_2494.AbstractShaftOrHousing)

    @property
    def bearing(self: "CastSelf") -> "_2497.Bearing":
        from mastapy._private.system_model.part_model import _2497

        return self.__parent__._cast(_2497.Bearing)

    @property
    def bolt(self: "CastSelf") -> "_2500.Bolt":
        from mastapy._private.system_model.part_model import _2500

        return self.__parent__._cast(_2500.Bolt)

    @property
    def bolted_joint(self: "CastSelf") -> "_2501.BoltedJoint":
        from mastapy._private.system_model.part_model import _2501

        return self.__parent__._cast(_2501.BoltedJoint)

    @property
    def component(self: "CastSelf") -> "_2502.Component":
        from mastapy._private.system_model.part_model import _2502

        return self.__parent__._cast(_2502.Component)

    @property
    def connector(self: "CastSelf") -> "_2505.Connector":
        from mastapy._private.system_model.part_model import _2505

        return self.__parent__._cast(_2505.Connector)

    @property
    def datum(self: "CastSelf") -> "_2506.Datum":
        from mastapy._private.system_model.part_model import _2506

        return self.__parent__._cast(_2506.Datum)

    @property
    def external_cad_model(self: "CastSelf") -> "_2510.ExternalCADModel":
        from mastapy._private.system_model.part_model import _2510

        return self.__parent__._cast(_2510.ExternalCADModel)

    @property
    def fe_part(self: "CastSelf") -> "_2511.FEPart":
        from mastapy._private.system_model.part_model import _2511

        return self.__parent__._cast(_2511.FEPart)

    @property
    def flexible_pin_assembly(self: "CastSelf") -> "_2512.FlexiblePinAssembly":
        from mastapy._private.system_model.part_model import _2512

        return self.__parent__._cast(_2512.FlexiblePinAssembly)

    @property
    def guide_dxf_model(self: "CastSelf") -> "_2513.GuideDxfModel":
        from mastapy._private.system_model.part_model import _2513

        return self.__parent__._cast(_2513.GuideDxfModel)

    @property
    def mass_disc(self: "CastSelf") -> "_2520.MassDisc":
        from mastapy._private.system_model.part_model import _2520

        return self.__parent__._cast(_2520.MassDisc)

    @property
    def measurement_component(self: "CastSelf") -> "_2521.MeasurementComponent":
        from mastapy._private.system_model.part_model import _2521

        return self.__parent__._cast(_2521.MeasurementComponent)

    @property
    def microphone(self: "CastSelf") -> "_2522.Microphone":
        from mastapy._private.system_model.part_model import _2522

        return self.__parent__._cast(_2522.Microphone)

    @property
    def microphone_array(self: "CastSelf") -> "_2523.MicrophoneArray":
        from mastapy._private.system_model.part_model import _2523

        return self.__parent__._cast(_2523.MicrophoneArray)

    @property
    def mountable_component(self: "CastSelf") -> "_2524.MountableComponent":
        from mastapy._private.system_model.part_model import _2524

        return self.__parent__._cast(_2524.MountableComponent)

    @property
    def oil_seal(self: "CastSelf") -> "_2526.OilSeal":
        from mastapy._private.system_model.part_model import _2526

        return self.__parent__._cast(_2526.OilSeal)

    @property
    def part(self: "CastSelf") -> "_2528.Part":
        from mastapy._private.system_model.part_model import _2528

        return self.__parent__._cast(_2528.Part)

    @property
    def planet_carrier(self: "CastSelf") -> "_2529.PlanetCarrier":
        from mastapy._private.system_model.part_model import _2529

        return self.__parent__._cast(_2529.PlanetCarrier)

    @property
    def point_load(self: "CastSelf") -> "_2531.PointLoad":
        from mastapy._private.system_model.part_model import _2531

        return self.__parent__._cast(_2531.PointLoad)

    @property
    def power_load(self: "CastSelf") -> "_2532.PowerLoad":
        from mastapy._private.system_model.part_model import _2532

        return self.__parent__._cast(_2532.PowerLoad)

    @property
    def root_assembly(self: "CastSelf") -> "_2535.RootAssembly":
        from mastapy._private.system_model.part_model import _2535

        return self.__parent__._cast(_2535.RootAssembly)

    @property
    def specialised_assembly(self: "CastSelf") -> "_2537.SpecialisedAssembly":
        from mastapy._private.system_model.part_model import _2537

        return self.__parent__._cast(_2537.SpecialisedAssembly)

    @property
    def unbalanced_mass(self: "CastSelf") -> "_2538.UnbalancedMass":
        from mastapy._private.system_model.part_model import _2538

        return self.__parent__._cast(_2538.UnbalancedMass)

    @property
    def virtual_component(self: "CastSelf") -> "_2540.VirtualComponent":
        from mastapy._private.system_model.part_model import _2540

        return self.__parent__._cast(_2540.VirtualComponent)

    @property
    def shaft(self: "CastSelf") -> "_2543.Shaft":
        from mastapy._private.system_model.part_model.shaft_model import _2543

        return self.__parent__._cast(_2543.Shaft)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2574.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2574

        return self.__parent__._cast(_2574.AGMAGleasonConicalGear)

    @property
    def agma_gleason_conical_gear_set(
        self: "CastSelf",
    ) -> "_2575.AGMAGleasonConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2575

        return self.__parent__._cast(_2575.AGMAGleasonConicalGearSet)

    @property
    def bevel_differential_gear(self: "CastSelf") -> "_2576.BevelDifferentialGear":
        from mastapy._private.system_model.part_model.gears import _2576

        return self.__parent__._cast(_2576.BevelDifferentialGear)

    @property
    def bevel_differential_gear_set(
        self: "CastSelf",
    ) -> "_2577.BevelDifferentialGearSet":
        from mastapy._private.system_model.part_model.gears import _2577

        return self.__parent__._cast(_2577.BevelDifferentialGearSet)

    @property
    def bevel_differential_planet_gear(
        self: "CastSelf",
    ) -> "_2578.BevelDifferentialPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2578

        return self.__parent__._cast(_2578.BevelDifferentialPlanetGear)

    @property
    def bevel_differential_sun_gear(
        self: "CastSelf",
    ) -> "_2579.BevelDifferentialSunGear":
        from mastapy._private.system_model.part_model.gears import _2579

        return self.__parent__._cast(_2579.BevelDifferentialSunGear)

    @property
    def bevel_gear(self: "CastSelf") -> "_2580.BevelGear":
        from mastapy._private.system_model.part_model.gears import _2580

        return self.__parent__._cast(_2580.BevelGear)

    @property
    def bevel_gear_set(self: "CastSelf") -> "_2581.BevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2581

        return self.__parent__._cast(_2581.BevelGearSet)

    @property
    def concept_gear(self: "CastSelf") -> "_2582.ConceptGear":
        from mastapy._private.system_model.part_model.gears import _2582

        return self.__parent__._cast(_2582.ConceptGear)

    @property
    def concept_gear_set(self: "CastSelf") -> "_2583.ConceptGearSet":
        from mastapy._private.system_model.part_model.gears import _2583

        return self.__parent__._cast(_2583.ConceptGearSet)

    @property
    def conical_gear(self: "CastSelf") -> "_2584.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2584

        return self.__parent__._cast(_2584.ConicalGear)

    @property
    def conical_gear_set(self: "CastSelf") -> "_2585.ConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2585

        return self.__parent__._cast(_2585.ConicalGearSet)

    @property
    def cylindrical_gear(self: "CastSelf") -> "_2586.CylindricalGear":
        from mastapy._private.system_model.part_model.gears import _2586

        return self.__parent__._cast(_2586.CylindricalGear)

    @property
    def cylindrical_gear_set(self: "CastSelf") -> "_2587.CylindricalGearSet":
        from mastapy._private.system_model.part_model.gears import _2587

        return self.__parent__._cast(_2587.CylindricalGearSet)

    @property
    def cylindrical_planet_gear(self: "CastSelf") -> "_2588.CylindricalPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2588

        return self.__parent__._cast(_2588.CylindricalPlanetGear)

    @property
    def face_gear(self: "CastSelf") -> "_2589.FaceGear":
        from mastapy._private.system_model.part_model.gears import _2589

        return self.__parent__._cast(_2589.FaceGear)

    @property
    def face_gear_set(self: "CastSelf") -> "_2590.FaceGearSet":
        from mastapy._private.system_model.part_model.gears import _2590

        return self.__parent__._cast(_2590.FaceGearSet)

    @property
    def gear(self: "CastSelf") -> "_2591.Gear":
        from mastapy._private.system_model.part_model.gears import _2591

        return self.__parent__._cast(_2591.Gear)

    @property
    def gear_set(self: "CastSelf") -> "_2593.GearSet":
        from mastapy._private.system_model.part_model.gears import _2593

        return self.__parent__._cast(_2593.GearSet)

    @property
    def hypoid_gear(self: "CastSelf") -> "_2595.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2595

        return self.__parent__._cast(_2595.HypoidGear)

    @property
    def hypoid_gear_set(self: "CastSelf") -> "_2596.HypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2596

        return self.__parent__._cast(_2596.HypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_conical_gear(
        self: "CastSelf",
    ) -> "_2597.KlingelnbergCycloPalloidConicalGear":
        from mastapy._private.system_model.part_model.gears import _2597

        return self.__parent__._cast(_2597.KlingelnbergCycloPalloidConicalGear)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set(
        self: "CastSelf",
    ) -> "_2598.KlingelnbergCycloPalloidConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2598

        return self.__parent__._cast(_2598.KlingelnbergCycloPalloidConicalGearSet)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear(
        self: "CastSelf",
    ) -> "_2599.KlingelnbergCycloPalloidHypoidGear":
        from mastapy._private.system_model.part_model.gears import _2599

        return self.__parent__._cast(_2599.KlingelnbergCycloPalloidHypoidGear)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "CastSelf",
    ) -> "_2600.KlingelnbergCycloPalloidHypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2600

        return self.__parent__._cast(_2600.KlingelnbergCycloPalloidHypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "CastSelf",
    ) -> "_2601.KlingelnbergCycloPalloidSpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2601

        return self.__parent__._cast(_2601.KlingelnbergCycloPalloidSpiralBevelGear)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
        self: "CastSelf",
    ) -> "_2602.KlingelnbergCycloPalloidSpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2602

        return self.__parent__._cast(_2602.KlingelnbergCycloPalloidSpiralBevelGearSet)

    @property
    def planetary_gear_set(self: "CastSelf") -> "_2603.PlanetaryGearSet":
        from mastapy._private.system_model.part_model.gears import _2603

        return self.__parent__._cast(_2603.PlanetaryGearSet)

    @property
    def spiral_bevel_gear(self: "CastSelf") -> "_2604.SpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2604

        return self.__parent__._cast(_2604.SpiralBevelGear)

    @property
    def spiral_bevel_gear_set(self: "CastSelf") -> "_2605.SpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2605

        return self.__parent__._cast(_2605.SpiralBevelGearSet)

    @property
    def straight_bevel_diff_gear(self: "CastSelf") -> "_2606.StraightBevelDiffGear":
        from mastapy._private.system_model.part_model.gears import _2606

        return self.__parent__._cast(_2606.StraightBevelDiffGear)

    @property
    def straight_bevel_diff_gear_set(
        self: "CastSelf",
    ) -> "_2607.StraightBevelDiffGearSet":
        from mastapy._private.system_model.part_model.gears import _2607

        return self.__parent__._cast(_2607.StraightBevelDiffGearSet)

    @property
    def straight_bevel_gear(self: "CastSelf") -> "_2608.StraightBevelGear":
        from mastapy._private.system_model.part_model.gears import _2608

        return self.__parent__._cast(_2608.StraightBevelGear)

    @property
    def straight_bevel_gear_set(self: "CastSelf") -> "_2609.StraightBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2609

        return self.__parent__._cast(_2609.StraightBevelGearSet)

    @property
    def straight_bevel_planet_gear(self: "CastSelf") -> "_2610.StraightBevelPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2610

        return self.__parent__._cast(_2610.StraightBevelPlanetGear)

    @property
    def straight_bevel_sun_gear(self: "CastSelf") -> "_2611.StraightBevelSunGear":
        from mastapy._private.system_model.part_model.gears import _2611

        return self.__parent__._cast(_2611.StraightBevelSunGear)

    @property
    def worm_gear(self: "CastSelf") -> "_2612.WormGear":
        from mastapy._private.system_model.part_model.gears import _2612

        return self.__parent__._cast(_2612.WormGear)

    @property
    def worm_gear_set(self: "CastSelf") -> "_2613.WormGearSet":
        from mastapy._private.system_model.part_model.gears import _2613

        return self.__parent__._cast(_2613.WormGearSet)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2614.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2614

        return self.__parent__._cast(_2614.ZerolBevelGear)

    @property
    def zerol_bevel_gear_set(self: "CastSelf") -> "_2615.ZerolBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2615

        return self.__parent__._cast(_2615.ZerolBevelGearSet)

    @property
    def cycloidal_assembly(self: "CastSelf") -> "_2629.CycloidalAssembly":
        from mastapy._private.system_model.part_model.cycloidal import _2629

        return self.__parent__._cast(_2629.CycloidalAssembly)

    @property
    def cycloidal_disc(self: "CastSelf") -> "_2630.CycloidalDisc":
        from mastapy._private.system_model.part_model.cycloidal import _2630

        return self.__parent__._cast(_2630.CycloidalDisc)

    @property
    def ring_pins(self: "CastSelf") -> "_2631.RingPins":
        from mastapy._private.system_model.part_model.cycloidal import _2631

        return self.__parent__._cast(_2631.RingPins)

    @property
    def belt_drive(self: "CastSelf") -> "_2638.BeltDrive":
        from mastapy._private.system_model.part_model.couplings import _2638

        return self.__parent__._cast(_2638.BeltDrive)

    @property
    def clutch(self: "CastSelf") -> "_2640.Clutch":
        from mastapy._private.system_model.part_model.couplings import _2640

        return self.__parent__._cast(_2640.Clutch)

    @property
    def clutch_half(self: "CastSelf") -> "_2641.ClutchHalf":
        from mastapy._private.system_model.part_model.couplings import _2641

        return self.__parent__._cast(_2641.ClutchHalf)

    @property
    def concept_coupling(self: "CastSelf") -> "_2643.ConceptCoupling":
        from mastapy._private.system_model.part_model.couplings import _2643

        return self.__parent__._cast(_2643.ConceptCoupling)

    @property
    def concept_coupling_half(self: "CastSelf") -> "_2644.ConceptCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2644

        return self.__parent__._cast(_2644.ConceptCouplingHalf)

    @property
    def coupling(self: "CastSelf") -> "_2646.Coupling":
        from mastapy._private.system_model.part_model.couplings import _2646

        return self.__parent__._cast(_2646.Coupling)

    @property
    def coupling_half(self: "CastSelf") -> "_2647.CouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2647

        return self.__parent__._cast(_2647.CouplingHalf)

    @property
    def cvt(self: "CastSelf") -> "_2649.CVT":
        from mastapy._private.system_model.part_model.couplings import _2649

        return self.__parent__._cast(_2649.CVT)

    @property
    def cvt_pulley(self: "CastSelf") -> "_2650.CVTPulley":
        from mastapy._private.system_model.part_model.couplings import _2650

        return self.__parent__._cast(_2650.CVTPulley)

    @property
    def part_to_part_shear_coupling(
        self: "CastSelf",
    ) -> "_2651.PartToPartShearCoupling":
        from mastapy._private.system_model.part_model.couplings import _2651

        return self.__parent__._cast(_2651.PartToPartShearCoupling)

    @property
    def part_to_part_shear_coupling_half(
        self: "CastSelf",
    ) -> "_2652.PartToPartShearCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2652

        return self.__parent__._cast(_2652.PartToPartShearCouplingHalf)

    @property
    def pulley(self: "CastSelf") -> "_2654.Pulley":
        from mastapy._private.system_model.part_model.couplings import _2654

        return self.__parent__._cast(_2654.Pulley)

    @property
    def rolling_ring(self: "CastSelf") -> "_2660.RollingRing":
        from mastapy._private.system_model.part_model.couplings import _2660

        return self.__parent__._cast(_2660.RollingRing)

    @property
    def rolling_ring_assembly(self: "CastSelf") -> "_2661.RollingRingAssembly":
        from mastapy._private.system_model.part_model.couplings import _2661

        return self.__parent__._cast(_2661.RollingRingAssembly)

    @property
    def shaft_hub_connection(self: "CastSelf") -> "_2662.ShaftHubConnection":
        from mastapy._private.system_model.part_model.couplings import _2662

        return self.__parent__._cast(_2662.ShaftHubConnection)

    @property
    def spring_damper(self: "CastSelf") -> "_2667.SpringDamper":
        from mastapy._private.system_model.part_model.couplings import _2667

        return self.__parent__._cast(_2667.SpringDamper)

    @property
    def spring_damper_half(self: "CastSelf") -> "_2668.SpringDamperHalf":
        from mastapy._private.system_model.part_model.couplings import _2668

        return self.__parent__._cast(_2668.SpringDamperHalf)

    @property
    def synchroniser(self: "CastSelf") -> "_2669.Synchroniser":
        from mastapy._private.system_model.part_model.couplings import _2669

        return self.__parent__._cast(_2669.Synchroniser)

    @property
    def synchroniser_half(self: "CastSelf") -> "_2671.SynchroniserHalf":
        from mastapy._private.system_model.part_model.couplings import _2671

        return self.__parent__._cast(_2671.SynchroniserHalf)

    @property
    def synchroniser_part(self: "CastSelf") -> "_2672.SynchroniserPart":
        from mastapy._private.system_model.part_model.couplings import _2672

        return self.__parent__._cast(_2672.SynchroniserPart)

    @property
    def synchroniser_sleeve(self: "CastSelf") -> "_2673.SynchroniserSleeve":
        from mastapy._private.system_model.part_model.couplings import _2673

        return self.__parent__._cast(_2673.SynchroniserSleeve)

    @property
    def torque_converter(self: "CastSelf") -> "_2674.TorqueConverter":
        from mastapy._private.system_model.part_model.couplings import _2674

        return self.__parent__._cast(_2674.TorqueConverter)

    @property
    def torque_converter_pump(self: "CastSelf") -> "_2675.TorqueConverterPump":
        from mastapy._private.system_model.part_model.couplings import _2675

        return self.__parent__._cast(_2675.TorqueConverterPump)

    @property
    def torque_converter_turbine(self: "CastSelf") -> "_2677.TorqueConverterTurbine":
        from mastapy._private.system_model.part_model.couplings import _2677

        return self.__parent__._cast(_2677.TorqueConverterTurbine)

    @property
    def design_entity(self: "CastSelf") -> "DesignEntity":
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
class DesignEntity(_0.APIBase):
    """DesignEntity

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DESIGN_ENTITY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def comment(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Comment")

        if temp is None:
            return ""

        return temp

    @comment.setter
    @enforce_parameter_types
    def comment(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Comment", str(value) if value is not None else ""
        )

    @property
    def full_name_without_root_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FullNameWithoutRootName")

        if temp is None:
            return ""

        return temp

    @property
    def id(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ID")

        if temp is None:
            return ""

        return temp

    @property
    def icon(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Icon")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def small_icon(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SmallIcon")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def unique_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UniqueName")

        if temp is None:
            return ""

        return temp

    @property
    def design_properties(self: "Self") -> "_2257.Design":
        """mastapy.system_model.Design

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignProperties")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def all_design_entities(self: "Self") -> "List[DesignEntity]":
        """List[mastapy.system_model.DesignEntity]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllDesignEntities")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def all_status_errors(self: "Self") -> "List[_1847.StatusItem]":
        """List[mastapy.utility.model_validation.StatusItem]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllStatusErrors")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def status(self: "Self") -> "_1846.Status":
        """mastapy.utility.model_validation.Status

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Status")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def user_specified_data(self: "Self") -> "_1794.UserSpecifiedData":
        """mastapy.utility.scripting.UserSpecifiedData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedData")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    def delete(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Delete")

    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputDefaultReportTo", file_path if file_path else ""
        )

    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportTo", file_path if file_path else ""
        )

    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportAsTextTo", file_path if file_path else ""
        )

    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_DesignEntity":
        """Cast to another type.

        Returns:
            _Cast_DesignEntity
        """
        return _Cast_DesignEntity(self)
