"""MultiNodeConnectorFELink"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.fe.links import _2483

_MULTI_NODE_CONNECTOR_FE_LINK = python_net_import(
    "SMT.MastaAPI.SystemModel.FE.Links", "MultiNodeConnectorFELink"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.fe.links import _2476, _2489

    Self = TypeVar("Self", bound="MultiNodeConnectorFELink")
    CastSelf = TypeVar(
        "CastSelf", bound="MultiNodeConnectorFELink._Cast_MultiNodeConnectorFELink"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MultiNodeConnectorFELink",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MultiNodeConnectorFELink:
    """Special nested class for casting MultiNodeConnectorFELink to subclasses."""

    __parent__: "MultiNodeConnectorFELink"

    @property
    def multi_node_fe_link(self: "CastSelf") -> "_2483.MultiNodeFELink":
        return self.__parent__._cast(_2483.MultiNodeFELink)

    @property
    def fe_link(self: "CastSelf") -> "_2476.FELink":
        from mastapy._private.system_model.fe.links import _2476

        return self.__parent__._cast(_2476.FELink)

    @property
    def shaft_hub_connection_fe_link(
        self: "CastSelf",
    ) -> "_2489.ShaftHubConnectionFELink":
        from mastapy._private.system_model.fe.links import _2489

        return self.__parent__._cast(_2489.ShaftHubConnectionFELink)

    @property
    def multi_node_connector_fe_link(self: "CastSelf") -> "MultiNodeConnectorFELink":
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
class MultiNodeConnectorFELink(_2483.MultiNodeFELink):
    """MultiNodeConnectorFELink

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MULTI_NODE_CONNECTOR_FE_LINK

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_MultiNodeConnectorFELink":
        """Cast to another type.

        Returns:
            _Cast_MultiNodeConnectorFELink
        """
        return _Cast_MultiNodeConnectorFELink(self)
