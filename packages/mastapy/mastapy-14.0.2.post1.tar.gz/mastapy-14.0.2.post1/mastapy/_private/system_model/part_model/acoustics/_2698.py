"""MeshedResultSurface"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model.acoustics import _2699

_MESHED_RESULT_SURFACE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Acoustics", "MeshedResultSurface"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.system_model.part_model.acoustics import _2696, _2697, _2705

    Self = TypeVar("Self", bound="MeshedResultSurface")
    CastSelf = TypeVar(
        "CastSelf", bound="MeshedResultSurface._Cast_MeshedResultSurface"
    )

T = TypeVar("T", bound="_2705.ResultSurfaceOptions")

__docformat__ = "restructuredtext en"
__all__ = ("MeshedResultSurface",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MeshedResultSurface:
    """Special nested class for casting MeshedResultSurface to subclasses."""

    __parent__: "MeshedResultSurface"

    @property
    def meshed_result_surface_base(self: "CastSelf") -> "_2699.MeshedResultSurfaceBase":
        return self.__parent__._cast(_2699.MeshedResultSurfaceBase)

    @property
    def meshed_result_plane(self: "CastSelf") -> "_2696.MeshedResultPlane":
        from mastapy._private.system_model.part_model.acoustics import _2696

        return self.__parent__._cast(_2696.MeshedResultPlane)

    @property
    def meshed_result_sphere(self: "CastSelf") -> "_2697.MeshedResultSphere":
        from mastapy._private.system_model.part_model.acoustics import _2697

        return self.__parent__._cast(_2697.MeshedResultSphere)

    @property
    def meshed_result_surface(self: "CastSelf") -> "MeshedResultSurface":
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
class MeshedResultSurface(_2699.MeshedResultSurfaceBase, Generic[T]):
    """MeshedResultSurface

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _MESHED_RESULT_SURFACE

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
    def cast_to(self: "Self") -> "_Cast_MeshedResultSurface":
        """Cast to another type.

        Returns:
            _Cast_MeshedResultSurface
        """
        return _Cast_MeshedResultSurface(self)
