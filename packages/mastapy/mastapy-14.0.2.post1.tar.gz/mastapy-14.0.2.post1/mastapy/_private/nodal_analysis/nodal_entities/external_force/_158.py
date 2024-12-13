"""ExternalForceSinglePointEntity"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities.external_force import _156

_EXTERNAL_FORCE_SINGLE_POINT_ENTITY = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities.ExternalForce",
    "ExternalForceSinglePointEntity",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import _144, _146

    Self = TypeVar("Self", bound="ExternalForceSinglePointEntity")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ExternalForceSinglePointEntity._Cast_ExternalForceSinglePointEntity",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ExternalForceSinglePointEntity",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ExternalForceSinglePointEntity:
    """Special nested class for casting ExternalForceSinglePointEntity to subclasses."""

    __parent__: "ExternalForceSinglePointEntity"

    @property
    def external_force_entity(self: "CastSelf") -> "_156.ExternalForceEntity":
        return self.__parent__._cast(_156.ExternalForceEntity)

    @property
    def nodal_component(self: "CastSelf") -> "_144.NodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _144

        return self.__parent__._cast(_144.NodalComponent)

    @property
    def nodal_entity(self: "CastSelf") -> "_146.NodalEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _146

        return self.__parent__._cast(_146.NodalEntity)

    @property
    def external_force_single_point_entity(
        self: "CastSelf",
    ) -> "ExternalForceSinglePointEntity":
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
class ExternalForceSinglePointEntity(_156.ExternalForceEntity):
    """ExternalForceSinglePointEntity

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _EXTERNAL_FORCE_SINGLE_POINT_ENTITY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ExternalForceSinglePointEntity":
        """Cast to another type.

        Returns:
            _Cast_ExternalForceSinglePointEntity
        """
        return _Cast_ExternalForceSinglePointEntity(self)
