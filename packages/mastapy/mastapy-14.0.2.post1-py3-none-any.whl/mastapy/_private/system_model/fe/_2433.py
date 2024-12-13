"""ElementFaceGroupWithSelection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.fe_tools.vis_tools_global import _1274
from mastapy._private.nodal_analysis.component_mode_synthesis import _237
from mastapy._private.system_model.fe import _2435

_ELEMENT_FACE_GROUP_WITH_SELECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "ElementFaceGroupWithSelection"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ElementFaceGroupWithSelection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElementFaceGroupWithSelection._Cast_ElementFaceGroupWithSelection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElementFaceGroupWithSelection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElementFaceGroupWithSelection:
    """Special nested class for casting ElementFaceGroupWithSelection to subclasses."""

    __parent__: "ElementFaceGroupWithSelection"

    @property
    def fe_entity_group_with_selection(
        self: "CastSelf",
    ) -> "_2435.FEEntityGroupWithSelection":
        return self.__parent__._cast(_2435.FEEntityGroupWithSelection)

    @property
    def element_face_group_with_selection(
        self: "CastSelf",
    ) -> "ElementFaceGroupWithSelection":
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
class ElementFaceGroupWithSelection(
    _2435.FEEntityGroupWithSelection[_237.CMSElementFaceGroup, _1274.ElementFace]
):
    """ElementFaceGroupWithSelection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELEMENT_FACE_GROUP_WITH_SELECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ElementFaceGroupWithSelection":
        """Cast to another type.

        Returns:
            _Cast_ElementFaceGroupWithSelection
        """
        return _Cast_ElementFaceGroupWithSelection(self)
