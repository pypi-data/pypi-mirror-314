"""CustomReportNameableItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.report import _1816

_CUSTOM_REPORT_NAMEABLE_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportNameableItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2002, _2003, _2006, _2014
    from mastapy._private.gears.gear_designs.cylindrical import _1067
    from mastapy._private.shafts import _20
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
        _4836,
        _4840,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4501,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
        _2940,
    )
    from mastapy._private.utility.report import (
        _1795,
        _1803,
        _1804,
        _1805,
        _1806,
        _1808,
        _1809,
        _1813,
        _1815,
        _1822,
        _1823,
        _1825,
        _1827,
        _1830,
        _1832,
        _1833,
        _1835,
    )
    from mastapy._private.utility_gui.charts import _1909, _1910

    Self = TypeVar("Self", bound="CustomReportNameableItem")
    CastSelf = TypeVar(
        "CastSelf", bound="CustomReportNameableItem._Cast_CustomReportNameableItem"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportNameableItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportNameableItem:
    """Special nested class for casting CustomReportNameableItem to subclasses."""

    __parent__: "CustomReportNameableItem"

    @property
    def custom_report_item(self: "CastSelf") -> "_1816.CustomReportItem":
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
    def ad_hoc_custom_table(self: "CastSelf") -> "_1795.AdHocCustomTable":
        from mastapy._private.utility.report import _1795

        return self.__parent__._cast(_1795.AdHocCustomTable)

    @property
    def custom_chart(self: "CastSelf") -> "_1803.CustomChart":
        from mastapy._private.utility.report import _1803

        return self.__parent__._cast(_1803.CustomChart)

    @property
    def custom_drawing(self: "CastSelf") -> "_1804.CustomDrawing":
        from mastapy._private.utility.report import _1804

        return self.__parent__._cast(_1804.CustomDrawing)

    @property
    def custom_graphic(self: "CastSelf") -> "_1805.CustomGraphic":
        from mastapy._private.utility.report import _1805

        return self.__parent__._cast(_1805.CustomGraphic)

    @property
    def custom_image(self: "CastSelf") -> "_1806.CustomImage":
        from mastapy._private.utility.report import _1806

        return self.__parent__._cast(_1806.CustomImage)

    @property
    def custom_report_cad_drawing(self: "CastSelf") -> "_1808.CustomReportCadDrawing":
        from mastapy._private.utility.report import _1808

        return self.__parent__._cast(_1808.CustomReportCadDrawing)

    @property
    def custom_report_chart(self: "CastSelf") -> "_1809.CustomReportChart":
        from mastapy._private.utility.report import _1809

        return self.__parent__._cast(_1809.CustomReportChart)

    @property
    def custom_report_definition_item(
        self: "CastSelf",
    ) -> "_1813.CustomReportDefinitionItem":
        from mastapy._private.utility.report import _1813

        return self.__parent__._cast(_1813.CustomReportDefinitionItem)

    @property
    def custom_report_html_item(self: "CastSelf") -> "_1815.CustomReportHtmlItem":
        from mastapy._private.utility.report import _1815

        return self.__parent__._cast(_1815.CustomReportHtmlItem)

    @property
    def custom_report_multi_property_item(
        self: "CastSelf",
    ) -> "_1822.CustomReportMultiPropertyItem":
        from mastapy._private.utility.report import _1822

        return self.__parent__._cast(_1822.CustomReportMultiPropertyItem)

    @property
    def custom_report_multi_property_item_base(
        self: "CastSelf",
    ) -> "_1823.CustomReportMultiPropertyItemBase":
        from mastapy._private.utility.report import _1823

        return self.__parent__._cast(_1823.CustomReportMultiPropertyItemBase)

    @property
    def custom_report_named_item(self: "CastSelf") -> "_1825.CustomReportNamedItem":
        from mastapy._private.utility.report import _1825

        return self.__parent__._cast(_1825.CustomReportNamedItem)

    @property
    def custom_report_status_item(self: "CastSelf") -> "_1827.CustomReportStatusItem":
        from mastapy._private.utility.report import _1827

        return self.__parent__._cast(_1827.CustomReportStatusItem)

    @property
    def custom_report_text(self: "CastSelf") -> "_1830.CustomReportText":
        from mastapy._private.utility.report import _1830

        return self.__parent__._cast(_1830.CustomReportText)

    @property
    def custom_sub_report(self: "CastSelf") -> "_1832.CustomSubReport":
        from mastapy._private.utility.report import _1832

        return self.__parent__._cast(_1832.CustomSubReport)

    @property
    def custom_table(self: "CastSelf") -> "_1833.CustomTable":
        from mastapy._private.utility.report import _1833

        return self.__parent__._cast(_1833.CustomTable)

    @property
    def dynamic_custom_report_item(self: "CastSelf") -> "_1835.DynamicCustomReportItem":
        from mastapy._private.utility.report import _1835

        return self.__parent__._cast(_1835.DynamicCustomReportItem)

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
    def loaded_bearing_chart_reporter(
        self: "CastSelf",
    ) -> "_2003.LoadedBearingChartReporter":
        from mastapy._private.bearings.bearing_results import _2003

        return self.__parent__._cast(_2003.LoadedBearingChartReporter)

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
    def parametric_study_histogram(
        self: "CastSelf",
    ) -> "_4501.ParametricStudyHistogram":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4501,
        )

        return self.__parent__._cast(_4501.ParametricStudyHistogram)

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
    def custom_report_nameable_item(self: "CastSelf") -> "CustomReportNameableItem":
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
class CustomReportNameableItem(_1816.CustomReportItem):
    """CustomReportNameableItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_NAMEABLE_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    def x_position_for_cad(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "XPositionForCAD")

        if temp is None:
            return 0.0

        return temp

    @x_position_for_cad.setter
    @enforce_parameter_types
    def x_position_for_cad(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "XPositionForCAD", float(value) if value is not None else 0.0
        )

    @property
    def y_position_for_cad(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "YPositionForCAD")

        if temp is None:
            return 0.0

        return temp

    @y_position_for_cad.setter
    @enforce_parameter_types
    def y_position_for_cad(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "YPositionForCAD", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportNameableItem":
        """Cast to another type.

        Returns:
            _Cast_CustomReportNameableItem
        """
        return _Cast_CustomReportNameableItem(self)
