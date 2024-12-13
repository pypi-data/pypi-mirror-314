"""AbstractShaftLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.static_loads import _6961

_ABSTRACT_SHAFT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "AbstractShaftLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740, _2742, _2746
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6990,
        _7012,
        _7083,
        _7105,
    )
    from mastapy._private.system_model.part_model import _2493

    Self = TypeVar("Self", bound="AbstractShaftLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="AbstractShaftLoadCase._Cast_AbstractShaftLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftLoadCase:
    """Special nested class for casting AbstractShaftLoadCase to subclasses."""

    __parent__: "AbstractShaftLoadCase"

    @property
    def abstract_shaft_or_housing_load_case(
        self: "CastSelf",
    ) -> "_6961.AbstractShaftOrHousingLoadCase":
        return self.__parent__._cast(_6961.AbstractShaftOrHousingLoadCase)

    @property
    def component_load_case(self: "CastSelf") -> "_6990.ComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6990,
        )

        return self.__parent__._cast(_6990.ComponentLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7083.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7083,
        )

        return self.__parent__._cast(_7083.PartLoadCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2746.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2746

        return self.__parent__._cast(_2746.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2742.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2742

        return self.__parent__._cast(_2742.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2740.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2740

        return self.__parent__._cast(_2740.DesignEntityAnalysis)

    @property
    def cycloidal_disc_load_case(self: "CastSelf") -> "_7012.CycloidalDiscLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7012,
        )

        return self.__parent__._cast(_7012.CycloidalDiscLoadCase)

    @property
    def shaft_load_case(self: "CastSelf") -> "_7105.ShaftLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7105,
        )

        return self.__parent__._cast(_7105.ShaftLoadCase)

    @property
    def abstract_shaft_load_case(self: "CastSelf") -> "AbstractShaftLoadCase":
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
class AbstractShaftLoadCase(_6961.AbstractShaftOrHousingLoadCase):
    """AbstractShaftLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_SHAFT_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2493.AbstractShaft":
        """mastapy.system_model.part_model.AbstractShaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractShaftLoadCase":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftLoadCase
        """
        return _Cast_AbstractShaftLoadCase(self)
