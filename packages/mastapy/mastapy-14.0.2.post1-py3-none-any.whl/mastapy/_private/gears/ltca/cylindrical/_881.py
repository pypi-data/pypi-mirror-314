"""CylindricalGearLoadDistributionAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.ltca import _865

_CYLINDRICAL_GEAR_LOAD_DISTRIBUTION_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.LTCA.Cylindrical", "CylindricalGearLoadDistributionAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1255, _1258, _1259
    from mastapy._private.gears.gear_two_d_fe_analysis import _923
    from mastapy._private.gears.rating.cylindrical import _473

    Self = TypeVar("Self", bound="CylindricalGearLoadDistributionAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearLoadDistributionAnalysis._Cast_CylindricalGearLoadDistributionAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearLoadDistributionAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearLoadDistributionAnalysis:
    """Special nested class for casting CylindricalGearLoadDistributionAnalysis to subclasses."""

    __parent__: "CylindricalGearLoadDistributionAnalysis"

    @property
    def gear_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_865.GearLoadDistributionAnalysis":
        return self.__parent__._cast(_865.GearLoadDistributionAnalysis)

    @property
    def gear_implementation_analysis(
        self: "CastSelf",
    ) -> "_1259.GearImplementationAnalysis":
        from mastapy._private.gears.analysis import _1259

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
    ) -> "CylindricalGearLoadDistributionAnalysis":
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
class CylindricalGearLoadDistributionAnalysis(_865.GearLoadDistributionAnalysis):
    """CylindricalGearLoadDistributionAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_LOAD_DISTRIBUTION_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def rating(self: "Self") -> "_473.CylindricalGearRating":
        """mastapy.gears.rating.cylindrical.CylindricalGearRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def tiff_analysis(self: "Self") -> "_923.CylindricalGearTIFFAnalysis":
        """mastapy.gears.gear_two_d_fe_analysis.CylindricalGearTIFFAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TIFFAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearLoadDistributionAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearLoadDistributionAnalysis
        """
        return _Cast_CylindricalGearLoadDistributionAnalysis(self)
