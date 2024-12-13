"""ShaftSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._math.vector_3d import Vector3D
from mastapy._private.system_model.analyses_and_results.system_deflections import _2776

_SHAFT_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "ShaftSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, Iterable, List, Type, TypeVar

    from mastapy._private.math_utility.measured_vectors import _1611
    from mastapy._private.shafts import _19, _34
    from mastapy._private.system_model.analyses_and_results import _2740, _2742, _2746
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7719,
        _7721,
        _7722,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4244
    from mastapy._private.system_model.analyses_and_results.static_loads import _7105
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2775,
        _2804,
        _2876,
        _2893,
        _2894,
    )
    from mastapy._private.system_model.part_model.shaft_model import _2543

    Self = TypeVar("Self", bound="ShaftSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf", bound="ShaftSystemDeflection._Cast_ShaftSystemDeflection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftSystemDeflection:
    """Special nested class for casting ShaftSystemDeflection to subclasses."""

    __parent__: "ShaftSystemDeflection"

    @property
    def abstract_shaft_system_deflection(
        self: "CastSelf",
    ) -> "_2776.AbstractShaftSystemDeflection":
        return self.__parent__._cast(_2776.AbstractShaftSystemDeflection)

    @property
    def abstract_shaft_or_housing_system_deflection(
        self: "CastSelf",
    ) -> "_2775.AbstractShaftOrHousingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2775,
        )

        return self.__parent__._cast(_2775.AbstractShaftOrHousingSystemDeflection)

    @property
    def component_system_deflection(
        self: "CastSelf",
    ) -> "_2804.ComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2804,
        )

        return self.__parent__._cast(_2804.ComponentSystemDeflection)

    @property
    def part_system_deflection(self: "CastSelf") -> "_2876.PartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2876,
        )

        return self.__parent__._cast(_2876.PartSystemDeflection)

    @property
    def part_fe_analysis(self: "CastSelf") -> "_7721.PartFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7721,
        )

        return self.__parent__._cast(_7721.PartFEAnalysis)

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
    def shaft_system_deflection(self: "CastSelf") -> "ShaftSystemDeflection":
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
class ShaftSystemDeflection(_2776.AbstractShaftSystemDeflection):
    """ShaftSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def two_d_drawing_showing_axial_forces_with_mounted_components(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TwoDDrawingShowingAxialForcesWithMountedComponents"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def first_node_deflection_angular(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FirstNodeDeflectionAngular")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def first_node_deflection_linear(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FirstNodeDeflectionLinear")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def flexible_pin_additional_deflection_amplitude(
        self: "Self",
    ) -> "Iterable[Vector3D]":
        """Iterable[Vector3D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FlexiblePinAdditionalDeflectionAmplitude"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_iterable(temp, Vector3D)

        if value is None:
            return None

        return value

    @property
    def number_of_cycles_for_fatigue(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfCyclesForFatigue")

        if temp is None:
            return 0.0

        return temp

    @property
    def pin_tangential_oscillation_amplitude(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinTangentialOscillationAmplitude")

        if temp is None:
            return 0.0

        return temp

    @property
    def shaft_rating_method(self: "Self") -> "_34.ShaftRatingMethod":
        """mastapy.shafts.ShaftRatingMethod

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftRatingMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Shafts.ShaftRatingMethod")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.shafts._34", "ShaftRatingMethod"
        )(value)

    @property
    def component_design(self: "Self") -> "_2543.Shaft":
        """mastapy.system_model.part_model.shaft_model.Shaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_detailed_analysis(self: "Self") -> "_19.ShaftDamageResults":
        """mastapy.shafts.ShaftDamageResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDetailedAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: "Self") -> "_7105.ShaftLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def power_flow_results(self: "Self") -> "_4244.ShaftPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.ShaftPowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlowResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def shaft_section_end_with_worst_fatigue_safety_factor(
        self: "Self",
    ) -> "_2893.ShaftSectionEndResultsSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.ShaftSectionEndResultsSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ShaftSectionEndWithWorstFatigueSafetyFactor"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def shaft_section_end_with_worst_fatigue_safety_factor_for_infinite_life(
        self: "Self",
    ) -> "_2893.ShaftSectionEndResultsSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.ShaftSectionEndResultsSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ShaftSectionEndWithWorstFatigueSafetyFactorForInfiniteLife"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def shaft_section_end_with_worst_static_safety_factor(
        self: "Self",
    ) -> "_2893.ShaftSectionEndResultsSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.ShaftSectionEndResultsSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ShaftSectionEndWithWorstStaticSafetyFactor"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def mounted_components_applying_torque(self: "Self") -> "List[_1611.ForceResults]":
        """List[mastapy.math_utility.measured_vectors.ForceResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MountedComponentsApplyingTorque")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def planetaries(self: "Self") -> "List[ShaftSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ShaftSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planetaries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def shaft_section_end_results_by_offset_with_worst_safety_factor(
        self: "Self",
    ) -> "List[_2893.ShaftSectionEndResultsSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ShaftSectionEndResultsSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ShaftSectionEndResultsByOffsetWithWorstSafetyFactor"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def shaft_section_results(
        self: "Self",
    ) -> "List[_2894.ShaftSectionSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ShaftSectionSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftSectionResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    def calculate_outer_diameter_to_achieve_fatigue_safety_factor_requirement(
        self: "Self",
    ) -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped,
            "CalculateOuterDiameterToAchieveFatigueSafetyFactorRequirement",
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_ShaftSystemDeflection
        """
        return _Cast_ShaftSystemDeflection(self)
