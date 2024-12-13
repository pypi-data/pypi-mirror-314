"""ParametricStudyStaticLoad"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.static_loads import _6957

_PARAMETRIC_STUDY_STATIC_LOAD = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "ParametricStudyStaticLoad",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2739
    from mastapy._private.system_model.analyses_and_results.static_loads import _6956

    Self = TypeVar("Self", bound="ParametricStudyStaticLoad")
    CastSelf = TypeVar(
        "CastSelf", bound="ParametricStudyStaticLoad._Cast_ParametricStudyStaticLoad"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParametricStudyStaticLoad",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ParametricStudyStaticLoad:
    """Special nested class for casting ParametricStudyStaticLoad to subclasses."""

    __parent__: "ParametricStudyStaticLoad"

    @property
    def static_load_case(self: "CastSelf") -> "_6957.StaticLoadCase":
        return self.__parent__._cast(_6957.StaticLoadCase)

    @property
    def load_case(self: "CastSelf") -> "_6956.LoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6956,
        )

        return self.__parent__._cast(_6956.LoadCase)

    @property
    def context(self: "CastSelf") -> "_2739.Context":
        from mastapy._private.system_model.analyses_and_results import _2739

        return self.__parent__._cast(_2739.Context)

    @property
    def parametric_study_static_load(self: "CastSelf") -> "ParametricStudyStaticLoad":
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
class ParametricStudyStaticLoad(_6957.StaticLoadCase):
    """ParametricStudyStaticLoad

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PARAMETRIC_STUDY_STATIC_LOAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ParametricStudyStaticLoad":
        """Cast to another type.

        Returns:
            _Cast_ParametricStudyStaticLoad
        """
        return _Cast_ParametricStudyStaticLoad(self)
