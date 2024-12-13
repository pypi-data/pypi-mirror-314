"""AGMACylindricalGearMaterial"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.materials import _606

_AGMA_CYLINDRICAL_GEAR_MATERIAL = python_net_import(
    "SMT.MastaAPI.Gears.Materials", "AGMACylindricalGearMaterial"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.materials import _610
    from mastapy._private.materials import _253, _254, _255, _282
    from mastapy._private.utility.databases import _1884

    Self = TypeVar("Self", bound="AGMACylindricalGearMaterial")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMACylindricalGearMaterial._Cast_AGMACylindricalGearMaterial",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMACylindricalGearMaterial",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMACylindricalGearMaterial:
    """Special nested class for casting AGMACylindricalGearMaterial to subclasses."""

    __parent__: "AGMACylindricalGearMaterial"

    @property
    def cylindrical_gear_material(self: "CastSelf") -> "_606.CylindricalGearMaterial":
        return self.__parent__._cast(_606.CylindricalGearMaterial)

    @property
    def gear_material(self: "CastSelf") -> "_610.GearMaterial":
        from mastapy._private.gears.materials import _610

        return self.__parent__._cast(_610.GearMaterial)

    @property
    def material(self: "CastSelf") -> "_282.Material":
        from mastapy._private.materials import _282

        return self.__parent__._cast(_282.Material)

    @property
    def named_database_item(self: "CastSelf") -> "_1884.NamedDatabaseItem":
        from mastapy._private.utility.databases import _1884

        return self.__parent__._cast(_1884.NamedDatabaseItem)

    @property
    def agma_cylindrical_gear_material(
        self: "CastSelf",
    ) -> "AGMACylindricalGearMaterial":
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
class AGMACylindricalGearMaterial(_606.CylindricalGearMaterial):
    """AGMACylindricalGearMaterial

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_CYLINDRICAL_GEAR_MATERIAL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def allowable_stress_number_bending(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AllowableStressNumberBending")

        if temp is None:
            return 0.0

        return temp

    @allowable_stress_number_bending.setter
    @enforce_parameter_types
    def allowable_stress_number_bending(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AllowableStressNumberBending",
            float(value) if value is not None else 0.0,
        )

    @property
    def grade(self: "Self") -> "_255.AGMAMaterialGrade":
        """mastapy.materials.AGMAMaterialGrade"""
        temp = pythonnet_property_get(self.wrapped, "Grade")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.AGMAMaterialGrade"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._255", "AGMAMaterialGrade"
        )(value)

    @grade.setter
    @enforce_parameter_types
    def grade(self: "Self", value: "_255.AGMAMaterialGrade") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.AGMAMaterialGrade"
        )
        pythonnet_property_set(self.wrapped, "Grade", value)

    @property
    def material_application(self: "Self") -> "_253.AGMAMaterialApplications":
        """mastapy.materials.AGMAMaterialApplications"""
        temp = pythonnet_property_get(self.wrapped, "MaterialApplication")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.AGMAMaterialApplications"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._253", "AGMAMaterialApplications"
        )(value)

    @material_application.setter
    @enforce_parameter_types
    def material_application(
        self: "Self", value: "_253.AGMAMaterialApplications"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.AGMAMaterialApplications"
        )
        pythonnet_property_set(self.wrapped, "MaterialApplication", value)

    @property
    def material_class(self: "Self") -> "_254.AGMAMaterialClasses":
        """mastapy.materials.AGMAMaterialClasses"""
        temp = pythonnet_property_get(self.wrapped, "MaterialClass")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.AGMAMaterialClasses"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._254", "AGMAMaterialClasses"
        )(value)

    @material_class.setter
    @enforce_parameter_types
    def material_class(self: "Self", value: "_254.AGMAMaterialClasses") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.AGMAMaterialClasses"
        )
        pythonnet_property_set(self.wrapped, "MaterialClass", value)

    @property
    def stress_cycle_factor_at_1e10_cycles_bending(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "StressCycleFactorAt1E10CyclesBending"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @stress_cycle_factor_at_1e10_cycles_bending.setter
    @enforce_parameter_types
    def stress_cycle_factor_at_1e10_cycles_bending(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "StressCycleFactorAt1E10CyclesBending", value
        )

    @property
    def stress_cycle_factor_at_1e10_cycles_contact(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "StressCycleFactorAt1E10CyclesContact"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @stress_cycle_factor_at_1e10_cycles_contact.setter
    @enforce_parameter_types
    def stress_cycle_factor_at_1e10_cycles_contact(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "StressCycleFactorAt1E10CyclesContact", value
        )

    @property
    def cast_to(self: "Self") -> "_Cast_AGMACylindricalGearMaterial":
        """Cast to another type.

        Returns:
            _Cast_AGMACylindricalGearMaterial
        """
        return _Cast_AGMACylindricalGearMaterial(self)
