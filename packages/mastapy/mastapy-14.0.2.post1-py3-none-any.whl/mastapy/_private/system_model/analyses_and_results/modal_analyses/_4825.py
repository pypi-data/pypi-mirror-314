"""VirtualComponentModalAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses import _4777

_VIRTUAL_COMPONENT_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "VirtualComponentModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740, _2742, _2746
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7719,
        _7722,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4714,
        _4769,
        _4770,
        _4781,
        _4788,
        _4789,
        _4824,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2926,
    )
    from mastapy._private.system_model.part_model import _2540

    Self = TypeVar("Self", bound="VirtualComponentModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="VirtualComponentModalAnalysis._Cast_VirtualComponentModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VirtualComponentModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualComponentModalAnalysis:
    """Special nested class for casting VirtualComponentModalAnalysis to subclasses."""

    __parent__: "VirtualComponentModalAnalysis"

    @property
    def mountable_component_modal_analysis(
        self: "CastSelf",
    ) -> "_4777.MountableComponentModalAnalysis":
        return self.__parent__._cast(_4777.MountableComponentModalAnalysis)

    @property
    def component_modal_analysis(self: "CastSelf") -> "_4714.ComponentModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4714,
        )

        return self.__parent__._cast(_4714.ComponentModalAnalysis)

    @property
    def part_modal_analysis(self: "CastSelf") -> "_4781.PartModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4781,
        )

        return self.__parent__._cast(_4781.PartModalAnalysis)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7722.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7722,
        )

        return self.__parent__._cast(_7722.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7719.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7719,
        )

        return self.__parent__._cast(_7719.PartAnalysisCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2746.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2746

        return self.__parent__._cast(_2746.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2742.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2742

        return self.__parent__._cast(_2742.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2740.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2740

        return self.__parent__._cast(_2740.DesignEntityAnalysis)

    @property
    def mass_disc_modal_analysis(self: "CastSelf") -> "_4769.MassDiscModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4769,
        )

        return self.__parent__._cast(_4769.MassDiscModalAnalysis)

    @property
    def measurement_component_modal_analysis(
        self: "CastSelf",
    ) -> "_4770.MeasurementComponentModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4770,
        )

        return self.__parent__._cast(_4770.MeasurementComponentModalAnalysis)

    @property
    def point_load_modal_analysis(self: "CastSelf") -> "_4788.PointLoadModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4788,
        )

        return self.__parent__._cast(_4788.PointLoadModalAnalysis)

    @property
    def power_load_modal_analysis(self: "CastSelf") -> "_4789.PowerLoadModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4789,
        )

        return self.__parent__._cast(_4789.PowerLoadModalAnalysis)

    @property
    def unbalanced_mass_modal_analysis(
        self: "CastSelf",
    ) -> "_4824.UnbalancedMassModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4824,
        )

        return self.__parent__._cast(_4824.UnbalancedMassModalAnalysis)

    @property
    def virtual_component_modal_analysis(
        self: "CastSelf",
    ) -> "VirtualComponentModalAnalysis":
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
class VirtualComponentModalAnalysis(_4777.MountableComponentModalAnalysis):
    """VirtualComponentModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VIRTUAL_COMPONENT_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2540.VirtualComponent":
        """mastapy.system_model.part_model.VirtualComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(
        self: "Self",
    ) -> "_2926.VirtualComponentSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.VirtualComponentSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_VirtualComponentModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_VirtualComponentModalAnalysis
        """
        return _Cast_VirtualComponentModalAnalysis(self)
