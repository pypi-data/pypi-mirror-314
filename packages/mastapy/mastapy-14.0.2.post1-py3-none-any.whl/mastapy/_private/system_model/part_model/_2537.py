"""SpecialisedAssembly"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model import _2492

_SPECIALISED_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "SpecialisedAssembly"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2260
    from mastapy._private.system_model.part_model import _2501, _2512, _2523, _2528
    from mastapy._private.system_model.part_model.couplings import (
        _2638,
        _2640,
        _2643,
        _2646,
        _2649,
        _2651,
        _2661,
        _2667,
        _2669,
        _2674,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2629
    from mastapy._private.system_model.part_model.gears import (
        _2575,
        _2577,
        _2581,
        _2583,
        _2585,
        _2587,
        _2590,
        _2593,
        _2596,
        _2598,
        _2600,
        _2602,
        _2603,
        _2605,
        _2607,
        _2609,
        _2613,
        _2615,
    )

    Self = TypeVar("Self", bound="SpecialisedAssembly")
    CastSelf = TypeVar(
        "CastSelf", bound="SpecialisedAssembly._Cast_SpecialisedAssembly"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssembly",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpecialisedAssembly:
    """Special nested class for casting SpecialisedAssembly to subclasses."""

    __parent__: "SpecialisedAssembly"

    @property
    def abstract_assembly(self: "CastSelf") -> "_2492.AbstractAssembly":
        return self.__parent__._cast(_2492.AbstractAssembly)

    @property
    def part(self: "CastSelf") -> "_2528.Part":
        from mastapy._private.system_model.part_model import _2528

        return self.__parent__._cast(_2528.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2260.DesignEntity":
        from mastapy._private.system_model import _2260

        return self.__parent__._cast(_2260.DesignEntity)

    @property
    def bolted_joint(self: "CastSelf") -> "_2501.BoltedJoint":
        from mastapy._private.system_model.part_model import _2501

        return self.__parent__._cast(_2501.BoltedJoint)

    @property
    def flexible_pin_assembly(self: "CastSelf") -> "_2512.FlexiblePinAssembly":
        from mastapy._private.system_model.part_model import _2512

        return self.__parent__._cast(_2512.FlexiblePinAssembly)

    @property
    def microphone_array(self: "CastSelf") -> "_2523.MicrophoneArray":
        from mastapy._private.system_model.part_model import _2523

        return self.__parent__._cast(_2523.MicrophoneArray)

    @property
    def agma_gleason_conical_gear_set(
        self: "CastSelf",
    ) -> "_2575.AGMAGleasonConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2575

        return self.__parent__._cast(_2575.AGMAGleasonConicalGearSet)

    @property
    def bevel_differential_gear_set(
        self: "CastSelf",
    ) -> "_2577.BevelDifferentialGearSet":
        from mastapy._private.system_model.part_model.gears import _2577

        return self.__parent__._cast(_2577.BevelDifferentialGearSet)

    @property
    def bevel_gear_set(self: "CastSelf") -> "_2581.BevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2581

        return self.__parent__._cast(_2581.BevelGearSet)

    @property
    def concept_gear_set(self: "CastSelf") -> "_2583.ConceptGearSet":
        from mastapy._private.system_model.part_model.gears import _2583

        return self.__parent__._cast(_2583.ConceptGearSet)

    @property
    def conical_gear_set(self: "CastSelf") -> "_2585.ConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2585

        return self.__parent__._cast(_2585.ConicalGearSet)

    @property
    def cylindrical_gear_set(self: "CastSelf") -> "_2587.CylindricalGearSet":
        from mastapy._private.system_model.part_model.gears import _2587

        return self.__parent__._cast(_2587.CylindricalGearSet)

    @property
    def face_gear_set(self: "CastSelf") -> "_2590.FaceGearSet":
        from mastapy._private.system_model.part_model.gears import _2590

        return self.__parent__._cast(_2590.FaceGearSet)

    @property
    def gear_set(self: "CastSelf") -> "_2593.GearSet":
        from mastapy._private.system_model.part_model.gears import _2593

        return self.__parent__._cast(_2593.GearSet)

    @property
    def hypoid_gear_set(self: "CastSelf") -> "_2596.HypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2596

        return self.__parent__._cast(_2596.HypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set(
        self: "CastSelf",
    ) -> "_2598.KlingelnbergCycloPalloidConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2598

        return self.__parent__._cast(_2598.KlingelnbergCycloPalloidConicalGearSet)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "CastSelf",
    ) -> "_2600.KlingelnbergCycloPalloidHypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2600

        return self.__parent__._cast(_2600.KlingelnbergCycloPalloidHypoidGearSet)

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
    def spiral_bevel_gear_set(self: "CastSelf") -> "_2605.SpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2605

        return self.__parent__._cast(_2605.SpiralBevelGearSet)

    @property
    def straight_bevel_diff_gear_set(
        self: "CastSelf",
    ) -> "_2607.StraightBevelDiffGearSet":
        from mastapy._private.system_model.part_model.gears import _2607

        return self.__parent__._cast(_2607.StraightBevelDiffGearSet)

    @property
    def straight_bevel_gear_set(self: "CastSelf") -> "_2609.StraightBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2609

        return self.__parent__._cast(_2609.StraightBevelGearSet)

    @property
    def worm_gear_set(self: "CastSelf") -> "_2613.WormGearSet":
        from mastapy._private.system_model.part_model.gears import _2613

        return self.__parent__._cast(_2613.WormGearSet)

    @property
    def zerol_bevel_gear_set(self: "CastSelf") -> "_2615.ZerolBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2615

        return self.__parent__._cast(_2615.ZerolBevelGearSet)

    @property
    def cycloidal_assembly(self: "CastSelf") -> "_2629.CycloidalAssembly":
        from mastapy._private.system_model.part_model.cycloidal import _2629

        return self.__parent__._cast(_2629.CycloidalAssembly)

    @property
    def belt_drive(self: "CastSelf") -> "_2638.BeltDrive":
        from mastapy._private.system_model.part_model.couplings import _2638

        return self.__parent__._cast(_2638.BeltDrive)

    @property
    def clutch(self: "CastSelf") -> "_2640.Clutch":
        from mastapy._private.system_model.part_model.couplings import _2640

        return self.__parent__._cast(_2640.Clutch)

    @property
    def concept_coupling(self: "CastSelf") -> "_2643.ConceptCoupling":
        from mastapy._private.system_model.part_model.couplings import _2643

        return self.__parent__._cast(_2643.ConceptCoupling)

    @property
    def coupling(self: "CastSelf") -> "_2646.Coupling":
        from mastapy._private.system_model.part_model.couplings import _2646

        return self.__parent__._cast(_2646.Coupling)

    @property
    def cvt(self: "CastSelf") -> "_2649.CVT":
        from mastapy._private.system_model.part_model.couplings import _2649

        return self.__parent__._cast(_2649.CVT)

    @property
    def part_to_part_shear_coupling(
        self: "CastSelf",
    ) -> "_2651.PartToPartShearCoupling":
        from mastapy._private.system_model.part_model.couplings import _2651

        return self.__parent__._cast(_2651.PartToPartShearCoupling)

    @property
    def rolling_ring_assembly(self: "CastSelf") -> "_2661.RollingRingAssembly":
        from mastapy._private.system_model.part_model.couplings import _2661

        return self.__parent__._cast(_2661.RollingRingAssembly)

    @property
    def spring_damper(self: "CastSelf") -> "_2667.SpringDamper":
        from mastapy._private.system_model.part_model.couplings import _2667

        return self.__parent__._cast(_2667.SpringDamper)

    @property
    def synchroniser(self: "CastSelf") -> "_2669.Synchroniser":
        from mastapy._private.system_model.part_model.couplings import _2669

        return self.__parent__._cast(_2669.Synchroniser)

    @property
    def torque_converter(self: "CastSelf") -> "_2674.TorqueConverter":
        from mastapy._private.system_model.part_model.couplings import _2674

        return self.__parent__._cast(_2674.TorqueConverter)

    @property
    def specialised_assembly(self: "CastSelf") -> "SpecialisedAssembly":
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
class SpecialisedAssembly(_2492.AbstractAssembly):
    """SpecialisedAssembly

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPECIALISED_ASSEMBLY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_SpecialisedAssembly":
        """Cast to another type.

        Returns:
            _Cast_SpecialisedAssembly
        """
        return _Cast_SpecialisedAssembly(self)
