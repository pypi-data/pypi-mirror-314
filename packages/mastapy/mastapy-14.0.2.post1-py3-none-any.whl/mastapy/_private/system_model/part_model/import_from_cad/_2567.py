"""PulleyFromCAD"""

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

_PULLEY_FROM_CAD = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD", "PulleyFromCAD"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model.import_from_cad import _2556

    Self = TypeVar("Self", bound="PulleyFromCAD")
    CastSelf = TypeVar("CastSelf", bound="PulleyFromCAD._Cast_PulleyFromCAD")


__docformat__ = "restructuredtext en"
__all__ = ("PulleyFromCAD",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PulleyFromCAD:
    """Special nested class for casting PulleyFromCAD to subclasses."""

    __parent__: "PulleyFromCAD"

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
    def pulley_from_cad(self: "CastSelf") -> "PulleyFromCAD":
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
class PulleyFromCAD(_2565.MountableComponentFromCAD):
    """PulleyFromCAD

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PULLEY_FROM_CAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def centre_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CentreDistance")

        if temp is None:
            return 0.0

        return temp

    @centre_distance.setter
    @enforce_parameter_types
    def centre_distance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CentreDistance", float(value) if value is not None else 0.0
        )

    @property
    def outer_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @outer_diameter.setter
    @enforce_parameter_types
    def outer_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "OuterDiameter", float(value) if value is not None else 0.0
        )

    @property
    def width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return temp

    @width.setter
    @enforce_parameter_types
    def width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PulleyFromCAD":
        """Cast to another type.

        Returns:
            _Cast_PulleyFromCAD
        """
        return _Cast_PulleyFromCAD(self)
