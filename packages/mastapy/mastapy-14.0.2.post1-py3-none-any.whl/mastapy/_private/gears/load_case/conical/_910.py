"""ConicalGearLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.load_case import _898

_CONICAL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.Gears.LoadCase.Conical", "ConicalGearLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1255, _1258
    from mastapy._private.gears.load_case.bevel import _916

    Self = TypeVar("Self", bound="ConicalGearLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="ConicalGearLoadCase._Cast_ConicalGearLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearLoadCase:
    """Special nested class for casting ConicalGearLoadCase to subclasses."""

    __parent__: "ConicalGearLoadCase"

    @property
    def gear_load_case_base(self: "CastSelf") -> "_898.GearLoadCaseBase":
        return self.__parent__._cast(_898.GearLoadCaseBase)

    @property
    def gear_design_analysis(self: "CastSelf") -> "_1258.GearDesignAnalysis":
        from mastapy._private.gears.analysis import _1258

        return self.__parent__._cast(_1258.GearDesignAnalysis)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1255.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1255

        return self.__parent__._cast(_1255.AbstractGearAnalysis)

    @property
    def bevel_load_case(self: "CastSelf") -> "_916.BevelLoadCase":
        from mastapy._private.gears.load_case.bevel import _916

        return self.__parent__._cast(_916.BevelLoadCase)

    @property
    def conical_gear_load_case(self: "CastSelf") -> "ConicalGearLoadCase":
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
class ConicalGearLoadCase(_898.GearLoadCaseBase):
    """ConicalGearLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearLoadCase":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearLoadCase
        """
        return _Cast_ConicalGearLoadCase(self)
