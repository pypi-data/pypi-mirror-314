"""ConicalMeshMicroGeometryConfig"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.bevel import _812

_CONICAL_MESH_MICRO_GEOMETRY_CONFIG = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "ConicalMeshMicroGeometryConfig"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1256, _1262, _1265

    Self = TypeVar("Self", bound="ConicalMeshMicroGeometryConfig")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalMeshMicroGeometryConfig._Cast_ConicalMeshMicroGeometryConfig",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalMeshMicroGeometryConfig",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalMeshMicroGeometryConfig:
    """Special nested class for casting ConicalMeshMicroGeometryConfig to subclasses."""

    __parent__: "ConicalMeshMicroGeometryConfig"

    @property
    def conical_mesh_micro_geometry_config_base(
        self: "CastSelf",
    ) -> "_812.ConicalMeshMicroGeometryConfigBase":
        return self.__parent__._cast(_812.ConicalMeshMicroGeometryConfigBase)

    @property
    def gear_mesh_implementation_detail(
        self: "CastSelf",
    ) -> "_1265.GearMeshImplementationDetail":
        from mastapy._private.gears.analysis import _1265

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
    def conical_mesh_micro_geometry_config(
        self: "CastSelf",
    ) -> "ConicalMeshMicroGeometryConfig":
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
class ConicalMeshMicroGeometryConfig(_812.ConicalMeshMicroGeometryConfigBase):
    """ConicalMeshMicroGeometryConfig

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_MESH_MICRO_GEOMETRY_CONFIG

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalMeshMicroGeometryConfig":
        """Cast to another type.

        Returns:
            _Cast_ConicalMeshMicroGeometryConfig
        """
        return _Cast_ConicalMeshMicroGeometryConfig(self)
