"""ModelViewOptionsDrawStyle"""

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
from mastapy._private.geometry import _319

_MODEL_VIEW_OPTIONS_DRAW_STYLE = python_net_import(
    "SMT.MastaAPI.SystemModel.Drawing", "ModelViewOptionsDrawStyle"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.geometry import _320

    Self = TypeVar("Self", bound="ModelViewOptionsDrawStyle")
    CastSelf = TypeVar(
        "CastSelf", bound="ModelViewOptionsDrawStyle._Cast_ModelViewOptionsDrawStyle"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ModelViewOptionsDrawStyle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ModelViewOptionsDrawStyle:
    """Special nested class for casting ModelViewOptionsDrawStyle to subclasses."""

    __parent__: "ModelViewOptionsDrawStyle"

    @property
    def draw_style(self: "CastSelf") -> "_319.DrawStyle":
        return self.__parent__._cast(_319.DrawStyle)

    @property
    def draw_style_base(self: "CastSelf") -> "_320.DrawStyleBase":
        from mastapy._private.geometry import _320

        return self.__parent__._cast(_320.DrawStyleBase)

    @property
    def model_view_options_draw_style(self: "CastSelf") -> "ModelViewOptionsDrawStyle":
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
class ModelViewOptionsDrawStyle(_319.DrawStyle):
    """ModelViewOptionsDrawStyle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MODEL_VIEW_OPTIONS_DRAW_STYLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def rigid_elements(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "RigidElements")

        if temp is None:
            return False

        return temp

    @rigid_elements.setter
    @enforce_parameter_types
    def rigid_elements(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "RigidElements", bool(value) if value is not None else False
        )

    @property
    def show_bearing_rings_which_are_in_f_es(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowBearingRingsWhichAreInFEs")

        if temp is None:
            return False

        return temp

    @show_bearing_rings_which_are_in_f_es.setter
    @enforce_parameter_types
    def show_bearing_rings_which_are_in_f_es(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowBearingRingsWhichAreInFEs",
            bool(value) if value is not None else False,
        )

    @property
    def show_nodes(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowNodes")

        if temp is None:
            return False

        return temp

    @show_nodes.setter
    @enforce_parameter_types
    def show_nodes(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowNodes", bool(value) if value is not None else False
        )

    @property
    def show_part_coordinate_system(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowPartCoordinateSystem")

        if temp is None:
            return False

        return temp

    @show_part_coordinate_system.setter
    @enforce_parameter_types
    def show_part_coordinate_system(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowPartCoordinateSystem",
            bool(value) if value is not None else False,
        )

    @property
    def show_part_labels(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowPartLabels")

        if temp is None:
            return False

        return temp

    @show_part_labels.setter
    @enforce_parameter_types
    def show_part_labels(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowPartLabels", bool(value) if value is not None else False
        )

    @property
    def solid_3d_shafts(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "Solid3DShafts")

        if temp is None:
            return False

        return temp

    @solid_3d_shafts.setter
    @enforce_parameter_types
    def solid_3d_shafts(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "Solid3DShafts", bool(value) if value is not None else False
        )

    @property
    def solid_components(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SolidComponents")

        if temp is None:
            return False

        return temp

    @solid_components.setter
    @enforce_parameter_types
    def solid_components(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "SolidComponents", bool(value) if value is not None else False
        )

    @property
    def solid_housing(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SolidHousing")

        if temp is None:
            return False

        return temp

    @solid_housing.setter
    @enforce_parameter_types
    def solid_housing(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "SolidHousing", bool(value) if value is not None else False
        )

    @property
    def transparent_model(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "TransparentModel")

        if temp is None:
            return False

        return temp

    @transparent_model.setter
    @enforce_parameter_types
    def transparent_model(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TransparentModel",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ModelViewOptionsDrawStyle":
        """Cast to another type.

        Returns:
            _Cast_ModelViewOptionsDrawStyle
        """
        return _Cast_ModelViewOptionsDrawStyle(self)
