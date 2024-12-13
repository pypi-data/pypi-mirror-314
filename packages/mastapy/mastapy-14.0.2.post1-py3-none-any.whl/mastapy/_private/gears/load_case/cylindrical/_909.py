"""CylindricalMeshLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.load_case import _900

_CYLINDRICAL_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.Gears.LoadCase.Cylindrical", "CylindricalMeshLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears import _335, _336
    from mastapy._private.gears.analysis import _1256, _1262
    from mastapy._private.gears.gear_designs.cylindrical import _1091

    Self = TypeVar("Self", bound="CylindricalMeshLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalMeshLoadCase._Cast_CylindricalMeshLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalMeshLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalMeshLoadCase:
    """Special nested class for casting CylindricalMeshLoadCase to subclasses."""

    __parent__: "CylindricalMeshLoadCase"

    @property
    def mesh_load_case(self: "CastSelf") -> "_900.MeshLoadCase":
        return self.__parent__._cast(_900.MeshLoadCase)

    @property
    def gear_mesh_design_analysis(self: "CastSelf") -> "_1262.GearMeshDesignAnalysis":
        from mastapy._private.gears.analysis import _1262

        return self.__parent__._cast(_1262.GearMeshDesignAnalysis)

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1256.AbstractGearMeshAnalysis":
        from mastapy._private.gears.analysis import _1256

        return self.__parent__._cast(_1256.AbstractGearMeshAnalysis)

    @property
    def cylindrical_mesh_load_case(self: "CastSelf") -> "CylindricalMeshLoadCase":
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
class CylindricalMeshLoadCase(_900.MeshLoadCase):
    """CylindricalMeshLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_MESH_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def active_flank(self: "Self") -> "_335.CylindricalFlanks":
        """mastapy.gears.CylindricalFlanks

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveFlank")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Gears.CylindricalFlanks")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._335", "CylindricalFlanks"
        )(value)

    @property
    def equivalent_misalignment(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EquivalentMisalignment")

        if temp is None:
            return 0.0

        return temp

    @equivalent_misalignment.setter
    @enforce_parameter_types
    def equivalent_misalignment(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EquivalentMisalignment",
            float(value) if value is not None else 0.0,
        )

    @property
    def equivalent_misalignment_due_to_system_deflection(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EquivalentMisalignmentDueToSystemDeflection"
        )

        if temp is None:
            return 0.0

        return temp

    @equivalent_misalignment_due_to_system_deflection.setter
    @enforce_parameter_types
    def equivalent_misalignment_due_to_system_deflection(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EquivalentMisalignmentDueToSystemDeflection",
            float(value) if value is not None else 0.0,
        )

    @property
    def gear_a_number_of_load_cycles(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearANumberOfLoadCycles")

        if temp is None:
            return 0.0

        return temp

    @property
    def gear_b_number_of_load_cycles(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearBNumberOfLoadCycles")

        if temp is None:
            return 0.0

        return temp

    @property
    def misalignment_source(self: "Self") -> "_336.CylindricalMisalignmentDataSource":
        """mastapy.gears.CylindricalMisalignmentDataSource"""
        temp = pythonnet_property_get(self.wrapped, "MisalignmentSource")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.CylindricalMisalignmentDataSource"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._336", "CylindricalMisalignmentDataSource"
        )(value)

    @misalignment_source.setter
    @enforce_parameter_types
    def misalignment_source(
        self: "Self", value: "_336.CylindricalMisalignmentDataSource"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.CylindricalMisalignmentDataSource"
        )
        pythonnet_property_set(self.wrapped, "MisalignmentSource", value)

    @property
    def misalignment_due_to_micro_geometry_lead_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MisalignmentDueToMicroGeometryLeadRelief"
        )

        if temp is None:
            return 0.0

        return temp

    @misalignment_due_to_micro_geometry_lead_relief.setter
    @enforce_parameter_types
    def misalignment_due_to_micro_geometry_lead_relief(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MisalignmentDueToMicroGeometryLeadRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    def pitch_line_velocity_at_operating_pitch_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PitchLineVelocityAtOperatingPitchDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def load_case_modifiable_settings(
        self: "Self",
    ) -> "_1091.LTCALoadCaseModifiableSettings":
        """mastapy.gears.gear_designs.cylindrical.LTCALoadCaseModifiableSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCaseModifiableSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalMeshLoadCase":
        """Cast to another type.

        Returns:
            _Cast_CylindricalMeshLoadCase
        """
        return _Cast_CylindricalMeshLoadCase(self)
