"""ShaftSectionSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.nodal_analysis.nodal_entities import _127

_SHAFT_SECTION_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "ShaftSectionSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import _144, _146
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2893,
    )

    Self = TypeVar("Self", bound="ShaftSectionSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShaftSectionSystemDeflection._Cast_ShaftSectionSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftSectionSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftSectionSystemDeflection:
    """Special nested class for casting ShaftSectionSystemDeflection to subclasses."""

    __parent__: "ShaftSectionSystemDeflection"

    @property
    def bar(self: "CastSelf") -> "_127.Bar":
        return self.__parent__._cast(_127.Bar)

    @property
    def nodal_component(self: "CastSelf") -> "_144.NodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _144

        return self.__parent__._cast(_144.NodalComponent)

    @property
    def nodal_entity(self: "CastSelf") -> "_146.NodalEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _146

        return self.__parent__._cast(_146.NodalEntity)

    @property
    def shaft_section_system_deflection(
        self: "CastSelf",
    ) -> "ShaftSectionSystemDeflection":
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
class ShaftSectionSystemDeflection(_127.Bar):
    """ShaftSectionSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_SECTION_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def left_end(self: "Self") -> "_2893.ShaftSectionEndResultsSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.ShaftSectionEndResultsSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftEnd")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def right_end(self: "Self") -> "_2893.ShaftSectionEndResultsSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.ShaftSectionEndResultsSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightEnd")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftSectionSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_ShaftSectionSystemDeflection
        """
        return _Cast_ShaftSectionSystemDeflection(self)
