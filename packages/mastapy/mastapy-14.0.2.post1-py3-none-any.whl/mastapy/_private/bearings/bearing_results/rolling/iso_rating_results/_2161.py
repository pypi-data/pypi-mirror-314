"""ISOResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ISO_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.IsoRatingResults", "ISOResults"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling.abma import (
        _2171,
        _2172,
        _2173,
    )
    from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
        _2157,
        _2158,
        _2159,
        _2162,
        _2163,
        _2164,
    )

    Self = TypeVar("Self", bound="ISOResults")
    CastSelf = TypeVar("CastSelf", bound="ISOResults._Cast_ISOResults")


__docformat__ = "restructuredtext en"
__all__ = ("ISOResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISOResults:
    """Special nested class for casting ISOResults to subclasses."""

    __parent__: "ISOResults"

    @property
    def ball_iso2812007_results(self: "CastSelf") -> "_2157.BallISO2812007Results":
        from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
            _2157,
        )

        return self.__parent__._cast(_2157.BallISO2812007Results)

    @property
    def ball_isots162812008_results(
        self: "CastSelf",
    ) -> "_2158.BallISOTS162812008Results":
        from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
            _2158,
        )

        return self.__parent__._cast(_2158.BallISOTS162812008Results)

    @property
    def iso2812007_results(self: "CastSelf") -> "_2159.ISO2812007Results":
        from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
            _2159,
        )

        return self.__parent__._cast(_2159.ISO2812007Results)

    @property
    def isots162812008_results(self: "CastSelf") -> "_2162.ISOTS162812008Results":
        from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
            _2162,
        )

        return self.__parent__._cast(_2162.ISOTS162812008Results)

    @property
    def roller_iso2812007_results(self: "CastSelf") -> "_2163.RollerISO2812007Results":
        from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
            _2163,
        )

        return self.__parent__._cast(_2163.RollerISO2812007Results)

    @property
    def roller_isots162812008_results(
        self: "CastSelf",
    ) -> "_2164.RollerISOTS162812008Results":
        from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
            _2164,
        )

        return self.__parent__._cast(_2164.RollerISOTS162812008Results)

    @property
    def ansiabma112014_results(self: "CastSelf") -> "_2171.ANSIABMA112014Results":
        from mastapy._private.bearings.bearing_results.rolling.abma import _2171

        return self.__parent__._cast(_2171.ANSIABMA112014Results)

    @property
    def ansiabma92015_results(self: "CastSelf") -> "_2172.ANSIABMA92015Results":
        from mastapy._private.bearings.bearing_results.rolling.abma import _2172

        return self.__parent__._cast(_2172.ANSIABMA92015Results)

    @property
    def ansiabma_results(self: "CastSelf") -> "_2173.ANSIABMAResults":
        from mastapy._private.bearings.bearing_results.rolling.abma import _2173

        return self.__parent__._cast(_2173.ANSIABMAResults)

    @property
    def iso_results(self: "CastSelf") -> "ISOResults":
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
class ISOResults(_0.APIBase):
    """ISOResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def life_modification_factor_for_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LifeModificationFactorForReliability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputDefaultReportTo", file_path if file_path else ""
        )

    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportTo", file_path if file_path else ""
        )

    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportAsTextTo", file_path if file_path else ""
        )

    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_ISOResults":
        """Cast to another type.

        Returns:
            _Cast_ISOResults
        """
        return _Cast_ISOResults(self)
