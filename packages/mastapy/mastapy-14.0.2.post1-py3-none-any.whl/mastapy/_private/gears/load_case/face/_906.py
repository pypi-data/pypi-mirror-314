"""FaceMeshLoadCase"""

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

_FACE_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.Gears.LoadCase.Face", "FaceMeshLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears import _336
    from mastapy._private.gears.analysis import _1256, _1262

    Self = TypeVar("Self", bound="FaceMeshLoadCase")
    CastSelf = TypeVar("CastSelf", bound="FaceMeshLoadCase._Cast_FaceMeshLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("FaceMeshLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FaceMeshLoadCase:
    """Special nested class for casting FaceMeshLoadCase to subclasses."""

    __parent__: "FaceMeshLoadCase"

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
    def face_mesh_load_case(self: "CastSelf") -> "FaceMeshLoadCase":
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
class FaceMeshLoadCase(_900.MeshLoadCase):
    """FaceMeshLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FACE_MESH_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def cast_to(self: "Self") -> "_Cast_FaceMeshLoadCase":
        """Cast to another type.

        Returns:
            _Cast_FaceMeshLoadCase
        """
        return _Cast_FaceMeshLoadCase(self)
