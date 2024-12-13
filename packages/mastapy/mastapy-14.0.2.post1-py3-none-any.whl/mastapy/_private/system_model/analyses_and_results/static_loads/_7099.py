"""RingPinsToDiscConnectionLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.static_loads import _7064

_RING_PINS_TO_DISC_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "RingPinsToDiscConnectionLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2742
    from mastapy._private.system_model.analyses_and_results.static_loads import _7002
    from mastapy._private.system_model.connections_and_sockets.cycloidal import _2398

    Self = TypeVar("Self", bound="RingPinsToDiscConnectionLoadCase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RingPinsToDiscConnectionLoadCase._Cast_RingPinsToDiscConnectionLoadCase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RingPinsToDiscConnectionLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RingPinsToDiscConnectionLoadCase:
    """Special nested class for casting RingPinsToDiscConnectionLoadCase to subclasses."""

    __parent__: "RingPinsToDiscConnectionLoadCase"

    @property
    def inter_mountable_component_connection_load_case(
        self: "CastSelf",
    ) -> "_7064.InterMountableComponentConnectionLoadCase":
        return self.__parent__._cast(_7064.InterMountableComponentConnectionLoadCase)

    @property
    def connection_load_case(self: "CastSelf") -> "_7002.ConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7002,
        )

        return self.__parent__._cast(_7002.ConnectionLoadCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2738.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2738

        return self.__parent__._cast(_2738.ConnectionAnalysis)

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
    def ring_pins_to_disc_connection_load_case(
        self: "CastSelf",
    ) -> "RingPinsToDiscConnectionLoadCase":
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
class RingPinsToDiscConnectionLoadCase(_7064.InterMountableComponentConnectionLoadCase):
    """RingPinsToDiscConnectionLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RING_PINS_TO_DISC_CONNECTION_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def number_of_lobes_passed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfLobesPassed")

        if temp is None:
            return 0.0

        return temp

    @number_of_lobes_passed.setter
    @enforce_parameter_types
    def number_of_lobes_passed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfLobesPassed",
            float(value) if value is not None else 0.0,
        )

    @property
    def number_of_steps_for_one_lobe_pass(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfStepsForOneLobePass")

        if temp is None:
            return 0

        return temp

    @property
    def specified_contact_stiffness(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedContactStiffness")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @specified_contact_stiffness.setter
    @enforce_parameter_types
    def specified_contact_stiffness(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "SpecifiedContactStiffness", value)

    @property
    def use_constant_mesh_stiffness(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseConstantMeshStiffness")

        if temp is None:
            return False

        return temp

    @use_constant_mesh_stiffness.setter
    @enforce_parameter_types
    def use_constant_mesh_stiffness(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseConstantMeshStiffness",
            bool(value) if value is not None else False,
        )

    @property
    def connection_design(self: "Self") -> "_2398.RingPinsToDiscConnection":
        """mastapy.system_model.connections_and_sockets.cycloidal.RingPinsToDiscConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_RingPinsToDiscConnectionLoadCase":
        """Cast to another type.

        Returns:
            _Cast_RingPinsToDiscConnectionLoadCase
        """
        return _Cast_RingPinsToDiscConnectionLoadCase(self)
