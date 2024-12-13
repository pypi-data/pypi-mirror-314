"""ClutchFromCAD"""

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
from mastapy._private.system_model.part_model.import_from_cad import _2565

_CLUTCH_FROM_CAD = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD", "ClutchFromCAD"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model.import_from_cad import _2556

    Self = TypeVar("Self", bound="ClutchFromCAD")
    CastSelf = TypeVar("CastSelf", bound="ClutchFromCAD._Cast_ClutchFromCAD")


__docformat__ = "restructuredtext en"
__all__ = ("ClutchFromCAD",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ClutchFromCAD:
    """Special nested class for casting ClutchFromCAD to subclasses."""

    __parent__: "ClutchFromCAD"

    @property
    def mountable_component_from_cad(
        self: "CastSelf",
    ) -> "_2565.MountableComponentFromCAD":
        return self.__parent__._cast(_2565.MountableComponentFromCAD)

    @property
    def component_from_cad(self: "CastSelf") -> "_2556.ComponentFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2556

        return self.__parent__._cast(_2556.ComponentFromCAD)

    @property
    def clutch_from_cad(self: "CastSelf") -> "ClutchFromCAD":
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
class ClutchFromCAD(_2565.MountableComponentFromCAD):
    """ClutchFromCAD

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CLUTCH_FROM_CAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def clutch_name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "ClutchName")

        if temp is None:
            return ""

        return temp

    @clutch_name.setter
    @enforce_parameter_types
    def clutch_name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "ClutchName", str(value) if value is not None else ""
        )

    @property
    def length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Length")

        if temp is None:
            return 0.0

        return temp

    @length.setter
    @enforce_parameter_types
    def length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Length", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ClutchFromCAD":
        """Cast to another type.

        Returns:
            _Cast_ClutchFromCAD
        """
        return _Cast_ClutchFromCAD(self)
