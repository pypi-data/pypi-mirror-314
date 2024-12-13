"""AGMAGleasonConicalGearMeshDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
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
from mastapy._private.gears.gear_designs.conical import _1195, _1209

_AGMA_GLEASON_CONICAL_GEAR_MESH_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.AGMAGleasonConical",
    "AGMAGleasonConicalGearMeshDesign",
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.gear_designs import _974, _975
    from mastapy._private.gears.gear_designs.bevel import _1221
    from mastapy._private.gears.gear_designs.hypoid import _1012
    from mastapy._private.gears.gear_designs.spiral_bevel import _996
    from mastapy._private.gears.gear_designs.straight_bevel import _988
    from mastapy._private.gears.gear_designs.straight_bevel_diff import _992
    from mastapy._private.gears.gear_designs.zerol_bevel import _979
    from mastapy._private.gears.rating.iso_10300 import _434, _447, _449, _450

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearMeshDesign")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearMeshDesign._Cast_AGMAGleasonConicalGearMeshDesign",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearMeshDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearMeshDesign:
    """Special nested class for casting AGMAGleasonConicalGearMeshDesign to subclasses."""

    __parent__: "AGMAGleasonConicalGearMeshDesign"

    @property
    def conical_gear_mesh_design(self: "CastSelf") -> "_1195.ConicalGearMeshDesign":
        return self.__parent__._cast(_1195.ConicalGearMeshDesign)

    @property
    def gear_mesh_design(self: "CastSelf") -> "_975.GearMeshDesign":
        from mastapy._private.gears.gear_designs import _975

        return self.__parent__._cast(_975.GearMeshDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_974.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _974

        return self.__parent__._cast(_974.GearDesignComponent)

    @property
    def zerol_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_979.ZerolBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _979

        return self.__parent__._cast(_979.ZerolBevelGearMeshDesign)

    @property
    def straight_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_988.StraightBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _988

        return self.__parent__._cast(_988.StraightBevelGearMeshDesign)

    @property
    def straight_bevel_diff_gear_mesh_design(
        self: "CastSelf",
    ) -> "_992.StraightBevelDiffGearMeshDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _992

        return self.__parent__._cast(_992.StraightBevelDiffGearMeshDesign)

    @property
    def spiral_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_996.SpiralBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _996

        return self.__parent__._cast(_996.SpiralBevelGearMeshDesign)

    @property
    def hypoid_gear_mesh_design(self: "CastSelf") -> "_1012.HypoidGearMeshDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1012

        return self.__parent__._cast(_1012.HypoidGearMeshDesign)

    @property
    def bevel_gear_mesh_design(self: "CastSelf") -> "_1221.BevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.bevel import _1221

        return self.__parent__._cast(_1221.BevelGearMeshDesign)

    @property
    def agma_gleason_conical_gear_mesh_design(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearMeshDesign":
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
class AGMAGleasonConicalGearMeshDesign(_1195.ConicalGearMeshDesign):
    """AGMAGleasonConicalGearMeshDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR_MESH_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def crowned(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "Crowned")

        if temp is None:
            return False

        return temp

    @crowned.setter
    @enforce_parameter_types
    def crowned(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "Crowned", bool(value) if value is not None else False
        )

    @property
    def crowning_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CrowningFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @crowning_factor.setter
    @enforce_parameter_types
    def crowning_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CrowningFactor", value)

    @property
    def dynamic_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "DynamicFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @dynamic_factor.setter
    @enforce_parameter_types
    def dynamic_factor(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DynamicFactor", value)

    @property
    def hardness_ratio_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HardnessRatioFactor")

        if temp is None:
            return 0.0

        return temp

    @hardness_ratio_factor.setter
    @enforce_parameter_types
    def hardness_ratio_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HardnessRatioFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def iso10300_gear_set_finishing_methods(
        self: "Self",
    ) -> "_434.Iso10300FinishingMethods":
        """mastapy.gears.rating.isoIso10300FinishingMethods"""
        temp = pythonnet_property_get(self.wrapped, "ISO10300GearSetFinishingMethods")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.Rating.Iso10300.Iso10300FinishingMethods"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating._434", "Iso10300FinishingMethods"
        )(value)

    @iso10300_gear_set_finishing_methods.setter
    @enforce_parameter_types
    def iso10300_gear_set_finishing_methods(
        self: "Self", value: "_434.Iso10300FinishingMethods"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.Rating.Iso10300.Iso10300FinishingMethods"
        )
        pythonnet_property_set(self.wrapped, "ISO10300GearSetFinishingMethods", value)

    @property
    def load_distribution_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LoadDistributionFactor")

        if temp is None:
            return 0.0

        return temp

    @load_distribution_factor.setter
    @enforce_parameter_types
    def load_distribution_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LoadDistributionFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def load_distribution_factor_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_LoadDistributionFactorMethods":
        """EnumWithSelectedValue[mastapy.gears.gear_designs.conical.LoadDistributionFactorMethods]"""
        temp = pythonnet_property_get(self.wrapped, "LoadDistributionFactorMethod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LoadDistributionFactorMethods.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @load_distribution_factor_method.setter
    @enforce_parameter_types
    def load_distribution_factor_method(
        self: "Self", value: "_1209.LoadDistributionFactorMethods"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LoadDistributionFactorMethods.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "LoadDistributionFactorMethod", value)

    @property
    def mounting_conditions_of_pinion_and_wheel(
        self: "Self",
    ) -> "_447.MountingConditionsOfPinionAndWheel":
        """mastapy.gears.rating.isoMountingConditionsOfPinionAndWheel"""
        temp = pythonnet_property_get(
            self.wrapped, "MountingConditionsOfPinionAndWheel"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.Rating.Iso10300.MountingConditionsOfPinionAndWheel",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating._447", "MountingConditionsOfPinionAndWheel"
        )(value)

    @mounting_conditions_of_pinion_and_wheel.setter
    @enforce_parameter_types
    def mounting_conditions_of_pinion_and_wheel(
        self: "Self", value: "_447.MountingConditionsOfPinionAndWheel"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.Rating.Iso10300.MountingConditionsOfPinionAndWheel",
        )
        pythonnet_property_set(
            self.wrapped, "MountingConditionsOfPinionAndWheel", value
        )

    @property
    def net_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NetFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    def pinion_face_width_offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PinionFaceWidthOffset")

        if temp is None:
            return 0.0

        return temp

    @pinion_face_width_offset.setter
    @enforce_parameter_types
    def pinion_face_width_offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PinionFaceWidthOffset",
            float(value) if value is not None else 0.0,
        )

    @property
    def profile_crowning_setting(self: "Self") -> "_449.ProfileCrowningSetting":
        """mastapy.gears.rating.isoProfileCrowningSetting"""
        temp = pythonnet_property_get(self.wrapped, "ProfileCrowningSetting")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.Rating.Iso10300.ProfileCrowningSetting"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating._449", "ProfileCrowningSetting"
        )(value)

    @profile_crowning_setting.setter
    @enforce_parameter_types
    def profile_crowning_setting(
        self: "Self", value: "_449.ProfileCrowningSetting"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.Rating.Iso10300.ProfileCrowningSetting"
        )
        pythonnet_property_set(self.wrapped, "ProfileCrowningSetting", value)

    @property
    def size_factor_bending(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "SizeFactorBending")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @size_factor_bending.setter
    @enforce_parameter_types
    def size_factor_bending(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "SizeFactorBending", value)

    @property
    def size_factor_contact(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "SizeFactorContact")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @size_factor_contact.setter
    @enforce_parameter_types
    def size_factor_contact(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "SizeFactorContact", value)

    @property
    def surface_condition_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SurfaceConditionFactor")

        if temp is None:
            return 0.0

        return temp

    @surface_condition_factor.setter
    @enforce_parameter_types
    def surface_condition_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SurfaceConditionFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def temperature_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "TemperatureFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @temperature_factor.setter
    @enforce_parameter_types
    def temperature_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "TemperatureFactor", value)

    @property
    def tooth_lengthwise_curvature_factor(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ToothLengthwiseCurvatureFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @tooth_lengthwise_curvature_factor.setter
    @enforce_parameter_types
    def tooth_lengthwise_curvature_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ToothLengthwiseCurvatureFactor", value)

    @property
    def verification_of_contact_pattern(
        self: "Self",
    ) -> "_450.VerificationOfContactPattern":
        """mastapy.gears.rating.isoVerificationOfContactPattern"""
        temp = pythonnet_property_get(self.wrapped, "VerificationOfContactPattern")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.Rating.Iso10300.VerificationOfContactPattern"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating._450", "VerificationOfContactPattern"
        )(value)

    @verification_of_contact_pattern.setter
    @enforce_parameter_types
    def verification_of_contact_pattern(
        self: "Self", value: "_450.VerificationOfContactPattern"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.Rating.Iso10300.VerificationOfContactPattern"
        )
        pythonnet_property_set(self.wrapped, "VerificationOfContactPattern", value)

    @property
    def wheel_effective_face_width_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WheelEffectiveFaceWidthFactor")

        if temp is None:
            return 0.0

        return temp

    @wheel_effective_face_width_factor.setter
    @enforce_parameter_types
    def wheel_effective_face_width_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WheelEffectiveFaceWidthFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalGearMeshDesign":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearMeshDesign
        """
        return _Cast_AGMAGleasonConicalGearMeshDesign(self)
