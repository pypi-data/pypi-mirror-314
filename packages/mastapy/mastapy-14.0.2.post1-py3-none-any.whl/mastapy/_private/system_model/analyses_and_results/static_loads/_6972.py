"""BearingLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    overridable_enum_runtime,
    utility,
)
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import enum_with_selected_value, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.bearing_results import _1998
from mastapy._private.bearings.bearing_results.rolling import _2022, _2023, _2028, _2125
from mastapy._private.materials.efficiency import _305
from mastapy._private.math_utility.hertzian_contact import _1624
from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5514
from mastapy._private.system_model.analyses_and_results.static_loads import _7003
from mastapy._private.system_model.part_model import _2498
from mastapy._private.utility import _1640

_ARRAY = python_net_import("System", "Array")
_BEARING_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BearingLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings.bearing_results.rolling import _2126
    from mastapy._private.bearings.bearing_results.rolling.dysla import _2170
    from mastapy._private.bearings.tolerances import _1971, _1975
    from mastapy._private.math_utility.measured_vectors import _1614
    from mastapy._private.system_model.analyses_and_results import _2740, _2742, _2746
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5516
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6990,
        _7079,
        _7083,
    )
    from mastapy._private.system_model.part_model import _2497, _2534

    Self = TypeVar("Self", bound="BearingLoadCase")
    CastSelf = TypeVar("CastSelf", bound="BearingLoadCase._Cast_BearingLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("BearingLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BearingLoadCase:
    """Special nested class for casting BearingLoadCase to subclasses."""

    __parent__: "BearingLoadCase"

    @property
    def connector_load_case(self: "CastSelf") -> "_7003.ConnectorLoadCase":
        return self.__parent__._cast(_7003.ConnectorLoadCase)

    @property
    def mountable_component_load_case(
        self: "CastSelf",
    ) -> "_7079.MountableComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7079,
        )

        return self.__parent__._cast(_7079.MountableComponentLoadCase)

    @property
    def component_load_case(self: "CastSelf") -> "_6990.ComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6990,
        )

        return self.__parent__._cast(_6990.ComponentLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7083.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7083,
        )

        return self.__parent__._cast(_7083.PartLoadCase)

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
    def bearing_load_case(self: "CastSelf") -> "BearingLoadCase":
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
class BearingLoadCase(_7003.ConnectorLoadCase):
    """BearingLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def axial_displacement_preload(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "AxialDisplacementPreload")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @axial_displacement_preload.setter
    @enforce_parameter_types
    def axial_displacement_preload(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AxialDisplacementPreload", value)

    @property
    def axial_force_preload(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "AxialForcePreload")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @axial_force_preload.setter
    @enforce_parameter_types
    def axial_force_preload(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AxialForcePreload", value)

    @property
    def axial_internal_clearance(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "AxialInternalClearance")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @axial_internal_clearance.setter
    @enforce_parameter_types
    def axial_internal_clearance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AxialInternalClearance", value)

    @property
    def axial_internal_clearance_tolerance_factor(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "AxialInternalClearanceToleranceFactor"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @axial_internal_clearance_tolerance_factor.setter
    @enforce_parameter_types
    def axial_internal_clearance_tolerance_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "AxialInternalClearanceToleranceFactor", value
        )

    @property
    def ball_bearing_analysis_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_BallBearingAnalysisMethod":
        """EnumWithSelectedValue[mastapy.bearings.bearing_results.rolling.BallBearingAnalysisMethod]"""
        temp = pythonnet_property_get(self.wrapped, "BallBearingAnalysisMethod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_BallBearingAnalysisMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @ball_bearing_analysis_method.setter
    @enforce_parameter_types
    def ball_bearing_analysis_method(
        self: "Self", value: "_2022.BallBearingAnalysisMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_BallBearingAnalysisMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "BallBearingAnalysisMethod", value)

    @property
    def ball_bearing_contact_calculation(
        self: "Self",
    ) -> "overridable.Overridable_BallBearingContactCalculation":
        """Overridable[mastapy.bearings.bearing_results.rolling.BallBearingContactCalculation]"""
        temp = pythonnet_property_get(self.wrapped, "BallBearingContactCalculation")

        if temp is None:
            return None

        value = overridable.Overridable_BallBearingContactCalculation.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @ball_bearing_contact_calculation.setter
    @enforce_parameter_types
    def ball_bearing_contact_calculation(
        self: "Self",
        value: "Union[_2023.BallBearingContactCalculation, Tuple[_2023.BallBearingContactCalculation, bool]]",
    ) -> None:
        wrapper_type = (
            overridable.Overridable_BallBearingContactCalculation.wrapper_type()
        )
        enclosed_type = (
            overridable.Overridable_BallBearingContactCalculation.implicit_type()
        )
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "BallBearingContactCalculation", value)

    @property
    def ball_bearing_friction_model_for_gyroscopic_moment(
        self: "Self",
    ) -> "overridable.Overridable_FrictionModelForGyroscopicMoment":
        """Overridable[mastapy.bearings.bearing_results.rolling.FrictionModelForGyroscopicMoment]"""
        temp = pythonnet_property_get(
            self.wrapped, "BallBearingFrictionModelForGyroscopicMoment"
        )

        if temp is None:
            return None

        value = overridable.Overridable_FrictionModelForGyroscopicMoment.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @ball_bearing_friction_model_for_gyroscopic_moment.setter
    @enforce_parameter_types
    def ball_bearing_friction_model_for_gyroscopic_moment(
        self: "Self",
        value: "Union[_2028.FrictionModelForGyroscopicMoment, Tuple[_2028.FrictionModelForGyroscopicMoment, bool]]",
    ) -> None:
        wrapper_type = (
            overridable.Overridable_FrictionModelForGyroscopicMoment.wrapper_type()
        )
        enclosed_type = (
            overridable.Overridable_FrictionModelForGyroscopicMoment.implicit_type()
        )
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "BallBearingFrictionModelForGyroscopicMoment", value
        )

    @property
    def bearing_element_orbit_model(
        self: "Self",
    ) -> "overridable.Overridable_BearingElementOrbitModel":
        """Overridable[mastapy.system_model.analyses_and_results.mbd_analyses.BearingElementOrbitModel]"""
        temp = pythonnet_property_get(self.wrapped, "BearingElementOrbitModel")

        if temp is None:
            return None

        value = overridable.Overridable_BearingElementOrbitModel.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @bearing_element_orbit_model.setter
    @enforce_parameter_types
    def bearing_element_orbit_model(
        self: "Self",
        value: "Union[_5514.BearingElementOrbitModel, Tuple[_5514.BearingElementOrbitModel, bool]]",
    ) -> None:
        wrapper_type = overridable.Overridable_BearingElementOrbitModel.wrapper_type()
        enclosed_type = overridable.Overridable_BearingElementOrbitModel.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "BearingElementOrbitModel", value)

    @property
    def bearing_life_adjustment_factor_for_operating_conditions(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "BearingLifeAdjustmentFactorForOperatingConditions"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @bearing_life_adjustment_factor_for_operating_conditions.setter
    @enforce_parameter_types
    def bearing_life_adjustment_factor_for_operating_conditions(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "BearingLifeAdjustmentFactorForOperatingConditions", value
        )

    @property
    def bearing_life_adjustment_factor_for_special_bearing_properties(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "BearingLifeAdjustmentFactorForSpecialBearingProperties"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @bearing_life_adjustment_factor_for_special_bearing_properties.setter
    @enforce_parameter_types
    def bearing_life_adjustment_factor_for_special_bearing_properties(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped,
            "BearingLifeAdjustmentFactorForSpecialBearingProperties",
            value,
        )

    @property
    def bearing_life_modification_factor(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "BearingLifeModificationFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @bearing_life_modification_factor.setter
    @enforce_parameter_types
    def bearing_life_modification_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "BearingLifeModificationFactor", value)

    @property
    def bearing_stiffness_model(self: "Self") -> "_5516.BearingStiffnessModel":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BearingStiffnessModel"""
        temp = pythonnet_property_get(self.wrapped, "BearingStiffnessModel")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.BearingStiffnessModel",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.mbd_analyses._5516",
            "BearingStiffnessModel",
        )(value)

    @bearing_stiffness_model.setter
    @enforce_parameter_types
    def bearing_stiffness_model(
        self: "Self", value: "_5516.BearingStiffnessModel"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.BearingStiffnessModel",
        )
        pythonnet_property_set(self.wrapped, "BearingStiffnessModel", value)

    @property
    def bearing_stiffness_model_used_in_analysis(
        self: "Self",
    ) -> "_5516.BearingStiffnessModel":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BearingStiffnessModel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BearingStiffnessModelUsedInAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.BearingStiffnessModel",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.mbd_analyses._5516",
            "BearingStiffnessModel",
        )(value)

    @property
    def coefficient_of_friction(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CoefficientOfFriction")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @coefficient_of_friction.setter
    @enforce_parameter_types
    def coefficient_of_friction(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CoefficientOfFriction", value)

    @property
    def contact_angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ContactAngle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @contact_angle.setter
    @enforce_parameter_types
    def contact_angle(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ContactAngle", value)

    @property
    def contact_stiffness(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ContactStiffness")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @contact_stiffness.setter
    @enforce_parameter_types
    def contact_stiffness(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ContactStiffness", value)

    @property
    def diametrical_clearance(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "DiametricalClearance")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @diametrical_clearance.setter
    @enforce_parameter_types
    def diametrical_clearance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DiametricalClearance", value)

    @property
    def drag_scaling_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "DragScalingFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @drag_scaling_factor.setter
    @enforce_parameter_types
    def drag_scaling_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DragScalingFactor", value)

    @property
    def efficiency_rating_method(
        self: "Self",
    ) -> "overridable.Overridable_BearingEfficiencyRatingMethod":
        """Overridable[mastapy.materials.efficiency.BearingEfficiencyRatingMethod]"""
        temp = pythonnet_property_get(self.wrapped, "EfficiencyRatingMethod")

        if temp is None:
            return None

        value = overridable.Overridable_BearingEfficiencyRatingMethod.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @efficiency_rating_method.setter
    @enforce_parameter_types
    def efficiency_rating_method(
        self: "Self",
        value: "Union[_305.BearingEfficiencyRatingMethod, Tuple[_305.BearingEfficiencyRatingMethod, bool]]",
    ) -> None:
        wrapper_type = (
            overridable.Overridable_BearingEfficiencyRatingMethod.wrapper_type()
        )
        enclosed_type = (
            overridable.Overridable_BearingEfficiencyRatingMethod.implicit_type()
        )
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "EfficiencyRatingMethod", value)

    @property
    def element_temperature(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ElementTemperature")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @element_temperature.setter
    @enforce_parameter_types
    def element_temperature(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ElementTemperature", value)

    @property
    def first_element_angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "FirstElementAngle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @first_element_angle.setter
    @enforce_parameter_types
    def first_element_angle(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "FirstElementAngle", value)

    @property
    def force_to_be_considered_axially_loaded_in_skf_loss_model(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "ForceToBeConsideredAxiallyLoadedInSKFLossModel"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @force_to_be_considered_axially_loaded_in_skf_loss_model.setter
    @enforce_parameter_types
    def force_to_be_considered_axially_loaded_in_skf_loss_model(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "ForceToBeConsideredAxiallyLoadedInSKFLossModel", value
        )

    @property
    def force_at_zero_displacement_input_method(
        self: "Self",
    ) -> "overridable.Overridable_BearingF0InputMethod":
        """Overridable[mastapy.system_model.part_model.BearingF0InputMethod]"""
        temp = pythonnet_property_get(
            self.wrapped, "ForceAtZeroDisplacementInputMethod"
        )

        if temp is None:
            return None

        value = overridable.Overridable_BearingF0InputMethod.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @force_at_zero_displacement_input_method.setter
    @enforce_parameter_types
    def force_at_zero_displacement_input_method(
        self: "Self",
        value: "Union[_2498.BearingF0InputMethod, Tuple[_2498.BearingF0InputMethod, bool]]",
    ) -> None:
        wrapper_type = overridable.Overridable_BearingF0InputMethod.wrapper_type()
        enclosed_type = overridable.Overridable_BearingF0InputMethod.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "ForceAtZeroDisplacementInputMethod", value
        )

    @property
    def grid_refinement_factor_contact_width(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "GridRefinementFactorContactWidth")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @grid_refinement_factor_contact_width.setter
    @enforce_parameter_types
    def grid_refinement_factor_contact_width(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "GridRefinementFactorContactWidth", value)

    @property
    def grid_refinement_factor_rib_height(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "GridRefinementFactorRibHeight")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @grid_refinement_factor_rib_height.setter
    @enforce_parameter_types
    def grid_refinement_factor_rib_height(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "GridRefinementFactorRibHeight", value)

    @property
    def heat_due_to_external_cooling_or_heating(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "HeatDueToExternalCoolingOrHeating")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @heat_due_to_external_cooling_or_heating.setter
    @enforce_parameter_types
    def heat_due_to_external_cooling_or_heating(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "HeatDueToExternalCoolingOrHeating", value)

    @property
    def hertzian_contact_deflection_calculation_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod":
        """EnumWithSelectedValue[mastapy.math_utility.hertzian_contact.HertzianContactDeflectionCalculationMethod]"""
        temp = pythonnet_property_get(
            self.wrapped, "HertzianContactDeflectionCalculationMethod"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @hertzian_contact_deflection_calculation_method.setter
    @enforce_parameter_types
    def hertzian_contact_deflection_calculation_method(
        self: "Self", value: "_1624.HertzianContactDeflectionCalculationMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped, "HertzianContactDeflectionCalculationMethod", value
        )

    @property
    def include_fitting_effects(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_LoadCaseOverrideOption":
        """EnumWithSelectedValue[mastapy.utility.LoadCaseOverrideOption]"""
        temp = pythonnet_property_get(self.wrapped, "IncludeFittingEffects")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LoadCaseOverrideOption.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @include_fitting_effects.setter
    @enforce_parameter_types
    def include_fitting_effects(
        self: "Self", value: "_1640.LoadCaseOverrideOption"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LoadCaseOverrideOption.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "IncludeFittingEffects", value)

    @property
    def include_heat_emitted_by_lubricant_in_thermal_limiting_speed_calculation(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "IncludeHeatEmittedByLubricantInThermalLimitingSpeedCalculation",
        )

        if temp is None:
            return False

        return temp

    @include_heat_emitted_by_lubricant_in_thermal_limiting_speed_calculation.setter
    @enforce_parameter_types
    def include_heat_emitted_by_lubricant_in_thermal_limiting_speed_calculation(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeHeatEmittedByLubricantInThermalLimitingSpeedCalculation",
            bool(value) if value is not None else False,
        )

    @property
    def include_rib_contact_analysis(self: "Self") -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(self.wrapped, "IncludeRibContactAnalysis")

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @include_rib_contact_analysis.setter
    @enforce_parameter_types
    def include_rib_contact_analysis(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(self.wrapped, "IncludeRibContactAnalysis", value)

    @property
    def include_ring_ovality(self: "Self") -> "_1640.LoadCaseOverrideOption":
        """mastapy.utility.LoadCaseOverrideOption"""
        temp = pythonnet_property_get(self.wrapped, "IncludeRingOvality")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.LoadCaseOverrideOption"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility._1640", "LoadCaseOverrideOption"
        )(value)

    @include_ring_ovality.setter
    @enforce_parameter_types
    def include_ring_ovality(
        self: "Self", value: "_1640.LoadCaseOverrideOption"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Utility.LoadCaseOverrideOption"
        )
        pythonnet_property_set(self.wrapped, "IncludeRingOvality", value)

    @property
    def include_thermal_expansion_effects(
        self: "Self",
    ) -> "_1640.LoadCaseOverrideOption":
        """mastapy.utility.LoadCaseOverrideOption"""
        temp = pythonnet_property_get(self.wrapped, "IncludeThermalExpansionEffects")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.LoadCaseOverrideOption"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility._1640", "LoadCaseOverrideOption"
        )(value)

    @include_thermal_expansion_effects.setter
    @enforce_parameter_types
    def include_thermal_expansion_effects(
        self: "Self", value: "_1640.LoadCaseOverrideOption"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Utility.LoadCaseOverrideOption"
        )
        pythonnet_property_set(self.wrapped, "IncludeThermalExpansionEffects", value)

    @property
    def inner_mounting_sleeve_bore_tolerance_factor(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "InnerMountingSleeveBoreToleranceFactor"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_mounting_sleeve_bore_tolerance_factor.setter
    @enforce_parameter_types
    def inner_mounting_sleeve_bore_tolerance_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "InnerMountingSleeveBoreToleranceFactor", value
        )

    @property
    def inner_mounting_sleeve_outer_diameter_tolerance_factor(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "InnerMountingSleeveOuterDiameterToleranceFactor"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_mounting_sleeve_outer_diameter_tolerance_factor.setter
    @enforce_parameter_types
    def inner_mounting_sleeve_outer_diameter_tolerance_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "InnerMountingSleeveOuterDiameterToleranceFactor", value
        )

    @property
    def inner_mounting_sleeve_temperature(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerMountingSleeveTemperature")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_mounting_sleeve_temperature.setter
    @enforce_parameter_types
    def inner_mounting_sleeve_temperature(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InnerMountingSleeveTemperature", value)

    @property
    def inner_node_meaning(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerNodeMeaning")

        if temp is None:
            return ""

        return temp

    @property
    def lubricant_feed_pressure(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "LubricantFeedPressure")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @lubricant_feed_pressure.setter
    @enforce_parameter_types
    def lubricant_feed_pressure(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "LubricantFeedPressure", value)

    @property
    def lubricant_film_temperature(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "LubricantFilmTemperature")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @lubricant_film_temperature.setter
    @enforce_parameter_types
    def lubricant_film_temperature(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "LubricantFilmTemperature", value)

    @property
    def lubricant_flow_rate(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "LubricantFlowRate")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @lubricant_flow_rate.setter
    @enforce_parameter_types
    def lubricant_flow_rate(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "LubricantFlowRate", value)

    @property
    def lubricant_windage_ampersand_churning_temperature(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "LubricantWindageAmpersandChurningTemperature"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @lubricant_windage_ampersand_churning_temperature.setter
    @enforce_parameter_types
    def lubricant_windage_ampersand_churning_temperature(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "LubricantWindageAmpersandChurningTemperature", value
        )

    @property
    def maximum_friction_coefficient_for_ball_bearing_analysis(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumFrictionCoefficientForBallBearingAnalysis"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_friction_coefficient_for_ball_bearing_analysis.setter
    @enforce_parameter_types
    def maximum_friction_coefficient_for_ball_bearing_analysis(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MaximumFrictionCoefficientForBallBearingAnalysis", value
        )

    @property
    def minimum_clearance_for_ribs(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MinimumClearanceForRibs")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_clearance_for_ribs.setter
    @enforce_parameter_types
    def minimum_clearance_for_ribs(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MinimumClearanceForRibs", value)

    @property
    def minimum_force_for_bearing_to_be_considered_loaded(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumForceForBearingToBeConsideredLoaded"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_force_for_bearing_to_be_considered_loaded.setter
    @enforce_parameter_types
    def minimum_force_for_bearing_to_be_considered_loaded(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MinimumForceForBearingToBeConsideredLoaded", value
        )

    @property
    def minimum_force_for_six_degree_of_freedom_models(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumForceForSixDegreeOfFreedomModels"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_force_for_six_degree_of_freedom_models.setter
    @enforce_parameter_types
    def minimum_force_for_six_degree_of_freedom_models(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MinimumForceForSixDegreeOfFreedomModels", value
        )

    @property
    def minimum_moment_for_bearing_to_be_considered_loaded(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumMomentForBearingToBeConsideredLoaded"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_moment_for_bearing_to_be_considered_loaded.setter
    @enforce_parameter_types
    def minimum_moment_for_bearing_to_be_considered_loaded(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MinimumMomentForBearingToBeConsideredLoaded", value
        )

    @property
    def model_bearing_mounting_clearances_automatically(
        self: "Self",
    ) -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(
            self.wrapped, "ModelBearingMountingClearancesAutomatically"
        )

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @model_bearing_mounting_clearances_automatically.setter
    @enforce_parameter_types
    def model_bearing_mounting_clearances_automatically(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "ModelBearingMountingClearancesAutomatically", value
        )

    @property
    def number_of_grid_points_across_rib_contact_width(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfGridPointsAcrossRibContactWidth"
        )

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_grid_points_across_rib_contact_width.setter
    @enforce_parameter_types
    def number_of_grid_points_across_rib_contact_width(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "NumberOfGridPointsAcrossRibContactWidth", value
        )

    @property
    def number_of_grid_points_across_rib_height(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfGridPointsAcrossRibHeight")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_grid_points_across_rib_height.setter
    @enforce_parameter_types
    def number_of_grid_points_across_rib_height(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NumberOfGridPointsAcrossRibHeight", value)

    @property
    def number_of_strips_for_roller_calculation(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfStripsForRollerCalculation"
        )

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_strips_for_roller_calculation.setter
    @enforce_parameter_types
    def number_of_strips_for_roller_calculation(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "NumberOfStripsForRollerCalculation", value
        )

    @property
    def oil_dip_coefficient(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OilDipCoefficient")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @oil_dip_coefficient.setter
    @enforce_parameter_types
    def oil_dip_coefficient(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OilDipCoefficient", value)

    @property
    def oil_inlet_temperature(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OilInletTemperature")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @oil_inlet_temperature.setter
    @enforce_parameter_types
    def oil_inlet_temperature(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OilInletTemperature", value)

    @property
    def oil_level(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OilLevel")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @oil_level.setter
    @enforce_parameter_types
    def oil_level(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OilLevel", value)

    @property
    def outer_mounting_sleeve_bore_tolerance_factor(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "OuterMountingSleeveBoreToleranceFactor"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_mounting_sleeve_bore_tolerance_factor.setter
    @enforce_parameter_types
    def outer_mounting_sleeve_bore_tolerance_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "OuterMountingSleeveBoreToleranceFactor", value
        )

    @property
    def outer_mounting_sleeve_outer_diameter_tolerance_factor(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "OuterMountingSleeveOuterDiameterToleranceFactor"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_mounting_sleeve_outer_diameter_tolerance_factor.setter
    @enforce_parameter_types
    def outer_mounting_sleeve_outer_diameter_tolerance_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "OuterMountingSleeveOuterDiameterToleranceFactor", value
        )

    @property
    def outer_mounting_sleeve_temperature(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterMountingSleeveTemperature")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_mounting_sleeve_temperature.setter
    @enforce_parameter_types
    def outer_mounting_sleeve_temperature(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterMountingSleeveTemperature", value)

    @property
    def outer_node_meaning(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterNodeMeaning")

        if temp is None:
            return ""

        return temp

    @property
    def override_all_planets_inner_support_detail(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "OverrideAllPlanetsInnerSupportDetail"
        )

        if temp is None:
            return False

        return temp

    @override_all_planets_inner_support_detail.setter
    @enforce_parameter_types
    def override_all_planets_inner_support_detail(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverrideAllPlanetsInnerSupportDetail",
            bool(value) if value is not None else False,
        )

    @property
    def override_all_planets_left_support_detail(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "OverrideAllPlanetsLeftSupportDetail"
        )

        if temp is None:
            return False

        return temp

    @override_all_planets_left_support_detail.setter
    @enforce_parameter_types
    def override_all_planets_left_support_detail(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverrideAllPlanetsLeftSupportDetail",
            bool(value) if value is not None else False,
        )

    @property
    def override_all_planets_outer_support_detail(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "OverrideAllPlanetsOuterSupportDetail"
        )

        if temp is None:
            return False

        return temp

    @override_all_planets_outer_support_detail.setter
    @enforce_parameter_types
    def override_all_planets_outer_support_detail(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverrideAllPlanetsOuterSupportDetail",
            bool(value) if value is not None else False,
        )

    @property
    def override_all_planets_right_support_detail(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "OverrideAllPlanetsRightSupportDetail"
        )

        if temp is None:
            return False

        return temp

    @override_all_planets_right_support_detail.setter
    @enforce_parameter_types
    def override_all_planets_right_support_detail(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverrideAllPlanetsRightSupportDetail",
            bool(value) if value is not None else False,
        )

    @property
    def override_design_inner_support_detail(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "OverrideDesignInnerSupportDetail")

        if temp is None:
            return False

        return temp

    @override_design_inner_support_detail.setter
    @enforce_parameter_types
    def override_design_inner_support_detail(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverrideDesignInnerSupportDetail",
            bool(value) if value is not None else False,
        )

    @property
    def override_design_left_support_detail(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "OverrideDesignLeftSupportDetail")

        if temp is None:
            return False

        return temp

    @override_design_left_support_detail.setter
    @enforce_parameter_types
    def override_design_left_support_detail(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverrideDesignLeftSupportDetail",
            bool(value) if value is not None else False,
        )

    @property
    def override_design_outer_support_detail(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "OverrideDesignOuterSupportDetail")

        if temp is None:
            return False

        return temp

    @override_design_outer_support_detail.setter
    @enforce_parameter_types
    def override_design_outer_support_detail(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverrideDesignOuterSupportDetail",
            bool(value) if value is not None else False,
        )

    @property
    def override_design_right_support_detail(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "OverrideDesignRightSupportDetail")

        if temp is None:
            return False

        return temp

    @override_design_right_support_detail.setter
    @enforce_parameter_types
    def override_design_right_support_detail(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverrideDesignRightSupportDetail",
            bool(value) if value is not None else False,
        )

    @property
    def override_design_specified_stiffness_matrix(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "OverrideDesignSpecifiedStiffnessMatrix"
        )

        if temp is None:
            return False

        return temp

    @override_design_specified_stiffness_matrix.setter
    @enforce_parameter_types
    def override_design_specified_stiffness_matrix(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverrideDesignSpecifiedStiffnessMatrix",
            bool(value) if value is not None else False,
        )

    @property
    def permissible_axial_load_calculation_method(
        self: "Self",
    ) -> "overridable.Overridable_CylindricalRollerMaxAxialLoadMethod":
        """Overridable[mastapy.bearings.bearing_results.CylindricalRollerMaxAxialLoadMethod]"""
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleAxialLoadCalculationMethod"
        )

        if temp is None:
            return None

        value = (
            overridable.Overridable_CylindricalRollerMaxAxialLoadMethod.wrapped_type()
        )
        return overridable_enum_runtime.create(temp, value)

    @permissible_axial_load_calculation_method.setter
    @enforce_parameter_types
    def permissible_axial_load_calculation_method(
        self: "Self",
        value: "Union[_1998.CylindricalRollerMaxAxialLoadMethod, Tuple[_1998.CylindricalRollerMaxAxialLoadMethod, bool]]",
    ) -> None:
        wrapper_type = (
            overridable.Overridable_CylindricalRollerMaxAxialLoadMethod.wrapper_type()
        )
        enclosed_type = (
            overridable.Overridable_CylindricalRollerMaxAxialLoadMethod.implicit_type()
        )
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "PermissibleAxialLoadCalculationMethod", value
        )

    @property
    def preload_spring_initial_compression(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "PreloadSpringInitialCompression")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @preload_spring_initial_compression.setter
    @enforce_parameter_types
    def preload_spring_initial_compression(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "PreloadSpringInitialCompression", value)

    @property
    def radial_internal_clearance(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RadialInternalClearance")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @radial_internal_clearance.setter
    @enforce_parameter_types
    def radial_internal_clearance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RadialInternalClearance", value)

    @property
    def radial_internal_clearance_tolerance_factor(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "RadialInternalClearanceToleranceFactor"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @radial_internal_clearance_tolerance_factor.setter
    @enforce_parameter_types
    def radial_internal_clearance_tolerance_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "RadialInternalClearanceToleranceFactor", value
        )

    @property
    def refine_grid_around_contact_point(
        self: "Self",
    ) -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(self.wrapped, "RefineGridAroundContactPoint")

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @refine_grid_around_contact_point.setter
    @enforce_parameter_types
    def refine_grid_around_contact_point(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RefineGridAroundContactPoint", value)

    @property
    def ring_ovality_scaling(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RingOvalityScaling")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @ring_ovality_scaling.setter
    @enforce_parameter_types
    def ring_ovality_scaling(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RingOvalityScaling", value)

    @property
    def roller_analysis_method(
        self: "Self",
    ) -> "overridable.Overridable_RollerAnalysisMethod":
        """Overridable[mastapy.bearings.bearing_results.rolling.RollerAnalysisMethod]"""
        temp = pythonnet_property_get(self.wrapped, "RollerAnalysisMethod")

        if temp is None:
            return None

        value = overridable.Overridable_RollerAnalysisMethod.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @roller_analysis_method.setter
    @enforce_parameter_types
    def roller_analysis_method(
        self: "Self",
        value: "Union[_2125.RollerAnalysisMethod, Tuple[_2125.RollerAnalysisMethod, bool]]",
    ) -> None:
        wrapper_type = overridable.Overridable_RollerAnalysisMethod.wrapper_type()
        enclosed_type = overridable.Overridable_RollerAnalysisMethod.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RollerAnalysisMethod", value)

    @property
    def rolling_frictional_moment_factor_for_newly_greased_bearing(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "RollingFrictionalMomentFactorForNewlyGreasedBearing"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @rolling_frictional_moment_factor_for_newly_greased_bearing.setter
    @enforce_parameter_types
    def rolling_frictional_moment_factor_for_newly_greased_bearing(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "RollingFrictionalMomentFactorForNewlyGreasedBearing", value
        )

    @property
    def set_first_element_angle_to_load_direction(
        self: "Self",
    ) -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(
            self.wrapped, "SetFirstElementAngleToLoadDirection"
        )

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @set_first_element_angle_to_load_direction.setter
    @enforce_parameter_types
    def set_first_element_angle_to_load_direction(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "SetFirstElementAngleToLoadDirection", value
        )

    @property
    def use_advanced_film_temperature_calculation(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseAdvancedFilmTemperatureCalculation"
        )

        if temp is None:
            return False

        return temp

    @use_advanced_film_temperature_calculation.setter
    @enforce_parameter_types
    def use_advanced_film_temperature_calculation(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseAdvancedFilmTemperatureCalculation",
            bool(value) if value is not None else False,
        )

    @property
    def use_design_friction_coefficients(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseDesignFrictionCoefficients")

        if temp is None:
            return False

        return temp

    @use_design_friction_coefficients.setter
    @enforce_parameter_types
    def use_design_friction_coefficients(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseDesignFrictionCoefficients",
            bool(value) if value is not None else False,
        )

    @property
    def use_element_contact_angles_for_angular_velocities_in_ball_bearing(
        self: "Self",
    ) -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(
            self.wrapped, "UseElementContactAnglesForAngularVelocitiesInBallBearing"
        )

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @use_element_contact_angles_for_angular_velocities_in_ball_bearing.setter
    @enforce_parameter_types
    def use_element_contact_angles_for_angular_velocities_in_ball_bearing(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(
            self.wrapped,
            "UseElementContactAnglesForAngularVelocitiesInBallBearing",
            value,
        )

    @property
    def use_mean_values_in_ball_bearing_friction_analysis(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseMeanValuesInBallBearingFrictionAnalysis"
        )

        if temp is None:
            return False

        return temp

    @use_mean_values_in_ball_bearing_friction_analysis.setter
    @enforce_parameter_types
    def use_mean_values_in_ball_bearing_friction_analysis(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseMeanValuesInBallBearingFrictionAnalysis",
            bool(value) if value is not None else False,
        )

    @property
    def use_node_per_row_inner(self: "Self") -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(self.wrapped, "UseNodePerRowInner")

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @use_node_per_row_inner.setter
    @enforce_parameter_types
    def use_node_per_row_inner(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(self.wrapped, "UseNodePerRowInner", value)

    @property
    def use_node_per_row_outer(self: "Self") -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(self.wrapped, "UseNodePerRowOuter")

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @use_node_per_row_outer.setter
    @enforce_parameter_types
    def use_node_per_row_outer(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(self.wrapped, "UseNodePerRowOuter", value)

    @property
    def use_specified_contact_stiffness(self: "Self") -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(self.wrapped, "UseSpecifiedContactStiffness")

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @use_specified_contact_stiffness.setter
    @enforce_parameter_types
    def use_specified_contact_stiffness(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(self.wrapped, "UseSpecifiedContactStiffness", value)

    @property
    def viscosity_ratio(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ViscosityRatio")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @viscosity_ratio.setter
    @enforce_parameter_types
    def viscosity_ratio(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ViscosityRatio", value)

    @property
    def x_stiffness(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "XStiffness")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @x_stiffness.setter
    @enforce_parameter_types
    def x_stiffness(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "XStiffness", value)

    @property
    def y_stiffness(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "YStiffness")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @y_stiffness.setter
    @enforce_parameter_types
    def y_stiffness(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "YStiffness", value)

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
    def displacement_for_stiffness_operating_point(
        self: "Self",
    ) -> "_1614.VectorWithLinearAndAngularComponents":
        """mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DisplacementForStiffnessOperatingPoint"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def dynamic_analysis_options(self: "Self") -> "_2170.DynamicBearingAnalysisOptions":
        """mastapy.bearings.bearing_results.rolling.dysla.DynamicBearingAnalysisOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicAnalysisOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def force_at_zero_displacement(
        self: "Self",
    ) -> "_1614.VectorWithLinearAndAngularComponents":
        """mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceAtZeroDisplacement")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def force_for_stiffness_operating_point(
        self: "Self",
    ) -> "_1614.VectorWithLinearAndAngularComponents":
        """mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceForStiffnessOperatingPoint")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def friction_coefficients(
        self: "Self",
    ) -> "_2126.RollingBearingFrictionCoefficients":
        """mastapy.bearings.bearing_results.rolling.RollingBearingFrictionCoefficients

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrictionCoefficients")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def inner_ring_detail(self: "Self") -> "_1971.RingDetail":
        """mastapy.bearings.tolerances.RingDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerRingDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def inner_support_detail(self: "Self") -> "_1975.SupportDetail":
        """mastapy.bearings.tolerances.SupportDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerSupportDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def left_ring_detail(self: "Self") -> "_1971.RingDetail":
        """mastapy.bearings.tolerances.RingDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftRingDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def left_support_detail(self: "Self") -> "_1975.SupportDetail":
        """mastapy.bearings.tolerances.SupportDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftSupportDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def outer_ring_detail(self: "Self") -> "_1971.RingDetail":
        """mastapy.bearings.tolerances.RingDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterRingDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def outer_support_detail(self: "Self") -> "_1975.SupportDetail":
        """mastapy.bearings.tolerances.SupportDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterSupportDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def right_ring_detail(self: "Self") -> "_1971.RingDetail":
        """mastapy.bearings.tolerances.RingDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightRingDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def right_support_detail(self: "Self") -> "_1975.SupportDetail":
        """mastapy.bearings.tolerances.SupportDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightSupportDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def elements(self: "Self") -> "List[_2534.RollingBearingElementLoadCase]":
        """List[mastapy.system_model.part_model.RollingBearingElementLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Elements")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def planetaries(self: "Self") -> "List[BearingLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase]

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
    def specified_stiffness_for_linear_bearing_in_local_coordinate_system(
        self: "Self",
    ) -> "List[List[float]]":
        """List[List[float]]"""
        temp = pythonnet_property_get(
            self.wrapped, "SpecifiedStiffnessForLinearBearingInLocalCoordinateSystem"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_list_float_2d(temp)

        if value is None:
            return None

        return value

    @specified_stiffness_for_linear_bearing_in_local_coordinate_system.setter
    @enforce_parameter_types
    def specified_stiffness_for_linear_bearing_in_local_coordinate_system(
        self: "Self", value: "List[List[float]]"
    ) -> None:
        value = conversion.mp_to_pn_list_float_2d(value)
        pythonnet_property_set(
            self.wrapped,
            "SpecifiedStiffnessForLinearBearingInLocalCoordinateSystem",
            value,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_BearingLoadCase":
        """Cast to another type.

        Returns:
            _Cast_BearingLoadCase
        """
        return _Cast_BearingLoadCase(self)
