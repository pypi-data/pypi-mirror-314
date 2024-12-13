"""ShaftFromCAD"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model.import_from_cad import _2554

_SHAFT_FROM_CAD = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD", "ShaftFromCAD"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model.import_from_cad import _2556

    Self = TypeVar("Self", bound="ShaftFromCAD")
    CastSelf = TypeVar("CastSelf", bound="ShaftFromCAD._Cast_ShaftFromCAD")


__docformat__ = "restructuredtext en"
__all__ = ("ShaftFromCAD",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftFromCAD:
    """Special nested class for casting ShaftFromCAD to subclasses."""

    __parent__: "ShaftFromCAD"

    @property
    def abstract_shaft_from_cad(self: "CastSelf") -> "_2554.AbstractShaftFromCAD":
        return self.__parent__._cast(_2554.AbstractShaftFromCAD)

    @property
    def component_from_cad(self: "CastSelf") -> "_2556.ComponentFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2556

        return self.__parent__._cast(_2556.ComponentFromCAD)

    @property
    def shaft_from_cad(self: "CastSelf") -> "ShaftFromCAD":
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
class ShaftFromCAD(_2554.AbstractShaftFromCAD):
    """ShaftFromCAD

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_FROM_CAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def create_assembly(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CreateAssembly")

        if temp is None:
            return False

        return temp

    @create_assembly.setter
    @enforce_parameter_types
    def create_assembly(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "CreateAssembly", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftFromCAD":
        """Cast to another type.

        Returns:
            _Cast_ShaftFromCAD
        """
        return _Cast_ShaftFromCAD(self)
