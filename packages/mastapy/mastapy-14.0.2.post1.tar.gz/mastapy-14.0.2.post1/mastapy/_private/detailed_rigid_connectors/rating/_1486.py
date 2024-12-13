"""ShaftHubConnectionRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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

_SHAFT_HUB_CONNECTION_RATING = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Rating", "ShaftHubConnectionRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.detailed_rigid_connectors import _1437
    from mastapy._private.detailed_rigid_connectors.interference_fits.rating import (
        _1499,
    )
    from mastapy._private.detailed_rigid_connectors.keyed_joints.rating import _1492
    from mastapy._private.detailed_rigid_connectors.splines.ratings import (
        _1474,
        _1476,
        _1478,
        _1480,
        _1482,
    )

    Self = TypeVar("Self", bound="ShaftHubConnectionRating")
    CastSelf = TypeVar(
        "CastSelf", bound="ShaftHubConnectionRating._Cast_ShaftHubConnectionRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftHubConnectionRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftHubConnectionRating:
    """Special nested class for casting ShaftHubConnectionRating to subclasses."""

    __parent__: "ShaftHubConnectionRating"

    @property
    def agma6123_spline_joint_rating(
        self: "CastSelf",
    ) -> "_1474.AGMA6123SplineJointRating":
        from mastapy._private.detailed_rigid_connectors.splines.ratings import _1474

        return self.__parent__._cast(_1474.AGMA6123SplineJointRating)

    @property
    def din5466_spline_rating(self: "CastSelf") -> "_1476.DIN5466SplineRating":
        from mastapy._private.detailed_rigid_connectors.splines.ratings import _1476

        return self.__parent__._cast(_1476.DIN5466SplineRating)

    @property
    def gbt17855_spline_joint_rating(
        self: "CastSelf",
    ) -> "_1478.GBT17855SplineJointRating":
        from mastapy._private.detailed_rigid_connectors.splines.ratings import _1478

        return self.__parent__._cast(_1478.GBT17855SplineJointRating)

    @property
    def sae_spline_joint_rating(self: "CastSelf") -> "_1480.SAESplineJointRating":
        from mastapy._private.detailed_rigid_connectors.splines.ratings import _1480

        return self.__parent__._cast(_1480.SAESplineJointRating)

    @property
    def spline_joint_rating(self: "CastSelf") -> "_1482.SplineJointRating":
        from mastapy._private.detailed_rigid_connectors.splines.ratings import _1482

        return self.__parent__._cast(_1482.SplineJointRating)

    @property
    def keyway_rating(self: "CastSelf") -> "_1492.KeywayRating":
        from mastapy._private.detailed_rigid_connectors.keyed_joints.rating import _1492

        return self.__parent__._cast(_1492.KeywayRating)

    @property
    def interference_fit_rating(self: "CastSelf") -> "_1499.InterferenceFitRating":
        from mastapy._private.detailed_rigid_connectors.interference_fits.rating import (
            _1499,
        )

        return self.__parent__._cast(_1499.InterferenceFitRating)

    @property
    def shaft_hub_connection_rating(self: "CastSelf") -> "ShaftHubConnectionRating":
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
class ShaftHubConnectionRating(_0.APIBase):
    """ShaftHubConnectionRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_HUB_CONNECTION_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def additional_rating_information(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "AdditionalRatingInformation")

        if temp is None:
            return ""

        return temp

    @additional_rating_information.setter
    @enforce_parameter_types
    def additional_rating_information(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AdditionalRatingInformation",
            str(value) if value is not None else "",
        )

    @property
    def axial_force(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AxialForce")

        if temp is None:
            return 0.0

        return temp

    @axial_force.setter
    @enforce_parameter_types
    def axial_force(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "AxialForce", float(value) if value is not None else 0.0
        )

    @property
    def moment(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Moment")

        if temp is None:
            return 0.0

        return temp

    @moment.setter
    @enforce_parameter_types
    def moment(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Moment", float(value) if value is not None else 0.0
        )

    @property
    def radial_force(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialForce")

        if temp is None:
            return 0.0

        return temp

    @radial_force.setter
    @enforce_parameter_types
    def radial_force(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RadialForce", float(value) if value is not None else 0.0
        )

    @property
    def rotational_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotationalSpeed")

        if temp is None:
            return 0.0

        return temp

    @rotational_speed.setter
    @enforce_parameter_types
    def rotational_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RotationalSpeed", float(value) if value is not None else 0.0
        )

    @property
    def torque(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Torque")

        if temp is None:
            return 0.0

        return temp

    @torque.setter
    @enforce_parameter_types
    def torque(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Torque", float(value) if value is not None else 0.0
        )

    @property
    def joint_design(self: "Self") -> "_1437.DetailedRigidConnectorDesign":
        """mastapy.detailed_rigid_connectors.DetailedRigidConnectorDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "JointDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

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
    def cast_to(self: "Self") -> "_Cast_ShaftHubConnectionRating":
        """Cast to another type.

        Returns:
            _Cast_ShaftHubConnectionRating
        """
        return _Cast_ShaftHubConnectionRating(self)
