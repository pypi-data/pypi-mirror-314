"""NDChartDefinition"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.report import _1801

_ND_CHART_DEFINITION = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Charts", "NDChartDefinition"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1796
    from mastapy._private.utility_gui.charts import (
        _1907,
        _1912,
        _1915,
        _1917,
        _1920,
        _1921,
        _1922,
    )

    Self = TypeVar("Self", bound="NDChartDefinition")
    CastSelf = TypeVar("CastSelf", bound="NDChartDefinition._Cast_NDChartDefinition")


__docformat__ = "restructuredtext en"
__all__ = ("NDChartDefinition",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NDChartDefinition:
    """Special nested class for casting NDChartDefinition to subclasses."""

    __parent__: "NDChartDefinition"

    @property
    def chart_definition(self: "CastSelf") -> "_1801.ChartDefinition":
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
    def three_d_chart_definition(self: "CastSelf") -> "_1920.ThreeDChartDefinition":
        from mastapy._private.utility_gui.charts import _1920

        return self.__parent__._cast(_1920.ThreeDChartDefinition)

    @property
    def three_d_vector_chart_definition(
        self: "CastSelf",
    ) -> "_1921.ThreeDVectorChartDefinition":
        from mastapy._private.utility_gui.charts import _1921

        return self.__parent__._cast(_1921.ThreeDVectorChartDefinition)

    @property
    def two_d_chart_definition(self: "CastSelf") -> "_1922.TwoDChartDefinition":
        from mastapy._private.utility_gui.charts import _1922

        return self.__parent__._cast(_1922.TwoDChartDefinition)

    @property
    def nd_chart_definition(self: "CastSelf") -> "NDChartDefinition":
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
class NDChartDefinition(_1801.ChartDefinition):
    """NDChartDefinition

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ND_CHART_DEFINITION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def specify_shared_chart_settings(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SpecifySharedChartSettings")

        if temp is None:
            return False

        return temp

    @specify_shared_chart_settings.setter
    @enforce_parameter_types
    def specify_shared_chart_settings(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifySharedChartSettings",
            bool(value) if value is not None else False,
        )

    @property
    def x_axis(self: "Self") -> "_1796.AxisSettings":
        """mastapy.utility.report.AxisSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "XAxis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def y_axis(self: "Self") -> "_1796.AxisSettings":
        """mastapy.utility.report.AxisSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "YAxis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_NDChartDefinition":
        """Cast to another type.

        Returns:
            _Cast_NDChartDefinition
        """
        return _Cast_NDChartDefinition(self)
