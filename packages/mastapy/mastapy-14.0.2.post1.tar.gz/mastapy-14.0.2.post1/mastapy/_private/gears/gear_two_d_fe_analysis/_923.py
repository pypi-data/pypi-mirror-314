"""CylindricalGearTIFFAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.analysis import _1258

_CYLINDRICAL_GEAR_TIFF_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.GearTwoDFEAnalysis", "CylindricalGearTIFFAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1255
    from mastapy._private.gears.gear_two_d_fe_analysis import _925

    Self = TypeVar("Self", bound="CylindricalGearTIFFAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearTIFFAnalysis._Cast_CylindricalGearTIFFAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearTIFFAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearTIFFAnalysis:
    """Special nested class for casting CylindricalGearTIFFAnalysis to subclasses."""

    __parent__: "CylindricalGearTIFFAnalysis"

    @property
    def gear_design_analysis(self: "CastSelf") -> "_1258.GearDesignAnalysis":
        return self.__parent__._cast(_1258.GearDesignAnalysis)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1255.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1255

        return self.__parent__._cast(_1255.AbstractGearAnalysis)

    @property
    def cylindrical_gear_tiff_analysis(
        self: "CastSelf",
    ) -> "CylindricalGearTIFFAnalysis":
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
class CylindricalGearTIFFAnalysis(_1258.GearDesignAnalysis):
    """CylindricalGearTIFFAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_TIFF_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def analysis(self: "Self") -> "_925.CylindricalGearTwoDimensionalFEAnalysis":
        """mastapy.gears.gear_two_d_fe_analysis.CylindricalGearTwoDimensionalFEAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Analysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearTIFFAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearTIFFAnalysis
        """
        return _Cast_CylindricalGearTIFFAnalysis(self)
