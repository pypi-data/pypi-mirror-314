"""TorsionalSystemDeflectionAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results import _2709

_TORSIONAL_SYSTEM_DEFLECTION_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults", "TorsionalSystemDeflectionAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private import _7727

    Self = TypeVar("Self", bound="TorsionalSystemDeflectionAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TorsionalSystemDeflectionAnalysis._Cast_TorsionalSystemDeflectionAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TorsionalSystemDeflectionAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TorsionalSystemDeflectionAnalysis:
    """Special nested class for casting TorsionalSystemDeflectionAnalysis to subclasses."""

    __parent__: "TorsionalSystemDeflectionAnalysis"

    @property
    def single_analysis(self: "CastSelf") -> "_2709.SingleAnalysis":
        return self.__parent__._cast(_2709.SingleAnalysis)

    @property
    def marshal_by_ref_object_permanent(
        self: "CastSelf",
    ) -> "_7727.MarshalByRefObjectPermanent":
        from mastapy._private import _7727

        return self.__parent__._cast(_7727.MarshalByRefObjectPermanent)

    @property
    def torsional_system_deflection_analysis(
        self: "CastSelf",
    ) -> "TorsionalSystemDeflectionAnalysis":
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
class TorsionalSystemDeflectionAnalysis(_2709.SingleAnalysis):
    """TorsionalSystemDeflectionAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TORSIONAL_SYSTEM_DEFLECTION_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_TorsionalSystemDeflectionAnalysis":
        """Cast to another type.

        Returns:
            _Cast_TorsionalSystemDeflectionAnalysis
        """
        return _Cast_TorsionalSystemDeflectionAnalysis(self)
