"""GearDesignAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.analysis import _1255

_GEAR_DESIGN_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearDesignAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1259, _1260, _1261
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

    Self = TypeVar("Self", bound="GearDesignAnalysis")
    CastSelf = TypeVar("CastSelf", bound="GearDesignAnalysis._Cast_GearDesignAnalysis")


__docformat__ = "restructuredtext en"
__all__ = ("GearDesignAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearDesignAnalysis:
    """Special nested class for casting GearDesignAnalysis to subclasses."""

    __parent__: "GearDesignAnalysis"

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1255.AbstractGearAnalysis":
        return self.__parent__._cast(_1255.AbstractGearAnalysis)

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
    def gear_design_analysis(self: "CastSelf") -> "GearDesignAnalysis":
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
class GearDesignAnalysis(_1255.AbstractGearAnalysis):
    """GearDesignAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_DESIGN_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearDesignAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearDesignAnalysis
        """
        return _Cast_GearDesignAnalysis(self)
