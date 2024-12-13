"""CylindricalGearSetLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.load_case import _899

_CYLINDRICAL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.Gears.LoadCase.Cylindrical", "CylindricalGearSetLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1257, _1266

    Self = TypeVar("Self", bound="CylindricalGearSetLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalGearSetLoadCase._Cast_CylindricalGearSetLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearSetLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearSetLoadCase:
    """Special nested class for casting CylindricalGearSetLoadCase to subclasses."""

    __parent__: "CylindricalGearSetLoadCase"

    @property
    def gear_set_load_case_base(self: "CastSelf") -> "_899.GearSetLoadCaseBase":
        return self.__parent__._cast(_899.GearSetLoadCaseBase)

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "_1266.GearSetDesignAnalysis":
        from mastapy._private.gears.analysis import _1266

        return self.__parent__._cast(_1266.GearSetDesignAnalysis)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1257.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1257

        return self.__parent__._cast(_1257.AbstractGearSetAnalysis)

    @property
    def cylindrical_gear_set_load_case(
        self: "CastSelf",
    ) -> "CylindricalGearSetLoadCase":
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
class CylindricalGearSetLoadCase(_899.GearSetLoadCaseBase):
    """CylindricalGearSetLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SET_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearSetLoadCase":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearSetLoadCase
        """
        return _Cast_CylindricalGearSetLoadCase(self)
