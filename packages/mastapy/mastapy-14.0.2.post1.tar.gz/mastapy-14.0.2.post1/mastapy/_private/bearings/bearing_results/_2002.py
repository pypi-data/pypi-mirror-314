"""LoadedBallElementChartReporter"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.bearing_results import _2018
from mastapy._private.utility.report import _1809

_LOADED_BALL_ELEMENT_CHART_REPORTER = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults", "LoadedBallElementChartReporter"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1816, _1822, _1823, _1824

    Self = TypeVar("Self", bound="LoadedBallElementChartReporter")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedBallElementChartReporter._Cast_LoadedBallElementChartReporter",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedBallElementChartReporter",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedBallElementChartReporter:
    """Special nested class for casting LoadedBallElementChartReporter to subclasses."""

    __parent__: "LoadedBallElementChartReporter"

    @property
    def custom_report_chart(self: "CastSelf") -> "_1809.CustomReportChart":
        return self.__parent__._cast(_1809.CustomReportChart)

    @property
    def custom_report_multi_property_item(
        self: "CastSelf",
    ) -> "_1822.CustomReportMultiPropertyItem":
        pass

        from mastapy._private.utility.report import _1822

        return self.__parent__._cast(_1822.CustomReportMultiPropertyItem)

    @property
    def custom_report_multi_property_item_base(
        self: "CastSelf",
    ) -> "_1823.CustomReportMultiPropertyItemBase":
        from mastapy._private.utility.report import _1823

        return self.__parent__._cast(_1823.CustomReportMultiPropertyItemBase)

    @property
    def custom_report_nameable_item(
        self: "CastSelf",
    ) -> "_1824.CustomReportNameableItem":
        from mastapy._private.utility.report import _1824

        return self.__parent__._cast(_1824.CustomReportNameableItem)

    @property
    def custom_report_item(self: "CastSelf") -> "_1816.CustomReportItem":
        from mastapy._private.utility.report import _1816

        return self.__parent__._cast(_1816.CustomReportItem)

    @property
    def loaded_ball_element_chart_reporter(
        self: "CastSelf",
    ) -> "LoadedBallElementChartReporter":
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
class LoadedBallElementChartReporter(_1809.CustomReportChart):
    """LoadedBallElementChartReporter

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_BALL_ELEMENT_CHART_REPORTER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def element_to_plot(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_LoadedBallElementPropertyType":
        """EnumWithSelectedValue[mastapy.bearings.bearing_results.LoadedBallElementPropertyType]"""
        temp = pythonnet_property_get(self.wrapped, "ElementToPlot")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LoadedBallElementPropertyType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @element_to_plot.setter
    @enforce_parameter_types
    def element_to_plot(
        self: "Self", value: "_2018.LoadedBallElementPropertyType"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LoadedBallElementPropertyType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ElementToPlot", value)

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedBallElementChartReporter":
        """Cast to another type.

        Returns:
            _Cast_LoadedBallElementChartReporter
        """
        return _Cast_LoadedBallElementChartReporter(self)
