"""ElementPropertiesWithMaterial"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import _221

_ELEMENT_PROPERTIES_WITH_MATERIAL = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting",
    "ElementPropertiesWithMaterial",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
        _222,
        _226,
        _227,
    )

    Self = TypeVar("Self", bound="ElementPropertiesWithMaterial")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElementPropertiesWithMaterial._Cast_ElementPropertiesWithMaterial",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElementPropertiesWithMaterial",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElementPropertiesWithMaterial:
    """Special nested class for casting ElementPropertiesWithMaterial to subclasses."""

    __parent__: "ElementPropertiesWithMaterial"

    @property
    def element_properties_base(self: "CastSelf") -> "_221.ElementPropertiesBase":
        return self.__parent__._cast(_221.ElementPropertiesBase)

    @property
    def element_properties_beam(self: "CastSelf") -> "_222.ElementPropertiesBeam":
        from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
            _222,
        )

        return self.__parent__._cast(_222.ElementPropertiesBeam)

    @property
    def element_properties_shell(self: "CastSelf") -> "_226.ElementPropertiesShell":
        from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
            _226,
        )

        return self.__parent__._cast(_226.ElementPropertiesShell)

    @property
    def element_properties_solid(self: "CastSelf") -> "_227.ElementPropertiesSolid":
        from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
            _227,
        )

        return self.__parent__._cast(_227.ElementPropertiesSolid)

    @property
    def element_properties_with_material(
        self: "CastSelf",
    ) -> "ElementPropertiesWithMaterial":
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
class ElementPropertiesWithMaterial(_221.ElementPropertiesBase):
    """ElementPropertiesWithMaterial

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELEMENT_PROPERTIES_WITH_MATERIAL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def material_coordinate_system_id(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_int":
        """ListWithSelectedItem[int]"""
        temp = pythonnet_property_get(self.wrapped, "MaterialCoordinateSystemID")

        if temp is None:
            return 0

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_int",
        )(temp)

    @material_coordinate_system_id.setter
    @enforce_parameter_types
    def material_coordinate_system_id(self: "Self", value: "int") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_int.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_int.implicit_type()
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0
        )
        pythonnet_property_set(self.wrapped, "MaterialCoordinateSystemID", value)

    @property
    def material_id(self: "Self") -> "list_with_selected_item.ListWithSelectedItem_int":
        """ListWithSelectedItem[int]"""
        temp = pythonnet_property_get(self.wrapped, "MaterialID")

        if temp is None:
            return 0

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_int",
        )(temp)

    @material_id.setter
    @enforce_parameter_types
    def material_id(self: "Self", value: "int") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_int.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_int.implicit_type()
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0
        )
        pythonnet_property_set(self.wrapped, "MaterialID", value)

    @property
    def cast_to(self: "Self") -> "_Cast_ElementPropertiesWithMaterial":
        """Cast to another type.

        Returns:
            _Cast_ElementPropertiesWithMaterial
        """
        return _Cast_ElementPropertiesWithMaterial(self)
