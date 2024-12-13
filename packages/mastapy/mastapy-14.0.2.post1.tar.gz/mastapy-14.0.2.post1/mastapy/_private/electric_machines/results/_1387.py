"""ElectricMachineResultsViewable"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines import _1339, _1342
from mastapy._private.electric_machines.results import _1376
from mastapy._private.nodal_analysis.elmer import _182

_ELECTRIC_MACHINE_RESULTS_VIEWABLE = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Results", "ElectricMachineResultsViewable"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.electric_machines.results import _1388
    from mastapy._private.utility.property import _1898

    Self = TypeVar("Self", bound="ElectricMachineResultsViewable")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineResultsViewable._Cast_ElectricMachineResultsViewable",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineResultsViewable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineResultsViewable:
    """Special nested class for casting ElectricMachineResultsViewable to subclasses."""

    __parent__: "ElectricMachineResultsViewable"

    @property
    def elmer_results_viewable(self: "CastSelf") -> "_182.ElmerResultsViewable":
        return self.__parent__._cast(_182.ElmerResultsViewable)

    @property
    def electric_machine_results_viewable(
        self: "CastSelf",
    ) -> "ElectricMachineResultsViewable":
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
class ElectricMachineResultsViewable(_182.ElmerResultsViewable):
    """ElectricMachineResultsViewable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_RESULTS_VIEWABLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def force_view_options(self: "Self") -> "_1388.ElectricMachineForceViewOptions":
        """mastapy.electric_machines.results.ElectricMachineForceViewOptions"""
        temp = pythonnet_property_get(self.wrapped, "ForceViewOptions")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.ElectricMachines.Results.ElectricMachineForceViewOptions",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines.results._1388",
            "ElectricMachineForceViewOptions",
        )(value)

    @force_view_options.setter
    @enforce_parameter_types
    def force_view_options(
        self: "Self", value: "_1388.ElectricMachineForceViewOptions"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.ElectricMachines.Results.ElectricMachineForceViewOptions",
        )
        pythonnet_property_set(self.wrapped, "ForceViewOptions", value)

    @property
    def number_of_lines(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfLines")

        if temp is None:
            return 0

        return temp

    @number_of_lines.setter
    @enforce_parameter_types
    def number_of_lines(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfLines", int(value) if value is not None else 0
        )

    @property
    def results(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_ElectricMachineResults":
        """ListWithSelectedItem[mastapy.electric_machines.results.ElectricMachineResults]"""
        temp = pythonnet_property_get(self.wrapped, "Results")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_ElectricMachineResults",
        )(temp)

    @results.setter
    @enforce_parameter_types
    def results(self: "Self", value: "_1376.ElectricMachineResults") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_ElectricMachineResults.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_ElectricMachineResults.implicit_type()
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "Results", value)

    @property
    def show_field_lines(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowFieldLines")

        if temp is None:
            return False

        return temp

    @show_field_lines.setter
    @enforce_parameter_types
    def show_field_lines(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowFieldLines", bool(value) if value is not None else False
        )

    @property
    def slice(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_RotorSkewSlice":
        """ListWithSelectedItem[mastapy.electric_machines.RotorSkewSlice]"""
        temp = pythonnet_property_get(self.wrapped, "Slice")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_RotorSkewSlice",
        )(temp)

    @slice.setter
    @enforce_parameter_types
    def slice(self: "Self", value: "_1342.RotorSkewSlice") -> None:
        wrapper_type = (
            list_with_selected_item.ListWithSelectedItem_RotorSkewSlice.wrapper_type()
        )
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_RotorSkewSlice.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "Slice", value)

    @property
    def parts_to_view(self: "Self") -> "List[_1898.EnumWithBoolean[_1339.RegionID]]":
        """List[mastapy.utility.property.EnumWithBoolean[mastapy.electric_machines.RegionID]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PartsToView")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    def deselect_all(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "DeselectAll")

    def select_all(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SelectAll")

    @property
    def cast_to(self: "Self") -> "_Cast_ElectricMachineResultsViewable":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineResultsViewable
        """
        return _Cast_ElectricMachineResultsViewable(self)
