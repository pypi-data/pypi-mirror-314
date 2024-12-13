"""BearingDetailConfiguration"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_designs import _2186
from mastapy._private.system_model.part_model import _2497
from mastapy._private.system_model.part_model.configurations import _2683, _2684

_BEARING_DETAIL_CONFIGURATION = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Configurations", "BearingDetailConfiguration"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BearingDetailConfiguration")
    CastSelf = TypeVar(
        "CastSelf", bound="BearingDetailConfiguration._Cast_BearingDetailConfiguration"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingDetailConfiguration",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BearingDetailConfiguration:
    """Special nested class for casting BearingDetailConfiguration to subclasses."""

    __parent__: "BearingDetailConfiguration"

    @property
    def part_detail_configuration(self: "CastSelf") -> "_2684.PartDetailConfiguration":
        return self.__parent__._cast(_2684.PartDetailConfiguration)

    @property
    def bearing_detail_configuration(self: "CastSelf") -> "BearingDetailConfiguration":
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
class BearingDetailConfiguration(
    _2684.PartDetailConfiguration[
        _2683.BearingDetailSelection, _2497.Bearing, _2186.BearingDesign
    ]
):
    """BearingDetailConfiguration

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING_DETAIL_CONFIGURATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_BearingDetailConfiguration":
        """Cast to another type.

        Returns:
            _Cast_BearingDetailConfiguration
        """
        return _Cast_BearingDetailConfiguration(self)
