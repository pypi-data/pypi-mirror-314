"""ConicalGearFEModel"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.fe_model import _1237

_CONICAL_GEAR_FE_MODEL = python_net_import(
    "SMT.MastaAPI.Gears.FEModel.Conical", "ConicalGearFEModel"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1255, _1258, _1261

    Self = TypeVar("Self", bound="ConicalGearFEModel")
    CastSelf = TypeVar("CastSelf", bound="ConicalGearFEModel._Cast_ConicalGearFEModel")


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearFEModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearFEModel:
    """Special nested class for casting ConicalGearFEModel to subclasses."""

    __parent__: "ConicalGearFEModel"

    @property
    def gear_fe_model(self: "CastSelf") -> "_1237.GearFEModel":
        return self.__parent__._cast(_1237.GearFEModel)

    @property
    def gear_implementation_detail(
        self: "CastSelf",
    ) -> "_1261.GearImplementationDetail":
        from mastapy._private.gears.analysis import _1261

        return self.__parent__._cast(_1261.GearImplementationDetail)

    @property
    def gear_design_analysis(self: "CastSelf") -> "_1258.GearDesignAnalysis":
        from mastapy._private.gears.analysis import _1258

        return self.__parent__._cast(_1258.GearDesignAnalysis)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1255.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1255

        return self.__parent__._cast(_1255.AbstractGearAnalysis)

    @property
    def conical_gear_fe_model(self: "CastSelf") -> "ConicalGearFEModel":
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
class ConicalGearFEModel(_1237.GearFEModel):
    """ConicalGearFEModel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_FE_MODEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearFEModel":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearFEModel
        """
        return _Cast_ConicalGearFEModel(self)
