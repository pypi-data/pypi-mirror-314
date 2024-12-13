"""LoadedPlainOilFedJournalBearingRow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results.fluid_film import _2179

_LOADED_PLAIN_OIL_FED_JOURNAL_BEARING_ROW = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.FluidFilm",
    "LoadedPlainOilFedJournalBearingRow",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LoadedPlainOilFedJournalBearingRow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedPlainOilFedJournalBearingRow._Cast_LoadedPlainOilFedJournalBearingRow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedPlainOilFedJournalBearingRow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedPlainOilFedJournalBearingRow:
    """Special nested class for casting LoadedPlainOilFedJournalBearingRow to subclasses."""

    __parent__: "LoadedPlainOilFedJournalBearingRow"

    @property
    def loaded_plain_journal_bearing_row(
        self: "CastSelf",
    ) -> "_2179.LoadedPlainJournalBearingRow":
        return self.__parent__._cast(_2179.LoadedPlainJournalBearingRow)

    @property
    def loaded_plain_oil_fed_journal_bearing_row(
        self: "CastSelf",
    ) -> "LoadedPlainOilFedJournalBearingRow":
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
class LoadedPlainOilFedJournalBearingRow(_2179.LoadedPlainJournalBearingRow):
    """LoadedPlainOilFedJournalBearingRow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_PLAIN_OIL_FED_JOURNAL_BEARING_ROW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def attitude_correction_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AttitudeCorrectionFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def load_correction_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCorrectionFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def misalignment_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MisalignmentAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def non_dimensional_misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NonDimensionalMisalignment")

        if temp is None:
            return 0.0

        return temp

    @property
    def power_correction_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerCorrectionFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def pressure_distribution(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PressureDistribution")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def side_flow_correction_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SideFlowCorrectionFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedPlainOilFedJournalBearingRow":
        """Cast to another type.

        Returns:
            _Cast_LoadedPlainOilFedJournalBearingRow
        """
        return _Cast_LoadedPlainOilFedJournalBearingRow(self)
