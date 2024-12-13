"""PartDetailConfiguration"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_PART_DETAIL_CONFIGURATION = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Configurations", "PartDetailConfiguration"
)

if TYPE_CHECKING:
    from typing import Any, List, Type

    from mastapy._private.system_model.part_model import _2528
    from mastapy._private.system_model.part_model.configurations import (
        _2679,
        _2681,
        _2682,
    )
    from mastapy._private.system_model.part_model.gears import _2573

    Self = TypeVar("Self", bound="PartDetailConfiguration")
    CastSelf = TypeVar(
        "CastSelf", bound="PartDetailConfiguration._Cast_PartDetailConfiguration"
    )

TPartDetailSelection = TypeVar("TPartDetailSelection")
TPart = TypeVar("TPart", bound="_2528.Part")
TSelectableItem = TypeVar("TSelectableItem")

__docformat__ = "restructuredtext en"
__all__ = ("PartDetailConfiguration",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartDetailConfiguration:
    """Special nested class for casting PartDetailConfiguration to subclasses."""

    __parent__: "PartDetailConfiguration"

    @property
    def active_gear_set_design_selection_group(
        self: "CastSelf",
    ) -> "_2573.ActiveGearSetDesignSelectionGroup":
        from mastapy._private.system_model.part_model.gears import _2573

        return self.__parent__._cast(_2573.ActiveGearSetDesignSelectionGroup)

    @property
    def active_fe_substructure_selection_group(
        self: "CastSelf",
    ) -> "_2679.ActiveFESubstructureSelectionGroup":
        from mastapy._private.system_model.part_model.configurations import _2679

        return self.__parent__._cast(_2679.ActiveFESubstructureSelectionGroup)

    @property
    def active_shaft_design_selection_group(
        self: "CastSelf",
    ) -> "_2681.ActiveShaftDesignSelectionGroup":
        from mastapy._private.system_model.part_model.configurations import _2681

        return self.__parent__._cast(_2681.ActiveShaftDesignSelectionGroup)

    @property
    def bearing_detail_configuration(
        self: "CastSelf",
    ) -> "_2682.BearingDetailConfiguration":
        from mastapy._private.system_model.part_model.configurations import _2682

        return self.__parent__._cast(_2682.BearingDetailConfiguration)

    @property
    def part_detail_configuration(self: "CastSelf") -> "PartDetailConfiguration":
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
class PartDetailConfiguration(
    _0.APIBase, Generic[TPartDetailSelection, TPart, TSelectableItem]
):
    """PartDetailConfiguration

    This is a mastapy class.

    Generic Types:
        TPartDetailSelection
        TPart
        TSelectableItem
    """

    TYPE: ClassVar["Type"] = _PART_DETAIL_CONFIGURATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def is_selected(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsSelected")

        if temp is None:
            return False

        return temp

    @property
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    def selections(self: "Self") -> "List[TPartDetailSelection]":
        """List[TPartDetailSelection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Selections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    def delete_configuration(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "DeleteConfiguration")

    def select_configuration(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SelectConfiguration")

    @property
    def cast_to(self: "Self") -> "_Cast_PartDetailConfiguration":
        """Cast to another type.

        Returns:
            _Cast_PartDetailConfiguration
        """
        return _Cast_PartDetailConfiguration(self)
