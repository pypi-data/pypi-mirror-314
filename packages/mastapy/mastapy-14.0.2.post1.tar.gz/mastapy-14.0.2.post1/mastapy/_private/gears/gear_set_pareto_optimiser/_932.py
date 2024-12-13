"""DesignSpaceSearchCandidateBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

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

_DESIGN_SPACE_SEARCH_CANDIDATE_BASE = python_net_import(
    "SMT.MastaAPI.Gears.GearSetParetoOptimiser", "DesignSpaceSearchCandidateBase"
)

if TYPE_CHECKING:
    from typing import Any, List, Type

    from mastapy._private.gears.analysis import _1257
    from mastapy._private.gears.gear_set_pareto_optimiser import _936, _942

    Self = TypeVar("Self", bound="DesignSpaceSearchCandidateBase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DesignSpaceSearchCandidateBase._Cast_DesignSpaceSearchCandidateBase",
    )

TAnalysis = TypeVar("TAnalysis", bound="_1257.AbstractGearSetAnalysis")
TCandidate = TypeVar("TCandidate", bound="DesignSpaceSearchCandidateBase")

__docformat__ = "restructuredtext en"
__all__ = ("DesignSpaceSearchCandidateBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DesignSpaceSearchCandidateBase:
    """Special nested class for casting DesignSpaceSearchCandidateBase to subclasses."""

    __parent__: "DesignSpaceSearchCandidateBase"

    @property
    def gear_set_optimiser_candidate(
        self: "CastSelf",
    ) -> "_936.GearSetOptimiserCandidate":
        from mastapy._private.gears.gear_set_pareto_optimiser import _936

        return self.__parent__._cast(_936.GearSetOptimiserCandidate)

    @property
    def micro_geometry_design_space_search_candidate(
        self: "CastSelf",
    ) -> "_942.MicroGeometryDesignSpaceSearchCandidate":
        from mastapy._private.gears.gear_set_pareto_optimiser import _942

        return self.__parent__._cast(_942.MicroGeometryDesignSpaceSearchCandidate)

    @property
    def design_space_search_candidate_base(
        self: "CastSelf",
    ) -> "DesignSpaceSearchCandidateBase":
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
class DesignSpaceSearchCandidateBase(_0.APIBase, Generic[TAnalysis, TCandidate]):
    """DesignSpaceSearchCandidateBase

    This is a mastapy class.

    Generic Types:
        TAnalysis
        TCandidate
    """

    TYPE: ClassVar["Type"] = _DESIGN_SPACE_SEARCH_CANDIDATE_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def design_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignName")

        if temp is None:
            return ""

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

    def select_candidate(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SelectCandidate")

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
    def cast_to(self: "Self") -> "_Cast_DesignSpaceSearchCandidateBase":
        """Cast to another type.

        Returns:
            _Cast_DesignSpaceSearchCandidateBase
        """
        return _Cast_DesignSpaceSearchCandidateBase(self)
