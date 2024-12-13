"""BearingRatingLife"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results.rolling.skf_module import _2152

_BEARING_RATING_LIFE = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule", "BearingRatingLife"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling.skf_module import _2146

    Self = TypeVar("Self", bound="BearingRatingLife")
    CastSelf = TypeVar("CastSelf", bound="BearingRatingLife._Cast_BearingRatingLife")


__docformat__ = "restructuredtext en"
__all__ = ("BearingRatingLife",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BearingRatingLife:
    """Special nested class for casting BearingRatingLife to subclasses."""

    __parent__: "BearingRatingLife"

    @property
    def skf_calculation_result(self: "CastSelf") -> "_2152.SKFCalculationResult":
        return self.__parent__._cast(_2152.SKFCalculationResult)

    @property
    def bearing_rating_life(self: "CastSelf") -> "BearingRatingLife":
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
class BearingRatingLife(_2152.SKFCalculationResult):
    """BearingRatingLife

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING_RATING_LIFE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def contamination_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContaminationFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def skf_life_modification_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SKFLifeModificationFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def life_model(self: "Self") -> "_2146.LifeModel":
        """mastapy.bearings.bearing_results.rolling.skf_module.LifeModel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LifeModel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_BearingRatingLife":
        """Cast to another type.

        Returns:
            _Cast_BearingRatingLife
        """
        return _Cast_BearingRatingLife(self)
