"""GearMeshDesignAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.analysis import _1256

_GEAR_MESH_DESIGN_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearMeshDesignAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1258, _1263, _1264, _1265, _1266
    from mastapy._private.gears.fe_model import _1238
    from mastapy._private.gears.fe_model.conical import _1245
    from mastapy._private.gears.fe_model.cylindrical import _1242
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1132,
        _1133,
    )
    from mastapy._private.gears.gear_designs.face import _1018
    from mastapy._private.gears.gear_two_d_fe_analysis import _919, _920
    from mastapy._private.gears.load_case import _900
    from mastapy._private.gears.load_case.bevel import _917
    from mastapy._private.gears.load_case.concept import _915
    from mastapy._private.gears.load_case.conical import _912
    from mastapy._private.gears.load_case.cylindrical import _909
    from mastapy._private.gears.load_case.face import _906
    from mastapy._private.gears.load_case.worm import _903
    from mastapy._private.gears.ltca import _866
    from mastapy._private.gears.ltca.conical import _895
    from mastapy._private.gears.ltca.cylindrical import _882
    from mastapy._private.gears.manufacturing.bevel import _809, _810, _811, _812
    from mastapy._private.gears.manufacturing.cylindrical import _643, _644, _647

    Self = TypeVar("Self", bound="GearMeshDesignAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="GearMeshDesignAnalysis._Cast_GearMeshDesignAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshDesignAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshDesignAnalysis:
    """Special nested class for casting GearMeshDesignAnalysis to subclasses."""

    __parent__: "GearMeshDesignAnalysis"

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1256.AbstractGearMeshAnalysis":
        return self.__parent__._cast(_1256.AbstractGearMeshAnalysis)

    @property
    def cylindrical_manufactured_gear_mesh_duty_cycle(
        self: "CastSelf",
    ) -> "_643.CylindricalManufacturedGearMeshDutyCycle":
        from mastapy._private.gears.manufacturing.cylindrical import _643

        return self.__parent__._cast(_643.CylindricalManufacturedGearMeshDutyCycle)

    @property
    def cylindrical_manufactured_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_644.CylindricalManufacturedGearMeshLoadCase":
        from mastapy._private.gears.manufacturing.cylindrical import _644

        return self.__parent__._cast(_644.CylindricalManufacturedGearMeshLoadCase)

    @property
    def cylindrical_mesh_manufacturing_config(
        self: "CastSelf",
    ) -> "_647.CylindricalMeshManufacturingConfig":
        from mastapy._private.gears.manufacturing.cylindrical import _647

        return self.__parent__._cast(_647.CylindricalMeshManufacturingConfig)

    @property
    def conical_mesh_manufacturing_analysis(
        self: "CastSelf",
    ) -> "_809.ConicalMeshManufacturingAnalysis":
        from mastapy._private.gears.manufacturing.bevel import _809

        return self.__parent__._cast(_809.ConicalMeshManufacturingAnalysis)

    @property
    def conical_mesh_manufacturing_config(
        self: "CastSelf",
    ) -> "_810.ConicalMeshManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _810

        return self.__parent__._cast(_810.ConicalMeshManufacturingConfig)

    @property
    def conical_mesh_micro_geometry_config(
        self: "CastSelf",
    ) -> "_811.ConicalMeshMicroGeometryConfig":
        from mastapy._private.gears.manufacturing.bevel import _811

        return self.__parent__._cast(_811.ConicalMeshMicroGeometryConfig)

    @property
    def conical_mesh_micro_geometry_config_base(
        self: "CastSelf",
    ) -> "_812.ConicalMeshMicroGeometryConfigBase":
        from mastapy._private.gears.manufacturing.bevel import _812

        return self.__parent__._cast(_812.ConicalMeshMicroGeometryConfigBase)

    @property
    def gear_mesh_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_866.GearMeshLoadDistributionAnalysis":
        from mastapy._private.gears.ltca import _866

        return self.__parent__._cast(_866.GearMeshLoadDistributionAnalysis)

    @property
    def cylindrical_gear_mesh_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_882.CylindricalGearMeshLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.cylindrical import _882

        return self.__parent__._cast(_882.CylindricalGearMeshLoadDistributionAnalysis)

    @property
    def conical_mesh_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_895.ConicalMeshLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.conical import _895

        return self.__parent__._cast(_895.ConicalMeshLoadDistributionAnalysis)

    @property
    def mesh_load_case(self: "CastSelf") -> "_900.MeshLoadCase":
        from mastapy._private.gears.load_case import _900

        return self.__parent__._cast(_900.MeshLoadCase)

    @property
    def worm_mesh_load_case(self: "CastSelf") -> "_903.WormMeshLoadCase":
        from mastapy._private.gears.load_case.worm import _903

        return self.__parent__._cast(_903.WormMeshLoadCase)

    @property
    def face_mesh_load_case(self: "CastSelf") -> "_906.FaceMeshLoadCase":
        from mastapy._private.gears.load_case.face import _906

        return self.__parent__._cast(_906.FaceMeshLoadCase)

    @property
    def cylindrical_mesh_load_case(self: "CastSelf") -> "_909.CylindricalMeshLoadCase":
        from mastapy._private.gears.load_case.cylindrical import _909

        return self.__parent__._cast(_909.CylindricalMeshLoadCase)

    @property
    def conical_mesh_load_case(self: "CastSelf") -> "_912.ConicalMeshLoadCase":
        from mastapy._private.gears.load_case.conical import _912

        return self.__parent__._cast(_912.ConicalMeshLoadCase)

    @property
    def concept_mesh_load_case(self: "CastSelf") -> "_915.ConceptMeshLoadCase":
        from mastapy._private.gears.load_case.concept import _915

        return self.__parent__._cast(_915.ConceptMeshLoadCase)

    @property
    def bevel_mesh_load_case(self: "CastSelf") -> "_917.BevelMeshLoadCase":
        from mastapy._private.gears.load_case.bevel import _917

        return self.__parent__._cast(_917.BevelMeshLoadCase)

    @property
    def cylindrical_gear_mesh_tiff_analysis(
        self: "CastSelf",
    ) -> "_919.CylindricalGearMeshTIFFAnalysis":
        from mastapy._private.gears.gear_two_d_fe_analysis import _919

        return self.__parent__._cast(_919.CylindricalGearMeshTIFFAnalysis)

    @property
    def cylindrical_gear_mesh_tiff_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_920.CylindricalGearMeshTIFFAnalysisDutyCycle":
        from mastapy._private.gears.gear_two_d_fe_analysis import _920

        return self.__parent__._cast(_920.CylindricalGearMeshTIFFAnalysisDutyCycle)

    @property
    def face_gear_mesh_micro_geometry(
        self: "CastSelf",
    ) -> "_1018.FaceGearMeshMicroGeometry":
        from mastapy._private.gears.gear_designs.face import _1018

        return self.__parent__._cast(_1018.FaceGearMeshMicroGeometry)

    @property
    def cylindrical_gear_mesh_micro_geometry(
        self: "CastSelf",
    ) -> "_1132.CylindricalGearMeshMicroGeometry":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1132

        return self.__parent__._cast(_1132.CylindricalGearMeshMicroGeometry)

    @property
    def cylindrical_gear_mesh_micro_geometry_duty_cycle(
        self: "CastSelf",
    ) -> "_1133.CylindricalGearMeshMicroGeometryDutyCycle":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1133

        return self.__parent__._cast(_1133.CylindricalGearMeshMicroGeometryDutyCycle)

    @property
    def gear_mesh_fe_model(self: "CastSelf") -> "_1238.GearMeshFEModel":
        from mastapy._private.gears.fe_model import _1238

        return self.__parent__._cast(_1238.GearMeshFEModel)

    @property
    def cylindrical_gear_mesh_fe_model(
        self: "CastSelf",
    ) -> "_1242.CylindricalGearMeshFEModel":
        from mastapy._private.gears.fe_model.cylindrical import _1242

        return self.__parent__._cast(_1242.CylindricalGearMeshFEModel)

    @property
    def conical_mesh_fe_model(self: "CastSelf") -> "_1245.ConicalMeshFEModel":
        from mastapy._private.gears.fe_model.conical import _1245

        return self.__parent__._cast(_1245.ConicalMeshFEModel)

    @property
    def gear_mesh_implementation_analysis(
        self: "CastSelf",
    ) -> "_1263.GearMeshImplementationAnalysis":
        from mastapy._private.gears.analysis import _1263

        return self.__parent__._cast(_1263.GearMeshImplementationAnalysis)

    @property
    def gear_mesh_implementation_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_1264.GearMeshImplementationAnalysisDutyCycle":
        from mastapy._private.gears.analysis import _1264

        return self.__parent__._cast(_1264.GearMeshImplementationAnalysisDutyCycle)

    @property
    def gear_mesh_implementation_detail(
        self: "CastSelf",
    ) -> "_1265.GearMeshImplementationDetail":
        from mastapy._private.gears.analysis import _1265

        return self.__parent__._cast(_1265.GearMeshImplementationDetail)

    @property
    def gear_mesh_design_analysis(self: "CastSelf") -> "GearMeshDesignAnalysis":
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
class GearMeshDesignAnalysis(_1256.AbstractGearMeshAnalysis):
    """GearMeshDesignAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_DESIGN_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def gear_a(self: "Self") -> "_1258.GearDesignAnalysis":
        """mastapy.gears.analysis.GearDesignAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearA")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gear_b(self: "Self") -> "_1258.GearDesignAnalysis":
        """mastapy.gears.analysis.GearDesignAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearB")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gear_set(self: "Self") -> "_1266.GearSetDesignAnalysis":
        """mastapy.gears.analysis.GearSetDesignAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshDesignAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearMeshDesignAnalysis
        """
        return _Cast_GearMeshDesignAnalysis(self)
