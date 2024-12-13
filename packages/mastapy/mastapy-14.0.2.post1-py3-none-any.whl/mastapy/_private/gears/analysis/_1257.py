"""AbstractGearSetAnalysis"""

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

_ABSTRACT_GEAR_SET_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "AbstractGearSetAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1266, _1268, _1269, _1270, _1271
    from mastapy._private.gears.fe_model import _1240
    from mastapy._private.gears.fe_model.conical import _1246
    from mastapy._private.gears.fe_model.cylindrical import _1243
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1141,
        _1142,
    )
    from mastapy._private.gears.gear_designs.face import _1022
    from mastapy._private.gears.gear_two_d_fe_analysis import _921, _922
    from mastapy._private.gears.load_case import _899
    from mastapy._private.gears.load_case.bevel import _918
    from mastapy._private.gears.load_case.concept import _914
    from mastapy._private.gears.load_case.conical import _911
    from mastapy._private.gears.load_case.cylindrical import _908
    from mastapy._private.gears.load_case.face import _905
    from mastapy._private.gears.load_case.worm import _902
    from mastapy._private.gears.ltca import _871
    from mastapy._private.gears.ltca.conical import _893
    from mastapy._private.gears.ltca.cylindrical import _885, _887
    from mastapy._private.gears.manufacturing.bevel import _815, _816, _817, _818
    from mastapy._private.gears.manufacturing.cylindrical import _645, _646, _650
    from mastapy._private.gears.rating import _367, _375, _376
    from mastapy._private.gears.rating.agma_gleason_conical import _580
    from mastapy._private.gears.rating.bevel import _569
    from mastapy._private.gears.rating.concept import _565, _566
    from mastapy._private.gears.rating.conical import _554, _555
    from mastapy._private.gears.rating.cylindrical import _476, _477, _493
    from mastapy._private.gears.rating.face import _462, _463
    from mastapy._private.gears.rating.hypoid import _453
    from mastapy._private.gears.rating.klingelnberg_conical import _426
    from mastapy._private.gears.rating.klingelnberg_hypoid import _423
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _420
    from mastapy._private.gears.rating.spiral_bevel import _417
    from mastapy._private.gears.rating.straight_bevel import _410
    from mastapy._private.gears.rating.straight_bevel_diff import _413
    from mastapy._private.gears.rating.worm import _388, _389
    from mastapy._private.gears.rating.zerol_bevel import _384
    from mastapy._private.utility.model_validation import _1846, _1847

    Self = TypeVar("Self", bound="AbstractGearSetAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractGearSetAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractGearSetAnalysis:
    """Special nested class for casting AbstractGearSetAnalysis to subclasses."""

    __parent__: "AbstractGearSetAnalysis"

    @property
    def abstract_gear_set_rating(self: "CastSelf") -> "_367.AbstractGearSetRating":
        from mastapy._private.gears.rating import _367

        return self.__parent__._cast(_367.AbstractGearSetRating)

    @property
    def gear_set_duty_cycle_rating(self: "CastSelf") -> "_375.GearSetDutyCycleRating":
        from mastapy._private.gears.rating import _375

        return self.__parent__._cast(_375.GearSetDutyCycleRating)

    @property
    def gear_set_rating(self: "CastSelf") -> "_376.GearSetRating":
        from mastapy._private.gears.rating import _376

        return self.__parent__._cast(_376.GearSetRating)

    @property
    def zerol_bevel_gear_set_rating(self: "CastSelf") -> "_384.ZerolBevelGearSetRating":
        from mastapy._private.gears.rating.zerol_bevel import _384

        return self.__parent__._cast(_384.ZerolBevelGearSetRating)

    @property
    def worm_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_388.WormGearSetDutyCycleRating":
        from mastapy._private.gears.rating.worm import _388

        return self.__parent__._cast(_388.WormGearSetDutyCycleRating)

    @property
    def worm_gear_set_rating(self: "CastSelf") -> "_389.WormGearSetRating":
        from mastapy._private.gears.rating.worm import _389

        return self.__parent__._cast(_389.WormGearSetRating)

    @property
    def straight_bevel_gear_set_rating(
        self: "CastSelf",
    ) -> "_410.StraightBevelGearSetRating":
        from mastapy._private.gears.rating.straight_bevel import _410

        return self.__parent__._cast(_410.StraightBevelGearSetRating)

    @property
    def straight_bevel_diff_gear_set_rating(
        self: "CastSelf",
    ) -> "_413.StraightBevelDiffGearSetRating":
        from mastapy._private.gears.rating.straight_bevel_diff import _413

        return self.__parent__._cast(_413.StraightBevelDiffGearSetRating)

    @property
    def spiral_bevel_gear_set_rating(
        self: "CastSelf",
    ) -> "_417.SpiralBevelGearSetRating":
        from mastapy._private.gears.rating.spiral_bevel import _417

        return self.__parent__._cast(_417.SpiralBevelGearSetRating)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_rating(
        self: "CastSelf",
    ) -> "_420.KlingelnbergCycloPalloidSpiralBevelGearSetRating":
        from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _420

        return self.__parent__._cast(
            _420.KlingelnbergCycloPalloidSpiralBevelGearSetRating
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_rating(
        self: "CastSelf",
    ) -> "_423.KlingelnbergCycloPalloidHypoidGearSetRating":
        from mastapy._private.gears.rating.klingelnberg_hypoid import _423

        return self.__parent__._cast(_423.KlingelnbergCycloPalloidHypoidGearSetRating)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_rating(
        self: "CastSelf",
    ) -> "_426.KlingelnbergCycloPalloidConicalGearSetRating":
        from mastapy._private.gears.rating.klingelnberg_conical import _426

        return self.__parent__._cast(_426.KlingelnbergCycloPalloidConicalGearSetRating)

    @property
    def hypoid_gear_set_rating(self: "CastSelf") -> "_453.HypoidGearSetRating":
        from mastapy._private.gears.rating.hypoid import _453

        return self.__parent__._cast(_453.HypoidGearSetRating)

    @property
    def face_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_462.FaceGearSetDutyCycleRating":
        from mastapy._private.gears.rating.face import _462

        return self.__parent__._cast(_462.FaceGearSetDutyCycleRating)

    @property
    def face_gear_set_rating(self: "CastSelf") -> "_463.FaceGearSetRating":
        from mastapy._private.gears.rating.face import _463

        return self.__parent__._cast(_463.FaceGearSetRating)

    @property
    def cylindrical_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_476.CylindricalGearSetDutyCycleRating":
        from mastapy._private.gears.rating.cylindrical import _476

        return self.__parent__._cast(_476.CylindricalGearSetDutyCycleRating)

    @property
    def cylindrical_gear_set_rating(
        self: "CastSelf",
    ) -> "_477.CylindricalGearSetRating":
        from mastapy._private.gears.rating.cylindrical import _477

        return self.__parent__._cast(_477.CylindricalGearSetRating)

    @property
    def reduced_cylindrical_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_493.ReducedCylindricalGearSetDutyCycleRating":
        from mastapy._private.gears.rating.cylindrical import _493

        return self.__parent__._cast(_493.ReducedCylindricalGearSetDutyCycleRating)

    @property
    def conical_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_554.ConicalGearSetDutyCycleRating":
        from mastapy._private.gears.rating.conical import _554

        return self.__parent__._cast(_554.ConicalGearSetDutyCycleRating)

    @property
    def conical_gear_set_rating(self: "CastSelf") -> "_555.ConicalGearSetRating":
        from mastapy._private.gears.rating.conical import _555

        return self.__parent__._cast(_555.ConicalGearSetRating)

    @property
    def concept_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_565.ConceptGearSetDutyCycleRating":
        from mastapy._private.gears.rating.concept import _565

        return self.__parent__._cast(_565.ConceptGearSetDutyCycleRating)

    @property
    def concept_gear_set_rating(self: "CastSelf") -> "_566.ConceptGearSetRating":
        from mastapy._private.gears.rating.concept import _566

        return self.__parent__._cast(_566.ConceptGearSetRating)

    @property
    def bevel_gear_set_rating(self: "CastSelf") -> "_569.BevelGearSetRating":
        from mastapy._private.gears.rating.bevel import _569

        return self.__parent__._cast(_569.BevelGearSetRating)

    @property
    def agma_gleason_conical_gear_set_rating(
        self: "CastSelf",
    ) -> "_580.AGMAGleasonConicalGearSetRating":
        from mastapy._private.gears.rating.agma_gleason_conical import _580

        return self.__parent__._cast(_580.AGMAGleasonConicalGearSetRating)

    @property
    def cylindrical_manufactured_gear_set_duty_cycle(
        self: "CastSelf",
    ) -> "_645.CylindricalManufacturedGearSetDutyCycle":
        from mastapy._private.gears.manufacturing.cylindrical import _645

        return self.__parent__._cast(_645.CylindricalManufacturedGearSetDutyCycle)

    @property
    def cylindrical_manufactured_gear_set_load_case(
        self: "CastSelf",
    ) -> "_646.CylindricalManufacturedGearSetLoadCase":
        from mastapy._private.gears.manufacturing.cylindrical import _646

        return self.__parent__._cast(_646.CylindricalManufacturedGearSetLoadCase)

    @property
    def cylindrical_set_manufacturing_config(
        self: "CastSelf",
    ) -> "_650.CylindricalSetManufacturingConfig":
        from mastapy._private.gears.manufacturing.cylindrical import _650

        return self.__parent__._cast(_650.CylindricalSetManufacturingConfig)

    @property
    def conical_set_manufacturing_analysis(
        self: "CastSelf",
    ) -> "_815.ConicalSetManufacturingAnalysis":
        from mastapy._private.gears.manufacturing.bevel import _815

        return self.__parent__._cast(_815.ConicalSetManufacturingAnalysis)

    @property
    def conical_set_manufacturing_config(
        self: "CastSelf",
    ) -> "_816.ConicalSetManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _816

        return self.__parent__._cast(_816.ConicalSetManufacturingConfig)

    @property
    def conical_set_micro_geometry_config(
        self: "CastSelf",
    ) -> "_817.ConicalSetMicroGeometryConfig":
        from mastapy._private.gears.manufacturing.bevel import _817

        return self.__parent__._cast(_817.ConicalSetMicroGeometryConfig)

    @property
    def conical_set_micro_geometry_config_base(
        self: "CastSelf",
    ) -> "_818.ConicalSetMicroGeometryConfigBase":
        from mastapy._private.gears.manufacturing.bevel import _818

        return self.__parent__._cast(_818.ConicalSetMicroGeometryConfigBase)

    @property
    def gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_871.GearSetLoadDistributionAnalysis":
        from mastapy._private.gears.ltca import _871

        return self.__parent__._cast(_871.GearSetLoadDistributionAnalysis)

    @property
    def cylindrical_gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_885.CylindricalGearSetLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.cylindrical import _885

        return self.__parent__._cast(_885.CylindricalGearSetLoadDistributionAnalysis)

    @property
    def face_gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_887.FaceGearSetLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.cylindrical import _887

        return self.__parent__._cast(_887.FaceGearSetLoadDistributionAnalysis)

    @property
    def conical_gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_893.ConicalGearSetLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.conical import _893

        return self.__parent__._cast(_893.ConicalGearSetLoadDistributionAnalysis)

    @property
    def gear_set_load_case_base(self: "CastSelf") -> "_899.GearSetLoadCaseBase":
        from mastapy._private.gears.load_case import _899

        return self.__parent__._cast(_899.GearSetLoadCaseBase)

    @property
    def worm_gear_set_load_case(self: "CastSelf") -> "_902.WormGearSetLoadCase":
        from mastapy._private.gears.load_case.worm import _902

        return self.__parent__._cast(_902.WormGearSetLoadCase)

    @property
    def face_gear_set_load_case(self: "CastSelf") -> "_905.FaceGearSetLoadCase":
        from mastapy._private.gears.load_case.face import _905

        return self.__parent__._cast(_905.FaceGearSetLoadCase)

    @property
    def cylindrical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_908.CylindricalGearSetLoadCase":
        from mastapy._private.gears.load_case.cylindrical import _908

        return self.__parent__._cast(_908.CylindricalGearSetLoadCase)

    @property
    def conical_gear_set_load_case(self: "CastSelf") -> "_911.ConicalGearSetLoadCase":
        from mastapy._private.gears.load_case.conical import _911

        return self.__parent__._cast(_911.ConicalGearSetLoadCase)

    @property
    def concept_gear_set_load_case(self: "CastSelf") -> "_914.ConceptGearSetLoadCase":
        from mastapy._private.gears.load_case.concept import _914

        return self.__parent__._cast(_914.ConceptGearSetLoadCase)

    @property
    def bevel_set_load_case(self: "CastSelf") -> "_918.BevelSetLoadCase":
        from mastapy._private.gears.load_case.bevel import _918

        return self.__parent__._cast(_918.BevelSetLoadCase)

    @property
    def cylindrical_gear_set_tiff_analysis(
        self: "CastSelf",
    ) -> "_921.CylindricalGearSetTIFFAnalysis":
        from mastapy._private.gears.gear_two_d_fe_analysis import _921

        return self.__parent__._cast(_921.CylindricalGearSetTIFFAnalysis)

    @property
    def cylindrical_gear_set_tiff_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_922.CylindricalGearSetTIFFAnalysisDutyCycle":
        from mastapy._private.gears.gear_two_d_fe_analysis import _922

        return self.__parent__._cast(_922.CylindricalGearSetTIFFAnalysisDutyCycle)

    @property
    def face_gear_set_micro_geometry(
        self: "CastSelf",
    ) -> "_1022.FaceGearSetMicroGeometry":
        from mastapy._private.gears.gear_designs.face import _1022

        return self.__parent__._cast(_1022.FaceGearSetMicroGeometry)

    @property
    def cylindrical_gear_set_micro_geometry(
        self: "CastSelf",
    ) -> "_1141.CylindricalGearSetMicroGeometry":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1141

        return self.__parent__._cast(_1141.CylindricalGearSetMicroGeometry)

    @property
    def cylindrical_gear_set_micro_geometry_duty_cycle(
        self: "CastSelf",
    ) -> "_1142.CylindricalGearSetMicroGeometryDutyCycle":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1142

        return self.__parent__._cast(_1142.CylindricalGearSetMicroGeometryDutyCycle)

    @property
    def gear_set_fe_model(self: "CastSelf") -> "_1240.GearSetFEModel":
        from mastapy._private.gears.fe_model import _1240

        return self.__parent__._cast(_1240.GearSetFEModel)

    @property
    def cylindrical_gear_set_fe_model(
        self: "CastSelf",
    ) -> "_1243.CylindricalGearSetFEModel":
        from mastapy._private.gears.fe_model.cylindrical import _1243

        return self.__parent__._cast(_1243.CylindricalGearSetFEModel)

    @property
    def conical_set_fe_model(self: "CastSelf") -> "_1246.ConicalSetFEModel":
        from mastapy._private.gears.fe_model.conical import _1246

        return self.__parent__._cast(_1246.ConicalSetFEModel)

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "_1266.GearSetDesignAnalysis":
        from mastapy._private.gears.analysis import _1266

        return self.__parent__._cast(_1266.GearSetDesignAnalysis)

    @property
    def gear_set_implementation_analysis(
        self: "CastSelf",
    ) -> "_1268.GearSetImplementationAnalysis":
        from mastapy._private.gears.analysis import _1268

        return self.__parent__._cast(_1268.GearSetImplementationAnalysis)

    @property
    def gear_set_implementation_analysis_abstract(
        self: "CastSelf",
    ) -> "_1269.GearSetImplementationAnalysisAbstract":
        from mastapy._private.gears.analysis import _1269

        return self.__parent__._cast(_1269.GearSetImplementationAnalysisAbstract)

    @property
    def gear_set_implementation_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_1270.GearSetImplementationAnalysisDutyCycle":
        from mastapy._private.gears.analysis import _1270

        return self.__parent__._cast(_1270.GearSetImplementationAnalysisDutyCycle)

    @property
    def gear_set_implementation_detail(
        self: "CastSelf",
    ) -> "_1271.GearSetImplementationDetail":
        from mastapy._private.gears.analysis import _1271

        return self.__parent__._cast(_1271.GearSetImplementationDetail)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "AbstractGearSetAnalysis":
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
class AbstractGearSetAnalysis(_0.APIBase):
    """AbstractGearSetAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_GEAR_SET_ANALYSIS

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
    def cast_to(self: "Self") -> "_Cast_AbstractGearSetAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AbstractGearSetAnalysis
        """
        return _Cast_AbstractGearSetAnalysis(self)
