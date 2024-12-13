"""PersistentSingleton"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_PERSISTENT_SINGLETON = python_net_import("SMT.MastaAPI.Utility", "PersistentSingleton")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings import _1954
    from mastapy._private.gears.gear_designs.cylindrical import _1043
    from mastapy._private.gears.ltca.cylindrical import _880
    from mastapy._private.gears.materials import _612
    from mastapy._private.nodal_analysis import _68
    from mastapy._private.nodal_analysis.geometry_modeller_link import _168
    from mastapy._private.system_model.part_model import _2530
    from mastapy._private.utility import _1645, _1647, _1648
    from mastapy._private.utility.cad_export import _1887
    from mastapy._private.utility.databases import _1882
    from mastapy._private.utility.scripting import _1792
    from mastapy._private.utility.units_and_measurements import _1658

    Self = TypeVar("Self", bound="PersistentSingleton")
    CastSelf = TypeVar(
        "CastSelf", bound="PersistentSingleton._Cast_PersistentSingleton"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PersistentSingleton",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PersistentSingleton:
    """Special nested class for casting PersistentSingleton to subclasses."""

    __parent__: "PersistentSingleton"

    @property
    def fe_user_settings(self: "CastSelf") -> "_68.FEUserSettings":
        from mastapy._private.nodal_analysis import _68

        return self.__parent__._cast(_68.FEUserSettings)

    @property
    def geometry_modeller_settings(self: "CastSelf") -> "_168.GeometryModellerSettings":
        from mastapy._private.nodal_analysis.geometry_modeller_link import _168

        return self.__parent__._cast(_168.GeometryModellerSettings)

    @property
    def gear_material_expert_system_factor_settings(
        self: "CastSelf",
    ) -> "_612.GearMaterialExpertSystemFactorSettings":
        from mastapy._private.gears.materials import _612

        return self.__parent__._cast(_612.GearMaterialExpertSystemFactorSettings)

    @property
    def cylindrical_gear_fe_settings(
        self: "CastSelf",
    ) -> "_880.CylindricalGearFESettings":
        from mastapy._private.gears.ltca.cylindrical import _880

        return self.__parent__._cast(_880.CylindricalGearFESettings)

    @property
    def cylindrical_gear_defaults(self: "CastSelf") -> "_1043.CylindricalGearDefaults":
        from mastapy._private.gears.gear_designs.cylindrical import _1043

        return self.__parent__._cast(_1043.CylindricalGearDefaults)

    @property
    def per_machine_settings(self: "CastSelf") -> "_1645.PerMachineSettings":
        from mastapy._private.utility import _1645

        return self.__parent__._cast(_1645.PerMachineSettings)

    @property
    def program_settings(self: "CastSelf") -> "_1647.ProgramSettings":
        from mastapy._private.utility import _1647

        return self.__parent__._cast(_1647.ProgramSettings)

    @property
    def pushbullet_settings(self: "CastSelf") -> "_1648.PushbulletSettings":
        from mastapy._private.utility import _1648

        return self.__parent__._cast(_1648.PushbulletSettings)

    @property
    def measurement_settings(self: "CastSelf") -> "_1658.MeasurementSettings":
        from mastapy._private.utility.units_and_measurements import _1658

        return self.__parent__._cast(_1658.MeasurementSettings)

    @property
    def scripting_setup(self: "CastSelf") -> "_1792.ScriptingSetup":
        from mastapy._private.utility.scripting import _1792

        return self.__parent__._cast(_1792.ScriptingSetup)

    @property
    def database_settings(self: "CastSelf") -> "_1882.DatabaseSettings":
        from mastapy._private.utility.databases import _1882

        return self.__parent__._cast(_1882.DatabaseSettings)

    @property
    def cad_export_settings(self: "CastSelf") -> "_1887.CADExportSettings":
        from mastapy._private.utility.cad_export import _1887

        return self.__parent__._cast(_1887.CADExportSettings)

    @property
    def skf_settings(self: "CastSelf") -> "_1954.SKFSettings":
        from mastapy._private.bearings import _1954

        return self.__parent__._cast(_1954.SKFSettings)

    @property
    def planet_carrier_settings(self: "CastSelf") -> "_2530.PlanetCarrierSettings":
        from mastapy._private.system_model.part_model import _2530

        return self.__parent__._cast(_2530.PlanetCarrierSettings)

    @property
    def persistent_singleton(self: "CastSelf") -> "PersistentSingleton":
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
class PersistentSingleton(_0.APIBase):
    """PersistentSingleton

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PERSISTENT_SINGLETON

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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

    def save(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Save")

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
    def cast_to(self: "Self") -> "_Cast_PersistentSingleton":
        """Cast to another type.

        Returns:
            _Cast_PersistentSingleton
        """
        return _Cast_PersistentSingleton(self)
