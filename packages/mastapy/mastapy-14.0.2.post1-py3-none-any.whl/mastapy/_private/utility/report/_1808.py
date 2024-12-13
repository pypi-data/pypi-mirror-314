"""CustomReportCadDrawing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.report import _1824

_CUSTOM_REPORT_CAD_DRAWING = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportCadDrawing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.cad_export import _1888
    from mastapy._private.utility.report import _1816

    Self = TypeVar("Self", bound="CustomReportCadDrawing")
    CastSelf = TypeVar(
        "CastSelf", bound="CustomReportCadDrawing._Cast_CustomReportCadDrawing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportCadDrawing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportCadDrawing:
    """Special nested class for casting CustomReportCadDrawing to subclasses."""

    __parent__: "CustomReportCadDrawing"

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
    def custom_report_cad_drawing(self: "CastSelf") -> "CustomReportCadDrawing":
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
class CustomReportCadDrawing(_1824.CustomReportNameableItem):
    """CustomReportCadDrawing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_CAD_DRAWING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def scale(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Scale")

        if temp is None:
            return 0.0

        return temp

    @scale.setter
    @enforce_parameter_types
    def scale(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Scale", float(value) if value is not None else 0.0
        )

    @property
    def stock_drawing(self: "Self") -> "_1888.StockDrawings":
        """mastapy.utility.cad_export.StockDrawings"""
        temp = pythonnet_property_get(self.wrapped, "StockDrawing")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.CadExport.StockDrawings"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility.cad_export._1888", "StockDrawings"
        )(value)

    @stock_drawing.setter
    @enforce_parameter_types
    def stock_drawing(self: "Self", value: "_1888.StockDrawings") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Utility.CadExport.StockDrawings"
        )
        pythonnet_property_set(self.wrapped, "StockDrawing", value)

    @property
    def use_stock_drawing(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseStockDrawing")

        if temp is None:
            return False

        return temp

    @use_stock_drawing.setter
    @enforce_parameter_types
    def use_stock_drawing(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "UseStockDrawing", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportCadDrawing":
        """Cast to another type.

        Returns:
            _Cast_CustomReportCadDrawing
        """
        return _Cast_CustomReportCadDrawing(self)
