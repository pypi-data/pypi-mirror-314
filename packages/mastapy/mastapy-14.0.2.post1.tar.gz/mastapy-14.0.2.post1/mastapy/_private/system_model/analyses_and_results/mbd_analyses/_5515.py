"""BearingMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private._math.vector_3d import Vector3D
from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5545

_BEARING_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "BearingMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740, _2742, _2746
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7719,
        _7723,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5534,
        _5596,
        _5599,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses.reporting import (
        _5658,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _6972
    from mastapy._private.system_model.part_model import _2497

    Self = TypeVar("Self", bound="BearingMultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BearingMultibodyDynamicsAnalysis._Cast_BearingMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BearingMultibodyDynamicsAnalysis:
    """Special nested class for casting BearingMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "BearingMultibodyDynamicsAnalysis"

    @property
    def connector_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5545.ConnectorMultibodyDynamicsAnalysis":
        return self.__parent__._cast(_5545.ConnectorMultibodyDynamicsAnalysis)

    @property
    def mountable_component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5596.MountableComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5596,
        )

        return self.__parent__._cast(_5596.MountableComponentMultibodyDynamicsAnalysis)

    @property
    def component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5534.ComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5534,
        )

        return self.__parent__._cast(_5534.ComponentMultibodyDynamicsAnalysis)

    @property
    def part_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5599.PartMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5599,
        )

        return self.__parent__._cast(_5599.PartMultibodyDynamicsAnalysis)

    @property
    def part_time_series_load_analysis_case(
        self: "CastSelf",
    ) -> "_7723.PartTimeSeriesLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7723,
        )

        return self.__parent__._cast(_7723.PartTimeSeriesLoadAnalysisCase)

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
    def bearing_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "BearingMultibodyDynamicsAnalysis":
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
class BearingMultibodyDynamicsAnalysis(_5545.ConnectorMultibodyDynamicsAnalysis):
    """BearingMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING_MULTIBODY_DYNAMICS_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def ansiabma_adjusted_rating_life_damage_rate(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ANSIABMAAdjustedRatingLifeDamageRate"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def ansiabma_adjusted_rating_life_damage_rate_during_analysis(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ANSIABMAAdjustedRatingLifeDamageRateDuringAnalysis"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def ansiabma_basic_rating_life_damage_rate(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ANSIABMABasicRatingLifeDamageRate")

        if temp is None:
            return 0.0

        return temp

    @property
    def ansiabma_basic_rating_life_damage_rate_during_analysis(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ANSIABMABasicRatingLifeDamageRateDuringAnalysis"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def ansiabma_static_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ANSIABMAStaticSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def ansiabma_static_safety_factor_at_current_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ANSIABMAStaticSafetyFactorAtCurrentTime"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def element_orbital_position(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementOrbitalPosition")

        if temp is None:
            return 0.0

        return temp

    @property
    def element_orbital_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementOrbitalVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    def element_passing_frequency(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementPassingFrequency")

        if temp is None:
            return 0.0

        return temp

    @property
    def force(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Force")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def force_angular(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceAngular")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def iso2812007_basic_rating_life_damage_during_analysis(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO2812007BasicRatingLifeDamageDuringAnalysis"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def iso2812007_basic_rating_life_damage_rate(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO2812007BasicRatingLifeDamageRate"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def iso2812007_modified_rating_life_damage_during_analysis(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO2812007ModifiedRatingLifeDamageDuringAnalysis"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def iso2812007_modified_rating_life_damage_rate(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO2812007ModifiedRatingLifeDamageRate"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def iso762006_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO762006SafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def iso762006_safety_factor_at_current_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO762006SafetyFactorAtCurrentTime"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def isots162812008_basic_reference_rating_life_damage_during_analysis(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISOTS162812008BasicReferenceRatingLifeDamageDuringAnalysis"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def isots162812008_basic_reference_rating_life_damage_rate(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISOTS162812008BasicReferenceRatingLifeDamageRate"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def isots162812008_modified_reference_rating_life_damage_during_analysis(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "ISOTS162812008ModifiedReferenceRatingLifeDamageDuringAnalysis",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def isots162812008_modified_reference_rating_life_damage_rate(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISOTS162812008ModifiedReferenceRatingLifeDamageRate"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_element_normal_stress_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumElementNormalStressInner")

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_element_normal_stress_inner_at_current_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumElementNormalStressInnerAtCurrentTime"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_element_normal_stress_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumElementNormalStressOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_element_normal_stress_outer_at_current_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumElementNormalStressOuterAtCurrentTime"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_static_contact_stress_inner_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumStaticContactStressInnerSafetyFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_static_contact_stress_inner_safety_factor_at_current_time(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumStaticContactStressInnerSafetyFactorAtCurrentTime"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_static_contact_stress_outer_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumStaticContactStressOuterSafetyFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_static_contact_stress_outer_safety_factor_at_current_time(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumStaticContactStressOuterSafetyFactorAtCurrentTime"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_time_step(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumTimeStep")

        if temp is None:
            return 0.0

        return temp

    @property
    def relative_acceleration(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeAcceleration")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def relative_displacement(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeDisplacement")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def relative_tilt(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeTilt")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def relative_velocity(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeVelocity")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def component_design(self: "Self") -> "_2497.Bearing":
        """mastapy.system_model.part_model.Bearing

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: "Self") -> "_6972.BearingLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def peak_dynamic_force(self: "Self") -> "_5658.DynamicForceVector3DResult":
        """mastapy.system_model.analyses_and_results.mbd_analyses.reporting.DynamicForceVector3DResult

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PeakDynamicForce")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def planetaries(self: "Self") -> "List[BearingMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.BearingMultibodyDynamicsAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_BearingMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_BearingMultibodyDynamicsAnalysis
        """
        return _Cast_BearingMultibodyDynamicsAnalysis(self)
