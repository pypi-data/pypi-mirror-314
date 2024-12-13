"""GearSetImplementationAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.analysis import _1269

_GEAR_SET_IMPLEMENTATION_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearSetImplementationAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private import _7733
    from mastapy._private.gears.analysis import _1257, _1266
    from mastapy._private.gears.ltca import _871
    from mastapy._private.gears.ltca.conical import _893
    from mastapy._private.gears.ltca.cylindrical import _885, _887
    from mastapy._private.gears.manufacturing.bevel import _815
    from mastapy._private.gears.manufacturing.cylindrical import _646

    Self = TypeVar("Self", bound="GearSetImplementationAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearSetImplementationAnalysis._Cast_GearSetImplementationAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetImplementationAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetImplementationAnalysis:
    """Special nested class for casting GearSetImplementationAnalysis to subclasses."""

    __parent__: "GearSetImplementationAnalysis"

    @property
    def gear_set_implementation_analysis_abstract(
        self: "CastSelf",
    ) -> "_1269.GearSetImplementationAnalysisAbstract":
        return self.__parent__._cast(_1269.GearSetImplementationAnalysisAbstract)

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "_1266.GearSetDesignAnalysis":
        from mastapy._private.gears.analysis import _1266

        return self.__parent__._cast(_1266.GearSetDesignAnalysis)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1257.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1257

        return self.__parent__._cast(_1257.AbstractGearSetAnalysis)

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
    def gear_set_implementation_analysis(
        self: "CastSelf",
    ) -> "GearSetImplementationAnalysis":
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
class GearSetImplementationAnalysis(_1269.GearSetImplementationAnalysisAbstract):
    """GearSetImplementationAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_IMPLEMENTATION_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def valid_results_ready(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ValidResultsReady")

        if temp is None:
            return False

        return temp

    @enforce_parameter_types
    def perform_analysis(self: "Self", run_all_planetary_meshes: "bool" = True) -> None:
        """Method does not return.

        Args:
            run_all_planetary_meshes (bool, optional)
        """
        run_all_planetary_meshes = bool(run_all_planetary_meshes)
        pythonnet_method_call(
            self.wrapped,
            "PerformAnalysis",
            run_all_planetary_meshes if run_all_planetary_meshes else False,
        )

    @enforce_parameter_types
    def perform_analysis_with_progress(
        self: "Self", run_all_planetary_meshes: "bool", progress: "_7733.TaskProgress"
    ) -> None:
        """Method does not return.

        Args:
            run_all_planetary_meshes (bool)
            progress (mastapy.TaskProgress)
        """
        run_all_planetary_meshes = bool(run_all_planetary_meshes)
        pythonnet_method_call(
            self.wrapped,
            "PerformAnalysisWithProgress",
            run_all_planetary_meshes if run_all_planetary_meshes else False,
            progress.wrapped if progress else None,
        )

    @enforce_parameter_types
    def results_ready_for(
        self: "Self", run_all_planetary_meshes: "bool" = True
    ) -> "bool":
        """bool

        Args:
            run_all_planetary_meshes (bool, optional)
        """
        run_all_planetary_meshes = bool(run_all_planetary_meshes)
        method_result = pythonnet_method_call(
            self.wrapped,
            "ResultsReadyFor",
            run_all_planetary_meshes if run_all_planetary_meshes else False,
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetImplementationAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearSetImplementationAnalysis
        """
        return _Cast_GearSetImplementationAnalysis(self)
