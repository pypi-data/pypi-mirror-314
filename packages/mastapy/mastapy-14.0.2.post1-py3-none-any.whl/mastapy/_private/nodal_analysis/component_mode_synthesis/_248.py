"""StaticCMSResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.nodal_analysis.component_mode_synthesis import _245

_STATIC_CMS_RESULTS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis", "StaticCMSResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.component_mode_synthesis import _242
    from mastapy._private.nodal_analysis.states import _125

    Self = TypeVar("Self", bound="StaticCMSResults")
    CastSelf = TypeVar("CastSelf", bound="StaticCMSResults._Cast_StaticCMSResults")


__docformat__ = "restructuredtext en"
__all__ = ("StaticCMSResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StaticCMSResults:
    """Special nested class for casting StaticCMSResults to subclasses."""

    __parent__: "StaticCMSResults"

    @property
    def real_cms_results(self: "CastSelf") -> "_245.RealCMSResults":
        return self.__parent__._cast(_245.RealCMSResults)

    @property
    def cms_results(self: "CastSelf") -> "_242.CMSResults":
        from mastapy._private.nodal_analysis.component_mode_synthesis import _242

        return self.__parent__._cast(_242.CMSResults)

    @property
    def static_cms_results(self: "CastSelf") -> "StaticCMSResults":
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
class StaticCMSResults(_245.RealCMSResults):
    """StaticCMSResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STATIC_CMS_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def node_stress_tensors(self: "Self") -> "_125.NodeVectorState":
        """mastapy.nodal_analysis.states.NodeVectorState

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NodeStressTensors")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    def calculate_stress(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CalculateStress")

    @property
    def cast_to(self: "Self") -> "_Cast_StaticCMSResults":
        """Cast to another type.

        Returns:
            _Cast_StaticCMSResults
        """
        return _Cast_StaticCMSResults(self)
