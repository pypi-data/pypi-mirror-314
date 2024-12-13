"""GearSingleFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_GEAR_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating", "GearSingleFlankRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating.bevel.standards import _570, _572, _574
    from mastapy._private.gears.rating.conical import _556
    from mastapy._private.gears.rating.cylindrical import _478
    from mastapy._private.gears.rating.cylindrical.agma import _547
    from mastapy._private.gears.rating.cylindrical.din3990 import _545
    from mastapy._private.gears.rating.cylindrical.iso6336 import (
        _524,
        _526,
        _528,
        _530,
        _532,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import (
        _504,
        _509,
        _510,
    )
    from mastapy._private.gears.rating.hypoid.standards import _455
    from mastapy._private.gears.rating.iso_10300 import _442, _443, _444, _445, _446
    from mastapy._private.gears.rating.klingelnberg_conical.kn3030 import _429, _430

    Self = TypeVar("Self", bound="GearSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf", bound="GearSingleFlankRating._Cast_GearSingleFlankRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSingleFlankRating:
    """Special nested class for casting GearSingleFlankRating to subclasses."""

    __parent__: "GearSingleFlankRating"

    @property
    def klingelnberg_cyclo_palloid_conical_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_429.KlingelnbergCycloPalloidConicalGearSingleFlankRating":
        from mastapy._private.gears.rating.klingelnberg_conical.kn3030 import _429

        return self.__parent__._cast(
            _429.KlingelnbergCycloPalloidConicalGearSingleFlankRating
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_430.KlingelnbergCycloPalloidHypoidGearSingleFlankRating":
        from mastapy._private.gears.rating.klingelnberg_conical.kn3030 import _430

        return self.__parent__._cast(
            _430.KlingelnbergCycloPalloidHypoidGearSingleFlankRating
        )

    @property
    def iso10300_single_flank_rating(
        self: "CastSelf",
    ) -> "_442.ISO10300SingleFlankRating":
        from mastapy._private.gears.rating.iso_10300 import _442

        return self.__parent__._cast(_442.ISO10300SingleFlankRating)

    @property
    def iso10300_single_flank_rating_bevel_method_b2(
        self: "CastSelf",
    ) -> "_443.ISO10300SingleFlankRatingBevelMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _443

        return self.__parent__._cast(_443.ISO10300SingleFlankRatingBevelMethodB2)

    @property
    def iso10300_single_flank_rating_hypoid_method_b2(
        self: "CastSelf",
    ) -> "_444.ISO10300SingleFlankRatingHypoidMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _444

        return self.__parent__._cast(_444.ISO10300SingleFlankRatingHypoidMethodB2)

    @property
    def iso10300_single_flank_rating_method_b1(
        self: "CastSelf",
    ) -> "_445.ISO10300SingleFlankRatingMethodB1":
        from mastapy._private.gears.rating.iso_10300 import _445

        return self.__parent__._cast(_445.ISO10300SingleFlankRatingMethodB1)

    @property
    def iso10300_single_flank_rating_method_b2(
        self: "CastSelf",
    ) -> "_446.ISO10300SingleFlankRatingMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _446

        return self.__parent__._cast(_446.ISO10300SingleFlankRatingMethodB2)

    @property
    def gleason_hypoid_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_455.GleasonHypoidGearSingleFlankRating":
        from mastapy._private.gears.rating.hypoid.standards import _455

        return self.__parent__._cast(_455.GleasonHypoidGearSingleFlankRating)

    @property
    def cylindrical_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_478.CylindricalGearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical import _478

        return self.__parent__._cast(_478.CylindricalGearSingleFlankRating)

    @property
    def plastic_gear_vdi2736_abstract_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_504.PlasticGearVDI2736AbstractGearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _504

        return self.__parent__._cast(
            _504.PlasticGearVDI2736AbstractGearSingleFlankRating
        )

    @property
    def plastic_vdi2736_gear_single_flank_rating_in_a_metal_plastic_or_a_plastic_metal_mesh(
        self: "CastSelf",
    ) -> "_509.PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _509

        return self.__parent__._cast(
            _509.PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh
        )

    @property
    def plastic_vdi2736_gear_single_flank_rating_in_a_plastic_plastic_mesh(
        self: "CastSelf",
    ) -> "_510.PlasticVDI2736GearSingleFlankRatingInAPlasticPlasticMesh":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _510

        return self.__parent__._cast(
            _510.PlasticVDI2736GearSingleFlankRatingInAPlasticPlasticMesh
        )

    @property
    def iso63361996_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_524.ISO63361996GearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _524

        return self.__parent__._cast(_524.ISO63361996GearSingleFlankRating)

    @property
    def iso63362006_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_526.ISO63362006GearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _526

        return self.__parent__._cast(_526.ISO63362006GearSingleFlankRating)

    @property
    def iso63362019_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_528.ISO63362019GearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _528

        return self.__parent__._cast(_528.ISO63362019GearSingleFlankRating)

    @property
    def iso6336_abstract_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_530.ISO6336AbstractGearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _530

        return self.__parent__._cast(_530.ISO6336AbstractGearSingleFlankRating)

    @property
    def iso6336_abstract_metal_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_532.ISO6336AbstractMetalGearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _532

        return self.__parent__._cast(_532.ISO6336AbstractMetalGearSingleFlankRating)

    @property
    def din3990_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_545.DIN3990GearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.din3990 import _545

        return self.__parent__._cast(_545.DIN3990GearSingleFlankRating)

    @property
    def agma2101_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_547.AGMA2101GearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.agma import _547

        return self.__parent__._cast(_547.AGMA2101GearSingleFlankRating)

    @property
    def conical_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_556.ConicalGearSingleFlankRating":
        from mastapy._private.gears.rating.conical import _556

        return self.__parent__._cast(_556.ConicalGearSingleFlankRating)

    @property
    def agma_spiral_bevel_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_570.AGMASpiralBevelGearSingleFlankRating":
        from mastapy._private.gears.rating.bevel.standards import _570

        return self.__parent__._cast(_570.AGMASpiralBevelGearSingleFlankRating)

    @property
    def gleason_spiral_bevel_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_572.GleasonSpiralBevelGearSingleFlankRating":
        from mastapy._private.gears.rating.bevel.standards import _572

        return self.__parent__._cast(_572.GleasonSpiralBevelGearSingleFlankRating)

    @property
    def spiral_bevel_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_574.SpiralBevelGearSingleFlankRating":
        from mastapy._private.gears.rating.bevel.standards import _574

        return self.__parent__._cast(_574.SpiralBevelGearSingleFlankRating)

    @property
    def gear_single_flank_rating(self: "CastSelf") -> "GearSingleFlankRating":
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
class GearSingleFlankRating(_0.APIBase):
    """GearSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def duration(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Duration")

        if temp is None:
            return 0.0

        return temp

    @property
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def number_of_load_cycles(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfLoadCycles")

        if temp is None:
            return 0.0

        return temp

    @property
    def power(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Power")

        if temp is None:
            return 0.0

        return temp

    @property
    def rotation_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RotationSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    def torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Torque")

        if temp is None:
            return 0.0

        return temp

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
    def cast_to(self: "Self") -> "_Cast_GearSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_GearSingleFlankRating
        """
        return _Cast_GearSingleFlankRating(self)
