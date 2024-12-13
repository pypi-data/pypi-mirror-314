"""GearDesignComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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

_GEAR_DESIGN_COMPONENT = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns", "GearDesignComponent"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs import _973, _975, _976
    from mastapy._private.gears.gear_designs.agma_gleason_conical import (
        _1233,
        _1234,
        _1235,
        _1236,
    )
    from mastapy._private.gears.gear_designs.bevel import _1220, _1221, _1222, _1223
    from mastapy._private.gears.gear_designs.concept import _1216, _1217, _1218
    from mastapy._private.gears.gear_designs.conical import _1194, _1195, _1196, _1199
    from mastapy._private.gears.gear_designs.cylindrical import (
        _1044,
        _1050,
        _1060,
        _1073,
        _1074,
    )
    from mastapy._private.gears.gear_designs.face import (
        _1015,
        _1017,
        _1020,
        _1021,
        _1023,
    )
    from mastapy._private.gears.gear_designs.hypoid import _1011, _1012, _1013, _1014
    from mastapy._private.gears.gear_designs.klingelnberg_conical import (
        _1007,
        _1008,
        _1009,
        _1010,
    )
    from mastapy._private.gears.gear_designs.klingelnberg_hypoid import (
        _1003,
        _1004,
        _1005,
        _1006,
    )
    from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import (
        _999,
        _1000,
        _1001,
        _1002,
    )
    from mastapy._private.gears.gear_designs.spiral_bevel import _995, _996, _997, _998
    from mastapy._private.gears.gear_designs.straight_bevel import (
        _987,
        _988,
        _989,
        _990,
    )
    from mastapy._private.gears.gear_designs.straight_bevel_diff import (
        _991,
        _992,
        _993,
        _994,
    )
    from mastapy._private.gears.gear_designs.worm import _982, _983, _984, _985, _986
    from mastapy._private.gears.gear_designs.zerol_bevel import _978, _979, _980, _981
    from mastapy._private.utility.scripting import _1794

    Self = TypeVar("Self", bound="GearDesignComponent")
    CastSelf = TypeVar(
        "CastSelf", bound="GearDesignComponent._Cast_GearDesignComponent"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearDesignComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearDesignComponent:
    """Special nested class for casting GearDesignComponent to subclasses."""

    __parent__: "GearDesignComponent"

    @property
    def gear_design(self: "CastSelf") -> "_973.GearDesign":
        from mastapy._private.gears.gear_designs import _973

        return self.__parent__._cast(_973.GearDesign)

    @property
    def gear_mesh_design(self: "CastSelf") -> "_975.GearMeshDesign":
        from mastapy._private.gears.gear_designs import _975

        return self.__parent__._cast(_975.GearMeshDesign)

    @property
    def gear_set_design(self: "CastSelf") -> "_976.GearSetDesign":
        from mastapy._private.gears.gear_designs import _976

        return self.__parent__._cast(_976.GearSetDesign)

    @property
    def zerol_bevel_gear_design(self: "CastSelf") -> "_978.ZerolBevelGearDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _978

        return self.__parent__._cast(_978.ZerolBevelGearDesign)

    @property
    def zerol_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_979.ZerolBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _979

        return self.__parent__._cast(_979.ZerolBevelGearMeshDesign)

    @property
    def zerol_bevel_gear_set_design(self: "CastSelf") -> "_980.ZerolBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _980

        return self.__parent__._cast(_980.ZerolBevelGearSetDesign)

    @property
    def zerol_bevel_meshed_gear_design(
        self: "CastSelf",
    ) -> "_981.ZerolBevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _981

        return self.__parent__._cast(_981.ZerolBevelMeshedGearDesign)

    @property
    def worm_design(self: "CastSelf") -> "_982.WormDesign":
        from mastapy._private.gears.gear_designs.worm import _982

        return self.__parent__._cast(_982.WormDesign)

    @property
    def worm_gear_design(self: "CastSelf") -> "_983.WormGearDesign":
        from mastapy._private.gears.gear_designs.worm import _983

        return self.__parent__._cast(_983.WormGearDesign)

    @property
    def worm_gear_mesh_design(self: "CastSelf") -> "_984.WormGearMeshDesign":
        from mastapy._private.gears.gear_designs.worm import _984

        return self.__parent__._cast(_984.WormGearMeshDesign)

    @property
    def worm_gear_set_design(self: "CastSelf") -> "_985.WormGearSetDesign":
        from mastapy._private.gears.gear_designs.worm import _985

        return self.__parent__._cast(_985.WormGearSetDesign)

    @property
    def worm_wheel_design(self: "CastSelf") -> "_986.WormWheelDesign":
        from mastapy._private.gears.gear_designs.worm import _986

        return self.__parent__._cast(_986.WormWheelDesign)

    @property
    def straight_bevel_gear_design(self: "CastSelf") -> "_987.StraightBevelGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _987

        return self.__parent__._cast(_987.StraightBevelGearDesign)

    @property
    def straight_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_988.StraightBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _988

        return self.__parent__._cast(_988.StraightBevelGearMeshDesign)

    @property
    def straight_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_989.StraightBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _989

        return self.__parent__._cast(_989.StraightBevelGearSetDesign)

    @property
    def straight_bevel_meshed_gear_design(
        self: "CastSelf",
    ) -> "_990.StraightBevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _990

        return self.__parent__._cast(_990.StraightBevelMeshedGearDesign)

    @property
    def straight_bevel_diff_gear_design(
        self: "CastSelf",
    ) -> "_991.StraightBevelDiffGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _991

        return self.__parent__._cast(_991.StraightBevelDiffGearDesign)

    @property
    def straight_bevel_diff_gear_mesh_design(
        self: "CastSelf",
    ) -> "_992.StraightBevelDiffGearMeshDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _992

        return self.__parent__._cast(_992.StraightBevelDiffGearMeshDesign)

    @property
    def straight_bevel_diff_gear_set_design(
        self: "CastSelf",
    ) -> "_993.StraightBevelDiffGearSetDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _993

        return self.__parent__._cast(_993.StraightBevelDiffGearSetDesign)

    @property
    def straight_bevel_diff_meshed_gear_design(
        self: "CastSelf",
    ) -> "_994.StraightBevelDiffMeshedGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _994

        return self.__parent__._cast(_994.StraightBevelDiffMeshedGearDesign)

    @property
    def spiral_bevel_gear_design(self: "CastSelf") -> "_995.SpiralBevelGearDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _995

        return self.__parent__._cast(_995.SpiralBevelGearDesign)

    @property
    def spiral_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_996.SpiralBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _996

        return self.__parent__._cast(_996.SpiralBevelGearMeshDesign)

    @property
    def spiral_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_997.SpiralBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _997

        return self.__parent__._cast(_997.SpiralBevelGearSetDesign)

    @property
    def spiral_bevel_meshed_gear_design(
        self: "CastSelf",
    ) -> "_998.SpiralBevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _998

        return self.__parent__._cast(_998.SpiralBevelMeshedGearDesign)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_design(
        self: "CastSelf",
    ) -> "_999.KlingelnbergCycloPalloidSpiralBevelGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _999

        return self.__parent__._cast(_999.KlingelnbergCycloPalloidSpiralBevelGearDesign)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1000.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1000

        return self.__parent__._cast(
            _1000.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_1001.KlingelnbergCycloPalloidSpiralBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1001

        return self.__parent__._cast(
            _1001.KlingelnbergCycloPalloidSpiralBevelGearSetDesign
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1002.KlingelnbergCycloPalloidSpiralBevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1002

        return self.__parent__._cast(
            _1002.KlingelnbergCycloPalloidSpiralBevelMeshedGearDesign
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_design(
        self: "CastSelf",
    ) -> "_1003.KlingelnbergCycloPalloidHypoidGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1003

        return self.__parent__._cast(_1003.KlingelnbergCycloPalloidHypoidGearDesign)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1004.KlingelnbergCycloPalloidHypoidGearMeshDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1004

        return self.__parent__._cast(_1004.KlingelnbergCycloPalloidHypoidGearMeshDesign)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_design(
        self: "CastSelf",
    ) -> "_1005.KlingelnbergCycloPalloidHypoidGearSetDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1005

        return self.__parent__._cast(_1005.KlingelnbergCycloPalloidHypoidGearSetDesign)

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1006.KlingelnbergCycloPalloidHypoidMeshedGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1006

        return self.__parent__._cast(
            _1006.KlingelnbergCycloPalloidHypoidMeshedGearDesign
        )

    @property
    def klingelnberg_conical_gear_design(
        self: "CastSelf",
    ) -> "_1007.KlingelnbergConicalGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_conical import _1007

        return self.__parent__._cast(_1007.KlingelnbergConicalGearDesign)

    @property
    def klingelnberg_conical_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1008.KlingelnbergConicalGearMeshDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_conical import _1008

        return self.__parent__._cast(_1008.KlingelnbergConicalGearMeshDesign)

    @property
    def klingelnberg_conical_gear_set_design(
        self: "CastSelf",
    ) -> "_1009.KlingelnbergConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_conical import _1009

        return self.__parent__._cast(_1009.KlingelnbergConicalGearSetDesign)

    @property
    def klingelnberg_conical_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1010.KlingelnbergConicalMeshedGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_conical import _1010

        return self.__parent__._cast(_1010.KlingelnbergConicalMeshedGearDesign)

    @property
    def hypoid_gear_design(self: "CastSelf") -> "_1011.HypoidGearDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1011

        return self.__parent__._cast(_1011.HypoidGearDesign)

    @property
    def hypoid_gear_mesh_design(self: "CastSelf") -> "_1012.HypoidGearMeshDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1012

        return self.__parent__._cast(_1012.HypoidGearMeshDesign)

    @property
    def hypoid_gear_set_design(self: "CastSelf") -> "_1013.HypoidGearSetDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1013

        return self.__parent__._cast(_1013.HypoidGearSetDesign)

    @property
    def hypoid_meshed_gear_design(self: "CastSelf") -> "_1014.HypoidMeshedGearDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1014

        return self.__parent__._cast(_1014.HypoidMeshedGearDesign)

    @property
    def face_gear_design(self: "CastSelf") -> "_1015.FaceGearDesign":
        from mastapy._private.gears.gear_designs.face import _1015

        return self.__parent__._cast(_1015.FaceGearDesign)

    @property
    def face_gear_mesh_design(self: "CastSelf") -> "_1017.FaceGearMeshDesign":
        from mastapy._private.gears.gear_designs.face import _1017

        return self.__parent__._cast(_1017.FaceGearMeshDesign)

    @property
    def face_gear_pinion_design(self: "CastSelf") -> "_1020.FaceGearPinionDesign":
        from mastapy._private.gears.gear_designs.face import _1020

        return self.__parent__._cast(_1020.FaceGearPinionDesign)

    @property
    def face_gear_set_design(self: "CastSelf") -> "_1021.FaceGearSetDesign":
        from mastapy._private.gears.gear_designs.face import _1021

        return self.__parent__._cast(_1021.FaceGearSetDesign)

    @property
    def face_gear_wheel_design(self: "CastSelf") -> "_1023.FaceGearWheelDesign":
        from mastapy._private.gears.gear_designs.face import _1023

        return self.__parent__._cast(_1023.FaceGearWheelDesign)

    @property
    def cylindrical_gear_design(self: "CastSelf") -> "_1044.CylindricalGearDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1044

        return self.__parent__._cast(_1044.CylindricalGearDesign)

    @property
    def cylindrical_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1050.CylindricalGearMeshDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1050

        return self.__parent__._cast(_1050.CylindricalGearMeshDesign)

    @property
    def cylindrical_gear_set_design(
        self: "CastSelf",
    ) -> "_1060.CylindricalGearSetDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1060

        return self.__parent__._cast(_1060.CylindricalGearSetDesign)

    @property
    def cylindrical_planetary_gear_set_design(
        self: "CastSelf",
    ) -> "_1073.CylindricalPlanetaryGearSetDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1073

        return self.__parent__._cast(_1073.CylindricalPlanetaryGearSetDesign)

    @property
    def cylindrical_planet_gear_design(
        self: "CastSelf",
    ) -> "_1074.CylindricalPlanetGearDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1074

        return self.__parent__._cast(_1074.CylindricalPlanetGearDesign)

    @property
    def conical_gear_design(self: "CastSelf") -> "_1194.ConicalGearDesign":
        from mastapy._private.gears.gear_designs.conical import _1194

        return self.__parent__._cast(_1194.ConicalGearDesign)

    @property
    def conical_gear_mesh_design(self: "CastSelf") -> "_1195.ConicalGearMeshDesign":
        from mastapy._private.gears.gear_designs.conical import _1195

        return self.__parent__._cast(_1195.ConicalGearMeshDesign)

    @property
    def conical_gear_set_design(self: "CastSelf") -> "_1196.ConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.conical import _1196

        return self.__parent__._cast(_1196.ConicalGearSetDesign)

    @property
    def conical_meshed_gear_design(self: "CastSelf") -> "_1199.ConicalMeshedGearDesign":
        from mastapy._private.gears.gear_designs.conical import _1199

        return self.__parent__._cast(_1199.ConicalMeshedGearDesign)

    @property
    def concept_gear_design(self: "CastSelf") -> "_1216.ConceptGearDesign":
        from mastapy._private.gears.gear_designs.concept import _1216

        return self.__parent__._cast(_1216.ConceptGearDesign)

    @property
    def concept_gear_mesh_design(self: "CastSelf") -> "_1217.ConceptGearMeshDesign":
        from mastapy._private.gears.gear_designs.concept import _1217

        return self.__parent__._cast(_1217.ConceptGearMeshDesign)

    @property
    def concept_gear_set_design(self: "CastSelf") -> "_1218.ConceptGearSetDesign":
        from mastapy._private.gears.gear_designs.concept import _1218

        return self.__parent__._cast(_1218.ConceptGearSetDesign)

    @property
    def bevel_gear_design(self: "CastSelf") -> "_1220.BevelGearDesign":
        from mastapy._private.gears.gear_designs.bevel import _1220

        return self.__parent__._cast(_1220.BevelGearDesign)

    @property
    def bevel_gear_mesh_design(self: "CastSelf") -> "_1221.BevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.bevel import _1221

        return self.__parent__._cast(_1221.BevelGearMeshDesign)

    @property
    def bevel_gear_set_design(self: "CastSelf") -> "_1222.BevelGearSetDesign":
        from mastapy._private.gears.gear_designs.bevel import _1222

        return self.__parent__._cast(_1222.BevelGearSetDesign)

    @property
    def bevel_meshed_gear_design(self: "CastSelf") -> "_1223.BevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.bevel import _1223

        return self.__parent__._cast(_1223.BevelMeshedGearDesign)

    @property
    def agma_gleason_conical_gear_design(
        self: "CastSelf",
    ) -> "_1233.AGMAGleasonConicalGearDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1233

        return self.__parent__._cast(_1233.AGMAGleasonConicalGearDesign)

    @property
    def agma_gleason_conical_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1234.AGMAGleasonConicalGearMeshDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1234

        return self.__parent__._cast(_1234.AGMAGleasonConicalGearMeshDesign)

    @property
    def agma_gleason_conical_gear_set_design(
        self: "CastSelf",
    ) -> "_1235.AGMAGleasonConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1235

        return self.__parent__._cast(_1235.AGMAGleasonConicalGearSetDesign)

    @property
    def agma_gleason_conical_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1236.AGMAGleasonConicalMeshedGearDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1236

        return self.__parent__._cast(_1236.AGMAGleasonConicalMeshedGearDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "GearDesignComponent":
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
class GearDesignComponent(_0.APIBase):
    """GearDesignComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_DESIGN_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

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

    def dispose(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Dispose")

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

    def __enter__(self: "Self") -> None:
        return self

    def __exit__(
        self: "Self", exception_type: "Any", exception_value: "Any", traceback: "Any"
    ) -> None:
        self.dispose()

    @property
    def cast_to(self: "Self") -> "_Cast_GearDesignComponent":
        """Cast to another type.

        Returns:
            _Cast_GearDesignComponent
        """
        return _Cast_GearDesignComponent(self)
