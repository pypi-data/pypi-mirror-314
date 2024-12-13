"""CylindricalGearGeometricEntityDrawStyle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.power_flows import _4234

_CYLINDRICAL_GEAR_GEOMETRIC_ENTITY_DRAW_STYLE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows",
    "CylindricalGearGeometricEntityDrawStyle",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.geometry import _319, _320

    Self = TypeVar("Self", bound="CylindricalGearGeometricEntityDrawStyle")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearGeometricEntityDrawStyle._Cast_CylindricalGearGeometricEntityDrawStyle",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearGeometricEntityDrawStyle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearGeometricEntityDrawStyle:
    """Special nested class for casting CylindricalGearGeometricEntityDrawStyle to subclasses."""

    __parent__: "CylindricalGearGeometricEntityDrawStyle"

    @property
    def power_flow_draw_style(self: "CastSelf") -> "_4234.PowerFlowDrawStyle":
        return self.__parent__._cast(_4234.PowerFlowDrawStyle)

    @property
    def draw_style(self: "CastSelf") -> "_319.DrawStyle":
        from mastapy._private.geometry import _319

        return self.__parent__._cast(_319.DrawStyle)

    @property
    def draw_style_base(self: "CastSelf") -> "_320.DrawStyleBase":
        from mastapy._private.geometry import _320

        return self.__parent__._cast(_320.DrawStyleBase)

    @property
    def cylindrical_gear_geometric_entity_draw_style(
        self: "CastSelf",
    ) -> "CylindricalGearGeometricEntityDrawStyle":
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
class CylindricalGearGeometricEntityDrawStyle(_4234.PowerFlowDrawStyle):
    """CylindricalGearGeometricEntityDrawStyle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_GEOMETRIC_ENTITY_DRAW_STYLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearGeometricEntityDrawStyle":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearGeometricEntityDrawStyle
        """
        return _Cast_CylindricalGearGeometricEntityDrawStyle(self)
