"""MeshSingleFlankRating"""

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

_MESH_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating", "MeshSingleFlankRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears import _331
    from mastapy._private.gears.rating import _372, _377
    from mastapy._private.gears.rating.bevel.standards import _571, _573, _575
    from mastapy._private.gears.rating.conical import _559
    from mastapy._private.gears.rating.cylindrical import _480
    from mastapy._private.gears.rating.cylindrical.agma import _548
    from mastapy._private.gears.rating.cylindrical.din3990 import _546
    from mastapy._private.gears.rating.cylindrical.iso6336 import (
        _525,
        _527,
        _529,
        _531,
        _533,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import (
        _503,
        _505,
        _507,
    )
    from mastapy._private.gears.rating.hypoid.standards import _456
    from mastapy._private.gears.rating.iso_10300 import _435, _436, _437, _438, _439
    from mastapy._private.gears.rating.klingelnberg_conical.kn3030 import (
        _427,
        _431,
        _432,
    )

    Self = TypeVar("Self", bound="MeshSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf", bound="MeshSingleFlankRating._Cast_MeshSingleFlankRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MeshSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MeshSingleFlankRating:
    """Special nested class for casting MeshSingleFlankRating to subclasses."""

    __parent__: "MeshSingleFlankRating"

    @property
    def klingelnberg_conical_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_427.KlingelnbergConicalMeshSingleFlankRating":
        from mastapy._private.gears.rating.klingelnberg_conical.kn3030 import _427

        return self.__parent__._cast(_427.KlingelnbergConicalMeshSingleFlankRating)

    @property
    def klingelnberg_cyclo_palloid_hypoid_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_431.KlingelnbergCycloPalloidHypoidMeshSingleFlankRating":
        from mastapy._private.gears.rating.klingelnberg_conical.kn3030 import _431

        return self.__parent__._cast(
            _431.KlingelnbergCycloPalloidHypoidMeshSingleFlankRating
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_432.KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating":
        from mastapy._private.gears.rating.klingelnberg_conical.kn3030 import _432

        return self.__parent__._cast(
            _432.KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating
        )

    @property
    def iso10300_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_435.ISO10300MeshSingleFlankRating":
        from mastapy._private.gears.rating.iso_10300 import _435

        return self.__parent__._cast(_435.ISO10300MeshSingleFlankRating)

    @property
    def iso10300_mesh_single_flank_rating_bevel_method_b2(
        self: "CastSelf",
    ) -> "_436.ISO10300MeshSingleFlankRatingBevelMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _436

        return self.__parent__._cast(_436.ISO10300MeshSingleFlankRatingBevelMethodB2)

    @property
    def iso10300_mesh_single_flank_rating_hypoid_method_b2(
        self: "CastSelf",
    ) -> "_437.ISO10300MeshSingleFlankRatingHypoidMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _437

        return self.__parent__._cast(_437.ISO10300MeshSingleFlankRatingHypoidMethodB2)

    @property
    def iso10300_mesh_single_flank_rating_method_b1(
        self: "CastSelf",
    ) -> "_438.ISO10300MeshSingleFlankRatingMethodB1":
        from mastapy._private.gears.rating.iso_10300 import _438

        return self.__parent__._cast(_438.ISO10300MeshSingleFlankRatingMethodB1)

    @property
    def iso10300_mesh_single_flank_rating_method_b2(
        self: "CastSelf",
    ) -> "_439.ISO10300MeshSingleFlankRatingMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _439

        return self.__parent__._cast(_439.ISO10300MeshSingleFlankRatingMethodB2)

    @property
    def gleason_hypoid_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_456.GleasonHypoidMeshSingleFlankRating":
        from mastapy._private.gears.rating.hypoid.standards import _456

        return self.__parent__._cast(_456.GleasonHypoidMeshSingleFlankRating)

    @property
    def cylindrical_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_480.CylindricalMeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical import _480

        return self.__parent__._cast(_480.CylindricalMeshSingleFlankRating)

    @property
    def metal_plastic_or_plastic_metal_vdi2736_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_503.MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _503

        return self.__parent__._cast(
            _503.MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating
        )

    @property
    def plastic_gear_vdi2736_abstract_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_505.PlasticGearVDI2736AbstractMeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _505

        return self.__parent__._cast(
            _505.PlasticGearVDI2736AbstractMeshSingleFlankRating
        )

    @property
    def plastic_plastic_vdi2736_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_507.PlasticPlasticVDI2736MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _507

        return self.__parent__._cast(_507.PlasticPlasticVDI2736MeshSingleFlankRating)

    @property
    def iso63361996_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_525.ISO63361996MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _525

        return self.__parent__._cast(_525.ISO63361996MeshSingleFlankRating)

    @property
    def iso63362006_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_527.ISO63362006MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _527

        return self.__parent__._cast(_527.ISO63362006MeshSingleFlankRating)

    @property
    def iso63362019_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_529.ISO63362019MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _529

        return self.__parent__._cast(_529.ISO63362019MeshSingleFlankRating)

    @property
    def iso6336_abstract_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_531.ISO6336AbstractMeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _531

        return self.__parent__._cast(_531.ISO6336AbstractMeshSingleFlankRating)

    @property
    def iso6336_abstract_metal_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_533.ISO6336AbstractMetalMeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _533

        return self.__parent__._cast(_533.ISO6336AbstractMetalMeshSingleFlankRating)

    @property
    def din3990_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_546.DIN3990MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.din3990 import _546

        return self.__parent__._cast(_546.DIN3990MeshSingleFlankRating)

    @property
    def agma2101_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_548.AGMA2101MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.agma import _548

        return self.__parent__._cast(_548.AGMA2101MeshSingleFlankRating)

    @property
    def conical_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_559.ConicalMeshSingleFlankRating":
        from mastapy._private.gears.rating.conical import _559

        return self.__parent__._cast(_559.ConicalMeshSingleFlankRating)

    @property
    def agma_spiral_bevel_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_571.AGMASpiralBevelMeshSingleFlankRating":
        from mastapy._private.gears.rating.bevel.standards import _571

        return self.__parent__._cast(_571.AGMASpiralBevelMeshSingleFlankRating)

    @property
    def gleason_spiral_bevel_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_573.GleasonSpiralBevelMeshSingleFlankRating":
        from mastapy._private.gears.rating.bevel.standards import _573

        return self.__parent__._cast(_573.GleasonSpiralBevelMeshSingleFlankRating)

    @property
    def spiral_bevel_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_575.SpiralBevelMeshSingleFlankRating":
        from mastapy._private.gears.rating.bevel.standards import _575

        return self.__parent__._cast(_575.SpiralBevelMeshSingleFlankRating)

    @property
    def mesh_single_flank_rating(self: "CastSelf") -> "MeshSingleFlankRating":
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
class MeshSingleFlankRating(_0.APIBase):
    """MeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MESH_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def coefficient_of_friction_calculation_method(
        self: "Self",
    ) -> "_331.CoefficientOfFrictionCalculationMethod":
        """mastapy.gears.CoefficientOfFrictionCalculationMethod"""
        temp = pythonnet_property_get(
            self.wrapped, "CoefficientOfFrictionCalculationMethod"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.CoefficientOfFrictionCalculationMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._331", "CoefficientOfFrictionCalculationMethod"
        )(value)

    @coefficient_of_friction_calculation_method.setter
    @enforce_parameter_types
    def coefficient_of_friction_calculation_method(
        self: "Self", value: "_331.CoefficientOfFrictionCalculationMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.CoefficientOfFrictionCalculationMethod"
        )
        pythonnet_property_set(
            self.wrapped, "CoefficientOfFrictionCalculationMethod", value
        )

    @property
    def efficiency_rating_method(self: "Self") -> "_372.GearMeshEfficiencyRatingMethod":
        """mastapy.gears.rating.GearMeshEfficiencyRatingMethod"""
        temp = pythonnet_property_get(self.wrapped, "EfficiencyRatingMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.Rating.GearMeshEfficiencyRatingMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating._372", "GearMeshEfficiencyRatingMethod"
        )(value)

    @efficiency_rating_method.setter
    @enforce_parameter_types
    def efficiency_rating_method(
        self: "Self", value: "_372.GearMeshEfficiencyRatingMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.Rating.GearMeshEfficiencyRatingMethod"
        )
        pythonnet_property_set(self.wrapped, "EfficiencyRatingMethod", value)

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
    def rating_standard_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatingStandardName")

        if temp is None:
            return ""

        return temp

    @property
    def gear_single_flank_ratings(self: "Self") -> "List[_377.GearSingleFlankRating]":
        """List[mastapy.gears.rating.GearSingleFlankRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSingleFlankRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

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
    def cast_to(self: "Self") -> "_Cast_MeshSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_MeshSingleFlankRating
        """
        return _Cast_MeshSingleFlankRating(self)
