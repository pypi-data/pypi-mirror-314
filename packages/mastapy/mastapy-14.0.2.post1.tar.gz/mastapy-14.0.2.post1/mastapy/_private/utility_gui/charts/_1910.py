"""CustomTableAndChart"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.report import _1833

_CUSTOM_TABLE_AND_CHART = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Charts", "CustomTableAndChart"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1816, _1822, _1823, _1824

    Self = TypeVar("Self", bound="CustomTableAndChart")
    CastSelf = TypeVar(
        "CastSelf", bound="CustomTableAndChart._Cast_CustomTableAndChart"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomTableAndChart",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomTableAndChart:
    """Special nested class for casting CustomTableAndChart to subclasses."""

    __parent__: "CustomTableAndChart"

    @property
    def custom_table(self: "CastSelf") -> "_1833.CustomTable":
        return self.__parent__._cast(_1833.CustomTable)

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
    def custom_table_and_chart(self: "CastSelf") -> "CustomTableAndChart":
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
class CustomTableAndChart(_1833.CustomTable):
    """CustomTableAndChart

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_TABLE_AND_CHART

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CustomTableAndChart":
        """Cast to another type.

        Returns:
            _Cast_CustomTableAndChart
        """
        return _Cast_CustomTableAndChart(self)
