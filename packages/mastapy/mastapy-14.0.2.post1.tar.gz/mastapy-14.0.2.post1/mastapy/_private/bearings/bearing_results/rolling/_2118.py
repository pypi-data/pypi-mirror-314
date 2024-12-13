"""MaximumStaticContactStressResultsAbstract"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_MAXIMUM_STATIC_CONTACT_STRESS_RESULTS_ABSTRACT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "MaximumStaticContactStressResultsAbstract",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2116, _2117

    Self = TypeVar("Self", bound="MaximumStaticContactStressResultsAbstract")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MaximumStaticContactStressResultsAbstract._Cast_MaximumStaticContactStressResultsAbstract",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MaximumStaticContactStressResultsAbstract",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MaximumStaticContactStressResultsAbstract:
    """Special nested class for casting MaximumStaticContactStressResultsAbstract to subclasses."""

    __parent__: "MaximumStaticContactStressResultsAbstract"

    @property
    def maximum_static_contact_stress(
        self: "CastSelf",
    ) -> "_2116.MaximumStaticContactStress":
        from mastapy._private.bearings.bearing_results.rolling import _2116

        return self.__parent__._cast(_2116.MaximumStaticContactStress)

    @property
    def maximum_static_contact_stress_duty_cycle(
        self: "CastSelf",
    ) -> "_2117.MaximumStaticContactStressDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2117

        return self.__parent__._cast(_2117.MaximumStaticContactStressDutyCycle)

    @property
    def maximum_static_contact_stress_results_abstract(
        self: "CastSelf",
    ) -> "MaximumStaticContactStressResultsAbstract":
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
class MaximumStaticContactStressResultsAbstract(_0.APIBase):
    """MaximumStaticContactStressResultsAbstract

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MAXIMUM_STATIC_CONTACT_STRESS_RESULTS_ABSTRACT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def safety_factor_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorInner")

        if temp is None:
            return 0.0

        return temp

    @property
    def safety_factor_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    def stress_ratio_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StressRatioInner")

        if temp is None:
            return 0.0

        return temp

    @property
    def stress_ratio_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StressRatioOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_MaximumStaticContactStressResultsAbstract":
        """Cast to another type.

        Returns:
            _Cast_MaximumStaticContactStressResultsAbstract
        """
        return _Cast_MaximumStaticContactStressResultsAbstract(self)
