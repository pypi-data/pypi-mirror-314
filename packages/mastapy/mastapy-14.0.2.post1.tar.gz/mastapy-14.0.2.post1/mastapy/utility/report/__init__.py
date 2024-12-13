"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.report._1795 import AdHocCustomTable
    from mastapy._private.utility.report._1796 import AxisSettings
    from mastapy._private.utility.report._1797 import BlankRow
    from mastapy._private.utility.report._1798 import CadPageOrientation
    from mastapy._private.utility.report._1799 import CadPageSize
    from mastapy._private.utility.report._1800 import CadTableBorderType
    from mastapy._private.utility.report._1801 import ChartDefinition
    from mastapy._private.utility.report._1802 import SMTChartPointShape
    from mastapy._private.utility.report._1803 import CustomChart
    from mastapy._private.utility.report._1804 import CustomDrawing
    from mastapy._private.utility.report._1805 import CustomGraphic
    from mastapy._private.utility.report._1806 import CustomImage
    from mastapy._private.utility.report._1807 import CustomReport
    from mastapy._private.utility.report._1808 import CustomReportCadDrawing
    from mastapy._private.utility.report._1809 import CustomReportChart
    from mastapy._private.utility.report._1810 import CustomReportChartItem
    from mastapy._private.utility.report._1811 import CustomReportColumn
    from mastapy._private.utility.report._1812 import CustomReportColumns
    from mastapy._private.utility.report._1813 import CustomReportDefinitionItem
    from mastapy._private.utility.report._1814 import CustomReportHorizontalLine
    from mastapy._private.utility.report._1815 import CustomReportHtmlItem
    from mastapy._private.utility.report._1816 import CustomReportItem
    from mastapy._private.utility.report._1817 import CustomReportItemContainer
    from mastapy._private.utility.report._1818 import (
        CustomReportItemContainerCollection,
    )
    from mastapy._private.utility.report._1819 import (
        CustomReportItemContainerCollectionBase,
    )
    from mastapy._private.utility.report._1820 import (
        CustomReportItemContainerCollectionItem,
    )
    from mastapy._private.utility.report._1821 import CustomReportKey
    from mastapy._private.utility.report._1822 import CustomReportMultiPropertyItem
    from mastapy._private.utility.report._1823 import CustomReportMultiPropertyItemBase
    from mastapy._private.utility.report._1824 import CustomReportNameableItem
    from mastapy._private.utility.report._1825 import CustomReportNamedItem
    from mastapy._private.utility.report._1826 import CustomReportPropertyItem
    from mastapy._private.utility.report._1827 import CustomReportStatusItem
    from mastapy._private.utility.report._1828 import CustomReportTab
    from mastapy._private.utility.report._1829 import CustomReportTabs
    from mastapy._private.utility.report._1830 import CustomReportText
    from mastapy._private.utility.report._1831 import CustomRow
    from mastapy._private.utility.report._1832 import CustomSubReport
    from mastapy._private.utility.report._1833 import CustomTable
    from mastapy._private.utility.report._1834 import DefinitionBooleanCheckOptions
    from mastapy._private.utility.report._1835 import DynamicCustomReportItem
    from mastapy._private.utility.report._1836 import FontStyle
    from mastapy._private.utility.report._1837 import FontWeight
    from mastapy._private.utility.report._1838 import HeadingSize
    from mastapy._private.utility.report._1839 import SimpleChartDefinition
    from mastapy._private.utility.report._1840 import UserTextRow
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.report._1795": ["AdHocCustomTable"],
        "_private.utility.report._1796": ["AxisSettings"],
        "_private.utility.report._1797": ["BlankRow"],
        "_private.utility.report._1798": ["CadPageOrientation"],
        "_private.utility.report._1799": ["CadPageSize"],
        "_private.utility.report._1800": ["CadTableBorderType"],
        "_private.utility.report._1801": ["ChartDefinition"],
        "_private.utility.report._1802": ["SMTChartPointShape"],
        "_private.utility.report._1803": ["CustomChart"],
        "_private.utility.report._1804": ["CustomDrawing"],
        "_private.utility.report._1805": ["CustomGraphic"],
        "_private.utility.report._1806": ["CustomImage"],
        "_private.utility.report._1807": ["CustomReport"],
        "_private.utility.report._1808": ["CustomReportCadDrawing"],
        "_private.utility.report._1809": ["CustomReportChart"],
        "_private.utility.report._1810": ["CustomReportChartItem"],
        "_private.utility.report._1811": ["CustomReportColumn"],
        "_private.utility.report._1812": ["CustomReportColumns"],
        "_private.utility.report._1813": ["CustomReportDefinitionItem"],
        "_private.utility.report._1814": ["CustomReportHorizontalLine"],
        "_private.utility.report._1815": ["CustomReportHtmlItem"],
        "_private.utility.report._1816": ["CustomReportItem"],
        "_private.utility.report._1817": ["CustomReportItemContainer"],
        "_private.utility.report._1818": ["CustomReportItemContainerCollection"],
        "_private.utility.report._1819": ["CustomReportItemContainerCollectionBase"],
        "_private.utility.report._1820": ["CustomReportItemContainerCollectionItem"],
        "_private.utility.report._1821": ["CustomReportKey"],
        "_private.utility.report._1822": ["CustomReportMultiPropertyItem"],
        "_private.utility.report._1823": ["CustomReportMultiPropertyItemBase"],
        "_private.utility.report._1824": ["CustomReportNameableItem"],
        "_private.utility.report._1825": ["CustomReportNamedItem"],
        "_private.utility.report._1826": ["CustomReportPropertyItem"],
        "_private.utility.report._1827": ["CustomReportStatusItem"],
        "_private.utility.report._1828": ["CustomReportTab"],
        "_private.utility.report._1829": ["CustomReportTabs"],
        "_private.utility.report._1830": ["CustomReportText"],
        "_private.utility.report._1831": ["CustomRow"],
        "_private.utility.report._1832": ["CustomSubReport"],
        "_private.utility.report._1833": ["CustomTable"],
        "_private.utility.report._1834": ["DefinitionBooleanCheckOptions"],
        "_private.utility.report._1835": ["DynamicCustomReportItem"],
        "_private.utility.report._1836": ["FontStyle"],
        "_private.utility.report._1837": ["FontWeight"],
        "_private.utility.report._1838": ["HeadingSize"],
        "_private.utility.report._1839": ["SimpleChartDefinition"],
        "_private.utility.report._1840": ["UserTextRow"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AdHocCustomTable",
    "AxisSettings",
    "BlankRow",
    "CadPageOrientation",
    "CadPageSize",
    "CadTableBorderType",
    "ChartDefinition",
    "SMTChartPointShape",
    "CustomChart",
    "CustomDrawing",
    "CustomGraphic",
    "CustomImage",
    "CustomReport",
    "CustomReportCadDrawing",
    "CustomReportChart",
    "CustomReportChartItem",
    "CustomReportColumn",
    "CustomReportColumns",
    "CustomReportDefinitionItem",
    "CustomReportHorizontalLine",
    "CustomReportHtmlItem",
    "CustomReportItem",
    "CustomReportItemContainer",
    "CustomReportItemContainerCollection",
    "CustomReportItemContainerCollectionBase",
    "CustomReportItemContainerCollectionItem",
    "CustomReportKey",
    "CustomReportMultiPropertyItem",
    "CustomReportMultiPropertyItemBase",
    "CustomReportNameableItem",
    "CustomReportNamedItem",
    "CustomReportPropertyItem",
    "CustomReportStatusItem",
    "CustomReportTab",
    "CustomReportTabs",
    "CustomReportText",
    "CustomRow",
    "CustomSubReport",
    "CustomTable",
    "DefinitionBooleanCheckOptions",
    "DynamicCustomReportItem",
    "FontStyle",
    "FontWeight",
    "HeadingSize",
    "SimpleChartDefinition",
    "UserTextRow",
)
