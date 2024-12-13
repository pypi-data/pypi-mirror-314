"""GearMeshFEModel"""

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
from mastapy._private.gears.analysis import _1265

_GEAR_MESH_FE_MODEL = python_net_import("SMT.MastaAPI.Gears.FEModel", "GearMeshFEModel")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1256, _1262
    from mastapy._private.gears.fe_model.conical import _1245
    from mastapy._private.gears.fe_model.cylindrical import _1242

    Self = TypeVar("Self", bound="GearMeshFEModel")
    CastSelf = TypeVar("CastSelf", bound="GearMeshFEModel._Cast_GearMeshFEModel")


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshFEModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshFEModel:
    """Special nested class for casting GearMeshFEModel to subclasses."""

    __parent__: "GearMeshFEModel"

    @property
    def gear_mesh_implementation_detail(
        self: "CastSelf",
    ) -> "_1265.GearMeshImplementationDetail":
        return self.__parent__._cast(_1265.GearMeshImplementationDetail)

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
    def cylindrical_gear_mesh_fe_model(
        self: "CastSelf",
    ) -> "_1242.CylindricalGearMeshFEModel":
        from mastapy._private.gears.fe_model.cylindrical import _1242

        return self.__parent__._cast(_1242.CylindricalGearMeshFEModel)

    @property
    def conical_mesh_fe_model(self: "CastSelf") -> "_1245.ConicalMeshFEModel":
        from mastapy._private.gears.fe_model.conical import _1245

        return self.__parent__._cast(_1245.ConicalMeshFEModel)

    @property
    def gear_mesh_fe_model(self: "CastSelf") -> "GearMeshFEModel":
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
class GearMeshFEModel(_1265.GearMeshImplementationDetail):
    """GearMeshFEModel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_FE_MODEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def number_of_loads_per_contact(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfLoadsPerContact")

        if temp is None:
            return 0

        return temp

    @number_of_loads_per_contact.setter
    @enforce_parameter_types
    def number_of_loads_per_contact(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfLoadsPerContact",
            int(value) if value is not None else 0,
        )

    @property
    def number_of_rotations(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfRotations")

        if temp is None:
            return 0

        return temp

    @number_of_rotations.setter
    @enforce_parameter_types
    def number_of_rotations(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfRotations", int(value) if value is not None else 0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshFEModel":
        """Cast to another type.

        Returns:
            _Cast_GearMeshFEModel
        """
        return _Cast_GearMeshFEModel(self)
