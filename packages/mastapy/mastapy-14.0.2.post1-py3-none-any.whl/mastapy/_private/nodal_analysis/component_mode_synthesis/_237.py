"""CMSElementFaceGroup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.nodal_analysis.dev_tools_analyses import _193

_CMS_ELEMENT_FACE_GROUP = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis", "CMSElementFaceGroup"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.component_mode_synthesis import _238
    from mastapy._private.nodal_analysis.dev_tools_analyses import _195

    Self = TypeVar("Self", bound="CMSElementFaceGroup")
    CastSelf = TypeVar(
        "CastSelf", bound="CMSElementFaceGroup._Cast_CMSElementFaceGroup"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CMSElementFaceGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CMSElementFaceGroup:
    """Special nested class for casting CMSElementFaceGroup to subclasses."""

    __parent__: "CMSElementFaceGroup"

    @property
    def element_face_group(self: "CastSelf") -> "_193.ElementFaceGroup":
        return self.__parent__._cast(_193.ElementFaceGroup)

    @property
    def fe_entity_group(self: "CastSelf") -> "_195.FEEntityGroup":
        pass

        from mastapy._private.nodal_analysis.dev_tools_analyses import _195

        return self.__parent__._cast(_195.FEEntityGroup)

    @property
    def cms_element_face_group_of_all_free_faces(
        self: "CastSelf",
    ) -> "_238.CMSElementFaceGroupOfAllFreeFaces":
        from mastapy._private.nodal_analysis.component_mode_synthesis import _238

        return self.__parent__._cast(_238.CMSElementFaceGroupOfAllFreeFaces)

    @property
    def cms_element_face_group(self: "CastSelf") -> "CMSElementFaceGroup":
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
class CMSElementFaceGroup(_193.ElementFaceGroup):
    """CMSElementFaceGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CMS_ELEMENT_FACE_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def area(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Area")

        if temp is None:
            return 0.0

        return temp

    def create_node_group(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CreateNodeGroup")

    def populate_rms_values_cache(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "PopulateRMSValuesCache")

    @property
    def cast_to(self: "Self") -> "_Cast_CMSElementFaceGroup":
        """Cast to another type.

        Returns:
            _Cast_CMSElementFaceGroup
        """
        return _Cast_CMSElementFaceGroup(self)
