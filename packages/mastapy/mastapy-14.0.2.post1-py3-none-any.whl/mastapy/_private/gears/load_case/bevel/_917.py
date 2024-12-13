"""BevelMeshLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.load_case.conical import _912

_BEVEL_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.Gears.LoadCase.Bevel", "BevelMeshLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1256, _1262
    from mastapy._private.gears.load_case import _900

    Self = TypeVar("Self", bound="BevelMeshLoadCase")
    CastSelf = TypeVar("CastSelf", bound="BevelMeshLoadCase._Cast_BevelMeshLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("BevelMeshLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelMeshLoadCase:
    """Special nested class for casting BevelMeshLoadCase to subclasses."""

    __parent__: "BevelMeshLoadCase"

    @property
    def conical_mesh_load_case(self: "CastSelf") -> "_912.ConicalMeshLoadCase":
        return self.__parent__._cast(_912.ConicalMeshLoadCase)

    @property
    def mesh_load_case(self: "CastSelf") -> "_900.MeshLoadCase":
        from mastapy._private.gears.load_case import _900

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
    def bevel_mesh_load_case(self: "CastSelf") -> "BevelMeshLoadCase":
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
class BevelMeshLoadCase(_912.ConicalMeshLoadCase):
    """BevelMeshLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_MESH_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_BevelMeshLoadCase":
        """Cast to another type.

        Returns:
            _Cast_BevelMeshLoadCase
        """
        return _Cast_BevelMeshLoadCase(self)
