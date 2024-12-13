"""PowerLoadInputOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
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
from mastapy._private.system_model.part_model import _2532
from mastapy._private.utility_gui import _1902

_POWER_LOAD_INPUT_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition",
    "PowerLoadInputOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
        _7155,
        _7158,
    )

    Self = TypeVar("Self", bound="PowerLoadInputOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="PowerLoadInputOptions._Cast_PowerLoadInputOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PowerLoadInputOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PowerLoadInputOptions:
    """Special nested class for casting PowerLoadInputOptions to subclasses."""

    __parent__: "PowerLoadInputOptions"

    @property
    def column_input_options(self: "CastSelf") -> "_1902.ColumnInputOptions":
        return self.__parent__._cast(_1902.ColumnInputOptions)

    @property
    def speed_input_options(self: "CastSelf") -> "_7155.SpeedInputOptions":
        from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
            _7155,
        )

        return self.__parent__._cast(_7155.SpeedInputOptions)

    @property
    def torque_input_options(self: "CastSelf") -> "_7158.TorqueInputOptions":
        from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
            _7158,
        )

        return self.__parent__._cast(_7158.TorqueInputOptions)

    @property
    def power_load_input_options(self: "CastSelf") -> "PowerLoadInputOptions":
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
class PowerLoadInputOptions(_1902.ColumnInputOptions):
    """PowerLoadInputOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _POWER_LOAD_INPUT_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def power_load(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_PowerLoad":
        """ListWithSelectedItem[mastapy.system_model.part_model.PowerLoad]"""
        temp = pythonnet_property_get(self.wrapped, "PowerLoad")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_PowerLoad",
        )(temp)

    @power_load.setter
    @enforce_parameter_types
    def power_load(self: "Self", value: "_2532.PowerLoad") -> None:
        wrapper_type = (
            list_with_selected_item.ListWithSelectedItem_PowerLoad.wrapper_type()
        )
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_PowerLoad.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "PowerLoad", value)

    @property
    def cast_to(self: "Self") -> "_Cast_PowerLoadInputOptions":
        """Cast to another type.

        Returns:
            _Cast_PowerLoadInputOptions
        """
        return _Cast_PowerLoadInputOptions(self)
