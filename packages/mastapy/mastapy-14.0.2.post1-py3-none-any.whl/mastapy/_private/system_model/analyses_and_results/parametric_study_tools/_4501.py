"""ParametricStudyHistogram"""

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

_PARAMETRIC_STUDY_HISTOGRAM = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "ParametricStudyHistogram",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1816, _1824

    Self = TypeVar("Self", bound="ParametricStudyHistogram")
    CastSelf = TypeVar(
        "CastSelf", bound="ParametricStudyHistogram._Cast_ParametricStudyHistogram"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParametricStudyHistogram",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ParametricStudyHistogram:
    """Special nested class for casting ParametricStudyHistogram to subclasses."""

    __parent__: "ParametricStudyHistogram"

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
    def parametric_study_histogram(self: "CastSelf") -> "ParametricStudyHistogram":
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
class ParametricStudyHistogram(_1813.CustomReportDefinitionItem):
    """ParametricStudyHistogram

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PARAMETRIC_STUDY_HISTOGRAM

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
    def number_of_bins(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfBins")

        if temp is None:
            return 0

        return temp

    @number_of_bins.setter
    @enforce_parameter_types
    def number_of_bins(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfBins", int(value) if value is not None else 0
        )

    @property
    def use_bin_range_for_label(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseBinRangeForLabel")

        if temp is None:
            return False

        return temp

    @use_bin_range_for_label.setter
    @enforce_parameter_types
    def use_bin_range_for_label(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseBinRangeForLabel",
            bool(value) if value is not None else False,
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
    def cast_to(self: "Self") -> "_Cast_ParametricStudyHistogram":
        """Cast to another type.

        Returns:
            _Cast_ParametricStudyHistogram
        """
        return _Cast_ParametricStudyHistogram(self)
