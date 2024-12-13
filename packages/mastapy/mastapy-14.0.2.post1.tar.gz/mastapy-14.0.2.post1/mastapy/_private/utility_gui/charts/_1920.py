"""ThreeDChartDefinition"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility_gui.charts import _1914

_THREE_D_CHART_DEFINITION = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Charts", "ThreeDChartDefinition"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility import _1539
    from mastapy._private.utility.report import _1796, _1801
    from mastapy._private.utility_gui.charts import _1916

    Self = TypeVar("Self", bound="ThreeDChartDefinition")
    CastSelf = TypeVar(
        "CastSelf", bound="ThreeDChartDefinition._Cast_ThreeDChartDefinition"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ThreeDChartDefinition",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ThreeDChartDefinition:
    """Special nested class for casting ThreeDChartDefinition to subclasses."""

    __parent__: "ThreeDChartDefinition"

    @property
    def nd_chart_definition(self: "CastSelf") -> "_1914.NDChartDefinition":
        return self.__parent__._cast(_1914.NDChartDefinition)

    @property
    def chart_definition(self: "CastSelf") -> "_1801.ChartDefinition":
        from mastapy._private.utility.report import _1801

        return self.__parent__._cast(_1801.ChartDefinition)

    @property
    def three_d_chart_definition(self: "CastSelf") -> "ThreeDChartDefinition":
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
class ThreeDChartDefinition(_1914.NDChartDefinition):
    """ThreeDChartDefinition

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _THREE_D_CHART_DEFINITION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def z_axis(self: "Self") -> "_1796.AxisSettings":
        """mastapy.utility.report.AxisSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZAxis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def x_axis_range(self: "Self") -> "_1539.Range":
        """mastapy.math_utility.Range"""
        temp = pythonnet_property_get(self.wrapped, "XAxisRange")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @x_axis_range.setter
    @enforce_parameter_types
    def x_axis_range(self: "Self", value: "_1539.Range") -> None:
        pythonnet_property_set(self.wrapped, "XAxisRange", value.wrapped)

    @property
    def y_axis_range(self: "Self") -> "_1539.Range":
        """mastapy.math_utility.Range"""
        temp = pythonnet_property_get(self.wrapped, "YAxisRange")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @y_axis_range.setter
    @enforce_parameter_types
    def y_axis_range(self: "Self", value: "_1539.Range") -> None:
        pythonnet_property_set(self.wrapped, "YAxisRange", value.wrapped)

    @property
    def z_axis_range(self: "Self") -> "_1539.Range":
        """mastapy.math_utility.Range"""
        temp = pythonnet_property_get(self.wrapped, "ZAxisRange")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @z_axis_range.setter
    @enforce_parameter_types
    def z_axis_range(self: "Self", value: "_1539.Range") -> None:
        pythonnet_property_set(self.wrapped, "ZAxisRange", value.wrapped)

    def data_points_for_surfaces(self: "Self") -> "List[_1916.PointsForSurface]":
        """List[mastapy.utility_gui.charts.PointsForSurface]"""
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(self.wrapped, "DataPointsForSurfaces")
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ThreeDChartDefinition":
        """Cast to another type.

        Returns:
            _Cast_ThreeDChartDefinition
        """
        return _Cast_ThreeDChartDefinition(self)
