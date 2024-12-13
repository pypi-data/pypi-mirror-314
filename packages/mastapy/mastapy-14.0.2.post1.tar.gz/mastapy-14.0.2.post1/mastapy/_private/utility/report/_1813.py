"""CustomReportDefinitionItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.report import _1824

_CUSTOM_REPORT_DEFINITION_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportDefinitionItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2003
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4501,
    )
    from mastapy._private.utility.report import (
        _1795,
        _1803,
        _1804,
        _1805,
        _1806,
        _1815,
        _1816,
        _1827,
        _1830,
        _1832,
    )

    Self = TypeVar("Self", bound="CustomReportDefinitionItem")
    CastSelf = TypeVar(
        "CastSelf", bound="CustomReportDefinitionItem._Cast_CustomReportDefinitionItem"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportDefinitionItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportDefinitionItem:
    """Special nested class for casting CustomReportDefinitionItem to subclasses."""

    __parent__: "CustomReportDefinitionItem"

    @property
    def custom_report_nameable_item(
        self: "CastSelf",
    ) -> "_1824.CustomReportNameableItem":
        return self.__parent__._cast(_1824.CustomReportNameableItem)

    @property
    def custom_report_item(self: "CastSelf") -> "_1816.CustomReportItem":
        from mastapy._private.utility.report import _1816

        return self.__parent__._cast(_1816.CustomReportItem)

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
    def custom_report_html_item(self: "CastSelf") -> "_1815.CustomReportHtmlItem":
        from mastapy._private.utility.report import _1815

        return self.__parent__._cast(_1815.CustomReportHtmlItem)

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
    def loaded_bearing_chart_reporter(
        self: "CastSelf",
    ) -> "_2003.LoadedBearingChartReporter":
        from mastapy._private.bearings.bearing_results import _2003

        return self.__parent__._cast(_2003.LoadedBearingChartReporter)

    @property
    def parametric_study_histogram(
        self: "CastSelf",
    ) -> "_4501.ParametricStudyHistogram":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4501,
        )

        return self.__parent__._cast(_4501.ParametricStudyHistogram)

    @property
    def custom_report_definition_item(self: "CastSelf") -> "CustomReportDefinitionItem":
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
class CustomReportDefinitionItem(_1824.CustomReportNameableItem):
    """CustomReportDefinitionItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_DEFINITION_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportDefinitionItem":
        """Cast to another type.

        Returns:
            _Cast_CustomReportDefinitionItem
        """
        return _Cast_CustomReportDefinitionItem(self)
