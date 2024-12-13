"""MicroGeometryDesignSpaceSearch"""

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
from mastapy._private.gears.gear_set_pareto_optimiser import _931, _942
from mastapy._private.gears.ltca.cylindrical import _881, _882, _885

_MICRO_GEOMETRY_DESIGN_SPACE_SEARCH = python_net_import(
    "SMT.MastaAPI.Gears.GearSetParetoOptimiser", "MicroGeometryDesignSpaceSearch"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1141
    from mastapy._private.gears.gear_set_pareto_optimiser import _945

    Self = TypeVar("Self", bound="MicroGeometryDesignSpaceSearch")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MicroGeometryDesignSpaceSearch._Cast_MicroGeometryDesignSpaceSearch",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MicroGeometryDesignSpaceSearch",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MicroGeometryDesignSpaceSearch:
    """Special nested class for casting MicroGeometryDesignSpaceSearch to subclasses."""

    __parent__: "MicroGeometryDesignSpaceSearch"

    @property
    def design_space_search_base(self: "CastSelf") -> "_931.DesignSpaceSearchBase":
        return self.__parent__._cast(_931.DesignSpaceSearchBase)

    @property
    def micro_geometry_gear_set_design_space_search(
        self: "CastSelf",
    ) -> "_945.MicroGeometryGearSetDesignSpaceSearch":
        from mastapy._private.gears.gear_set_pareto_optimiser import _945

        return self.__parent__._cast(_945.MicroGeometryGearSetDesignSpaceSearch)

    @property
    def micro_geometry_design_space_search(
        self: "CastSelf",
    ) -> "MicroGeometryDesignSpaceSearch":
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
class MicroGeometryDesignSpaceSearch(
    _931.DesignSpaceSearchBase[
        _885.CylindricalGearSetLoadDistributionAnalysis,
        _942.MicroGeometryDesignSpaceSearchCandidate,
    ]
):
    """MicroGeometryDesignSpaceSearch

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MICRO_GEOMETRY_DESIGN_SPACE_SEARCH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def run_all_planetary_meshes(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "RunAllPlanetaryMeshes")

        if temp is None:
            return False

        return temp

    @run_all_planetary_meshes.setter
    @enforce_parameter_types
    def run_all_planetary_meshes(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RunAllPlanetaryMeshes",
            bool(value) if value is not None else False,
        )

    @property
    def select_gear(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_CylindricalGearLoadDistributionAnalysis":
        """ListWithSelectedItem[mastapy.gears.ltca.cylindrical.CylindricalGearLoadDistributionAnalysis]"""
        temp = pythonnet_property_get(self.wrapped, "SelectGear")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_CylindricalGearLoadDistributionAnalysis",
        )(temp)

    @select_gear.setter
    @enforce_parameter_types
    def select_gear(
        self: "Self", value: "_881.CylindricalGearLoadDistributionAnalysis"
    ) -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_CylindricalGearLoadDistributionAnalysis.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_CylindricalGearLoadDistributionAnalysis.implicit_type()
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "SelectGear", value)

    @property
    def select_mesh(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis":
        """ListWithSelectedItem[mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadDistributionAnalysis]"""
        temp = pythonnet_property_get(self.wrapped, "SelectMesh")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis",
        )(temp)

    @select_mesh.setter
    @enforce_parameter_types
    def select_mesh(
        self: "Self", value: "_882.CylindricalGearMeshLoadDistributionAnalysis"
    ) -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis.implicit_type()
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "SelectMesh", value)

    @property
    def load_case_duty_cycle(
        self: "Self",
    ) -> "_885.CylindricalGearSetLoadDistributionAnalysis":
        """mastapy.gears.ltca.cylindrical.CylindricalGearSetLoadDistributionAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCaseDutyCycle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def selected_candidate_micro_geometry(
        self: "Self",
    ) -> "_1141.CylindricalGearSetMicroGeometry":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SelectedCandidateMicroGeometry")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def all_candidate_gear_sets(
        self: "Self",
    ) -> "List[_1141.CylindricalGearSetMicroGeometry]":
        """List[mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllCandidateGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def candidate_gear_sets(
        self: "Self",
    ) -> "List[_1141.CylindricalGearSetMicroGeometry]":
        """List[mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CandidateGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    def add_chart(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddChart")

    def reset_charts(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ResetCharts")

    @property
    def cast_to(self: "Self") -> "_Cast_MicroGeometryDesignSpaceSearch":
        """Cast to another type.

        Returns:
            _Cast_MicroGeometryDesignSpaceSearch
        """
        return _Cast_MicroGeometryDesignSpaceSearch(self)
