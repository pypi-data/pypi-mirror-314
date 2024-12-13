"""GearSetDesignAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.analysis import _1257

_GEAR_SET_DESIGN_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearSetDesignAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1268, _1269, _1270, _1271
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

    Self = TypeVar("Self", bound="GearSetDesignAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="GearSetDesignAnalysis._Cast_GearSetDesignAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetDesignAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetDesignAnalysis:
    """Special nested class for casting GearSetDesignAnalysis to subclasses."""

    __parent__: "GearSetDesignAnalysis"

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1257.AbstractGearSetAnalysis":
        return self.__parent__._cast(_1257.AbstractGearSetAnalysis)

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
    def gear_set_design_analysis(self: "CastSelf") -> "GearSetDesignAnalysis":
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
class GearSetDesignAnalysis(_1257.AbstractGearSetAnalysis):
    """GearSetDesignAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_DESIGN_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetDesignAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearSetDesignAnalysis
        """
        return _Cast_GearSetDesignAnalysis(self)
