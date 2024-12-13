"""GearSetImplementationAnalysisAbstract"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.analysis import _1266

_GEAR_SET_IMPLEMENTATION_ANALYSIS_ABSTRACT = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearSetImplementationAnalysisAbstract"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1257, _1268, _1270
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1142
    from mastapy._private.gears.ltca import _871
    from mastapy._private.gears.ltca.conical import _893
    from mastapy._private.gears.ltca.cylindrical import _885, _887
    from mastapy._private.gears.manufacturing.bevel import _815
    from mastapy._private.gears.manufacturing.cylindrical import _645, _646

    Self = TypeVar("Self", bound="GearSetImplementationAnalysisAbstract")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearSetImplementationAnalysisAbstract._Cast_GearSetImplementationAnalysisAbstract",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetImplementationAnalysisAbstract",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetImplementationAnalysisAbstract:
    """Special nested class for casting GearSetImplementationAnalysisAbstract to subclasses."""

    __parent__: "GearSetImplementationAnalysisAbstract"

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "_1266.GearSetDesignAnalysis":
        return self.__parent__._cast(_1266.GearSetDesignAnalysis)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1257.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1257

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
    def conical_set_manufacturing_analysis(
        self: "CastSelf",
    ) -> "_815.ConicalSetManufacturingAnalysis":
        from mastapy._private.gears.manufacturing.bevel import _815

        return self.__parent__._cast(_815.ConicalSetManufacturingAnalysis)

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
    def cylindrical_gear_set_micro_geometry_duty_cycle(
        self: "CastSelf",
    ) -> "_1142.CylindricalGearSetMicroGeometryDutyCycle":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1142

        return self.__parent__._cast(_1142.CylindricalGearSetMicroGeometryDutyCycle)

    @property
    def gear_set_implementation_analysis(
        self: "CastSelf",
    ) -> "_1268.GearSetImplementationAnalysis":
        from mastapy._private.gears.analysis import _1268

        return self.__parent__._cast(_1268.GearSetImplementationAnalysis)

    @property
    def gear_set_implementation_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_1270.GearSetImplementationAnalysisDutyCycle":
        from mastapy._private.gears.analysis import _1270

        return self.__parent__._cast(_1270.GearSetImplementationAnalysisDutyCycle)

    @property
    def gear_set_implementation_analysis_abstract(
        self: "CastSelf",
    ) -> "GearSetImplementationAnalysisAbstract":
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
class GearSetImplementationAnalysisAbstract(_1266.GearSetDesignAnalysis):
    """GearSetImplementationAnalysisAbstract

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_IMPLEMENTATION_ANALYSIS_ABSTRACT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetImplementationAnalysisAbstract":
        """Cast to another type.

        Returns:
            _Cast_GearSetImplementationAnalysisAbstract
        """
        return _Cast_GearSetImplementationAnalysisAbstract(self)
