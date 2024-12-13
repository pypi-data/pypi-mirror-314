"""PointLoadInputOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2531
from mastapy._private.utility_gui import _1902

_POINT_LOAD_INPUT_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition",
    "PointLoadInputOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1542
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
        _7143,
        _7147,
        _7150,
    )

    Self = TypeVar("Self", bound="PointLoadInputOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="PointLoadInputOptions._Cast_PointLoadInputOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PointLoadInputOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PointLoadInputOptions:
    """Special nested class for casting PointLoadInputOptions to subclasses."""

    __parent__: "PointLoadInputOptions"

    @property
    def column_input_options(self: "CastSelf") -> "_1902.ColumnInputOptions":
        return self.__parent__._cast(_1902.ColumnInputOptions)

    @property
    def force_input_options(self: "CastSelf") -> "_7147.ForceInputOptions":
        from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
            _7147,
        )

        return self.__parent__._cast(_7147.ForceInputOptions)

    @property
    def moment_input_options(self: "CastSelf") -> "_7150.MomentInputOptions":
        from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
            _7150,
        )

        return self.__parent__._cast(_7150.MomentInputOptions)

    @property
    def point_load_input_options(self: "CastSelf") -> "PointLoadInputOptions":
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
class PointLoadInputOptions(_1902.ColumnInputOptions):
    """PointLoadInputOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _POINT_LOAD_INPUT_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def axis(self: "Self") -> "_1542.Axis":
        """mastapy.math_utility.Axis"""
        temp = pythonnet_property_get(self.wrapped, "Axis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.MathUtility.Axis")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility._1542", "Axis"
        )(value)

    @axis.setter
    @enforce_parameter_types
    def axis(self: "Self", value: "_1542.Axis") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.MathUtility.Axis")
        pythonnet_property_set(self.wrapped, "Axis", value)

    @property
    def conversion_to_load_case(self: "Self") -> "_7143.AdditionalForcesObtainedFrom":
        """mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition.AdditionalForcesObtainedFrom"""
        temp = pythonnet_property_get(self.wrapped, "ConversionToLoadCase")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition.AdditionalForcesObtainedFrom",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7143",
            "AdditionalForcesObtainedFrom",
        )(value)

    @conversion_to_load_case.setter
    @enforce_parameter_types
    def conversion_to_load_case(
        self: "Self", value: "_7143.AdditionalForcesObtainedFrom"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition.AdditionalForcesObtainedFrom",
        )
        pythonnet_property_set(self.wrapped, "ConversionToLoadCase", value)

    @property
    def point_load(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_PointLoad":
        """ListWithSelectedItem[mastapy.system_model.part_model.PointLoad]"""
        temp = pythonnet_property_get(self.wrapped, "PointLoad")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_PointLoad",
        )(temp)

    @point_load.setter
    @enforce_parameter_types
    def point_load(self: "Self", value: "_2531.PointLoad") -> None:
        wrapper_type = (
            list_with_selected_item.ListWithSelectedItem_PointLoad.wrapper_type()
        )
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_PointLoad.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "PointLoad", value)

    @property
    def cast_to(self: "Self") -> "_Cast_PointLoadInputOptions":
        """Cast to another type.

        Returns:
            _Cast_PointLoadInputOptions
        """
        return _Cast_PointLoadInputOptions(self)
