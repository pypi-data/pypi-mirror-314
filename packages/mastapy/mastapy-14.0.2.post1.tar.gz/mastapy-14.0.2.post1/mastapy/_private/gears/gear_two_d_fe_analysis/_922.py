"""CylindricalGearSetTIFFAnalysisDutyCycle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.analysis import _1266

_CYLINDRICAL_GEAR_SET_TIFF_ANALYSIS_DUTY_CYCLE = python_net_import(
    "SMT.MastaAPI.Gears.GearTwoDFEAnalysis", "CylindricalGearSetTIFFAnalysisDutyCycle"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1257
    from mastapy._private.gears.gear_two_d_fe_analysis import _924

    Self = TypeVar("Self", bound="CylindricalGearSetTIFFAnalysisDutyCycle")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearSetTIFFAnalysisDutyCycle._Cast_CylindricalGearSetTIFFAnalysisDutyCycle",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearSetTIFFAnalysisDutyCycle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearSetTIFFAnalysisDutyCycle:
    """Special nested class for casting CylindricalGearSetTIFFAnalysisDutyCycle to subclasses."""

    __parent__: "CylindricalGearSetTIFFAnalysisDutyCycle"

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "_1266.GearSetDesignAnalysis":
        return self.__parent__._cast(_1266.GearSetDesignAnalysis)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1257.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1257

        return self.__parent__._cast(_1257.AbstractGearSetAnalysis)

    @property
    def cylindrical_gear_set_tiff_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "CylindricalGearSetTIFFAnalysisDutyCycle":
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
class CylindricalGearSetTIFFAnalysisDutyCycle(_1266.GearSetDesignAnalysis):
    """CylindricalGearSetTIFFAnalysisDutyCycle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SET_TIFF_ANALYSIS_DUTY_CYCLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def gears(self: "Self") -> "List[_924.CylindricalGearTIFFAnalysisDutyCycle]":
        """List[mastapy.gears.gear_two_d_fe_analysis.CylindricalGearTIFFAnalysisDutyCycle]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Gears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearSetTIFFAnalysisDutyCycle":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearSetTIFFAnalysisDutyCycle
        """
        return _Cast_CylindricalGearSetTIFFAnalysisDutyCycle(self)
