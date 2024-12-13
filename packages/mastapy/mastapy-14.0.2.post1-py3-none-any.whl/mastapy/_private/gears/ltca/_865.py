"""GearLoadDistributionAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.analysis import _1259

_GEAR_LOAD_DISTRIBUTION_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.LTCA", "GearLoadDistributionAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1255, _1258
    from mastapy._private.gears.ltca.conical import _892
    from mastapy._private.gears.ltca.cylindrical import _881

    Self = TypeVar("Self", bound="GearLoadDistributionAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearLoadDistributionAnalysis._Cast_GearLoadDistributionAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearLoadDistributionAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearLoadDistributionAnalysis:
    """Special nested class for casting GearLoadDistributionAnalysis to subclasses."""

    __parent__: "GearLoadDistributionAnalysis"

    @property
    def gear_implementation_analysis(
        self: "CastSelf",
    ) -> "_1259.GearImplementationAnalysis":
        return self.__parent__._cast(_1259.GearImplementationAnalysis)

    @property
    def gear_design_analysis(self: "CastSelf") -> "_1258.GearDesignAnalysis":
        from mastapy._private.gears.analysis import _1258

        return self.__parent__._cast(_1258.GearDesignAnalysis)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1255.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1255

        return self.__parent__._cast(_1255.AbstractGearAnalysis)

    @property
    def cylindrical_gear_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_881.CylindricalGearLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.cylindrical import _881

        return self.__parent__._cast(_881.CylindricalGearLoadDistributionAnalysis)

    @property
    def conical_gear_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_892.ConicalGearLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.conical import _892

        return self.__parent__._cast(_892.ConicalGearLoadDistributionAnalysis)

    @property
    def gear_load_distribution_analysis(
        self: "CastSelf",
    ) -> "GearLoadDistributionAnalysis":
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
class GearLoadDistributionAnalysis(_1259.GearImplementationAnalysis):
    """GearLoadDistributionAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_LOAD_DISTRIBUTION_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearLoadDistributionAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearLoadDistributionAnalysis
        """
        return _Cast_GearLoadDistributionAnalysis(self)
