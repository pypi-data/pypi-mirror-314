"""CycloidalAssembly"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2537

_CYCLOIDAL_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "CycloidalAssembly"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.cycloidal import _1503
    from mastapy._private.system_model import _2260
    from mastapy._private.system_model.part_model import _2492, _2528
    from mastapy._private.system_model.part_model.cycloidal import _2630, _2631

    Self = TypeVar("Self", bound="CycloidalAssembly")
    CastSelf = TypeVar("CastSelf", bound="CycloidalAssembly._Cast_CycloidalAssembly")


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalAssembly",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalAssembly:
    """Special nested class for casting CycloidalAssembly to subclasses."""

    __parent__: "CycloidalAssembly"

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
    def cycloidal_assembly(self: "CastSelf") -> "CycloidalAssembly":
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
class CycloidalAssembly(_2537.SpecialisedAssembly):
    """CycloidalAssembly

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYCLOIDAL_ASSEMBLY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cycloidal_assembly_design(self: "Self") -> "_1503.CycloidalAssemblyDesign":
        """mastapy.cycloidal.CycloidalAssemblyDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CycloidalAssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def ring_pins(self: "Self") -> "_2631.RingPins":
        """mastapy.system_model.part_model.cycloidal.RingPins

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RingPins")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def known_designs(self: "Self") -> "List[_1503.CycloidalAssemblyDesign]":
        """List[mastapy.cycloidal.CycloidalAssemblyDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KnownDesigns")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    def add_disc(self: "Self") -> "_2630.CycloidalDisc":
        """mastapy.system_model.part_model.cycloidal.CycloidalDisc"""
        method_result = pythonnet_method_call(self.wrapped, "AddDisc")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def design_named(self: "Self", name: "str") -> "_1503.CycloidalAssemblyDesign":
        """mastapy.cycloidal.CycloidalAssemblyDesign

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "DesignNamed", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def remove_disc_from_designs(self: "Self", disc_id: "int") -> None:
        """Method does not return.

        Args:
            disc_id (int)
        """
        disc_id = int(disc_id)
        pythonnet_method_call(
            self.wrapped, "RemoveDiscFromDesigns", disc_id if disc_id else 0
        )

    @enforce_parameter_types
    def set_active_cycloidal_assembly_design(
        self: "Self", cycloidal_assembly_design: "_1503.CycloidalAssemblyDesign"
    ) -> None:
        """Method does not return.

        Args:
            cycloidal_assembly_design (mastapy.cycloidal.CycloidalAssemblyDesign)
        """
        pythonnet_method_call(
            self.wrapped,
            "SetActiveCycloidalAssemblyDesign",
            cycloidal_assembly_design.wrapped if cycloidal_assembly_design else None,
        )

    @enforce_parameter_types
    def try_remove_design(
        self: "Self", design: "_1503.CycloidalAssemblyDesign"
    ) -> "bool":
        """bool

        Args:
            design (mastapy.cycloidal.CycloidalAssemblyDesign)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "TryRemoveDesign", design.wrapped if design else None
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_CycloidalAssembly":
        """Cast to another type.

        Returns:
            _Cast_CycloidalAssembly
        """
        return _Cast_CycloidalAssembly(self)
