"""ConicalGearSetLoadDistributionAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.ltca import _871

_CONICAL_GEAR_SET_LOAD_DISTRIBUTION_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.LTCA.Conical", "ConicalGearSetLoadDistributionAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1257, _1266, _1268, _1269

    Self = TypeVar("Self", bound="ConicalGearSetLoadDistributionAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearSetLoadDistributionAnalysis._Cast_ConicalGearSetLoadDistributionAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearSetLoadDistributionAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearSetLoadDistributionAnalysis:
    """Special nested class for casting ConicalGearSetLoadDistributionAnalysis to subclasses."""

    __parent__: "ConicalGearSetLoadDistributionAnalysis"

    @property
    def gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_871.GearSetLoadDistributionAnalysis":
        return self.__parent__._cast(_871.GearSetLoadDistributionAnalysis)

    @property
    def gear_set_implementation_analysis(
        self: "CastSelf",
    ) -> "_1268.GearSetImplementationAnalysis":
        from mastapy._private.gears.analysis import _1268

        return self.__parent__._cast(_1268.GearSetImplementationAnalysis)

    @property
    def gear_set_implementation_analysis_abstract(
        self: "CastSelf",
    ) -> "_1269.GearSetImplementationAnalysisAbstract":
        from mastapy._private.gears.analysis import _1269

        return self.__parent__._cast(_1269.GearSetImplementationAnalysisAbstract)

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "_1266.GearSetDesignAnalysis":
        from mastapy._private.gears.analysis import _1266

        return self.__parent__._cast(_1266.GearSetDesignAnalysis)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1257.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1257

        return self.__parent__._cast(_1257.AbstractGearSetAnalysis)

    @property
    def conical_gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "ConicalGearSetLoadDistributionAnalysis":
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
class ConicalGearSetLoadDistributionAnalysis(_871.GearSetLoadDistributionAnalysis):
    """ConicalGearSetLoadDistributionAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_SET_LOAD_DISTRIBUTION_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearSetLoadDistributionAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearSetLoadDistributionAnalysis
        """
        return _Cast_ConicalGearSetLoadDistributionAnalysis(self)
