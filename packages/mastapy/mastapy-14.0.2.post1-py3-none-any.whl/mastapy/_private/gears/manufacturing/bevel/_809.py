"""ConicalMeshManufacturingAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.analysis import _1263

_CONICAL_MESH_MANUFACTURING_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "ConicalMeshManufacturingAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1256, _1262
    from mastapy._private.gears.load_case.conical import _912
    from mastapy._private.gears.manufacturing.bevel import _804, _820

    Self = TypeVar("Self", bound="ConicalMeshManufacturingAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalMeshManufacturingAnalysis._Cast_ConicalMeshManufacturingAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalMeshManufacturingAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalMeshManufacturingAnalysis:
    """Special nested class for casting ConicalMeshManufacturingAnalysis to subclasses."""

    __parent__: "ConicalMeshManufacturingAnalysis"

    @property
    def gear_mesh_implementation_analysis(
        self: "CastSelf",
    ) -> "_1263.GearMeshImplementationAnalysis":
        return self.__parent__._cast(_1263.GearMeshImplementationAnalysis)

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
    def conical_mesh_manufacturing_analysis(
        self: "CastSelf",
    ) -> "ConicalMeshManufacturingAnalysis":
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
class ConicalMeshManufacturingAnalysis(_1263.GearMeshImplementationAnalysis):
    """ConicalMeshManufacturingAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_MESH_MANUFACTURING_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def conical_mesh_load_case(self: "Self") -> "_912.ConicalMeshLoadCase":
        """mastapy.gears.load_case.conical.ConicalMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalMeshLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def tca(self: "Self") -> "_820.EaseOffBasedTCA":
        """mastapy.gears.manufacturing.bevel.EaseOffBasedTCA

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TCA")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def meshed_gears(
        self: "Self",
    ) -> "List[_804.ConicalMeshedGearManufacturingAnalysis]":
        """List[mastapy.gears.manufacturing.bevel.ConicalMeshedGearManufacturingAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshedGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalMeshManufacturingAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConicalMeshManufacturingAnalysis
        """
        return _Cast_ConicalMeshManufacturingAnalysis(self)
