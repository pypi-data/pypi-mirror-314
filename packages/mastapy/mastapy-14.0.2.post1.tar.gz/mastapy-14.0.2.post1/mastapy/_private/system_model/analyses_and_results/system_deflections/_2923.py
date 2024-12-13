"""TorsionalSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.system_deflections import _2916

_TORSIONAL_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "TorsionalSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2739
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7709,
        _7718,
        _7724,
    )

    Self = TypeVar("Self", bound="TorsionalSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf", bound="TorsionalSystemDeflection._Cast_TorsionalSystemDeflection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TorsionalSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TorsionalSystemDeflection:
    """Special nested class for casting TorsionalSystemDeflection to subclasses."""

    __parent__: "TorsionalSystemDeflection"

    @property
    def system_deflection(self: "CastSelf") -> "_2916.SystemDeflection":
        return self.__parent__._cast(_2916.SystemDeflection)

    @property
    def fe_analysis(self: "CastSelf") -> "_7718.FEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7718,
        )

        return self.__parent__._cast(_7718.FEAnalysis)

    @property
    def static_load_analysis_case(self: "CastSelf") -> "_7724.StaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7724,
        )

        return self.__parent__._cast(_7724.StaticLoadAnalysisCase)

    @property
    def analysis_case(self: "CastSelf") -> "_7709.AnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7709,
        )

        return self.__parent__._cast(_7709.AnalysisCase)

    @property
    def context(self: "CastSelf") -> "_2739.Context":
        from mastapy._private.system_model.analyses_and_results import _2739

        return self.__parent__._cast(_2739.Context)

    @property
    def torsional_system_deflection(self: "CastSelf") -> "TorsionalSystemDeflection":
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
class TorsionalSystemDeflection(_2916.SystemDeflection):
    """TorsionalSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TORSIONAL_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_TorsionalSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_TorsionalSystemDeflection
        """
        return _Cast_TorsionalSystemDeflection(self)
