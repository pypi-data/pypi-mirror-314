"""CoordinateSystemEditor"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private._math.vector_3d import Vector3D

_COORDINATE_SYSTEM_EDITOR = python_net_import(
    "SMT.MastaAPI.MathUtility", "CoordinateSystemEditor"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility import _1549, _1551, _1552, _1578

    Self = TypeVar("Self", bound="CoordinateSystemEditor")
    CastSelf = TypeVar(
        "CastSelf", bound="CoordinateSystemEditor._Cast_CoordinateSystemEditor"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CoordinateSystemEditor",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CoordinateSystemEditor:
    """Special nested class for casting CoordinateSystemEditor to subclasses."""

    __parent__: "CoordinateSystemEditor"

    @property
    def coordinate_system_editor(self: "CastSelf") -> "CoordinateSystemEditor":
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
class CoordinateSystemEditor(_0.APIBase):
    """CoordinateSystemEditor

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COORDINATE_SYSTEM_EDITOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def containing_assembly_image(self: "Self") -> "Image":
        """Image"""
        temp = pythonnet_property_get(self.wrapped, "ContainingAssemblyImage")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @containing_assembly_image.setter
    @enforce_parameter_types
    def containing_assembly_image(self: "Self", value: "Image") -> None:
        value = conversion.mp_to_pn_smt_bitmap(value)
        pythonnet_property_set(self.wrapped, "ContainingAssemblyImage", value)

    @property
    def containing_assembly_text(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContainingAssemblyText")

        if temp is None:
            return ""

        return temp

    @property
    def coordinate_system_for_rotation_axes(
        self: "Self",
    ) -> "_1551.CoordinateSystemForRotation":
        """mastapy.math_utility.CoordinateSystemForRotation"""
        temp = pythonnet_property_get(self.wrapped, "CoordinateSystemForRotationAxes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.MathUtility.CoordinateSystemForRotation"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility._1551", "CoordinateSystemForRotation"
        )(value)

    @coordinate_system_for_rotation_axes.setter
    @enforce_parameter_types
    def coordinate_system_for_rotation_axes(
        self: "Self", value: "_1551.CoordinateSystemForRotation"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.MathUtility.CoordinateSystemForRotation"
        )
        pythonnet_property_set(self.wrapped, "CoordinateSystemForRotationAxes", value)

    @property
    def coordinate_system_for_rotation_origin(
        self: "Self",
    ) -> "_1552.CoordinateSystemForRotationOrigin":
        """mastapy.math_utility.CoordinateSystemForRotationOrigin"""
        temp = pythonnet_property_get(self.wrapped, "CoordinateSystemForRotationOrigin")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.MathUtility.CoordinateSystemForRotationOrigin"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility._1552", "CoordinateSystemForRotationOrigin"
        )(value)

    @coordinate_system_for_rotation_origin.setter
    @enforce_parameter_types
    def coordinate_system_for_rotation_origin(
        self: "Self", value: "_1552.CoordinateSystemForRotationOrigin"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.MathUtility.CoordinateSystemForRotationOrigin"
        )
        pythonnet_property_set(self.wrapped, "CoordinateSystemForRotationOrigin", value)

    @property
    def has_modified_coordinate_system_rotation(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HasModifiedCoordinateSystemRotation"
        )

        if temp is None:
            return False

        return temp

    @property
    def has_modified_coordinate_system_translation(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HasModifiedCoordinateSystemTranslation"
        )

        if temp is None:
            return False

        return temp

    @property
    def has_modified_coordinate_system(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HasModifiedCoordinateSystem")

        if temp is None:
            return False

        return temp

    @property
    def has_rotation(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HasRotation")

        if temp is None:
            return False

        return temp

    @property
    def has_translation(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HasTranslation")

        if temp is None:
            return False

        return temp

    @property
    def root_assembly_image(self: "Self") -> "Image":
        """Image"""
        temp = pythonnet_property_get(self.wrapped, "RootAssemblyImage")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @root_assembly_image.setter
    @enforce_parameter_types
    def root_assembly_image(self: "Self", value: "Image") -> None:
        value = conversion.mp_to_pn_smt_bitmap(value)
        pythonnet_property_set(self.wrapped, "RootAssemblyImage", value)

    @property
    def root_assembly_text(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootAssemblyText")

        if temp is None:
            return ""

        return temp

    @property
    def rotation_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotationAngle")

        if temp is None:
            return 0.0

        return temp

    @rotation_angle.setter
    @enforce_parameter_types
    def rotation_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RotationAngle", float(value) if value is not None else 0.0
        )

    @property
    def rotation_axis(self: "Self") -> "_1578.RotationAxis":
        """mastapy.math_utility.RotationAxis"""
        temp = pythonnet_property_get(self.wrapped, "RotationAxis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.MathUtility.RotationAxis")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility._1578", "RotationAxis"
        )(value)

    @rotation_axis.setter
    @enforce_parameter_types
    def rotation_axis(self: "Self", value: "_1578.RotationAxis") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.MathUtility.RotationAxis")
        pythonnet_property_set(self.wrapped, "RotationAxis", value)

    @property
    def show_preview(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowPreview")

        if temp is None:
            return False

        return temp

    @show_preview.setter
    @enforce_parameter_types
    def show_preview(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowPreview", bool(value) if value is not None else False
        )

    @property
    def coordinate_system(self: "Self") -> "_1549.CoordinateSystem3D":
        """mastapy.math_utility.CoordinateSystem3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CoordinateSystem")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def modified_coordinate_system_for_rotation(
        self: "Self",
    ) -> "_1549.CoordinateSystem3D":
        """mastapy.math_utility.CoordinateSystem3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ModifiedCoordinateSystemForRotation"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def modified_coordinate_system_for_translation(
        self: "Self",
    ) -> "_1549.CoordinateSystem3D":
        """mastapy.math_utility.CoordinateSystem3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ModifiedCoordinateSystemForTranslation"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def rotation_origin(self: "Self") -> "Vector3D":
        """Vector3D"""
        temp = pythonnet_property_get(self.wrapped, "RotationOrigin")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @rotation_origin.setter
    @enforce_parameter_types
    def rotation_origin(self: "Self", value: "Vector3D") -> None:
        value = conversion.mp_to_pn_vector3d(value)
        pythonnet_property_set(self.wrapped, "RotationOrigin", value)

    @property
    def specified_rotation_axis(self: "Self") -> "Vector3D":
        """Vector3D"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedRotationAxis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @specified_rotation_axis.setter
    @enforce_parameter_types
    def specified_rotation_axis(self: "Self", value: "Vector3D") -> None:
        value = conversion.mp_to_pn_vector3d(value)
        pythonnet_property_set(self.wrapped, "SpecifiedRotationAxis", value)

    @property
    def translation(self: "Self") -> "Vector3D":
        """Vector3D"""
        temp = pythonnet_property_get(self.wrapped, "Translation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @translation.setter
    @enforce_parameter_types
    def translation(self: "Self", value: "Vector3D") -> None:
        value = conversion.mp_to_pn_vector3d(value)
        pythonnet_property_set(self.wrapped, "Translation", value)

    @property
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    def align_to_world_coordinate_system(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AlignToWorldCoordinateSystem")

    def apply_rotation(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ApplyRotation")

    def cancel_pending_changes(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CancelPendingChanges")

    def set_local_origin_to_world_origin(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SetLocalOriginToWorldOrigin")

    def update_origin(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "UpdateOrigin")

    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputDefaultReportTo", file_path if file_path else ""
        )

    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportTo", file_path if file_path else ""
        )

    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportAsTextTo", file_path if file_path else ""
        )

    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_CoordinateSystemEditor":
        """Cast to another type.

        Returns:
            _Cast_CoordinateSystemEditor
        """
        return _Cast_CoordinateSystemEditor(self)
