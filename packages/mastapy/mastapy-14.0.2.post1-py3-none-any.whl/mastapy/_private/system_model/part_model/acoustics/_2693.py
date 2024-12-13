"""FEPartInputSurfaceOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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
from mastapy._private.nodal_analysis.component_mode_synthesis import _237
from mastapy._private.system_model.fe import _2441

_FE_PART_INPUT_SURFACE_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Acoustics", "FEPartInputSurfaceOptions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FEPartInputSurfaceOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="FEPartInputSurfaceOptions._Cast_FEPartInputSurfaceOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FEPartInputSurfaceOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEPartInputSurfaceOptions:
    """Special nested class for casting FEPartInputSurfaceOptions to subclasses."""

    __parent__: "FEPartInputSurfaceOptions"

    @property
    def fe_part_input_surface_options(self: "CastSelf") -> "FEPartInputSurfaceOptions":
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
class FEPartInputSurfaceOptions(_0.APIBase):
    """FEPartInputSurfaceOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_PART_INPUT_SURFACE_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def fe_substructure(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_FESubstructure":
        """ListWithSelectedItem[mastapy.system_model.fe.FESubstructure]"""
        temp = pythonnet_property_get(self.wrapped, "FESubstructure")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_FESubstructure",
        )(temp)

    @fe_substructure.setter
    @enforce_parameter_types
    def fe_substructure(self: "Self", value: "_2441.FESubstructure") -> None:
        wrapper_type = (
            list_with_selected_item.ListWithSelectedItem_FESubstructure.wrapper_type()
        )
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_FESubstructure.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "FESubstructure", value)

    @property
    def is_included(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsIncluded")

        if temp is None:
            return False

        return temp

    @is_included.setter
    @enforce_parameter_types
    def is_included(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IsIncluded", bool(value) if value is not None else False
        )

    @property
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def surfaces(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_CMSElementFaceGroup":
        """ListWithSelectedItem[mastapy.nodal_analysis.component_mode_synthesis.CMSElementFaceGroup]"""
        temp = pythonnet_property_get(self.wrapped, "Surfaces")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_CMSElementFaceGroup",
        )(temp)

    @surfaces.setter
    @enforce_parameter_types
    def surfaces(self: "Self", value: "_237.CMSElementFaceGroup") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_CMSElementFaceGroup.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_CMSElementFaceGroup.implicit_type()
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "Surfaces", value)

    @property
    def cast_to(self: "Self") -> "_Cast_FEPartInputSurfaceOptions":
        """Cast to another type.

        Returns:
            _Cast_FEPartInputSurfaceOptions
        """
        return _Cast_FEPartInputSurfaceOptions(self)
