"""AbstractGearAnalysis"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ABSTRACT_GEAR_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "AbstractGearAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1258, _1259, _1260, _1261
    from mastapy._private.gears.fe_model import _1237
    from mastapy._private.gears.fe_model.conical import _1244
    from mastapy._private.gears.fe_model.cylindrical import _1241
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1134,
        _1135,
        _1136,
        _1138,
    )
    from mastapy._private.gears.gear_designs.face import _1019
    from mastapy._private.gears.gear_two_d_fe_analysis import _923, _924
    from mastapy._private.gears.load_case import _898
    from mastapy._private.gears.load_case.bevel import _916
    from mastapy._private.gears.load_case.concept import _913
    from mastapy._private.gears.load_case.conical import _910
    from mastapy._private.gears.load_case.cylindrical import _907
    from mastapy._private.gears.load_case.face import _904
    from mastapy._private.gears.load_case.worm import _901
    from mastapy._private.gears.ltca import _865
    from mastapy._private.gears.ltca.conical import _892
    from mastapy._private.gears.ltca.cylindrical import _881
    from mastapy._private.gears.manufacturing.bevel import (
        _800,
        _801,
        _802,
        _803,
        _813,
        _814,
        _819,
    )
    from mastapy._private.gears.manufacturing.cylindrical import _637, _641, _642
    from mastapy._private.gears.rating import _366, _370, _374
    from mastapy._private.gears.rating.agma_gleason_conical import _579
    from mastapy._private.gears.rating.bevel import _568
    from mastapy._private.gears.rating.concept import _561, _564
    from mastapy._private.gears.rating.conical import _551, _553
    from mastapy._private.gears.rating.cylindrical import _468, _473
    from mastapy._private.gears.rating.face import _458, _461
    from mastapy._private.gears.rating.hypoid import _452
    from mastapy._private.gears.rating.klingelnberg_conical import _425
    from mastapy._private.gears.rating.klingelnberg_hypoid import _422
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _419
    from mastapy._private.gears.rating.spiral_bevel import _416
    from mastapy._private.gears.rating.straight_bevel import _409
    from mastapy._private.gears.rating.straight_bevel_diff import _412
    from mastapy._private.gears.rating.worm import _385, _387
    from mastapy._private.gears.rating.zerol_bevel import _383

    Self = TypeVar("Self", bound="AbstractGearAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="AbstractGearAnalysis._Cast_AbstractGearAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractGearAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractGearAnalysis:
    """Special nested class for casting AbstractGearAnalysis to subclasses."""

    __parent__: "AbstractGearAnalysis"

    @property
    def abstract_gear_rating(self: "CastSelf") -> "_366.AbstractGearRating":
        from mastapy._private.gears.rating import _366

        return self.__parent__._cast(_366.AbstractGearRating)

    @property
    def gear_duty_cycle_rating(self: "CastSelf") -> "_370.GearDutyCycleRating":
        from mastapy._private.gears.rating import _370

        return self.__parent__._cast(_370.GearDutyCycleRating)

    @property
    def gear_rating(self: "CastSelf") -> "_374.GearRating":
        from mastapy._private.gears.rating import _374

        return self.__parent__._cast(_374.GearRating)

    @property
    def zerol_bevel_gear_rating(self: "CastSelf") -> "_383.ZerolBevelGearRating":
        from mastapy._private.gears.rating.zerol_bevel import _383

        return self.__parent__._cast(_383.ZerolBevelGearRating)

    @property
    def worm_gear_duty_cycle_rating(self: "CastSelf") -> "_385.WormGearDutyCycleRating":
        from mastapy._private.gears.rating.worm import _385

        return self.__parent__._cast(_385.WormGearDutyCycleRating)

    @property
    def worm_gear_rating(self: "CastSelf") -> "_387.WormGearRating":
        from mastapy._private.gears.rating.worm import _387

        return self.__parent__._cast(_387.WormGearRating)

    @property
    def straight_bevel_gear_rating(self: "CastSelf") -> "_409.StraightBevelGearRating":
        from mastapy._private.gears.rating.straight_bevel import _409

        return self.__parent__._cast(_409.StraightBevelGearRating)

    @property
    def straight_bevel_diff_gear_rating(
        self: "CastSelf",
    ) -> "_412.StraightBevelDiffGearRating":
        from mastapy._private.gears.rating.straight_bevel_diff import _412

        return self.__parent__._cast(_412.StraightBevelDiffGearRating)

    @property
    def spiral_bevel_gear_rating(self: "CastSelf") -> "_416.SpiralBevelGearRating":
        from mastapy._private.gears.rating.spiral_bevel import _416

        return self.__parent__._cast(_416.SpiralBevelGearRating)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_rating(
        self: "CastSelf",
    ) -> "_419.KlingelnbergCycloPalloidSpiralBevelGearRating":
        from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _419

        return self.__parent__._cast(_419.KlingelnbergCycloPalloidSpiralBevelGearRating)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_rating(
        self: "CastSelf",
    ) -> "_422.KlingelnbergCycloPalloidHypoidGearRating":
        from mastapy._private.gears.rating.klingelnberg_hypoid import _422

        return self.__parent__._cast(_422.KlingelnbergCycloPalloidHypoidGearRating)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_rating(
        self: "CastSelf",
    ) -> "_425.KlingelnbergCycloPalloidConicalGearRating":
        from mastapy._private.gears.rating.klingelnberg_conical import _425

        return self.__parent__._cast(_425.KlingelnbergCycloPalloidConicalGearRating)

    @property
    def hypoid_gear_rating(self: "CastSelf") -> "_452.HypoidGearRating":
        from mastapy._private.gears.rating.hypoid import _452

        return self.__parent__._cast(_452.HypoidGearRating)

    @property
    def face_gear_duty_cycle_rating(self: "CastSelf") -> "_458.FaceGearDutyCycleRating":
        from mastapy._private.gears.rating.face import _458

        return self.__parent__._cast(_458.FaceGearDutyCycleRating)

    @property
    def face_gear_rating(self: "CastSelf") -> "_461.FaceGearRating":
        from mastapy._private.gears.rating.face import _461

        return self.__parent__._cast(_461.FaceGearRating)

    @property
    def cylindrical_gear_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_468.CylindricalGearDutyCycleRating":
        from mastapy._private.gears.rating.cylindrical import _468

        return self.__parent__._cast(_468.CylindricalGearDutyCycleRating)

    @property
    def cylindrical_gear_rating(self: "CastSelf") -> "_473.CylindricalGearRating":
        from mastapy._private.gears.rating.cylindrical import _473

        return self.__parent__._cast(_473.CylindricalGearRating)

    @property
    def conical_gear_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_551.ConicalGearDutyCycleRating":
        from mastapy._private.gears.rating.conical import _551

        return self.__parent__._cast(_551.ConicalGearDutyCycleRating)

    @property
    def conical_gear_rating(self: "CastSelf") -> "_553.ConicalGearRating":
        from mastapy._private.gears.rating.conical import _553

        return self.__parent__._cast(_553.ConicalGearRating)

    @property
    def concept_gear_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_561.ConceptGearDutyCycleRating":
        from mastapy._private.gears.rating.concept import _561

        return self.__parent__._cast(_561.ConceptGearDutyCycleRating)

    @property
    def concept_gear_rating(self: "CastSelf") -> "_564.ConceptGearRating":
        from mastapy._private.gears.rating.concept import _564

        return self.__parent__._cast(_564.ConceptGearRating)

    @property
    def bevel_gear_rating(self: "CastSelf") -> "_568.BevelGearRating":
        from mastapy._private.gears.rating.bevel import _568

        return self.__parent__._cast(_568.BevelGearRating)

    @property
    def agma_gleason_conical_gear_rating(
        self: "CastSelf",
    ) -> "_579.AGMAGleasonConicalGearRating":
        from mastapy._private.gears.rating.agma_gleason_conical import _579

        return self.__parent__._cast(_579.AGMAGleasonConicalGearRating)

    @property
    def cylindrical_gear_manufacturing_config(
        self: "CastSelf",
    ) -> "_637.CylindricalGearManufacturingConfig":
        from mastapy._private.gears.manufacturing.cylindrical import _637

        return self.__parent__._cast(_637.CylindricalGearManufacturingConfig)

    @property
    def cylindrical_manufactured_gear_duty_cycle(
        self: "CastSelf",
    ) -> "_641.CylindricalManufacturedGearDutyCycle":
        from mastapy._private.gears.manufacturing.cylindrical import _641

        return self.__parent__._cast(_641.CylindricalManufacturedGearDutyCycle)

    @property
    def cylindrical_manufactured_gear_load_case(
        self: "CastSelf",
    ) -> "_642.CylindricalManufacturedGearLoadCase":
        from mastapy._private.gears.manufacturing.cylindrical import _642

        return self.__parent__._cast(_642.CylindricalManufacturedGearLoadCase)

    @property
    def conical_gear_manufacturing_analysis(
        self: "CastSelf",
    ) -> "_800.ConicalGearManufacturingAnalysis":
        from mastapy._private.gears.manufacturing.bevel import _800

        return self.__parent__._cast(_800.ConicalGearManufacturingAnalysis)

    @property
    def conical_gear_manufacturing_config(
        self: "CastSelf",
    ) -> "_801.ConicalGearManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _801

        return self.__parent__._cast(_801.ConicalGearManufacturingConfig)

    @property
    def conical_gear_micro_geometry_config(
        self: "CastSelf",
    ) -> "_802.ConicalGearMicroGeometryConfig":
        from mastapy._private.gears.manufacturing.bevel import _802

        return self.__parent__._cast(_802.ConicalGearMicroGeometryConfig)

    @property
    def conical_gear_micro_geometry_config_base(
        self: "CastSelf",
    ) -> "_803.ConicalGearMicroGeometryConfigBase":
        from mastapy._private.gears.manufacturing.bevel import _803

        return self.__parent__._cast(_803.ConicalGearMicroGeometryConfigBase)

    @property
    def conical_pinion_manufacturing_config(
        self: "CastSelf",
    ) -> "_813.ConicalPinionManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _813

        return self.__parent__._cast(_813.ConicalPinionManufacturingConfig)

    @property
    def conical_pinion_micro_geometry_config(
        self: "CastSelf",
    ) -> "_814.ConicalPinionMicroGeometryConfig":
        from mastapy._private.gears.manufacturing.bevel import _814

        return self.__parent__._cast(_814.ConicalPinionMicroGeometryConfig)

    @property
    def conical_wheel_manufacturing_config(
        self: "CastSelf",
    ) -> "_819.ConicalWheelManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _819

        return self.__parent__._cast(_819.ConicalWheelManufacturingConfig)

    @property
    def gear_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_865.GearLoadDistributionAnalysis":
        from mastapy._private.gears.ltca import _865

        return self.__parent__._cast(_865.GearLoadDistributionAnalysis)

    @property
    def cylindrical_gear_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_881.CylindricalGearLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.cylindrical import _881

        return self.__parent__._cast(_881.CylindricalGearLoadDistributionAnalysis)

    @property
    def conical_gear_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_892.ConicalGearLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.conical import _892

        return self.__parent__._cast(_892.ConicalGearLoadDistributionAnalysis)

    @property
    def gear_load_case_base(self: "CastSelf") -> "_898.GearLoadCaseBase":
        from mastapy._private.gears.load_case import _898

        return self.__parent__._cast(_898.GearLoadCaseBase)

    @property
    def worm_gear_load_case(self: "CastSelf") -> "_901.WormGearLoadCase":
        from mastapy._private.gears.load_case.worm import _901

        return self.__parent__._cast(_901.WormGearLoadCase)

    @property
    def face_gear_load_case(self: "CastSelf") -> "_904.FaceGearLoadCase":
        from mastapy._private.gears.load_case.face import _904

        return self.__parent__._cast(_904.FaceGearLoadCase)

    @property
    def cylindrical_gear_load_case(self: "CastSelf") -> "_907.CylindricalGearLoadCase":
        from mastapy._private.gears.load_case.cylindrical import _907

        return self.__parent__._cast(_907.CylindricalGearLoadCase)

    @property
    def conical_gear_load_case(self: "CastSelf") -> "_910.ConicalGearLoadCase":
        from mastapy._private.gears.load_case.conical import _910

        return self.__parent__._cast(_910.ConicalGearLoadCase)

    @property
    def concept_gear_load_case(self: "CastSelf") -> "_913.ConceptGearLoadCase":
        from mastapy._private.gears.load_case.concept import _913

        return self.__parent__._cast(_913.ConceptGearLoadCase)

    @property
    def bevel_load_case(self: "CastSelf") -> "_916.BevelLoadCase":
        from mastapy._private.gears.load_case.bevel import _916

        return self.__parent__._cast(_916.BevelLoadCase)

    @property
    def cylindrical_gear_tiff_analysis(
        self: "CastSelf",
    ) -> "_923.CylindricalGearTIFFAnalysis":
        from mastapy._private.gears.gear_two_d_fe_analysis import _923

        return self.__parent__._cast(_923.CylindricalGearTIFFAnalysis)

    @property
    def cylindrical_gear_tiff_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_924.CylindricalGearTIFFAnalysisDutyCycle":
        from mastapy._private.gears.gear_two_d_fe_analysis import _924

        return self.__parent__._cast(_924.CylindricalGearTIFFAnalysisDutyCycle)

    @property
    def face_gear_micro_geometry(self: "CastSelf") -> "_1019.FaceGearMicroGeometry":
        from mastapy._private.gears.gear_designs.face import _1019

        return self.__parent__._cast(_1019.FaceGearMicroGeometry)

    @property
    def cylindrical_gear_micro_geometry(
        self: "CastSelf",
    ) -> "_1134.CylindricalGearMicroGeometry":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1134

        return self.__parent__._cast(_1134.CylindricalGearMicroGeometry)

    @property
    def cylindrical_gear_micro_geometry_base(
        self: "CastSelf",
    ) -> "_1135.CylindricalGearMicroGeometryBase":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1135

        return self.__parent__._cast(_1135.CylindricalGearMicroGeometryBase)

    @property
    def cylindrical_gear_micro_geometry_duty_cycle(
        self: "CastSelf",
    ) -> "_1136.CylindricalGearMicroGeometryDutyCycle":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1136

        return self.__parent__._cast(_1136.CylindricalGearMicroGeometryDutyCycle)

    @property
    def cylindrical_gear_micro_geometry_per_tooth(
        self: "CastSelf",
    ) -> "_1138.CylindricalGearMicroGeometryPerTooth":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1138

        return self.__parent__._cast(_1138.CylindricalGearMicroGeometryPerTooth)

    @property
    def gear_fe_model(self: "CastSelf") -> "_1237.GearFEModel":
        from mastapy._private.gears.fe_model import _1237

        return self.__parent__._cast(_1237.GearFEModel)

    @property
    def cylindrical_gear_fe_model(self: "CastSelf") -> "_1241.CylindricalGearFEModel":
        from mastapy._private.gears.fe_model.cylindrical import _1241

        return self.__parent__._cast(_1241.CylindricalGearFEModel)

    @property
    def conical_gear_fe_model(self: "CastSelf") -> "_1244.ConicalGearFEModel":
        from mastapy._private.gears.fe_model.conical import _1244

        return self.__parent__._cast(_1244.ConicalGearFEModel)

    @property
    def gear_design_analysis(self: "CastSelf") -> "_1258.GearDesignAnalysis":
        from mastapy._private.gears.analysis import _1258

        return self.__parent__._cast(_1258.GearDesignAnalysis)

    @property
    def gear_implementation_analysis(
        self: "CastSelf",
    ) -> "_1259.GearImplementationAnalysis":
        from mastapy._private.gears.analysis import _1259

        return self.__parent__._cast(_1259.GearImplementationAnalysis)

    @property
    def gear_implementation_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_1260.GearImplementationAnalysisDutyCycle":
        from mastapy._private.gears.analysis import _1260

        return self.__parent__._cast(_1260.GearImplementationAnalysisDutyCycle)

    @property
    def gear_implementation_detail(
        self: "CastSelf",
    ) -> "_1261.GearImplementationDetail":
        from mastapy._private.gears.analysis import _1261

        return self.__parent__._cast(_1261.GearImplementationDetail)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "AbstractGearAnalysis":
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
class AbstractGearAnalysis(_0.APIBase):
    """AbstractGearAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_GEAR_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def name_with_gear_set_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NameWithGearSetName")

        if temp is None:
            return ""

        return temp

    @property
    def planet_index(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "PlanetIndex")

        if temp is None:
            return 0

        return temp

    @planet_index.setter
    @enforce_parameter_types
    def planet_index(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "PlanetIndex", int(value) if value is not None else 0
        )

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
    def cast_to(self: "Self") -> "_Cast_AbstractGearAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AbstractGearAnalysis
        """
        return _Cast_AbstractGearAnalysis(self)
