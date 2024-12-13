"""MountableComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2502

_MOUNTABLE_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MountableComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2260
    from mastapy._private.system_model.connections_and_sockets import (
        _2326,
        _2329,
        _2333,
    )
    from mastapy._private.system_model.part_model import (
        _2493,
        _2497,
        _2503,
        _2505,
        _2520,
        _2521,
        _2526,
        _2528,
        _2529,
        _2531,
        _2532,
        _2538,
        _2540,
    )
    from mastapy._private.system_model.part_model.couplings import (
        _2641,
        _2644,
        _2647,
        _2650,
        _2652,
        _2654,
        _2660,
        _2662,
        _2668,
        _2671,
        _2672,
        _2673,
        _2675,
        _2677,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2631
    from mastapy._private.system_model.part_model.gears import (
        _2574,
        _2576,
        _2578,
        _2579,
        _2580,
        _2582,
        _2584,
        _2586,
        _2588,
        _2589,
        _2591,
        _2595,
        _2597,
        _2599,
        _2601,
        _2604,
        _2606,
        _2608,
        _2610,
        _2611,
        _2612,
        _2614,
    )

    Self = TypeVar("Self", bound="MountableComponent")
    CastSelf = TypeVar("CastSelf", bound="MountableComponent._Cast_MountableComponent")


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountableComponent:
    """Special nested class for casting MountableComponent to subclasses."""

    __parent__: "MountableComponent"

    @property
    def component(self: "CastSelf") -> "_2502.Component":
        return self.__parent__._cast(_2502.Component)

    @property
    def part(self: "CastSelf") -> "_2528.Part":
        from mastapy._private.system_model.part_model import _2528

        return self.__parent__._cast(_2528.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2260.DesignEntity":
        from mastapy._private.system_model import _2260

        return self.__parent__._cast(_2260.DesignEntity)

    @property
    def bearing(self: "CastSelf") -> "_2497.Bearing":
        from mastapy._private.system_model.part_model import _2497

        return self.__parent__._cast(_2497.Bearing)

    @property
    def connector(self: "CastSelf") -> "_2505.Connector":
        from mastapy._private.system_model.part_model import _2505

        return self.__parent__._cast(_2505.Connector)

    @property
    def mass_disc(self: "CastSelf") -> "_2520.MassDisc":
        from mastapy._private.system_model.part_model import _2520

        return self.__parent__._cast(_2520.MassDisc)

    @property
    def measurement_component(self: "CastSelf") -> "_2521.MeasurementComponent":
        from mastapy._private.system_model.part_model import _2521

        return self.__parent__._cast(_2521.MeasurementComponent)

    @property
    def oil_seal(self: "CastSelf") -> "_2526.OilSeal":
        from mastapy._private.system_model.part_model import _2526

        return self.__parent__._cast(_2526.OilSeal)

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
    def unbalanced_mass(self: "CastSelf") -> "_2538.UnbalancedMass":
        from mastapy._private.system_model.part_model import _2538

        return self.__parent__._cast(_2538.UnbalancedMass)

    @property
    def virtual_component(self: "CastSelf") -> "_2540.VirtualComponent":
        from mastapy._private.system_model.part_model import _2540

        return self.__parent__._cast(_2540.VirtualComponent)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2574.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2574

        return self.__parent__._cast(_2574.AGMAGleasonConicalGear)

    @property
    def bevel_differential_gear(self: "CastSelf") -> "_2576.BevelDifferentialGear":
        from mastapy._private.system_model.part_model.gears import _2576

        return self.__parent__._cast(_2576.BevelDifferentialGear)

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
    def concept_gear(self: "CastSelf") -> "_2582.ConceptGear":
        from mastapy._private.system_model.part_model.gears import _2582

        return self.__parent__._cast(_2582.ConceptGear)

    @property
    def conical_gear(self: "CastSelf") -> "_2584.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2584

        return self.__parent__._cast(_2584.ConicalGear)

    @property
    def cylindrical_gear(self: "CastSelf") -> "_2586.CylindricalGear":
        from mastapy._private.system_model.part_model.gears import _2586

        return self.__parent__._cast(_2586.CylindricalGear)

    @property
    def cylindrical_planet_gear(self: "CastSelf") -> "_2588.CylindricalPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2588

        return self.__parent__._cast(_2588.CylindricalPlanetGear)

    @property
    def face_gear(self: "CastSelf") -> "_2589.FaceGear":
        from mastapy._private.system_model.part_model.gears import _2589

        return self.__parent__._cast(_2589.FaceGear)

    @property
    def gear(self: "CastSelf") -> "_2591.Gear":
        from mastapy._private.system_model.part_model.gears import _2591

        return self.__parent__._cast(_2591.Gear)

    @property
    def hypoid_gear(self: "CastSelf") -> "_2595.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2595

        return self.__parent__._cast(_2595.HypoidGear)

    @property
    def klingelnberg_cyclo_palloid_conical_gear(
        self: "CastSelf",
    ) -> "_2597.KlingelnbergCycloPalloidConicalGear":
        from mastapy._private.system_model.part_model.gears import _2597

        return self.__parent__._cast(_2597.KlingelnbergCycloPalloidConicalGear)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear(
        self: "CastSelf",
    ) -> "_2599.KlingelnbergCycloPalloidHypoidGear":
        from mastapy._private.system_model.part_model.gears import _2599

        return self.__parent__._cast(_2599.KlingelnbergCycloPalloidHypoidGear)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "CastSelf",
    ) -> "_2601.KlingelnbergCycloPalloidSpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2601

        return self.__parent__._cast(_2601.KlingelnbergCycloPalloidSpiralBevelGear)

    @property
    def spiral_bevel_gear(self: "CastSelf") -> "_2604.SpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2604

        return self.__parent__._cast(_2604.SpiralBevelGear)

    @property
    def straight_bevel_diff_gear(self: "CastSelf") -> "_2606.StraightBevelDiffGear":
        from mastapy._private.system_model.part_model.gears import _2606

        return self.__parent__._cast(_2606.StraightBevelDiffGear)

    @property
    def straight_bevel_gear(self: "CastSelf") -> "_2608.StraightBevelGear":
        from mastapy._private.system_model.part_model.gears import _2608

        return self.__parent__._cast(_2608.StraightBevelGear)

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
    def zerol_bevel_gear(self: "CastSelf") -> "_2614.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2614

        return self.__parent__._cast(_2614.ZerolBevelGear)

    @property
    def ring_pins(self: "CastSelf") -> "_2631.RingPins":
        from mastapy._private.system_model.part_model.cycloidal import _2631

        return self.__parent__._cast(_2631.RingPins)

    @property
    def clutch_half(self: "CastSelf") -> "_2641.ClutchHalf":
        from mastapy._private.system_model.part_model.couplings import _2641

        return self.__parent__._cast(_2641.ClutchHalf)

    @property
    def concept_coupling_half(self: "CastSelf") -> "_2644.ConceptCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2644

        return self.__parent__._cast(_2644.ConceptCouplingHalf)

    @property
    def coupling_half(self: "CastSelf") -> "_2647.CouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2647

        return self.__parent__._cast(_2647.CouplingHalf)

    @property
    def cvt_pulley(self: "CastSelf") -> "_2650.CVTPulley":
        from mastapy._private.system_model.part_model.couplings import _2650

        return self.__parent__._cast(_2650.CVTPulley)

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
    def shaft_hub_connection(self: "CastSelf") -> "_2662.ShaftHubConnection":
        from mastapy._private.system_model.part_model.couplings import _2662

        return self.__parent__._cast(_2662.ShaftHubConnection)

    @property
    def spring_damper_half(self: "CastSelf") -> "_2668.SpringDamperHalf":
        from mastapy._private.system_model.part_model.couplings import _2668

        return self.__parent__._cast(_2668.SpringDamperHalf)

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
    def torque_converter_pump(self: "CastSelf") -> "_2675.TorqueConverterPump":
        from mastapy._private.system_model.part_model.couplings import _2675

        return self.__parent__._cast(_2675.TorqueConverterPump)

    @property
    def torque_converter_turbine(self: "CastSelf") -> "_2677.TorqueConverterTurbine":
        from mastapy._private.system_model.part_model.couplings import _2677

        return self.__parent__._cast(_2677.TorqueConverterTurbine)

    @property
    def mountable_component(self: "CastSelf") -> "MountableComponent":
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
class MountableComponent(_2502.Component):
    """MountableComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUNTABLE_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def rotation_about_axis(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotationAboutAxis")

        if temp is None:
            return 0.0

        return temp

    @rotation_about_axis.setter
    @enforce_parameter_types
    def rotation_about_axis(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RotationAboutAxis",
            float(value) if value is not None else 0.0,
        )

    @property
    def inner_component(self: "Self") -> "_2493.AbstractShaft":
        """mastapy.system_model.part_model.AbstractShaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerComponent")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def inner_connection(self: "Self") -> "_2329.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerConnection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def inner_socket(self: "Self") -> "_2333.CylindricalSocket":
        """mastapy.system_model.connections_and_sockets.CylindricalSocket

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerSocket")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def is_mounted(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsMounted")

        if temp is None:
            return False

        return temp

    @enforce_parameter_types
    def mount_on(
        self: "Self", shaft: "_2493.AbstractShaft", offset: "float" = float("nan")
    ) -> "_2326.CoaxialConnection":
        """mastapy.system_model.connections_and_sockets.CoaxialConnection

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)
        """
        offset = float(offset)
        method_result = pythonnet_method_call(
            self.wrapped,
            "MountOn",
            shaft.wrapped if shaft else None,
            offset if offset else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def try_mount_on(
        self: "Self", shaft: "_2493.AbstractShaft", offset: "float" = float("nan")
    ) -> "_2503.ComponentsConnectedResult":
        """mastapy.system_model.part_model.ComponentsConnectedResult

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)
        """
        offset = float(offset)
        method_result = pythonnet_method_call(
            self.wrapped,
            "TryMountOn",
            shaft.wrapped if shaft else None,
            offset if offset else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_MountableComponent":
        """Cast to another type.

        Returns:
            _Cast_MountableComponent
        """
        return _Cast_MountableComponent(self)
