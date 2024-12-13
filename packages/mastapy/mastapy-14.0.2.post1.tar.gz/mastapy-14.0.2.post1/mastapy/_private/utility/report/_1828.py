"""CustomReportTab"""

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
from mastapy._private.utility.report import _1820

_CUSTOM_REPORT_TAB = python_net_import("SMT.MastaAPI.Utility.Report", "CustomReportTab")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1816, _1817

    Self = TypeVar("Self", bound="CustomReportTab")
    CastSelf = TypeVar("CastSelf", bound="CustomReportTab._Cast_CustomReportTab")


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportTab",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportTab:
    """Special nested class for casting CustomReportTab to subclasses."""

    __parent__: "CustomReportTab"

    @property
    def custom_report_item_container_collection_item(
        self: "CastSelf",
    ) -> "_1820.CustomReportItemContainerCollectionItem":
        return self.__parent__._cast(_1820.CustomReportItemContainerCollectionItem)

    @property
    def custom_report_item_container(
        self: "CastSelf",
    ) -> "_1817.CustomReportItemContainer":
        from mastapy._private.utility.report import _1817

        return self.__parent__._cast(_1817.CustomReportItemContainer)

    @property
    def custom_report_item(self: "CastSelf") -> "_1816.CustomReportItem":
        from mastapy._private.utility.report import _1816

        return self.__parent__._cast(_1816.CustomReportItem)

    @property
    def custom_report_tab(self: "CastSelf") -> "CustomReportTab":
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
class CustomReportTab(_1820.CustomReportItemContainerCollectionItem):
    """CustomReportTab

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_TAB

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def hide_when_has_no_content(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HideWhenHasNoContent")

        if temp is None:
            return False

        return temp

    @hide_when_has_no_content.setter
    @enforce_parameter_types
    def hide_when_has_no_content(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HideWhenHasNoContent",
            bool(value) if value is not None else False,
        )

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
    def show_if_empty(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowIfEmpty")

        if temp is None:
            return False

        return temp

    @show_if_empty.setter
    @enforce_parameter_types
    def show_if_empty(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowIfEmpty", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportTab":
        """Cast to another type.

        Returns:
            _Cast_CustomReportTab
        """
        return _Cast_CustomReportTab(self)
