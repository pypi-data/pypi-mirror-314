"""CustomReportHtmlItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.report import _1813

_CUSTOM_REPORT_HTML_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportHtmlItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1816, _1824

    Self = TypeVar("Self", bound="CustomReportHtmlItem")
    CastSelf = TypeVar(
        "CastSelf", bound="CustomReportHtmlItem._Cast_CustomReportHtmlItem"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportHtmlItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportHtmlItem:
    """Special nested class for casting CustomReportHtmlItem to subclasses."""

    __parent__: "CustomReportHtmlItem"

    @property
    def custom_report_definition_item(
        self: "CastSelf",
    ) -> "_1813.CustomReportDefinitionItem":
        return self.__parent__._cast(_1813.CustomReportDefinitionItem)

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
    def custom_report_html_item(self: "CastSelf") -> "CustomReportHtmlItem":
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
class CustomReportHtmlItem(_1813.CustomReportDefinitionItem):
    """CustomReportHtmlItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_HTML_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportHtmlItem":
        """Cast to another type.

        Returns:
            _Cast_CustomReportHtmlItem
        """
        return _Cast_CustomReportHtmlItem(self)
