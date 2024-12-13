"""ShaftDutyCycleSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_SHAFT_DUTY_CYCLE_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "ShaftDutyCycleSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.shafts import _19
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2895,
    )
    from mastapy._private.system_model.part_model.shaft_model import _2543

    Self = TypeVar("Self", bound="ShaftDutyCycleSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShaftDutyCycleSystemDeflection._Cast_ShaftDutyCycleSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftDutyCycleSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftDutyCycleSystemDeflection:
    """Special nested class for casting ShaftDutyCycleSystemDeflection to subclasses."""

    __parent__: "ShaftDutyCycleSystemDeflection"

    @property
    def shaft_duty_cycle_system_deflection(
        self: "CastSelf",
    ) -> "ShaftDutyCycleSystemDeflection":
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
class ShaftDutyCycleSystemDeflection(_0.APIBase):
    """ShaftDutyCycleSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_DUTY_CYCLE_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def shaft_damage_results(self: "Self") -> "_19.ShaftDamageResults":
        """mastapy.shafts.ShaftDamageResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftDamageResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def shaft_design(self: "Self") -> "_2543.Shaft":
        """mastapy.system_model.part_model.shaft_model.Shaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def shaft_static_analyses(self: "Self") -> "List[_2895.ShaftSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ShaftSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftStaticAnalyses")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftDutyCycleSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_ShaftDutyCycleSystemDeflection
        """
        return _Cast_ShaftDutyCycleSystemDeflection(self)
