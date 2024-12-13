"""CustomReportMultiPropertyItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.report import _1823

_CUSTOM_REPORT_MULTI_PROPERTY_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportMultiPropertyItem"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.bearings.bearing_results import _2002, _2006, _2014
    from mastapy._private.gears.gear_designs.cylindrical import _1067
    from mastapy._private.shafts import _20
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
        _4836,
        _4840,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
        _2940,
    )
    from mastapy._private.utility.report import _1809, _1816, _1824, _1826, _1833
    from mastapy._private.utility_gui.charts import _1909, _1910

    Self = TypeVar("Self", bound="CustomReportMultiPropertyItem")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
    )

TItem = TypeVar("TItem", bound="_1826.CustomReportPropertyItem")

__docformat__ = "restructuredtext en"
__all__ = ("CustomReportMultiPropertyItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportMultiPropertyItem:
    """Special nested class for casting CustomReportMultiPropertyItem to subclasses."""

    __parent__: "CustomReportMultiPropertyItem"

    @property
    def custom_report_multi_property_item_base(
        self: "CastSelf",
    ) -> "_1823.CustomReportMultiPropertyItemBase":
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
    def shaft_damage_results_table_and_chart(
        self: "CastSelf",
    ) -> "_20.ShaftDamageResultsTableAndChart":
        from mastapy._private.shafts import _20

        return self.__parent__._cast(_20.ShaftDamageResultsTableAndChart)

    @property
    def cylindrical_gear_table_with_mg_charts(
        self: "CastSelf",
    ) -> "_1067.CylindricalGearTableWithMGCharts":
        from mastapy._private.gears.gear_designs.cylindrical import _1067

        return self.__parent__._cast(_1067.CylindricalGearTableWithMGCharts)

    @property
    def custom_report_chart(self: "CastSelf") -> "_1809.CustomReportChart":
        from mastapy._private.utility.report import _1809

        return self.__parent__._cast(_1809.CustomReportChart)

    @property
    def custom_table(self: "CastSelf") -> "_1833.CustomTable":
        from mastapy._private.utility.report import _1833

        return self.__parent__._cast(_1833.CustomTable)

    @property
    def custom_line_chart(self: "CastSelf") -> "_1909.CustomLineChart":
        from mastapy._private.utility_gui.charts import _1909

        return self.__parent__._cast(_1909.CustomLineChart)

    @property
    def custom_table_and_chart(self: "CastSelf") -> "_1910.CustomTableAndChart":
        from mastapy._private.utility_gui.charts import _1910

        return self.__parent__._cast(_1910.CustomTableAndChart)

    @property
    def loaded_ball_element_chart_reporter(
        self: "CastSelf",
    ) -> "_2002.LoadedBallElementChartReporter":
        from mastapy._private.bearings.bearing_results import _2002

        return self.__parent__._cast(_2002.LoadedBallElementChartReporter)

    @property
    def loaded_bearing_temperature_chart(
        self: "CastSelf",
    ) -> "_2006.LoadedBearingTemperatureChart":
        from mastapy._private.bearings.bearing_results import _2006

        return self.__parent__._cast(_2006.LoadedBearingTemperatureChart)

    @property
    def loaded_roller_element_chart_reporter(
        self: "CastSelf",
    ) -> "_2014.LoadedRollerElementChartReporter":
        from mastapy._private.bearings.bearing_results import _2014

        return self.__parent__._cast(_2014.LoadedRollerElementChartReporter)

    @property
    def shaft_system_deflection_sections_report(
        self: "CastSelf",
    ) -> "_2940.ShaftSystemDeflectionSectionsReport":
        from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
            _2940,
        )

        return self.__parent__._cast(_2940.ShaftSystemDeflectionSectionsReport)

    @property
    def campbell_diagram_report(self: "CastSelf") -> "_4836.CampbellDiagramReport":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
            _4836,
        )

        return self.__parent__._cast(_4836.CampbellDiagramReport)

    @property
    def per_mode_results_report(self: "CastSelf") -> "_4840.PerModeResultsReport":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
            _4840,
        )

        return self.__parent__._cast(_4840.PerModeResultsReport)

    @property
    def custom_report_multi_property_item(
        self: "CastSelf",
    ) -> "CustomReportMultiPropertyItem":
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
class CustomReportMultiPropertyItem(
    _1823.CustomReportMultiPropertyItemBase, Generic[TItem]
):
    """CustomReportMultiPropertyItem

    This is a mastapy class.

    Generic Types:
        TItem
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_MULTI_PROPERTY_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportMultiPropertyItem":
        """Cast to another type.

        Returns:
            _Cast_CustomReportMultiPropertyItem
        """
        return _Cast_CustomReportMultiPropertyItem(self)
