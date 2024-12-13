"""AbstractTCA"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_ABSTRACT_TCA = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "AbstractTCA"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.conical import _1200
    from mastapy._private.gears.manufacturing.bevel import _820

    Self = TypeVar("Self", bound="AbstractTCA")
    CastSelf = TypeVar("CastSelf", bound="AbstractTCA._Cast_AbstractTCA")


__docformat__ = "restructuredtext en"
__all__ = ("AbstractTCA",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractTCA:
    """Special nested class for casting AbstractTCA to subclasses."""

    __parent__: "AbstractTCA"

    @property
    def ease_off_based_tca(self: "CastSelf") -> "_820.EaseOffBasedTCA":
        from mastapy._private.gears.manufacturing.bevel import _820

        return self.__parent__._cast(_820.EaseOffBasedTCA)

    @property
    def abstract_tca(self: "CastSelf") -> "AbstractTCA":
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
class AbstractTCA(_0.APIBase):
    """AbstractTCA

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_TCA

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def mean_transmission_error_with_respect_to_wheel(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeanTransmissionErrorWithRespectToWheel"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def peak_to_peak_transmission_error_with_respect_to_wheel(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PeakToPeakTransmissionErrorWithRespectToWheel"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def conical_mesh_misalignments(self: "Self") -> "_1200.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalMeshMisalignments")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractTCA":
        """Cast to another type.

        Returns:
            _Cast_AbstractTCA
        """
        return _Cast_AbstractTCA(self)
