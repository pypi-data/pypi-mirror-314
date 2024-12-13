"""CylindricalMeshedGearSystemDeflection"""

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
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_CYLINDRICAL_MESHED_GEAR_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "CylindricalMeshedGearSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.ltca import _870
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2828,
        _2834,
        _2837,
    )

    Self = TypeVar("Self", bound="CylindricalMeshedGearSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalMeshedGearSystemDeflection._Cast_CylindricalMeshedGearSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalMeshedGearSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalMeshedGearSystemDeflection:
    """Special nested class for casting CylindricalMeshedGearSystemDeflection to subclasses."""

    __parent__: "CylindricalMeshedGearSystemDeflection"

    @property
    def cylindrical_meshed_gear_system_deflection(
        self: "CastSelf",
    ) -> "CylindricalMeshedGearSystemDeflection":
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
class CylindricalMeshedGearSystemDeflection(_0.APIBase):
    """CylindricalMeshedGearSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_MESHED_GEAR_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def change_in_operating_pitch_diameter_due_to_thermal_effects(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ChangeInOperatingPitchDiameterDueToThermalEffects"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_operating_tip_clearance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumOperatingTipClearance")

        if temp is None:
            return 0.0

        return temp

    @property
    def operating_tip_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OperatingTipDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def tilt_x(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TiltX")

        if temp is None:
            return 0.0

        return temp

    @property
    def tilt_y(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TiltY")

        if temp is None:
            return 0.0

        return temp

    @property
    def left_flank(self: "Self") -> "_2837.CylindricalMeshedGearFlankSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.CylindricalMeshedGearFlankSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def right_flank(self: "Self") -> "_2837.CylindricalMeshedGearFlankSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.CylindricalMeshedGearFlankSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def compression_side_fillet_results(
        self: "Self",
    ) -> "List[_870.GearRootFilletStressResults]":
        """List[mastapy.gears.ltca.GearRootFilletStressResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CompressionSideFilletResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def flanks(
        self: "Self",
    ) -> "List[_2837.CylindricalMeshedGearFlankSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.CylindricalMeshedGearFlankSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Flanks")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def tension_side_fillet_results(
        self: "Self",
    ) -> "List[_870.GearRootFilletStressResults]":
        """List[mastapy.gears.ltca.GearRootFilletStressResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TensionSideFilletResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def both_flanks(self: "Self") -> "_2837.CylindricalMeshedGearFlankSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.CylindricalMeshedGearFlankSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BothFlanks")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_gear_system_deflection(
        self: "Self",
    ) -> "_2834.CylindricalGearSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.CylindricalGearSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearSystemDeflection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_gear_mesh_system_deflection(
        self: "Self",
    ) -> "_2828.CylindricalGearMeshSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.CylindricalGearMeshSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearMeshSystemDeflection"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def other_cylindrical_gear_system_deflection(
        self: "Self",
    ) -> "_2834.CylindricalGearSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.CylindricalGearSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "OtherCylindricalGearSystemDeflection"
        )

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
    def cast_to(self: "Self") -> "_Cast_CylindricalMeshedGearSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_CylindricalMeshedGearSystemDeflection
        """
        return _Cast_CylindricalMeshedGearSystemDeflection(self)
