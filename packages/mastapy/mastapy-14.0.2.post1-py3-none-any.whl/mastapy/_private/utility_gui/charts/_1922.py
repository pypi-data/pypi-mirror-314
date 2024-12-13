"""TwoDChartDefinition"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.utility_gui.charts import _1914

_TWO_D_CHART_DEFINITION = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Charts", "TwoDChartDefinition"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.utility.report import _1801
    from mastapy._private.utility_gui.charts import (
        _1907,
        _1908,
        _1912,
        _1915,
        _1917,
        _1918,
    )

    Self = TypeVar("Self", bound="TwoDChartDefinition")
    CastSelf = TypeVar(
        "CastSelf", bound="TwoDChartDefinition._Cast_TwoDChartDefinition"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TwoDChartDefinition",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TwoDChartDefinition:
    """Special nested class for casting TwoDChartDefinition to subclasses."""

    __parent__: "TwoDChartDefinition"

    @property
    def nd_chart_definition(self: "CastSelf") -> "_1914.NDChartDefinition":
        return self.__parent__._cast(_1914.NDChartDefinition)

    @property
    def chart_definition(self: "CastSelf") -> "_1801.ChartDefinition":
        from mastapy._private.utility.report import _1801

        return self.__parent__._cast(_1801.ChartDefinition)

    @property
    def bubble_chart_definition(self: "CastSelf") -> "_1907.BubbleChartDefinition":
        from mastapy._private.utility_gui.charts import _1907

        return self.__parent__._cast(_1907.BubbleChartDefinition)

    @property
    def matrix_visualisation_definition(
        self: "CastSelf",
    ) -> "_1912.MatrixVisualisationDefinition":
        from mastapy._private.utility_gui.charts import _1912

        return self.__parent__._cast(_1912.MatrixVisualisationDefinition)

    @property
    def parallel_coordinates_chart_definition(
        self: "CastSelf",
    ) -> "_1915.ParallelCoordinatesChartDefinition":
        from mastapy._private.utility_gui.charts import _1915

        return self.__parent__._cast(_1915.ParallelCoordinatesChartDefinition)

    @property
    def scatter_chart_definition(self: "CastSelf") -> "_1917.ScatterChartDefinition":
        from mastapy._private.utility_gui.charts import _1917

        return self.__parent__._cast(_1917.ScatterChartDefinition)

    @property
    def two_d_chart_definition(self: "CastSelf") -> "TwoDChartDefinition":
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
class TwoDChartDefinition(_1914.NDChartDefinition):
    """TwoDChartDefinition

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TWO_D_CHART_DEFINITION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def const_lines(self: "Self") -> "List[_1908.ConstantLine]":
        """List[mastapy.utility_gui.charts.ConstantLine]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConstLines")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def series_list(self: "Self") -> "List[_1918.Series2D]":
        """List[mastapy.utility_gui.charts.Series2D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SeriesList")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_TwoDChartDefinition":
        """Cast to another type.

        Returns:
            _Cast_TwoDChartDefinition
        """
        return _Cast_TwoDChartDefinition(self)
