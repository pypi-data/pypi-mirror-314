"""ElementFaceGroup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.fe_tools.vis_tools_global import _1274
from mastapy._private.nodal_analysis.dev_tools_analyses import _195

_ELEMENT_FACE_GROUP = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses", "ElementFaceGroup"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.component_mode_synthesis import _237, _238

    Self = TypeVar("Self", bound="ElementFaceGroup")
    CastSelf = TypeVar("CastSelf", bound="ElementFaceGroup._Cast_ElementFaceGroup")


__docformat__ = "restructuredtext en"
__all__ = ("ElementFaceGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElementFaceGroup:
    """Special nested class for casting ElementFaceGroup to subclasses."""

    __parent__: "ElementFaceGroup"

    @property
    def fe_entity_group(self: "CastSelf") -> "_195.FEEntityGroup":
        return self.__parent__._cast(_195.FEEntityGroup)

    @property
    def cms_element_face_group(self: "CastSelf") -> "_237.CMSElementFaceGroup":
        from mastapy._private.nodal_analysis.component_mode_synthesis import _237

        return self.__parent__._cast(_237.CMSElementFaceGroup)

    @property
    def cms_element_face_group_of_all_free_faces(
        self: "CastSelf",
    ) -> "_238.CMSElementFaceGroupOfAllFreeFaces":
        from mastapy._private.nodal_analysis.component_mode_synthesis import _238

        return self.__parent__._cast(_238.CMSElementFaceGroupOfAllFreeFaces)

    @property
    def element_face_group(self: "CastSelf") -> "ElementFaceGroup":
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
class ElementFaceGroup(_195.FEEntityGroup[_1274.ElementFace]):
    """ElementFaceGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELEMENT_FACE_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ElementFaceGroup":
        """Cast to another type.

        Returns:
            _Cast_ElementFaceGroup
        """
        return _Cast_ElementFaceGroup(self)
