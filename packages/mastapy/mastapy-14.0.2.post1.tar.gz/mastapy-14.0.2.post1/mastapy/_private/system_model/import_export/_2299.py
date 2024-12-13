"""GeometryExportOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_GEOMETRY_EXPORT_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.ImportExport", "GeometryExportOptions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private import _7733

    Self = TypeVar("Self", bound="GeometryExportOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="GeometryExportOptions._Cast_GeometryExportOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GeometryExportOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GeometryExportOptions:
    """Special nested class for casting GeometryExportOptions to subclasses."""

    __parent__: "GeometryExportOptions"

    @property
    def geometry_export_options(self: "CastSelf") -> "GeometryExportOptions":
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
class GeometryExportOptions(_0.APIBase):
    """GeometryExportOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEOMETRY_EXPORT_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def create_solid(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CreateSolid")

        if temp is None:
            return False

        return temp

    @create_solid.setter
    @enforce_parameter_types
    def create_solid(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "CreateSolid", bool(value) if value is not None else False
        )

    @property
    def draw_fillets(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "DrawFillets")

        if temp is None:
            return False

        return temp

    @draw_fillets.setter
    @enforce_parameter_types
    def draw_fillets(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "DrawFillets", bool(value) if value is not None else False
        )

    @property
    def draw_gear_teeth(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "DrawGearTeeth")

        if temp is None:
            return False

        return temp

    @draw_gear_teeth.setter
    @enforce_parameter_types
    def draw_gear_teeth(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "DrawGearTeeth", bool(value) if value is not None else False
        )

    @property
    def draw_to_tip_diameter(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "DrawToTipDiameter")

        if temp is None:
            return False

        return temp

    @draw_to_tip_diameter.setter
    @enforce_parameter_types
    def draw_to_tip_diameter(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DrawToTipDiameter",
            bool(value) if value is not None else False,
        )

    @property
    def include_bearing_cage(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeBearingCage")

        if temp is None:
            return False

        return temp

    @include_bearing_cage.setter
    @enforce_parameter_types
    def include_bearing_cage(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeBearingCage",
            bool(value) if value is not None else False,
        )

    @property
    def include_bearing_elements(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeBearingElements")

        if temp is None:
            return False

        return temp

    @include_bearing_elements.setter
    @enforce_parameter_types
    def include_bearing_elements(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeBearingElements",
            bool(value) if value is not None else False,
        )

    @property
    def include_bearing_inner_race(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeBearingInnerRace")

        if temp is None:
            return False

        return temp

    @include_bearing_inner_race.setter
    @enforce_parameter_types
    def include_bearing_inner_race(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeBearingInnerRace",
            bool(value) if value is not None else False,
        )

    @property
    def include_bearing_outer_race(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeBearingOuterRace")

        if temp is None:
            return False

        return temp

    @include_bearing_outer_race.setter
    @enforce_parameter_types
    def include_bearing_outer_race(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeBearingOuterRace",
            bool(value) if value is not None else False,
        )

    @property
    def include_planetary_duplicates(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludePlanetaryDuplicates")

        if temp is None:
            return False

        return temp

    @include_planetary_duplicates.setter
    @enforce_parameter_types
    def include_planetary_duplicates(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludePlanetaryDuplicates",
            bool(value) if value is not None else False,
        )

    @property
    def include_virtual_components(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeVirtualComponents")

        if temp is None:
            return False

        return temp

    @include_virtual_components.setter
    @enforce_parameter_types
    def include_virtual_components(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeVirtualComponents",
            bool(value) if value is not None else False,
        )

    @property
    def number_of_points_per_cycloidal_disc_half_lobe(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfPointsPerCycloidalDiscHalfLobe"
        )

        if temp is None:
            return 0

        return temp

    @number_of_points_per_cycloidal_disc_half_lobe.setter
    @enforce_parameter_types
    def number_of_points_per_cycloidal_disc_half_lobe(
        self: "Self", value: "int"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfPointsPerCycloidalDiscHalfLobe",
            int(value) if value is not None else 0,
        )

    @enforce_parameter_types
    def export_to_stl(
        self: "Self", file_name: "str", progress: "_7733.TaskProgress"
    ) -> None:
        """Method does not return.

        Args:
            file_name (str)
            progress (mastapy.TaskProgress)
        """
        file_name = str(file_name)
        pythonnet_method_call(
            self.wrapped,
            "ExportToSTL",
            file_name if file_name else "",
            progress.wrapped if progress else None,
        )

    @enforce_parameter_types
    def export_to_stp(self: "Self", file_name: "str") -> None:
        """Method does not return.

        Args:
            file_name (str)
        """
        file_name = str(file_name)
        pythonnet_method_call(
            self.wrapped, "ExportToSTP", file_name if file_name else ""
        )

    @enforce_parameter_types
    def save_stl_to_separate_files(
        self: "Self", directory_path: "str", save_in_sub_folders: "bool"
    ) -> None:
        """Method does not return.

        Args:
            directory_path (str)
            save_in_sub_folders (bool)
        """
        directory_path = str(directory_path)
        save_in_sub_folders = bool(save_in_sub_folders)
        pythonnet_method_call(
            self.wrapped,
            "SaveStlToSeparateFiles",
            directory_path if directory_path else "",
            save_in_sub_folders if save_in_sub_folders else False,
        )

    def to_stl_code(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(self.wrapped, "ToSTLCode")
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_GeometryExportOptions":
        """Cast to another type.

        Returns:
            _Cast_GeometryExportOptions
        """
        return _Cast_GeometryExportOptions(self)
