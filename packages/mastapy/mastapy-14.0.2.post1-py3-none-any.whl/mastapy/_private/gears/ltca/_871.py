"""GearSetLoadDistributionAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.analysis import _1268

_GEAR_SET_LOAD_DISTRIBUTION_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.LTCA", "GearSetLoadDistributionAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1257, _1266, _1269
    from mastapy._private.gears.ltca.conical import _893
    from mastapy._private.gears.ltca.cylindrical import _885, _887

    Self = TypeVar("Self", bound="GearSetLoadDistributionAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearSetLoadDistributionAnalysis._Cast_GearSetLoadDistributionAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetLoadDistributionAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetLoadDistributionAnalysis:
    """Special nested class for casting GearSetLoadDistributionAnalysis to subclasses."""

    __parent__: "GearSetLoadDistributionAnalysis"

    @property
    def gear_set_implementation_analysis(
        self: "CastSelf",
    ) -> "_1268.GearSetImplementationAnalysis":
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
    def cylindrical_gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_885.CylindricalGearSetLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.cylindrical import _885

        return self.__parent__._cast(_885.CylindricalGearSetLoadDistributionAnalysis)

    @property
    def face_gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_887.FaceGearSetLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.cylindrical import _887

        return self.__parent__._cast(_887.FaceGearSetLoadDistributionAnalysis)

    @property
    def conical_gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_893.ConicalGearSetLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.conical import _893

        return self.__parent__._cast(_893.ConicalGearSetLoadDistributionAnalysis)

    @property
    def gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "GearSetLoadDistributionAnalysis":
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
class GearSetLoadDistributionAnalysis(_1268.GearSetImplementationAnalysis):
    """GearSetLoadDistributionAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_LOAD_DISTRIBUTION_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def is_a_system_deflection_analysis(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsASystemDeflectionAnalysis")

        if temp is None:
            return False

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetLoadDistributionAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearSetLoadDistributionAnalysis
        """
        return _Cast_GearSetLoadDistributionAnalysis(self)
