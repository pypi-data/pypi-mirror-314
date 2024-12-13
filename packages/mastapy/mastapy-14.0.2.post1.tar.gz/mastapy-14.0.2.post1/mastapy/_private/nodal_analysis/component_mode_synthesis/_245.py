"""RealCMSResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.nodal_analysis.component_mode_synthesis import _242

_REAL_CMS_RESULTS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis", "RealCMSResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.component_mode_synthesis import _244, _248
    from mastapy._private.nodal_analysis.states import _125

    Self = TypeVar("Self", bound="RealCMSResults")
    CastSelf = TypeVar("CastSelf", bound="RealCMSResults._Cast_RealCMSResults")


__docformat__ = "restructuredtext en"
__all__ = ("RealCMSResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RealCMSResults:
    """Special nested class for casting RealCMSResults to subclasses."""

    __parent__: "RealCMSResults"

    @property
    def cms_results(self: "CastSelf") -> "_242.CMSResults":
        return self.__parent__._cast(_242.CMSResults)

    @property
    def modal_cms_results(self: "CastSelf") -> "_244.ModalCMSResults":
        from mastapy._private.nodal_analysis.component_mode_synthesis import _244

        return self.__parent__._cast(_244.ModalCMSResults)

    @property
    def static_cms_results(self: "CastSelf") -> "_248.StaticCMSResults":
        from mastapy._private.nodal_analysis.component_mode_synthesis import _248

        return self.__parent__._cast(_248.StaticCMSResults)

    @property
    def real_cms_results(self: "CastSelf") -> "RealCMSResults":
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
class RealCMSResults(_242.CMSResults):
    """RealCMSResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _REAL_CMS_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def node_displacements(self: "Self") -> "_125.NodeVectorState":
        """mastapy.nodal_analysis.states.NodeVectorState

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NodeDisplacements")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_RealCMSResults":
        """Cast to another type.

        Returns:
            _Cast_RealCMSResults
        """
        return _Cast_RealCMSResults(self)
