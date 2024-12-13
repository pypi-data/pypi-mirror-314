"""SpiralBevelRateableMesh"""

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
from mastapy._private.gears.rating.agma_gleason_conical import _581

_SPIRAL_BEVEL_RATEABLE_MESH = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Bevel.Standards", "SpiralBevelRateableMesh"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _380
    from mastapy._private.gears.rating.conical import _560

    Self = TypeVar("Self", bound="SpiralBevelRateableMesh")
    CastSelf = TypeVar(
        "CastSelf", bound="SpiralBevelRateableMesh._Cast_SpiralBevelRateableMesh"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpiralBevelRateableMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpiralBevelRateableMesh:
    """Special nested class for casting SpiralBevelRateableMesh to subclasses."""

    __parent__: "SpiralBevelRateableMesh"

    @property
    def agma_gleason_conical_rateable_mesh(
        self: "CastSelf",
    ) -> "_581.AGMAGleasonConicalRateableMesh":
        return self.__parent__._cast(_581.AGMAGleasonConicalRateableMesh)

    @property
    def conical_rateable_mesh(self: "CastSelf") -> "_560.ConicalRateableMesh":
        from mastapy._private.gears.rating.conical import _560

        return self.__parent__._cast(_560.ConicalRateableMesh)

    @property
    def rateable_mesh(self: "CastSelf") -> "_380.RateableMesh":
        from mastapy._private.gears.rating import _380

        return self.__parent__._cast(_380.RateableMesh)

    @property
    def spiral_bevel_rateable_mesh(self: "CastSelf") -> "SpiralBevelRateableMesh":
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
class SpiralBevelRateableMesh(_581.AGMAGleasonConicalRateableMesh):
    """SpiralBevelRateableMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPIRAL_BEVEL_RATEABLE_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def safety_factor_scoring(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorScoring")

        if temp is None:
            return 0.0

        return temp

    @safety_factor_scoring.setter
    @enforce_parameter_types
    def safety_factor_scoring(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SafetyFactorScoring",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_SpiralBevelRateableMesh":
        """Cast to another type.

        Returns:
            _Cast_SpiralBevelRateableMesh
        """
        return _Cast_SpiralBevelRateableMesh(self)
