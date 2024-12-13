"""MicrophoneArray"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2537

_MICROPHONE_ARRAY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MicrophoneArray"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model import _2260
    from mastapy._private.system_model.part_model import _2492, _2522, _2528
    from mastapy._private.system_model.part_model.acoustics import _2700

    Self = TypeVar("Self", bound="MicrophoneArray")
    CastSelf = TypeVar("CastSelf", bound="MicrophoneArray._Cast_MicrophoneArray")


__docformat__ = "restructuredtext en"
__all__ = ("MicrophoneArray",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MicrophoneArray:
    """Special nested class for casting MicrophoneArray to subclasses."""

    __parent__: "MicrophoneArray"

    @property
    def specialised_assembly(self: "CastSelf") -> "_2537.SpecialisedAssembly":
        return self.__parent__._cast(_2537.SpecialisedAssembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2492.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2492

        return self.__parent__._cast(_2492.AbstractAssembly)

    @property
    def part(self: "CastSelf") -> "_2528.Part":
        from mastapy._private.system_model.part_model import _2528

        return self.__parent__._cast(_2528.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2260.DesignEntity":
        from mastapy._private.system_model import _2260

        return self.__parent__._cast(_2260.DesignEntity)

    @property
    def microphone_array(self: "CastSelf") -> "MicrophoneArray":
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
class MicrophoneArray(_2537.SpecialisedAssembly):
    """MicrophoneArray

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MICROPHONE_ARRAY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def drawing_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DrawingDiameter")

        if temp is None:
            return 0.0

        return temp

    @drawing_diameter.setter
    @enforce_parameter_types
    def drawing_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DrawingDiameter", float(value) if value is not None else 0.0
        )

    @property
    def array_design(self: "Self") -> "_2700.MicrophoneArrayDesign":
        """mastapy.system_model.part_model.acoustics.MicrophoneArrayDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ArrayDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def microphones(self: "Self") -> "List[_2522.Microphone]":
        """List[mastapy.system_model.part_model.Microphone]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Microphones")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_MicrophoneArray":
        """Cast to another type.

        Returns:
            _Cast_MicrophoneArray
        """
        return _Cast_MicrophoneArray(self)
