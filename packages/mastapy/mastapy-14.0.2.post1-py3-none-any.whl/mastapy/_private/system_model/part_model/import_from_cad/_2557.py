"""ConceptBearingFromCAD"""

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
from mastapy._private.system_model.part_model.import_from_cad import _2558

_CONCEPT_BEARING_FROM_CAD = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD", "ConceptBearingFromCAD"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model.import_from_cad import _2556, _2565

    Self = TypeVar("Self", bound="ConceptBearingFromCAD")
    CastSelf = TypeVar(
        "CastSelf", bound="ConceptBearingFromCAD._Cast_ConceptBearingFromCAD"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConceptBearingFromCAD",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConceptBearingFromCAD:
    """Special nested class for casting ConceptBearingFromCAD to subclasses."""

    __parent__: "ConceptBearingFromCAD"

    @property
    def connector_from_cad(self: "CastSelf") -> "_2558.ConnectorFromCAD":
        return self.__parent__._cast(_2558.ConnectorFromCAD)

    @property
    def mountable_component_from_cad(
        self: "CastSelf",
    ) -> "_2565.MountableComponentFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2565

        return self.__parent__._cast(_2565.MountableComponentFromCAD)

    @property
    def component_from_cad(self: "CastSelf") -> "_2556.ComponentFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2556

        return self.__parent__._cast(_2556.ComponentFromCAD)

    @property
    def concept_bearing_from_cad(self: "CastSelf") -> "ConceptBearingFromCAD":
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
class ConceptBearingFromCAD(_2558.ConnectorFromCAD):
    """ConceptBearingFromCAD

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCEPT_BEARING_FROM_CAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def cast_to(self: "Self") -> "_Cast_ConceptBearingFromCAD":
        """Cast to another type.

        Returns:
            _Cast_ConceptBearingFromCAD
        """
        return _Cast_ConceptBearingFromCAD(self)
