"""CustomGraphic"""

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
from mastapy._private.utility.report import _1813

_CUSTOM_GRAPHIC = python_net_import("SMT.MastaAPI.Utility.Report", "CustomGraphic")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2003
    from mastapy._private.utility.report import _1803, _1804, _1806, _1816, _1824

    Self = TypeVar("Self", bound="CustomGraphic")
    CastSelf = TypeVar("CastSelf", bound="CustomGraphic._Cast_CustomGraphic")


__docformat__ = "restructuredtext en"
__all__ = ("CustomGraphic",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomGraphic:
    """Special nested class for casting CustomGraphic to subclasses."""

    __parent__: "CustomGraphic"

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
    def custom_chart(self: "CastSelf") -> "_1803.CustomChart":
        from mastapy._private.utility.report import _1803

        return self.__parent__._cast(_1803.CustomChart)

    @property
    def custom_drawing(self: "CastSelf") -> "_1804.CustomDrawing":
        from mastapy._private.utility.report import _1804

        return self.__parent__._cast(_1804.CustomDrawing)

    @property
    def custom_image(self: "CastSelf") -> "_1806.CustomImage":
        from mastapy._private.utility.report import _1806

        return self.__parent__._cast(_1806.CustomImage)

    @property
    def loaded_bearing_chart_reporter(
        self: "CastSelf",
    ) -> "_2003.LoadedBearingChartReporter":
        from mastapy._private.bearings.bearing_results import _2003

        return self.__parent__._cast(_2003.LoadedBearingChartReporter)

    @property
    def custom_graphic(self: "CastSelf") -> "CustomGraphic":
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
class CustomGraphic(_1813.CustomReportDefinitionItem):
    """CustomGraphic

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_GRAPHIC

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def height(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "Height")

        if temp is None:
            return 0

        return temp

    @height.setter
    @enforce_parameter_types
    def height(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "Height", int(value) if value is not None else 0
        )

    @property
    def height_for_cad(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HeightForCAD")

        if temp is None:
            return 0.0

        return temp

    @height_for_cad.setter
    @enforce_parameter_types
    def height_for_cad(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "HeightForCAD", float(value) if value is not None else 0.0
        )

    @property
    def transposed(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "Transposed")

        if temp is None:
            return False

        return temp

    @transposed.setter
    @enforce_parameter_types
    def transposed(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "Transposed", bool(value) if value is not None else False
        )

    @property
    def width(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0

        return temp

    @width.setter
    @enforce_parameter_types
    def width(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", int(value) if value is not None else 0
        )

    @property
    def width_for_cad(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WidthForCAD")

        if temp is None:
            return 0.0

        return temp

    @width_for_cad.setter
    @enforce_parameter_types
    def width_for_cad(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "WidthForCAD", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CustomGraphic":
        """Cast to another type.

        Returns:
            _Cast_CustomGraphic
        """
        return _Cast_CustomGraphic(self)
